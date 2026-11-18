"""The full film, always current: each shot's newest render spliced in, the blocking animatic where a shot isn't built yet.

    python3 tools/edit.py splice <film> <shot id> <clip.mp4> [--kind draft|final]   # register a shot's render, rebuild
    python3 tools/edit.py full <film>                                               # rebuild renders/full/full-latest.mp4
    python3 tools/edit.py section <film> <section or scene name>                    # one section or scene, joined, with its song
    python3 tools/edit.py final <film>                                              # the delivery file (at run.json's
                                                                                    # "deliverySize" if set), checked

Shots come from shots/shots.json (film order, t0/t1 in master seconds). A shot's frames are round(t0 × fps) up to
round(t1 × fps), so every frame of the song belongs to exactly one shot. A clip must have exactly its shot's frame count.
The animatic is run.json's "animatic" (default renders/blocking/blocking.mp4). Every piece is re-encoded to one format
(H.264, yuv420p, BT.709, the film's size and fps) and the song is laid under the joined picture once, from the master.
"""
from __future__ import annotations

import _env  # noqa: F401
import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

from common import ToolError, fail, film_dir, load_run, need, probe_seconds, probe_video, run, write_json

COLOUR = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"]


def shots_of(film: Path, fps: float) -> list[dict]:
    shots = json.loads((film / "shots" / "shots.json").read_text())
    prev = 0
    for s in shots:
        s["f0"], s["f1"] = round(s["t0"] * fps), round(s["t1"] * fps)
        if s["f0"] != prev:
            raise ToolError(f"shot {s['id']} starts at frame {s['f0']}, but the shot before ends at {prev}: "
                            "shots must follow each other with no gap or overlap")
        if s["f1"] <= s["f0"]:
            raise ToolError(f"shot {s['id']} has no frames")
        prev = s["f1"]
    return shots


def master_of(film: Path) -> Path:
    mdir = film / "song" / "master"
    for j in sorted(mdir.glob("*.json")) if mdir.is_dir() else []:
        info = json.loads(j.read_text())
        if "wav" in info:
            return mdir / info["wav"]
    raise ToolError("no master in song/master (stage 2)")


def encode_args(run_: dict, crf: int, preset: str) -> list[str]:
    w, h = run_.get("size", [1920, 1080])
    return ["-vf", f"scale={w}:{h}:flags=lanczos:out_color_matrix=bt709:out_range=tv,fps={run_.get('fps', 30)}",
            "-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-pix_fmt", "yuv420p", *COLOUR]


def segment(src: Path, f0: int, f1: int | None, out: Path, run_: dict, crf=16, preset="medium") -> None:
    """Frames [f0, f1) of src by frame number (all of it when f1 is None), re-encoded to the film's format."""
    sel = [] if f1 is None else ["-vf", f"select='between(n\\,{f0}\\,{f1 - 1})',setpts=N/FRAME_RATE/TB"]
    if sel:
        tmp = out.with_suffix(".sel.mkv")
        run(["ffmpeg", "-v", "error", "-y", "-i", str(src), *sel, "-fps_mode", "passthrough", "-c:v", "ffv1", str(tmp)])
        src = tmp
    run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-an", *encode_args(run_, crf, preset), str(out)])
    if sel:
        tmp.unlink(missing_ok=True)


