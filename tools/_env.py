"""Run every tool with the repo's own Python environment (.venv) when it exists.

Imported first by each tool: if .venv/ exists and this isn't its Python, re-run the same command with it. Set
ONE_SHOT_NO_VENV=1 to use whatever Python started the tool.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_VENV = ROOT / ".venv"
_PY = _VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")

if _PY.exists() and not os.environ.get("ONE_SHOT_NO_VENV"):
    try:
        same = Path(sys.prefix).resolve() == _VENV.resolve()
    except OSError:
        same = False
    if not same:
        os.execv(str(_PY), [str(_PY), *sys.argv])
