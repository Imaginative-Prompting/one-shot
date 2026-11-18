"""Render a range of the open .blend to PNG frames, then encode them with the song's matching stretch.

    python3 tools/gpu.py run --label <what> -- \
      blender -b <file.blend> -P tools/blender/render.py -- --preset blocking|draft|look|final [--frames a-b]
                                                            [--out <dir>] [--name <name>] [--samples N] [--no-audio]

Presets (the scene's own look is kept; these set speed):
  blocking  Workbench, 50% size: layout, camera and timing only
  draft     the scene's engine, 50% size, 16 samples (EEVEE) / 32 (Cycles), motion blur on
  look      the scene's engine, full size, the scene's own samples: stills to judge
  final     the scene's engine, the delivery size (run.json "deliverySize", e.g. [3840, 2160]; else full size), the
            scene's own samples, motion blur on. --size WxH overrides the size for any preset.

Frames go to <out>/frames/<frame>.png (frame numbers are the film's), and <out>/<name>.mp4 is encoded at the scene's
fps, BT.709 tagged, with the master's audio for exactly that range when the film has one. Each run renders from the
file as it was loaded, so building can go on in another Blender meanwhile. Default <out>: renders/<name> in the film.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy  # noqa: E402

from _film import args, eevee_id, film_from, frame_range, master_of  # noqa: E402

a = args()


def opt(name, default=None):
    return a[a.index(name) + 1] if name in a else default


preset = opt("--preset", "draft")
if preset not in ("blocking", "draft", "look", "final"):
    raise SystemExit("error: --preset is blocking, draft, look or final")
scene = bpy.context.scene
frames = frame_range(opt("--frames"), scene)
try:
    film = film_from(opt("--film"))
except SystemExit:
    film = None
name = opt("--name", f"{preset}-{frames[0]}-{frames[-1]}")
out = Path(opt("--out") or (film / "renders" / name if film else Path(bpy.data.filepath).parent / "renders" / name))
(out / "frames").mkdir(parents=True, exist_ok=True)

r = scene.render
if preset == "blocking":
    r.engine = "BLENDER_WORKBENCH"
    r.resolution_percentage = 50
elif preset == "draft":
    r.resolution_percentage = 50
    r.use_motion_blur = True
    if r.engine.startswith("BLENDER_EEVEE"):
        scene.eevee.taa_render_samples = int(opt("--samples", 16))
    elif r.engine == "CYCLES":
        scene.cycles.samples = int(opt("--samples", 32))
else:
    r.resolution_percentage = 100
    if preset == "final":
        r.use_motion_blur = True
    if opt("--samples"):
        if r.engine.startswith("BLENDER_EEVEE"):
            scene.eevee.taa_render_samples = int(opt("--samples"))
        elif r.engine == "CYCLES":
            scene.cycles.samples = int(opt("--samples"))
size = opt("--size")
if not size and preset == "final" and film and (film / "run.json").exists():
    ds = json.loads((film / "run.json").read_text()).get("deliverySize")
    size = f"{ds[0]}x{ds[1]}" if ds else None
if size:
    w, _, h = size.lower().partition("x")
    if abs(int(w) / int(h) - r.resolution_x / r.resolution_y) > 0.01:
        raise SystemExit(f"error: {size} isn't the scene's aspect ({r.resolution_x}x{r.resolution_y})")
    r.resolution_x, r.resolution_y = int(w), int(h)
    if preset in ("look", "final"):
        r.resolution_percentage = 100
r.image_settings.file_format = "PNG"
r.image_settings.color_mode = "RGB"
r.image_settings.color_depth = "8"
r.use_file_extension = True

t0 = time.time()
for f in frames:
    scene.frame_set(f)
    r.filepath = str(out / "frames" / f"{f:06d}")
    bpy.ops.render.render(write_still=True)
took = time.time() - t0

fps = scene.render.fps / scene.render.fps_base
mp4 = out / f"{name}.mp4"
cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", f"{fps:g}", "-start_number", str(frames[0]),
       "-i", str(out / "frames" / "%06d.png")]
master = master_of(film)[0] if film else None
step = frames[1] - frames[0] if len(frames) > 1 else 1
if master and "--no-audio" not in a and step == 1:
    cmd += ["-ss", f"{frames[0] / fps:.6f}", "-t", f"{len(frames) / fps:.6f}", "-i", str(master),
            "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "256k"]
cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
        "-vf", "scale=out_color_matrix=bt709:out_range=tv",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart", str(mp4)]
if step == 1:
    subprocess.run(cmd, check=True)
print(json.dumps({"preset": preset, "engine": r.engine, "size": [r.resolution_x * r.resolution_percentage // 100,
                                                                  r.resolution_y * r.resolution_percentage // 100],
                  "frames": [frames[0], frames[-1]], "count": len(frames),
                  "secondsPerFrame": round(took / len(frames), 2), "out": str(out),
                  "mp4": str(mp4) if step == 1 else None}))
