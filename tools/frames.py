"""Frames to look at: exact full-size frames, and contact sheets for finding things (never for passing them).

    python3 tools/frames.py <video> --at <s> [<s> …] [--out <dir>]          # full-size PNGs at song times
    python3 tools/frames.py <video> --frames <a-b[:step]> [--out <dir>]     # full-size PNGs of frame numbers
    python3 tools/frames.py <video|frames dir> --strip <step> [--range a-b] [--cols 8] [--width 360] [--out <dir>]
                                                                           # contact sheets: every <step>th frame, labelled

Frame n of a video is the one shown from n/fps to (n+1)/fps. Times and frame numbers are exact (no off-by-one from
seeking). Sheets are numbered and labelled with frame number and time.
"""
from __future__ import annotations

import _env  # noqa: F401
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from common import ToolError, clock, fail, need, probe_video, run


def parse_range(s: str) -> tuple[int, int, int]:
    rng, _, step = s.partition(":")
    a, _, b = rng.partition("-")
    return int(a), int(b or a), int(step or 1)


def exact_frames(video: Path, frames: list[int], fps: float, out: Path, prefix: str = "f") -> list[Path]:
    """Each frame by number: seek near it, then select the frame whose time is at least n/fps − half a frame."""
    paths = []
    for n in frames:
        t = n / fps
        p = out / f"{prefix}{n:06d}.png"
        pre = max(0.0, t - 2.0)
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{pre:.6f}", "-i", str(video), "-copyts", "-vf",
             f"select='gte(t\\,{t - 0.5 / fps:.6f})'", "-frames:v", "1", "-fps_mode", "passthrough", str(p)])
        if not p.exists():
            raise ToolError(f"frame {n} ({t:.3f} s) is past the end of {video.name}")
        paths.append(p)
    return paths


def sheet(images: list[tuple[Path, str]], out: Path, cols: int, width: int) -> None:
    from PIL import Image, ImageDraw, ImageFont
    first = Image.open(images[0][0])
    h = int(round(first.height * width / first.width))
    rows = (len(images) + cols - 1) // cols
    label_h = 18
    img = Image.new("RGB", (cols * width + (cols + 1) * 4, rows * (h + label_h) + (rows + 1) * 4), (20, 20, 22))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default(size=13)
    except TypeError:
        font = ImageFont.load_default()
    for i, (p, label) in enumerate(images):
        r, c = divmod(i, cols)
        x, y = 4 + c * (width + 4), 4 + r * (h + label_h + 4)
        im = Image.open(p).convert("RGB").resize((width, h))
        img.paste(im, (x, y + label_h))
        d.text((x + 2, y + 2), label, fill=(220, 220, 220), font=font)
    img.save(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", type=Path)
    ap.add_argument("--at", type=float, nargs="+")
    ap.add_argument("--frames")
    ap.add_argument("--strip", type=int)
    ap.add_argument("--range")
    ap.add_argument("--cols", type=int, default=8)
    ap.add_argument("--width", type=int, default=360)
    ap.add_argument("--per-sheet", type=int, default=48)
    ap.add_argument("--fps", type=float, help="for a folder of frames (default 30)")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    need("ffmpeg", "Install ffmpeg.")
    src = a.src.resolve()
    out = (a.out or src.parent / f"{src.stem}.frames").resolve()
    out.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    if src.is_dir():
        files = sorted(p for p in src.iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".exr", ".tif"))
        if not files:
            raise ToolError(f"no frames in {src}")
        fps = a.fps or 30.0
        if not a.strip:
            raise ToolError("for a folder of frames, use --strip <step>")
        lo, hi, _ = parse_range(a.range) if a.range else (0, len(files) - 1, 1)
        chosen = [(files[i], i) for i in range(lo, min(hi, len(files) - 1) + 1, a.strip)]
        for k in range(0, len(chosen), a.per_sheet):
            part = chosen[k:k + a.per_sheet]
            p = out / f"sheet-{part[0][1]:06d}-{part[-1][1]:06d}.png"
            sheet([(f, f"{f.stem}  {clock(i / fps)}") for f, i in part], p, a.cols, a.width)
            written.append(str(p))
        print(json.dumps({"sheets": written}, indent=1))
        return
    info = probe_video(src)
    fps = info["fps"]
    if a.at:
        frames = [int(t * fps + 1e-6) for t in a.at]
        written = [str(p) for p in exact_frames(src, frames, fps, out, "t")]
    if a.frames:
        lo, hi, step = parse_range(a.frames)
        written += [str(p) for p in exact_frames(src, list(range(lo, hi + 1, step)), fps, out)]
    if a.strip:
        lo, hi, _ = parse_range(a.range) if a.range else (0, info["frames"] - 1, 1)
        with tempfile.TemporaryDirectory() as td:
            # every <step>th frame by number, scaled down once, numbered by frame
            run(["ffmpeg", "-v", "error", "-i", str(src), "-vf",
                 f"select='between(n\\,{lo}\\,{hi})*not(mod(n-{lo}\\,{a.strip}))',scale={a.width}:-2",
                 "-fps_mode", "passthrough", "-frame_pts", "1", str(Path(td) / "%08d.png")])
            files = sorted(Path(td).glob("*.png"))
            # -frame_pts names by pts in the stream's time base: map back to frame numbers by order
            numbers = list(range(lo, hi + 1, a.strip))[:len(files)]
            pairs = list(zip(files, numbers))
            for k in range(0, len(pairs), a.per_sheet):
                part = pairs[k:k + a.per_sheet]
                p = out / f"sheet-{part[0][1]:06d}-{part[-1][1]:06d}.png"
                sheet([(f, f"f{n}  {clock(n / fps)}") for f, n in part], p, a.cols, a.width)
                written.append(str(p))
    if not written:
        ap.error("give --at, --frames or --strip")
    print(json.dumps({"fps": fps, "frames": info["frames"], "wrote": written}, indent=1))


if __name__ == "__main__":
    try:
        main()
    except ToolError as e:
        fail(str(e))
    except subprocess.CalledProcessError as e:
        fail(str(e))
