"""Time used and left, and each remaining shot's share when the run has a number of hours.

    python3 tools/clock.py <film>

Reads run.json (started, hours, pauses, finalRenderAfterLimit, firstCreateAt, renderSecondsPerFrame, fps) and
shots/shots.json (each shot's id, t0, t1, and status: "done" once its final render is spliced, or once it's finished at
its final look when the final render comes after the limit).

- Time spent paused doesn't count: run.json "pauses" is a list of {"from": iso, "to": iso}; a pause with no "to" is
  still going.
- The edit's reserve is 45 minutes for the joins, checks and the report, plus the final render of whatever isn't
  rendered yet (frames × the measured seconds per frame, plus 15%). With "finalRenderAfterLimit": true, the person has
  set the final render outside the time limit, so it isn't reserved: every shot is finished at its final look inside
  the limit, and the final render runs after it.
- The rest is shared equally among the shots not done, so a shot that finishes early gives its time to the others.
"""
from __future__ import annotations

import _env  # noqa: F401
import argparse
import json
from datetime import datetime, timedelta

from common import ToolError, fail, film_dir, load_run


def hm(s: float) -> str:
    s = max(0, int(s))
    return f"{s // 3600}h{(s % 3600) // 60:02d}m"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("film")
    a = ap.parse_args()
    film = film_dir(a.film)
    run = load_run(film)
    started = datetime.fromisoformat(run["started"])
    now = datetime.now().astimezone()
    paused = 0.0
    for p in run.get("pauses") or []:
        p0 = datetime.fromisoformat(p["from"])
        p1 = datetime.fromisoformat(p["to"]) if p.get("to") else now
        paused += max(0.0, (min(p1, now) - p0).total_seconds())
    elapsed = (now - started).total_seconds() - paused
    out = {"now": now.isoformat(timespec="minutes"), "started": run["started"], "elapsed": hm(elapsed),
           "stage": run.get("stage")}
    if paused:
        out["paused"] = hm(paused)
    first = run.get("firstCreateAt")
    if first:
        took = (datetime.fromisoformat(first) - started).total_seconds()
        out["firstCreate"] = f"{int(took // 60)} min after the start (target: 20)"
    else:
        out["firstCreate"] = (f"not yet: {int(elapsed // 60)} min in, target 20"
                              + ("; past the target: skip to the Create now" if elapsed > 20 * 60 else ""))
    shots_path = film / "shots" / "shots.json"
    shots = json.loads(shots_path.read_text()) if shots_path.exists() else []
    fps = run.get("fps", 30)
    left = [s for s in shots if s.get("status") != "done"]
    frames_left = sum(round(s["t1"] * fps) - round(s["t0"] * fps) for s in left)
    out["shots"] = {"total": len(shots), "done": len(shots) - len(left), "framesLeft": frames_left}
    if run.get("hours"):
        total = run["hours"] * 3600
        remaining = total - elapsed
        open_pause = any(not p.get("to") for p in run.get("pauses") or [])
        out["deadline"] = ("paused: the deadline moves on when the pause ends" if open_pause else
                           (now + timedelta(seconds=remaining)).isoformat(timespec="minutes"))
        spf = run.get("renderSecondsPerFrame")
        after = bool(run.get("finalRenderAfterLimit"))
        render = frames_left * spf * 1.15 if spf else None
        reserve = (0 if after else (render or 0)) + 45 * 60
        out.update({"hours": run["hours"], "remaining": hm(remaining), "editReserve": hm(reserve)})
        if run.get("graceHours"):
            out["grace"] = (f"up to {run['graceHours']:g} h more past the deadline, if you ask the person near the end and "
                            "say how much and what for; plan the shots for the deadline, not the grace")
        if after:
            out["finalRender"] = ("after the limit (the person's call): finish every shot at its final look inside it; "
                                  "the final render and its checks run afterwards"
                                  + (f", about {hm(render)} at the measured speed" if render is not None else ""))
        else:
            out["renderEstimate"] = (hm(render) if render is not None else
                                     "unknown: set run.json renderSecondsPerFrame from a look frame's final render")
        if left:
            per = (remaining - reserve) / len(left)
            out["perShot"] = hm(per)
            if per <= 0:
                out["warning"] = ("No time left for the shots beyond the edit's reserve: finish each remaining shot "
                                  "cleanly at its simplest strong version, and keep the reserve for the final render.")
    else:
        out["hours"] = None
        out["note"] = "No time limit: a shot is finished when you and the critic can't find anything worth improving."
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    try:
        main()
    except ToolError as e:
        fail(str(e))
