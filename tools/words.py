"""What Whisper hears in a take, against the lyric, line by line.

    python3 tools/words.py <audio> <lyric.txt> <outDir>

Writes <outDir>/heard.json (Whisper's words with times), words.md (a table to read) and words.json, and prints a summary:
the length, lines heard clearly (at least 70% of their words), words heard, where the first word starts, and the unclear
lines. Whisper hears sung words less reliably than speech: a flagged line is one to listen to, not proof.

Run it once per take; never in a loop. On a Mac the MLX backend needs the GPU, so run it outside any sandbox.
"""
from __future__ import annotations

import _env  # noqa: F401
import argparse
import json
from pathlib import Path

from common import ToolError, align, clock, fail, probe_seconds, read_lyric, transcribe, words_of, write_json

CLEAR = 0.7


def check(audio: Path, lyric: Path, out: Path, heard: dict | None = None) -> dict:
    lines = read_lyric(lyric)
    out.mkdir(parents=True, exist_ok=True)
    if heard is None:
        prompt = " ".join(l.text for l in lines)[:800]  # the lyric as a hint helps Whisper with names and odd words
        heard = transcribe(audio, prompt=prompt)
        write_json(out / "heard.json", heard)
    expected, line_of = [], []
    for i, ln in enumerate(lines):
        for w in words_of(ln.text):
            expected.append(w)
            line_of.append(i)
    tokens, times = [], []
    for w in heard["words"]:
        for t in words_of(w["word"]):
            tokens.append(t)
            times.append(w["start"])
    hits = [0] * len(lines)
    first_at: list[float | None] = [None] * len(lines)
    for kind, i, j in align(expected, tokens):
        if i is None:
            continue
        li = line_of[i]
        if kind == "same":
            hits[li] += 1
        if j is not None and first_at[li] is None:
            first_at[li] = times[j]
    report = []
    for i, ln in enumerate(lines):
        n = max(1, len(words_of(ln.text)))
        report.append({"line": ln.id, "section": ln.section, "text": ln.text, "heard": round(100 * hits[i] / n),
                       "at": first_at[i]})
    unclear = [r for r in report if r["heard"] / 100 < CLEAR]
    seconds = probe_seconds(audio)
    summary = {
        "take": audio.name, "seconds": round(seconds, 2), "clock": clock(seconds), "lines": len(lines),
        "clear": len(lines) - len(unclear), "words": len(expected), "wordsHeard": sum(hits),
        "firstWordAt": heard["words"][0]["start"] if heard["words"] else None,
        "lastWordEnd": heard["words"][-1]["end"] if heard["words"] else None,
        "whisper": f'{heard.get("backend")} {heard.get("model")}',
        "unclear": [{"line": u["line"], "heard": u["heard"], "at": None if u["at"] is None else clock(u["at"]),
                     "text": u["text"]} for u in unclear],
    }
    write_json(out / "words.json", {"summary": summary, "lines": report})
    rows = "\n".join(f"| {r['line']} | {r['heard']}%{' ✕' if r['heard'] / 100 < CLEAR else ''} | "
                     f"{'—' if r['at'] is None else clock(r['at'])} | {r['text']} |" for r in report)
    (out / "words.md").write_text(
        f"# Words check: {audio.name}\n\nLength {summary['clock']}. Whisper heard {summary['clear']} of {len(lines)} lines "
        f"clearly (at least {int(CLEAR * 100)}% of their words) and {sum(hits)} of {len(expected)} words. A flagged line is "
        f"one to listen to, not proof it's unclear.\n\n| Line | Heard | At | Lyric |\n|---|---|---|---|\n{rows}\n\n"
        f"## What Whisper heard\n\n{heard.get('text', '')}\n")
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio", type=Path)
    ap.add_argument("lyric", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--heard", type=Path, help="reuse an earlier heard.json instead of running Whisper again")
    a = ap.parse_args()
    heard = json.loads(a.heard.read_text()) if a.heard else None
    print(json.dumps(check(a.audio, a.lyric, a.out, heard), indent=1))


if __name__ == "__main__":
    try:
        main()
    except ToolError as e:
        fail(str(e))
