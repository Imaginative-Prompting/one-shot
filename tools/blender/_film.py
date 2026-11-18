"""Shared helpers for the Blender scripts (they run inside Blender's own Python, which has bpy and numpy)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def args() -> list[str]:
    """The script's own arguments: everything after the `--` on Blender's command line."""
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def film_from(arg: str | None = None) -> Path:
    """A film folder by slug or path; with none given, the film whose blender/ folder holds the open file."""
    import bpy
    if arg:
        p = Path(arg)
        if (p / "run.json").exists():
            return p.resolve()
        q = ROOT / "films" / arg
        if (q / "run.json").exists():
            return q
        raise SystemExit(f"error: no film {arg!r}")
    blend = Path(bpy.data.filepath)
    for parent in blend.parents:
        if (parent / "run.json").exists():
            return parent
    raise SystemExit("error: this .blend isn't inside a film folder; pass the film")


def frame_range(spec: str, scene) -> list[int]:
    if not spec:
        return list(range(scene.frame_start, scene.frame_end + 1))
    rng, _, step = spec.partition(":")
    a, _, b = rng.partition("-")
    return list(range(int(a), int(b or a) + 1, int(step or 1)))


def write_report(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1) + "\n")


def master_of(film: Path) -> tuple[Path | None, dict | None]:
    mdir = film / "song" / "master"
    if mdir.is_dir():
        for j in sorted(mdir.glob("*.json")):
            info = json.loads(j.read_text())
            if "wav" in info:
                return mdir / info["wav"], info
    return None, None


def eevee_id() -> str:
    import bpy
    ids = {e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items}
    for cand in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        if cand in ids:
            return cand
    return "CYCLES"
