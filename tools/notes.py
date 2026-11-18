"""The person's notes on the film's WIP entries, and your replies.

    python3 tools/notes.py <film>                         # notes not yet answered, oldest first (exit 0; none → [])
    python3 tools/notes.py <film> --all                   # every note and reply
    python3 tools/notes.py <film> --reply <note id> "…"   # your answer under their note; marks it answered
    python3 tools/notes.py <film> --wait <minutes>        # the note watcher: ends when a NEW note arrives or the time
                                                          # is up (run it in the background, restart it after: it wakes you)

With the WIP set up (settings.local.json), notes are the ones written on the film's entries in the WIP page. Without it,
the person can write notes into films/<slug>/notes.md (a blank line between notes); each note's id is a hash of its text,
and replies go under it in the same file. Notes typed in chat count the same: copy them into prompt.md yourself.
"""
from __future__ import annotations

import _env  # noqa: F401
import argparse
import hashlib
import json
from pathlib import Path

from common import ToolError, fail, film_dir, load_run, now_iso, save_run
from wip import project, wip_cfg, wip_cli


def from_wip(film: Path, everything: bool) -> list[dict]:
    cfg, binp = wip_cfg()
    pid, _ = project(film)
    r = wip_cli(cfg, binp, "notes", "--project", pid, "--state", "all" if everything else "open")
    if r.returncode != 0:
        msg = r.stderr.strip()
        if "Unknown command" in msg:
            raise ToolError("this WIP has no notes yet: update it (git pull in the WIP's folder) and restart its server")
        if "ENOENT" in msg or "not found" in msg.lower():
            return []
        raise ToolError(f"couldn't read notes: {msg}")
    return json.loads(r.stdout or "[]")


def from_file(film: Path, everything: bool) -> list[dict]:
    p = film / "notes.md"
    if not p.exists():
        return []
    run = load_run(film)
    answered = set(run.get("notesAnswered", []))
    notes = []
    for block in [b.strip() for b in p.read_text().split("\n\n") if b.strip()]:
        if block.startswith("#") or block.startswith("> reply"):
            continue
        nid = hashlib.sha1(block.encode()).hexdigest()[:10]
        if everything or nid not in answered:
            notes.append({"id": nid, "entry": None, "author": "owner", "text": block, "open": nid not in answered})
    return notes


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("film")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--reply", nargs=2, metavar=("NOTE_ID", "TEXT"))
    ap.add_argument("--wait", type=float, metavar="MINUTES")
    a = ap.parse_args()
    film = film_dir(a.film)
    if a.wait:
        # The note watcher: ends as soon as a note arrives that it hasn't reported before (so restarting it after
        # handling one doesn't return the same note again), or when the time is up.
        import time
        end = time.time() + a.wait * 60
        while True:
            run = load_run(film)
            seen = set(run.get("notesSeen", []))
            notes = [n for n in (from_wip(film, False) if wip_cfg() else from_file(film, False)) if n["id"] not in seen]
            if notes or time.time() >= end:
                if notes:
                    run = load_run(film)
                    run["notesSeen"] = sorted(set(run.get("notesSeen", [])) | {n["id"] for n in notes})
                    save_run(film, run)
                print(json.dumps({"waited": "until a new note" if notes else f"{a.wait:g} minutes, no new note",
                                  "notes": notes}, indent=1, ensure_ascii=False))
                return
            time.sleep(max(1.0, min(20.0, end - time.time())))
    if a.reply:
        nid, text = a.reply
        if wip_cfg():
            cfg, binp = wip_cfg()
            pid, _ = project(film)
            notes = from_wip(film, True)
            target = next((n for n in notes if n["id"] == nid), None)
            if not target:
                raise ToolError(f"no note {nid}")
            r = wip_cli(cfg, binp, "note", "--project", pid, "--entry", target["entry"], "--reply-to", nid, "--text", text)
            if r.returncode != 0:
                raise ToolError(f"couldn't reply: {r.stderr.strip()}")
            print(r.stdout.strip())
        else:
            p = film / "notes.md"
            blocks = p.read_text().split("\n\n")
            for i, b in enumerate(blocks):
                if hashlib.sha1(b.strip().encode()).hexdigest()[:10] == nid:
                    blocks.insert(i + 1, f"> reply ({now_iso()}): {text}")
                    break
            else:
                raise ToolError(f"no note {nid}")
            p.write_text("\n\n".join(blocks))
            run = load_run(film)
            run.setdefault("notesAnswered", []).append(nid)
            save_run(film, run)
            print(json.dumps({"replied": nid}))
        return
    notes = from_wip(film, a.all) if wip_cfg() else from_file(film, a.all)
    print(json.dumps(notes, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except ToolError as e:
        fail(str(e))
