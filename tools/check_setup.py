"""What's installed, what's missing, and how to get it.

    python3 tools/check_setup.py [--install]

--install makes .venv/ and installs requirements.txt into it (the tools then use it automatically).
"""
from __future__ import annotations

import argparse
import importlib
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import _env  # noqa: E402,F401  (re-runs with .venv's Python once it exists)


def version(cmd: list[str]) -> str | None:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return (r.stdout or r.stderr).strip().splitlines()[0] if r.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--install", action="store_true")
    a = ap.parse_args()
    venv = ROOT / ".venv"
    if a.install:
        if not venv.exists():
            subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
        pip = venv / ("Scripts/pip.exe" if sys.platform == "win32" else "bin/pip")
        subprocess.run([str(pip), "install", "-q", "-r", str(ROOT / "requirements.txt")], check=True)
        print(f"installed requirements into {venv}")
        py = venv / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        raise SystemExit(subprocess.run([str(py), __file__]).returncode)

    rows: list[tuple[str, str, str]] = []  # (what, status, how to fix)

    def row(what: str, ok: str | None, fix: str) -> None:
        rows.append((what, ok or "MISSING", "" if ok else fix))

    row("Python 3.10+", platform.python_version() if sys.version_info >= (3, 10) else None, "Install Python 3.10 or newer.")
    row("tools environment (.venv)", "present" if venv.exists() else None, "python3 tools/check_setup.py --install")
    for mod, pip in [("numpy", "numpy"), ("scipy", "scipy"), ("PIL", "pillow"), ("cv2", "opencv-python-headless"),
                     ("mido", "mido"), ("pronouncing", "pronouncing")]:
        try:
            m = importlib.import_module(mod)
            row(f"python: {pip}", getattr(m, "__version__", "ok"), "")
        except ImportError:
            row(f"python: {pip}", None, "python3 tools/check_setup.py --install")
    row("ffmpeg", version(["ffmpeg", "-version"]), "Install ffmpeg (macOS: brew install ffmpeg).")
    blender = shutil.which("blender") or ("/Applications/Blender.app/Contents/MacOS/Blender"
                                          if Path("/Applications/Blender.app").exists() else None)
    row("Blender", version([blender, "--version"]) if blender else None,
        "Install Blender 4.2 or newer from blender.org and put `blender` on your PATH.")
    try:
        from common import whisper_backend
        row("Whisper", whisper_backend(), "")
    except Exception as e:  # noqa: BLE001
        row("Whisper", None, str(e))
    from common import settings
    s = settings()
    local = ROOT / "settings.local.json"
    row("settings.local.json", "present" if local.exists() else None,
        "Optional: copy settings.example.json to settings.local.json for the WIP and a GPU queue.")
    wip_cfg = s["wip"].get("config")
    wip_bin = s["wip"].get("bin")
    wip_ok = wip_cfg and wip_bin and Path(wip_cfg).exists() and Path(wip_bin).exists()
    row("WIP (optional)", "connected" if wip_ok else None,
        "Optional: install https://github.com/Imaginative-Prompting/wip and set wip.config and wip.bin; "
        "without it, entries are written to films/<slug>/wip/ as Markdown.")
    row("node (for the WIP)", version(["node", "--version"]) if wip_ok else "not needed", "Install Node.js 22+.")
    row("GPU queue (optional)", "set" if s["gpu"].get("wrapper") else "built-in lock", "")

    w = max(len(r[0]) for r in rows)
    for what, status, fix in rows:
        print(f"{what.ljust(w)}  {status}" + (f"\n{' ' * w}  -> {fix}" if fix else ""))
    print("\nAlso needed, outside this machine's tools: a Suno account (a paid plan for commercial use, WAV and stems) "
          "signed in in Chrome, and Claude in Chrome connected, so the run can drive suno.com.")
    missing = [r for r in rows if r[1] == "MISSING" and "Optional" not in r[2]]
    print(json.dumps({"ok": not missing, "missing": [r[0] for r in missing]}))


if __name__ == "__main__":
    main()
