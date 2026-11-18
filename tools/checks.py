"""Numbers about a render that tell you where to look. Never verdicts: a flagged frame is a frame to step through.

    python3 tools/checks.py <video> [--checks exposure,flicker,pops,speed] [--range a-b] [--out <dir>]
    python3 tools/checks.py <image> --checks colourblind [--out <dir>]

  exposure   per frame: the share of the picture near white (luma above 215 of 255) and near black (below 10). Large
             pale areas read as blown out even when nothing clips.
  flicker    a region of the picture (a 16×9 grid) that jumps one way and straight back within a frame or two, while
             the frames around it are steady: strobing lights, surfaces fighting for the same depth, popping texture.
  pops       a frame that differs from its neighbours far more than they differ from theirs: something appearing or
             vanishing, a jump in a camera path, a dropped or repeated frame.
  speed      how far the picture moves per frame (optical flow, at 1080p scale): the median and the fastest 1%. Very
             fast motion strobes without motion blur and can't be read.
  colourblind  the image as seen with protanopia, deuteranopia and tritanopia (Machado et al. 2009), side by side.

Writes <out>/checks.json and checks.md (default <video>.checks/), and prints a summary.
"""
from __future__ import annotations

import _env  # noqa: F401
import argparse
import json
import subprocess
from pathlib import Path

import numpy as np

from common import ToolError, clock, fail, need, probe_video, write_json

GRID_W, GRID_H = 16, 9


def frames_gray(video: Path, width: int, rng: tuple[int, int] | None):
    """Yield (frame number, gray float32 HxW 0–255) at the given width, every frame, in order."""
    info = probe_video(video)
    h = int(round(info["height"] * width / info["width"] / 2) * 2)
    vf = f"scale={width}:{h}:flags=area,format=gray"
    if rng:
        vf = f"select='between(n\\,{rng[0]}\\,{rng[1]})'," + vf
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(video), "-vf", vf, "-fps_mode", "passthrough",
                          "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
    n = rng[0] if rng else 0
    size = width * h
    while True:
        buf = p.stdout.read(size)
        if len(buf) < size:
            break
        yield n, np.frombuffer(buf, np.uint8).reshape(h, width).astype(np.float32)
        n += 1
    p.wait()


def luma_bt709(video: Path, rng, every: int):
    info = probe_video(video)
    w = 640
    h = int(round(info["height"] * w / info["width"] / 2) * 2)
    sel = f"select='not(mod(n\\,{every}))" + (f"*between(n\\,{rng[0]}\\,{rng[1]})" if rng else "") + "'"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(video), "-vf",
                          f"{sel},scale={w}:{h}:flags=area,format=rgb24", "-fps_mode", "passthrough",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = rng[0] if rng else 0
    n -= n % every
    if rng and n < rng[0]:
        n += every
    size = w * h * 3
    while True:
        buf = p.stdout.read(size)
        if len(buf) < size:
            break
        rgb = np.frombuffer(buf, np.uint8).reshape(h, w, 3).astype(np.float32)
        yield n, rgb @ np.array([0.2126, 0.7152, 0.0722], np.float32)
        n += every
    p.wait()


def check_exposure(video, rng, fps, every=3):
    rows = []
    for n, y in luma_bt709(video, rng, every):
        rows.append({"frame": n, "t": round(n / fps, 3), "nearWhite": round(float((y > 215).mean()), 4),
                     "nearBlack": round(float((y < 10).mean()), 4), "mean": round(float(y.mean()), 1)})
    if not rows:
        return {"frames": 0}
    hw = np.array([r["nearWhite"] for r in rows])
    worst = sorted(rows, key=lambda r: -r["nearWhite"])[:10]
    return {"sampledEvery": every, "frames": len(rows), "nearWhiteMedian": round(float(np.median(hw)), 4),
            "nearWhiteP95": round(float(np.percentile(hw, 95)), 4),
            "framesOver25pctNearWhite": [r["frame"] for r in rows if r["nearWhite"] > 0.25],
            "worst": worst, "series": rows}


