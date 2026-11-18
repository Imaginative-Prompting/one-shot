"""Run a heavy job (a render, a batch of Blender frames, Whisper) one at a time.

    python3 tools/gpu.py run --label <what> -- <command …>
    python3 tools/gpu.py status

If settings.local.json has gpu.wrapper (a command template with {label} and {command}), the job goes through the
person's own queue that way. Otherwise a lock file in the system's temp folder makes jobs from every One Shot run on
this machine wait their turn. The job's exit code is this command's exit code.
"""
from __future__ import annotations

import _env  # noqa: F401
import argparse
import fcntl
import json
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path

from common import settings


def lock_path() -> Path:
    p = Path(os.environ.get("ONE_SHOT_GPU_LOCK", str(Path.home() / ".cache" / "one-shot" / "gpu.lock")))
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--label", required=True)
    r.add_argument("command", nargs=argparse.REMAINDER)
    sub.add_parser("status")
    a = ap.parse_args()
    lp = lock_path()
    if a.cmd == "status":
        info = lp.with_suffix(".json")
        print(info.read_text() if info.exists() else "nothing running")
        return
    cmd = a.command[1:] if a.command and a.command[0] == "--" else a.command
    if not cmd:
        ap.error("give the command after --")
    wrapper = settings()["gpu"].get("wrapper")
    if wrapper:
        line = wrapper.replace("{label}", shlex.quote(a.label)).replace("{command}", shlex.join(cmd))
        raise SystemExit(subprocess.run(line, shell=True).returncode)
    with open(lp, "w") as fh:
        t0 = time.time()
        print(f"[gpu] waiting for the lock: {a.label}", file=sys.stderr, flush=True)
        fcntl.flock(fh, fcntl.LOCK_EX)
        waited = time.time() - t0
        info = lp.with_suffix(".json")
        info.write_text(json.dumps({"label": a.label, "pid": os.getpid(), "since": time.strftime("%H:%M:%S"),
                                    "command": shlex.join(cmd)}))
        print(f"[gpu] running after {waited:.0f} s: {a.label}", file=sys.stderr, flush=True)
        try:
            code = subprocess.run(cmd).returncode
        finally:
            info.unlink(missing_ok=True)
        print(f"[gpu] done in {time.time() - t0 - waited:.0f} s (exit {code}): {a.label}", file=sys.stderr, flush=True)
        raise SystemExit(code)


if __name__ == "__main__":
    main()