def join(film: Path, shots: list[dict], parts: dict, out: Path, run_: dict, t0: float, t1: float, crf=16,
         preset="medium") -> dict:
    fps = run_.get("fps", 30)
    segdir = film / "renders" / "full" / "segments"
    segdir.mkdir(parents=True, exist_ok=True)
    animatic = film / run_.get("animatic", "renders/blocking/blocking.mp4")
    listing, used = [], []
    for s in shots:
        p = parts.get(s["id"])
        if p:
            src = film / p["clip"]
            key = f"{s['id']}-{p['kind']}-{int(src.stat().st_mtime)}-c{crf}"
            seg = segdir / f"{key}.mp4"
            if not seg.exists():
                segment(src, 0, None, seg, run_, crf, preset)
            used.append(f"{s['id']}:{p['kind']}")
        else:
            if not animatic.exists():
                raise ToolError(f"shot {s['id']} has no render and there's no animatic at {animatic}")
            key = f"{s['id']}-blocking-{int(animatic.stat().st_mtime)}-c{crf}"
            seg = segdir / f"{key}.mp4"
            if not seg.exists():
                segment(animatic, s["f0"], s["f1"], seg, run_, crf, preset)
            used.append(f"{s['id']}:blocking")
        listing.append(f"file '{seg.as_posix()}'")
    lst = out.with_suffix(".txt")
    lst.write_text("\n".join(listing) + "\n")
    picture = out.with_suffix(".picture.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(picture)])
    master = master_of(film)
    run(["ffmpeg", "-v", "error", "-y", "-i", str(picture), "-ss", f"{t0:.6f}", "-t", f"{t1 - t0:.6f}", "-i", str(master),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         "-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
         "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", str(out)])
    picture.unlink(missing_ok=True)
    lst.unlink(missing_ok=True)
    info = probe_video(out)
    expected = sum(s["f1"] - s["f0"] for s in shots)
    return {"file": str(out), "frames": info["frames"], "expectedFrames": expected, "fps": info["fps"],
            "seconds": round(probe_seconds(out), 3), "shots": used,
            "frameCountOK": info["frames"] == expected}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["splice", "full", "section", "final"])
    ap.add_argument("film")
    ap.add_argument("rest", nargs="*")
    ap.add_argument("--kind", default="draft", choices=["draft", "final"])
    a = ap.parse_args()
    need("ffmpeg", "Install ffmpeg.")
    film = film_dir(a.film)
    run_ = load_run(film)
    fps = run_.get("fps", 30)
    shots = shots_of(film, fps)
    parts_path = film / "renders" / "full" / "parts.json"
    parts = json.loads(parts_path.read_text()) if parts_path.exists() else {}
    full_dir = film / "renders" / "full"
    full_dir.mkdir(parents=True, exist_ok=True)

    if a.cmd == "splice":
        if len(a.rest) != 2:
            ap.error("splice <film> <shot id> <clip.mp4>")
        sid, clip = a.rest[0], Path(a.rest[1]).resolve()
        shot = next((s for s in shots if s["id"] == sid), None)
        if not shot:
            raise ToolError(f"no shot {sid} in shots/shots.json")
        n = probe_video(clip)["frames"]
        if n != shot["f1"] - shot["f0"]:
            raise ToolError(f"{clip.name} has {n} frames; shot {sid} has {shot['f1'] - shot['f0']} "
                            f"(frames {shot['f0']}–{shot['f1'] - 1})")
        parts[sid] = {"clip": clip.relative_to(film).as_posix(), "kind": a.kind, "at": datetime.now().isoformat(timespec="seconds")}
        write_json(parts_path, parts)
    if a.cmd in ("splice", "full"):
        out = full_dir / "full-latest.mp4"
        res = join(film, shots, parts, out, run_, 0.0, shots[-1]["t1"])
        stamped = full_dir / f"full-{datetime.now():%Y%m%d-%H%M%S}.mp4"
        shutil.copyfile(out, stamped)
        res["copy"] = str(stamped)
    elif a.cmd == "section":
        if not a.rest:
            ap.error("section <film> <section name>")
        name = " ".join(a.rest)
        sec = [s for s in shots if s.get("section") == name or s.get("scene") == name]
        if not sec:
            raise ToolError(f"no shots in a section or scene called {name!r}; sections: "
                            f"{sorted({str(s.get('section')) for s in shots})}; scenes: {sorted({str(s.get('scene')) for s in shots})}")
        out = film / "renders" / "sections" / f"{name.lower().replace(' ', '-')}.mp4"
        out.parent.mkdir(parents=True, exist_ok=True)
        res = join(film, sec, parts, out, run_, sec[0]["t0"], sec[-1]["t1"])
    else:  # final
        not_final = [s["id"] for s in shots if parts.get(s["id"], {}).get("kind") != "final"]
        out = film / "renders" / "final" / f"{run_['slug']}.mp4"
        out.parent.mkdir(parents=True, exist_ok=True)
        deliver = {**run_, "size": run_.get("deliverySize") or run_.get("size", [1920, 1080])}
        res = join(film, shots, parts, out, deliver, 0.0, shots[-1]["t1"], crf=12, preset="slow")
        res["notFinal"] = not_final
        song = probe_seconds(master_of(film))
        res["songSeconds"] = round(song, 3)
        res["lengthMatchesSong"] = abs(res["seconds"] - song) < 1.5 / fps
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    try:
        main()
    except ToolError as e:
        fail(str(e))