def check_motion(video, rng, fps, want_flicker, want_pops, want_speed):
    """One pass over the frames at 270 lines. Flicker is motion-compensated: each frame's two neighbours are warped onto
    it by optical flow; where the two warps agree with each other but the frame itself differs from both, the region
    jumped and came straight back. Cuts, whips and occlusions make the warps disagree, so they aren't counted."""
    import cv2
    win: list[tuple[int, np.ndarray]] = []
    mad, mad_nums, speeds, events = [], [], [], []
    scale_to_1080 = 1080 / 270

    def flow(a, b):  # for each pixel of a, where it is in b
        return cv2.calcOpticalFlowFarneback(a, b, None, 0.5, 4, 21, 3, 7, 1.5, 0)

    def warp(img, f):
        h, w = img.shape
        gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
        return cv2.remap(img, gx + f[..., 0], gy + f[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

    for n, g in frames_gray(video, 480, rng):
        h, w = g.shape
        small = cv2.resize(g, (int(w * 270 / h), 270), interpolation=cv2.INTER_AREA).astype(np.uint8)
        if win:
            mad.append(float(np.abs(small.astype(np.float32) - win[-1][1].astype(np.float32)).mean()))
            mad_nums.append(n)
        win.append((n, small))
        if len(win) > 3:
            win.pop(0)
        if len(win) < 3:
            continue
        (n0, a), (n1, b), (n2, c) = win
        fb = flow(b, a)  # b -> previous
        if want_speed:
            mag = np.hypot(fb[..., 0], fb[..., 1]) * scale_to_1080
            speeds.append({"frame": n1, "median": round(float(np.median(mag)), 1),
                           "p99": round(float(np.percentile(mag, 99)), 1)})
        if want_flicker:
            ff = flow(b, c)
            wa, wc = warp(a.astype(np.float32), fb), warp(c.astype(np.float32), ff)
            agree = np.abs(wa - wc) < 6
            resid = b.astype(np.float32) - 0.5 * (wa + wc)
            H, W = resid.shape
            rh, rw = H // GRID_H, W // GRID_W
            r = resid[: rh * GRID_H, : rw * GRID_W].reshape(GRID_H, rh, GRID_W, rw)
            g_ = agree[: rh * GRID_H, : rw * GRID_W].reshape(GRID_H, rh, GRID_W, rw)
            share = g_.mean(axis=(1, 3))
            cell = np.where(g_, r, 0).sum(axis=(1, 3)) / np.maximum(1, g_.sum(axis=(1, 3)))
            hit = (share > 0.6) & (np.abs(cell) > 10)
            if hit.any():
                ys, xs = np.nonzero(hit)
                events.append({"frame": n1, "t": round(n1 / fps, 3), "cells": int(hit.sum()),
                               "strength": round(float(np.abs(cell)[hit].max()), 1),
                               "box": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]})
    res = {}
    if want_flicker:
        res["flicker"] = {"grid": [GRID_W, GRID_H], "events": len(events),
                          "strongest": sorted(events, key=lambda e: -e["strength"])[:20], "all": events,
                          "note": "box = grid cells [x0, y0, x1, y1] on a 16×9 grid; strength = how far the region sits "
                                  "from where its two motion-compensated neighbours agree it should be (levels of 255)"}
    if want_pops and mad:
        m = np.array(mad)
        pops = []
        for i in range(1, len(m)):
            lo, hi = max(0, i - 8), min(len(m), i + 9)
            around = np.concatenate([m[lo:i], m[i + 1:hi]])
            base = float(np.median(around)) if around.size else 0
            if m[i] > 4 * base + 2 and m[i] > 6:
                pops.append({"frame": mad_nums[i], "t": round(mad_nums[i] / fps, 3), "diff": round(float(m[i]), 1),
                             "usual": round(base, 1)})
        res["pops"] = {"events": len(pops), "list": pops,
                       "note": "diff = mean absolute change from the frame before (levels of 255); usual = its neighbours'"}
    if want_speed and speeds:
        p99 = np.array([s["p99"] for s in speeds])
        res["speed"] = {"pxPerFrameAt1080": True,
                        "medianOfMedians": round(float(np.median([s["median"] for s in speeds])), 1),
                        "p99Max": round(float(p99.max()), 1),
                        "framesWholePictureOver30px": [s["frame"] for s in speeds if s["median"] > 30],
                        "framesFastestPartOver120px": [s["frame"] for s in speeds if s["p99"] > 120],
                        "fastest": sorted(speeds, key=lambda s: -s["p99"])[:15], "series": speeds}
    return res


MACHADO = {  # severity 1.0, linear RGB
    "protanopia": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    "deuteranopia": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    "tritanopia": [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
}


def colourblind(image: Path, out: Path) -> dict:
    from PIL import Image, ImageDraw
    im = np.asarray(Image.open(image).convert("RGB")).astype(np.float32) / 255
    lin = np.where(im <= 0.04045, im / 12.92, ((im + 0.055) / 1.055) ** 2.4)
    tiles = [("original", im)]
    for name, M in MACHADO.items():
        sim = np.clip(lin @ np.array(M, np.float32).T, 0, 1)
        srgb = np.where(sim <= 0.0031308, sim * 12.92, 1.055 * sim ** (1 / 2.4) - 0.055)
        tiles.append((name, srgb))
    gray = (lin @ np.array([0.2126, 0.7152, 0.0722], np.float32))
    gray = np.where(gray <= 0.0031308, gray * 12.92, 1.055 * gray ** (1 / 2.4) - 0.055)
    tiles.append(("greyscale", np.repeat(gray[..., None], 3, axis=2)))
    h, w = im.shape[:2]
    tw = 800
    th = int(h * tw / w)
    sheet = Image.new("RGB", (tw * 3 + 16, (th + 22) * 2 + 12), (20, 20, 22))
    d = ImageDraw.Draw(sheet)
    for i, (name, arr) in enumerate(tiles):
        r, c = divmod(i, 3)
        x, y = 4 + c * (tw + 4), 4 + r * (th + 26)
        sheet.paste(Image.fromarray((arr * 255).astype(np.uint8)).resize((tw, th)), (x, y + 20))
        d.text((x + 2, y + 2), name, fill=(220, 220, 220))
    p = out / f"{image.stem}-colourblind.png"
    sheet.save(p)
    return {"wrote": str(p)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", type=Path)
    ap.add_argument("--checks", default="exposure,flicker,pops,speed")
    ap.add_argument("--range")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    need("ffmpeg", "Install ffmpeg.")
    src = a.src.resolve()
    out = (a.out or src.parent / f"{src.stem}.checks").resolve()
    out.mkdir(parents=True, exist_ok=True)
    want = set(a.checks.split(","))
    if "colourblind" in want:
        print(json.dumps(colourblind(src, out), indent=1))
        return
    info = probe_video(src)
    fps = info["fps"]
    rng = tuple(int(x) for x in a.range.split("-")) if a.range else None
    res: dict = {"video": str(src), "fps": fps, "frames": info["frames"], "size": [info["width"], info["height"]],
                 "colour": {k: info.get(k) for k in ("color_space", "color_transfer", "color_primaries")}}
    if "exposure" in want:
        res["exposure"] = check_exposure(src, rng, fps)
    if want & {"flicker", "pops", "speed"}:
        res.update(check_motion(src, rng, fps, "flicker" in want, "pops" in want, "speed" in want))
    write_json(out / "checks.json", res)
    md = [f"# Checks: {src.name}\n", f"{info['frames']} frames at {fps:g} fps, {info['width']}×{info['height']}, "
          f"colour tags {res['colour']}. These are numbers to look at, not verdicts.\n"]
    summary = {}
    if "exposure" in res and res["exposure"].get("frames"):
        e = res["exposure"]
        md += ["## Exposure\n", f"Near white (luma > 215): median {e['nearWhiteMedian']:.1%}, 95th percentile "
               f"{e['nearWhiteP95']:.1%}. Frames over 25%: {len(e['framesOver25pctNearWhite'])}.\n",
               "| Frame | Time | Near white | Near black |", "|---|---|---|---|",
               *[f"| {r['frame']} | {clock(r['t'])} | {r['nearWhite']:.1%} | {r['nearBlack']:.1%} |" for r in e["worst"]], ""]
        summary["exposure"] = {"nearWhiteP95": e["nearWhiteP95"], "framesOver25pct": len(e["framesOver25pctNearWhite"])}
    if "flicker" in res:
        f = res["flicker"]
        md += ["## Flicker (a region jumping and straight back)\n", f"{f['events']} events.\n",
               "| Frame | Time | Cells | Strength | Box (16×9 grid) |", "|---|---|---|---|---|",
               *[f"| {x['frame']} | {clock(x['t'])} | {x['cells']} | {x['strength']} | {x['box']} |" for x in f["strongest"]], ""]
        summary["flicker"] = f["events"]
    if "pops" in res:
        p = res["pops"]
        md += ["## Pops (a frame far more different than its neighbours)\n", f"{p['events']} events.\n",
               "| Frame | Time | Change | Usual |", "|---|---|---|---|",
               *[f"| {x['frame']} | {clock(x['t'])} | {x['diff']} | {x['usual']} |" for x in p["list"][:40]], ""]
        summary["pops"] = p["events"]
    if "speed" in res:
        s = res["speed"]
        md += ["## Image speed (px per frame at 1080p)\n", f"Typical {s['medianOfMedians']}, fastest 1% up to "
               f"{s['p99Max']}. Frames where the whole picture moves over 30: {len(s['framesWholePictureOver30px'])}; "
               f"where its fastest part moves over 120: {len(s['framesFastestPartOver120px'])}.\n",
               "| Frame | Median | Fastest 1% |", "|---|---|---|",
               *[f"| {x['frame']} | {x['median']} | {x['p99']} |" for x in s["fastest"]], ""]
        summary["speed"] = {"p99Max": s["p99Max"], "wholePictureOver30px": len(s["framesWholePictureOver30px"]),
                            "fastestPartOver120px": len(s["framesFastestPartOver120px"])}
    (out / "checks.md").write_text("\n".join(md) + "\n")
    summary["wrote"] = [str(out / "checks.json"), str(out / "checks.md")]
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    try:
        main()
    except ToolError as e:
        fail(str(e))
