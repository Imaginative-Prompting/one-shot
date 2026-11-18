"""Transcribe audio with word times, once, to a JSON file other tools can reuse (words.py --heard, timing.py --heard).

    python3 tools/whisper.py <audio> <out.json> [--lyric <lyric.txt>] [<audio> <out.json> …]

Several pairs load the model once each but run in one call, so one GPU ticket covers them. The lyric, when given, is
passed as Whisper's prompt (it helps with names and odd words). Never run it in a loop: on a Mac the MLX backend needs
the GPU and runs outside any sandbox.
"""
from __future__ import annotations

import _env  # noqa: F401
import argparse
import json
import time
from pathlib import Path

from common import ToolError, fail, read_lyric, transcribe, write_json


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pairs", nargs="+", help="<audio> <out.json> [<audio> <out.json> …]")
    ap.add_argument("--lyric", type=Path)
    a = ap.parse_args()
    if len(a.pairs) % 2:
        fail("give pairs of <audio> <out.json>")
    prompt = " ".join(l.text for l in read_lyric(a.lyric))[:800] if a.lyric else None
    for audio, out in zip(a.pairs[::2], a.pairs[1::2]):
        t0 = time.time()
        heard = transcribe(Path(audio), prompt=prompt)
        heard["took"] = round(time.time() - t0, 1)
        write_json(Path(out), heard)
        print(json.dumps({"audio": audio, "out": out, "words": len(heard["words"]), "took": heard["took"]}))


if __name__ == "__main__":
    try:
        main()
    except ToolError as e:
        fail(str(e))
