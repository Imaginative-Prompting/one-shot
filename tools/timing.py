"""Every sung word's onset, measured on the vocal stem: song/timing.json, and song/timing.png to look at.

    python3 tools/timing.py <song dir> [--lyric <lyric.txt>] [--vocal <stem.wav>] [--heard <heard.json>] [--out <dir>]

1. Whisper on the vocal stem (or --heard, an earlier transcript of the same audio), aligned to the lyric word by word.
2. Each heard word's start moved onto the voice's real onset: the strongest rise of the vocal stem's 150 Hz–4 kHz flux
   near Whisper's time (Whisper's word times on singing drift by a tenth of a second or more), never before the word
   before it.
3. Words Whisper missed are placed evenly between their timed neighbours, and marked "heard": false.

Song time is the master's: when song/master/<name>.json says the take was trimmed, its stems in song/master/stems/ are
used (they're trimmed the same way). If the song has Suno's vocal MIDI in song/midi/, the median gap between word onsets
and the nearest note starts is reported as a cross-check only: MIDI note times can run early or late against the audio.
"""
from __future__ import annotations

import _env  # noqa: F401
import argparse
import json
from pathlib import Path

import numpy as np

from audio import FPS, envelopes, frame_time, load, midi_notes, onset_peaks
from common import ToolError, align, clock, fail, probe_seconds, read_lyric, transcribe, words_of, write_json


def find_master(song: Path) -> tuple[Path | None, dict | None]:
    mdir = song / "master"
    if mdir.is_dir():
        for j in sorted(mdir.glob("*.json")):
            info = json.loads(j.read_text())
            if "wav" in info:
                return mdir / info["wav"], info
    return None, None


def find_vocal(song: Path, info: dict | None) -> Path:
    for d in ([song / "master" / "stems"] if info and info.get("stems") else []) + [song / "stems"]:
        if d.is_dir():
            cands = [f for f in sorted(d.iterdir()) if "vocal" in f.name.lower() and "backing" not in f.name.lower()]
            if cands:
                return cands[0]
    raise ToolError(f"no vocal stem in {song}/master/stems or {song}/stems (a file with 'vocal' in its name); pass --vocal")


def refine_onsets(starts: list[float], env: dict) -> tuple[list[float], list[float]]:
    """Move each start onto the voice's real onset; returns (refined, shift).

    First, where the stem is silent at Whisper's start (Whisper often folds the silence before a phrase into its first
    word), the start moves to where voicing begins, up to 1.2 s later and never past the next word. Then it moves onto
    the strongest nearby rise of the voice band."""
    voice = env["voice"]
    rms = env["rms_db"]
    loud = float(np.percentile(rms, 95))
    active = rms > loud - 30
    t_env = env["t"]
    peaks = onset_peaks(voice, min_gap_frames=4, median_frames=101)
    pk_frames = np.array([p[0] for p in peaks]) if peaks else np.zeros(0, int)
    pk_strength = np.array([p[1] for p in peaks]) if peaks else np.zeros(0)
    pk_t = frame_time(pk_frames)
    out, shift = [], []
    prev = -1.0
    for k, s0 in enumerate(starts):
        s = s0
        nxt = starts[k + 1] if k + 1 < len(starts) else s + 1.2
        i = int(np.searchsorted(t_env, s))
        if i < active.size and not active[i:i + 5].any():
            limit = min(s + 1.2, nxt - 0.05)
            j = int(np.searchsorted(t_env, limit))
            on = np.nonzero(active[i:j])[0]
            if on.size:
                s = float(t_env[i + on[0]])
        lo, hi = s - 0.20, s + 0.15
        m = (pk_t >= max(lo, prev + 0.05)) & (pk_t <= hi) & (pk_strength >= 0.08)
        if m.any():
            cand_t, cand_s = pk_t[m], pk_strength[m]
            score = cand_s - 2.0 * np.abs(cand_t - s)  # strong, and close to where the voice starts
            t = float(cand_t[int(np.argmax(score))])
        else:
            t = max(s, prev + 0.05)
        out.append(t)
        shift.append(t - s0)
        prev = t
    return out, shift


