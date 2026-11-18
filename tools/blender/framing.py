"""How a subject sits in frame, whether it's actually seen, and how the camera moves: numbers to set against a shot card.

    blender -b <file.blend> -P tools/blender/framing.py -- --frames a-b[:step] --subject <object|collection>
                                                         [--camera <name>] [--out <report.json>]

Per frame: the subject's height in frame (0–1 of the frame's height: a close-up head is about 0.33–0.5), its centre
(x, y from the bottom-left, 0–1), how much of it is inside the frame, how much of it the camera actually sees (rays from
the lens to points on it, blocked by anything else), the camera's speed (m/s), turn rate (degrees/s) and their changes,
and whether the camera sits inside geometry. Turns faster than about 90°/s or sudden speed changes read as jolts unless
they're a deliberate whip with motion blur. These are numbers to read against the card, not a pass or fail.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402
from mathutils import Vector  # noqa: E402

from _film import args, frame_range, write_report  # noqa: E402

a = args()


def opt(name, default=None):
    return a[a.index(name) + 1] if name in a else default


scene = bpy.context.scene
cam = bpy.data.objects[opt("--camera")] if opt("--camera") else scene.camera
if cam is None:
    raise SystemExit("error: no camera")
subj_name = opt("--subject")
if not subj_name:
    raise SystemExit("error: --subject <object or collection>")
if subj_name in bpy.data.collections:
    subjects = [o for o in bpy.data.collections[subj_name].all_objects if o.type == "MESH"]
elif subj_name in bpy.data.objects:
    root = bpy.data.objects[subj_name]
    subjects = [o for o in [root, *root.children_recursive] if o.type == "MESH"]
else:
    raise SystemExit(f"error: no object or collection {subj_name!r}")
if not subjects:
    raise SystemExit("error: the subject has no meshes")
subject_set = set(o.name for o in subjects)
frames = frame_range(opt("--frames"), scene)
fps = scene.render.fps / scene.render.fps_base


def sample_points(dg, limit=400):
    pts = []
    for o in subjects:
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ev.matrix_world
        n = len(me.vertices)
        step = max(1, n * len(subjects) // limit)
        pts += [mw @ me.vertices[i].co for i in range(0, n, step)]
        ev.to_mesh_clear()
    return pts


rows = []
prev = None
for f in frames:
    scene.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    cam_ev = cam.evaluated_get(dg)
    loc = cam_ev.matrix_world.translation.copy()
    fwd = (cam_ev.matrix_world.to_3x3() @ Vector((0, 0, -1))).normalized()
    pts = sample_points(dg)
    proj = [world_to_camera_view(scene, cam_ev, p) for p in pts]
    front = [(p, q) for p, q in zip(pts, proj) if q.z > 0]
    inside = [q for _, q in front if 0 <= q.x <= 1 and 0 <= q.y <= 1]
    row = {"frame": f, "t": round(f / fps, 3)}
    if front:
        xs = [q.x for _, q in front]
        ys = [q.y for _, q in front]
        row.update({"height": round(max(ys) - min(ys), 3), "width": round(max(xs) - min(xs), 3),
                    "centre": [round((max(xs) + min(xs)) / 2, 3), round((max(ys) + min(ys)) / 2, 3)],
                    "inFrame": round(len(inside) / len(pts), 3),
                    "distance": round(min((p - loc).length for p, _ in front), 2)})
        # seen: rays from the lens to up to 60 points inside the frame
        probe = [p for p, q in front if 0 <= q.x <= 1 and 0 <= q.y <= 1][:: max(1, len(inside) // 60)]
        seen = 0
        for p in probe:
            d = p - loc
            dist = d.length
            hit, hloc, _n, _i, hobj, _m = scene.ray_cast(dg, loc, d.normalized(), distance=dist + 0.01)
            if not hit or (hobj and hobj.original.name in subject_set) or (hloc - loc).length >= dist - 0.02:
                seen += 1
        row["seen"] = round(seen / len(probe), 3) if probe else 0.0
    else:
        row.update({"height": 0, "inFrame": 0, "seen": 0})
    # inside geometry: rays in six directions that hit the back of a face nearby
    backs = 0
    for v in (Vector((1, 0, 0)), Vector((-1, 0, 0)), Vector((0, 1, 0)), Vector((0, -1, 0)), Vector((0, 0, 1)), Vector((0, 0, -1))):
        hit, _hl, nrm, _i, _o, _m = scene.ray_cast(dg, loc, v, distance=200)
        if hit and nrm.dot(v) > 0:
            backs += 1
    row["insideGeometry"] = backs >= 4
    if prev:
        dt = (f - prev["f"]) / fps
        speed = (loc - prev["loc"]).length / dt
        ang = math.degrees(math.acos(max(-1.0, min(1.0, fwd.dot(prev["fwd"]))))) / dt
        row["speed"] = round(speed, 2)
        row["turn"] = round(ang, 1)
        if "speed" in prev:
            row["accel"] = round((speed - prev["speed"]) / dt, 2)
            row["turnChange"] = round((ang - prev["turn"]) / dt, 1)
    prev = {"f": f, "loc": loc, "fwd": fwd, **({"speed": row["speed"], "turn": row["turn"]} if "speed" in row else {})}
    rows.append(row)

def mx(k):
    vals = [abs(r[k]) for r in rows if k in r]
    return max(vals) if vals else None

summary = {"subject": subj_name, "camera": cam.name, "frames": [frames[0], frames[-1]], "step": frames[1] - frames[0] if len(frames) > 1 else 1,
           "height": [min(r["height"] for r in rows), max(r["height"] for r in rows)],
           "seenMin": min(r["seen"] for r in rows), "inFrameMin": min(r["inFrame"] for r in rows),
           "speedMax": mx("speed"), "turnMax": mx("turn"), "accelMax": mx("accel"), "turnChangeMax": mx("turnChange"),
           "framesInsideGeometry": [r["frame"] for r in rows if r["insideGeometry"]],
           "framesSubjectMostlyHidden": [r["frame"] for r in rows if r["inFrame"] > 0.3 and r["seen"] < 0.5]}
out = opt("--out")
if out:
    write_report(Path(out), {"summary": summary, "frames": rows})
print(json.dumps(summary))
