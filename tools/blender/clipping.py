"""Things passing through things: every pair of visible meshes whose surfaces intersect, frame by frame.

    blender -b <file.blend> -P tools/blender/clipping.py -- --frames a-b[:step] [--only <collection,…>]
                                                          [--ignore <pairs.json>] [--out <report.json>]

Meshes under the same top-level parent (one character's body, clothes and hair; one prop's parts) count as one thing,
so their own overlaps aren't reported. A pair that intersects in every checked frame is listed apart ("always"): often a
resting contact (a cup on a table) or modelled that way on purpose; look at it once. A pair that starts intersecting
partway is usually motion going through something (a hand into a table, two people walking through each other).
--ignore takes a JSON list of [objectA, objectB] pairs you've decided are fine. Numbers to look at, not a verdict.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy  # noqa: E402
from mathutils.bvhtree import BVHTree  # noqa: E402

from _film import args, frame_range, write_report  # noqa: E402

a = args()


def opt(name, default=None):
    return a[a.index(name) + 1] if name in a else default


scene = bpy.context.scene
frames = frame_range(opt("--frames"), scene)
fps = scene.render.fps / scene.render.fps_base
if opt("--only"):
    objs = {o for c in opt("--only").split(",") for o in bpy.data.collections[c].all_objects}
else:
    objs = set(scene.objects)
meshes = [o for o in objs if o.type == "MESH" and not o.hide_render and o.visible_get()]
ignore = {tuple(sorted(p)) for p in json.loads(Path(opt("--ignore")).read_text())} if opt("--ignore") else set()


def group(o):
    while o.parent:
        o = o.parent
    return o.name


hits: dict[tuple[str, str], list[tuple[int, int]]] = {}
for f in frames:
    scene.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    data = []
    for o in meshes:
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ev.matrix_world
        verts = [mw @ v.co for v in me.vertices]
        polys = [tuple(p.vertices) for p in me.polygons]
        ev.to_mesh_clear()
        if not verts or not polys:
            continue
        lo = [min(v[i] for v in verts) for i in range(3)]
        hi = [max(v[i] for v in verts) for i in range(3)]
        data.append((o, group(o), lo, hi, verts, polys))
    trees = {}
    for i in range(len(data)):
        oa, ga, loa, hia, va, pa = data[i]
        for j in range(i + 1, len(data)):
            ob, gb, lob, hib, vb, pb = data[j]
            if ga == gb:
                continue
            pair = tuple(sorted((oa.name, ob.name)))
            if pair in ignore:
                continue
            if any(hia[k] < lob[k] or hib[k] < loa[k] for k in range(3)):
                continue
            ta = trees.get(oa.name) or trees.setdefault(oa.name, BVHTree.FromPolygons(va, pa))
            tb = trees.get(ob.name) or trees.setdefault(ob.name, BVHTree.FromPolygons(vb, pb))
            n = len(ta.overlap(tb))
            if n:
                hits.setdefault(pair, []).append((f, n))

always, starts = [], []
for pair, fl in sorted(hits.items()):
    item = {"pair": list(pair), "frames": len(fl), "first": fl[0][0], "last": fl[-1][0],
            "firstTime": round(fl[0][0] / fps, 3), "maxFaces": max(n for _, n in fl)}
    (always if len(fl) == len(frames) else starts).append(item)
summary = {"frames": [frames[0], frames[-1]], "checked": len(frames), "meshes": len(meshes),
           "pairsIntersecting": len(hits), "partway": starts, "always": always}
out = opt("--out")
if out:
    write_report(Path(out), {"summary": summary, "perFrame": {"|".join(k): v for k, v in hits.items()}})
print(json.dumps(summary))
