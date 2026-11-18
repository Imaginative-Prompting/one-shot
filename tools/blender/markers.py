"""Put the song's clock into the open .blend: fps, size and length from the film, the master as a sound strip, a marker
for every section and line, and the full timing as a text datablock ("one_shot_timing") scripts can read. Then save.

    blender -b <file.blend> -P tools/blender/markers.py -- [<film>] [--no-save]

Song time t is frame t × fps from frame 0. Markers named "§<section>" and "L<line id>" are replaced each run; other
markers are left alone.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy  # noqa: E402

from _film import args, film_from, master_of  # noqa: E402

a = args()
save = "--no-save" not in a
pos = [x for x in a if not x.startswith("--")]
film = film_from(pos[0] if pos else None)
run = json.loads((film / "run.json").read_text())
timing = json.loads((film / "song" / "timing.json").read_text())
smap_path = film / "song" / "map.json"
smap = json.loads(smap_path.read_text()) if smap_path.exists() else None
fps = int(run.get("fps", 30))
w, h = run.get("size", [1920, 1080])
master, _ = master_of(film)
duration = smap["duration"] if smap else timing["duration"]

scene = bpy.context.scene
scene.render.fps = fps
scene.render.fps_base = 1.0
scene.render.resolution_x, scene.render.resolution_y = int(w), int(h)
scene.frame_start = 0
scene.frame_end = int(round(duration * fps)) - 1

for m in list(scene.timeline_markers):
    if m.name.startswith("§") or (m.name.startswith("L") and m.name[1:].isdigit()):
        scene.timeline_markers.remove(m)
sections = smap["sections"] if smap else timing["sections"]
for s in sections:
    scene.timeline_markers.new(f"§{s['name']}", frame=int(round(s["t0"] * fps)))
for line in timing["lines"]:
    scene.timeline_markers.new(f"L{line['id']}", frame=int(round(line["t0"] * fps)))

if master:
    se = scene.sequence_editor or scene.sequence_editor_create()
    strips = se.strips if hasattr(se, "strips") else se.sequences  # Blender 5 renamed sequences to strips
    for st in list(strips):
        if st.type == "SOUND" and st.name == "song":
            strips.remove(st)
    new = strips.new_sound("song", str(master), channel=1, frame_start=0)
    new.name = "song"

txt = bpy.data.texts.get("one_shot_timing") or bpy.data.texts.new("one_shot_timing")
txt.clear()
txt.write(json.dumps({"fps": fps, "timing": timing, "map": smap}))

if save:
    bpy.ops.wm.save_mainfile()
print(json.dumps({"fps": fps, "frames": scene.frame_end + 1, "sections": len(sections), "lines": len(timing["lines"]),
                  "sound": str(master) if master else None, "saved": save}))