def draw(png: Path, y: np.ndarray, sr: int, lines: list[dict], duration: float, row_s: float = 15.0) -> None:
    from PIL import Image, ImageDraw, ImageFont
    rows = int(np.ceil(duration / row_s))
    W, RH = 1800, 150
    img = Image.new("RGB", (W, rows * RH + 10), (22, 23, 26))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default(size=13)
    except TypeError:
        font = ImageFont.load_default()
    hop = sr // 200
    env = np.sqrt(np.convolve(y ** 2, np.ones(hop) / hop, mode="same")[::hop])
    env = env / (env.max() + 1e-9)
    words = [(w, l["id"]) for l in lines for w in l["words"]]
    for r in range(rows):
        top = r * RH + 5
        t0 = r * row_s
        d.text((6, top + 2), clock(t0), fill=(150, 150, 150), font=font)
        a, b = int(t0 * 200), int(min(duration, t0 + row_s) * 200)
        seg = env[a:b]
        mid = top + 95
        for i, v in enumerate(seg):
            x = 60 + int(i / (row_s * 200) * (W - 70))
            d.line([(x, mid - v * 45), (x, mid + v * 45)], fill=(86, 180, 233))
        for w, lid in words:
            if t0 <= w["t0"] < t0 + row_s:
                x = 60 + int((w["t0"] - t0) / row_s * (W - 70))
                col = (230, 159, 0) if w["heard"] else (204, 121, 167)
                d.line([(x, top + 30), (x, top + 145)], fill=col, width=1)
                d.text((x + 2, top + 18 + (hash((lid, w["w"], w["t0"])) % 3) * 4), w["w"], fill=col, font=font)
    d.text((W - 520, 4), "blue: vocal level   orange: heard word onset   pink: placed between neighbours",
           fill=(150, 150, 150), font=font)
    img.save(png)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("song", type=Path)
    ap.add_argument("--lyric", type=Path)
    ap.add_argument("--vocal", type=Path)
    ap.add_argument("--heard", type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    song = a.song.resolve()
    out = (a.out or song).resolve()
    lyric = a.lyric or song.parent / "lyric" / "lyric.txt"
    master, info = find_master(song)
    vocal = a.vocal or find_vocal(song, info)
    duration = probe_seconds(master) if master else probe_seconds(vocal)

    if a.heard:
        heard = json.loads(a.heard.read_text())
    else:
        heard = transcribe(vocal, prompt=" ".join(l.text for l in read_lyric(lyric))[:800])
        write_json(out / "timing-heard.json", heard)

    lines = read_lyric(lyric)
    disp = []  # (line index, display word)
    tokens, owner = [], []
    for li, ln in enumerate(lines):
        for wi, w in enumerate(ln.text.split()):
            disp.append({"line": li, "w": w, "t0": None, "t1": None, "heard": False, "whisper": None})
            for tok in words_of(w):
                tokens.append(tok)
                owner.append(len(disp) - 1)
    htoks, hspan = [], []
    for w in heard["words"]:
        for tok in words_of(w["word"]):
            htoks.append(tok)
            hspan.append((w["start"], w["end"]))
    for kind, i, j in align(tokens, htoks):
        if i is None or j is None:
            continue
        d = disp[owner[i]]
        s, e = hspan[j]
        if d["t0"] is None:
            d["t0"] = s
            d["whisper"] = s
        d["t1"] = e
        if kind == "same":
            d["heard"] = True

    y = load(vocal)
    env = envelopes(y)
    timed = [i for i, d in enumerate(disp) if d["t0"] is not None]
    refined, shift = refine_onsets([disp[i]["t0"] for i in timed], env)
    for i, t in zip(timed, refined):
        disp[i]["t1"] = max(disp[i]["t1"], t + 0.05)
        disp[i]["t0"] = t

    # words with no time: share the gap between timed neighbours
    k = 0
    while k < len(disp):
        if disp[k]["t0"] is not None:
            k += 1
            continue
        j = k
        while j < len(disp) and disp[j]["t0"] is None:
            j += 1
        before = disp[k - 1]["t1"] if k > 0 else 0.0
        after = disp[j]["t0"] if j < len(disp) else duration
        n = j - k
        step = min(0.45, max(0.05, (after - before) / (n + 1)))
        start = max(before, after - step * n - 0.05) if (n == 1 or j == len(disp)) else before
        for m in range(n):
            disp[k + m]["t0"] = start + step * m + (0.02 if n > 1 else 0)
            disp[k + m]["t1"] = start + step * (m + 1)
        k = j
    last = 0.0
    for d in disp:  # monotonic
        d["t0"] = max(last, d["t0"])
        d["t1"] = max(d["t0"] + 0.04, d["t1"])
        last = d["t0"]

    r3 = lambda v: round(float(v), 3)  # noqa: E731
    out_lines = []
    for li, ln in enumerate(lines):
        ws = [d for d in disp if d["line"] == li]
        out_lines.append({"id": ln.id, "section": ln.section, "text": ln.text, "t0": r3(ws[0]["t0"]),
                          "t1": r3(ws[-1]["t1"]),
                          "words": [{"w": d["w"], "t0": r3(d["t0"]), "t1": r3(d["t1"]), "heard": d["heard"]} for d in ws]})
    sections = []
    for L in out_lines:
        s = sections[-1] if sections else None
        if s and s["name"] == L["section"]:
            s["t1"], s["last"] = L["t1"], L["id"]
        else:
            sections.append({"name": L["section"], "t0": L["t0"], "t1": L["t1"], "first": L["id"], "last": L["id"]})

    report: dict = {
        "lines": len(out_lines), "words": len(disp), "heard": sum(d["heard"] for d in disp),
        "placed": sum(not d["heard"] for d in disp),
        "onsetShift": {"median": r3(np.median(shift)) if shift else 0, "p90abs": r3(np.percentile(np.abs(shift), 90)) if shift else 0},
    }
    midi_dir = song / "midi"
    mids = [f for f in sorted(midi_dir.glob("*.mid")) if "vocal" in f.name.lower() and "backing" not in f.name.lower()] \
        if midi_dir.is_dir() else []
    if mids:
        notes = np.array([n[0] for n in midi_notes(mids[0])]) - (info["start"] if info else 0.0)
        if notes.size:
            gaps = []
            for d in disp:
                if d["heard"]:
                    j = int(np.argmin(np.abs(notes - d["t0"])))
                    if abs(notes[j] - d["t0"]) < 0.3:
                        gaps.append(notes[j] - d["t0"])
            if gaps:
                report["midiCrossCheck"] = {"file": mids[0].name, "matched": len(gaps),
                                            "medianNoteMinusOnset": r3(np.median(gaps)),
                                            "note": "negative = the MIDI note starts before the sung onset"}
    data = {"source": vocal.name, "master": master.name if master else None, "duration": r3(duration),
            "sections": sections, "lines": out_lines, "report": report}
    write_json(out / "timing.json", data)
    draw(out / "timing.png", y, 22050, out_lines, duration)
    report["sections"] = [f"{s['name']} {clock(s['t0'])}–{clock(s['t1'])} (lines {s['first']}–{s['last']})" for s in sections]
    report["wrote"] = [str(out / "timing.json"), str(out / "timing.png")]
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    try:
        main()
    except ToolError as e:
        fail(str(e))
