"""Make a film folder: films/<slug>/ with its run.json, log.md and empty stage folders.

    python3 tools/new_film.py <slug> [--hours N] [--engine blender] [--length 3:30]
"""
from __future__ import annotations

import _env  # noqa: F401
import argparse
import re

from common import FILMS, ToolError, fail, now_iso, save_run, settings

STAGES = ["intake", "lyric", "song", "treatment", "shots", "blocking", "build", "edit"]
FOLDERS = ["research", "lyric", "song", "treatment", "shots", "blender/build", "renders", "review", "wip"]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("--hours", type=float, default=None, help="a time limit for the whole run, if the prompt gives one")
    ap.add_argument("--engine", default="blender")
    ap.add_argument("--length", default=None, help="target song length, m:ss, if the prompt gives one")
    a = ap.parse_args()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,60}", a.slug):
        fail("the slug is lowercase letters, digits and dashes (at most 61 characters)")
    film = FILMS / a.slug
    if film.exists():
        fail(f"{film} already exists; pick another name or carry on with that film")
    for f in FOLDERS:
        (film / f).mkdir(parents=True)
    run = {
        "slug": a.slug,
        "stage": "intake",
        "stages": {s: "pending" for s in STAGES},
        "started": now_iso(),
        "hours": a.hours,
        "engine": a.engine,
        "length": a.length,
        "fps": 30,
        "size": [1920, 1080],
        "pickWindowMinutes": settings().get("pickWindowMinutes", 30),
        "wipProject": f"{settings()['wip'].get('projectPrefix') or ''}{a.slug}",
        "decisions": [],
    }
    save_run(film, run)
    (film / "prompt.md").write_text("# The person's words, verbatim\n\nPaste the opening prompt below with its date and time. "
                                    "Every later note goes here too, verbatim, with its time and where it was written.\n\n")
    (film / "log.md").write_text(f"# {a.slug}\n\nNEXT: stage 0, intake (pipeline/0-intake.md).\n\n## Log (newest last)\n\n"
                                 f"- {run['started']}: film folder made.\n")
    (film / "assets.md").write_text("# Assets\n\nEvery downloaded asset: what, where from, its license, and where it's used.\n\n")
    print(film)


if __name__ == "__main__":
    try:
        main()
    except ToolError as e:
        fail(str(e))
