"""The song's map: tempo, beats, bars, sections, energy, which instruments play where, and the accents worth landing on.

    python3 tools/beats.py <song dir> [--master <wav>] [--stems <dir>] [--timing <timing.json>] [--out <dir>]

Writes song/map.json (the data the film keys to) and song/map.md (how you "hear" the song: read it before planning).
Beats come from the drums stem when there is one (cleaner than the mix), else the master; the bar's first beat is the
phase with the most kick. Sections are the sung sections from timing.json (run timing.py first), with the instrumental
stretches between them (intro, breaks, outro). Energy is each beat's loudness on the master, scaled 0–1 over the song.
A stem is "playing" in a section when it sounds (within 20 dB of its own loudest, above −60 dBFS) for at least half of it,
and plays "part of it" for 15–50%.
Everything here is measured; what it means for the film is your call.
"""
from __future__ import annotations

import _env  # noqa: F401
import argparse
import json
from pathlib import Path

import numpy as np

from audio import FPS, envelopes, frame_time, load, midi_notes, onset_peaks, refine, tempo, track
from common import ToolError, clock, fail, probe_seconds, write_json
from timing import find_master


def stems_of(song: Path, info: dict | None, given: Path | None) -> dict[str, Path]:
    d = given or (song / "master" / "stems" if info and info.get("stems") else song / "stems")
    if not d.is_dir():
        return {}
    out = {}
    for f in sorted(d.iterdir()):
        if f.suffix.lower() in (".wav", ".flac", ".mp3", ".m4a", ".aif", ".aiff"):
            name = f.stem.lower().lstrip("0123456789-_ ").replace("_", " ").replace("-", " ").strip()
            out[name] = f
    return out


def per_beat_db(rms_db: np.ndarray, beat_frames: np.ndarray) -> np.ndarray:
    edges = np.concatenate([beat_frames, [rms_db.size]]).astype(int)
    lin = 10 ** (rms_db / 10)
    return np.array([10 * np.log10(lin[a:max(a + 1, b)].mean() + 1e-12) for a, b in zip(edges[:-1], edges[1:])])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("song", type=Path)
    ap.add_argument("--master", type=Path)
    ap.add_argument("--stems", type=Path)
    ap.add_argument("--timing", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--bpm", type=float, help="force the tempo (when the tracker locks onto half or double time)")
    a = ap.parse_args()
    song = a.song.resolve()
    out = (a.out or song).resolve()
    master, info = find_master(song)
    master = a.master or master
    if not master:
        raise ToolError(f"no master in {song}/master (run tools/master.py first) and no --master given")
    stems = stems_of(song, info, a.stems)
    timing_path = a.timing or song / "timing.json"
    timing = json.loads(timing_path.read_text()) if timing_path.exists() else None
    duration = probe_seconds(master)

    mix = envelopes(load(master))
    drums_key = next((k for k in stems if "drum" in k), None)
    grid_env = envelopes(load(stems[drums_key])) if drums_key else mix
    bpm = a.bpm or tempo(grid_env["env"])
    frames = refine(track(grid_env["env"], bpm), grid_env["env"])
    beats = frame_time(frames)
    at = np.clip(np.round(frames).astype(int), 0, grid_env["low"].size - 1)
    kick = [float(grid_env["low"][at[ph::4]].mean()) for ph in range(4)]
    phase = int(np.argmax(kick))
    downbeats = beats[phase::4]
    beat_s = 60 / bpm

    midi_bpm = None
    mid_dir = song / "midi"
    if mid_dir.is_dir():
        import mido
        for f in sorted(mid_dir.glob("*.mid")):
            try:
                tempos = [m.tempo for tr in mido.MidiFile(str(f)).tracks for m in tr if m.type == "set_tempo"]
            except Exception:  # noqa: BLE001
                midi_notes(f)  # installs the tolerant key-signature reader, then try again
                tempos = [m.tempo for tr in mido.MidiFile(str(f)).tracks for m in tr if m.type == "set_tempo"]
            if tempos:
                midi_bpm = round(float(np.median([60e6 / t for t in tempos])), 2)
                break

    # energy per beat on the master, 0–1
    beat_frames = np.round((beats * 22050 - 1024) / (22050 // 100)).astype(int).clip(0, mix["rms_db"].size - 1)
    e_db = per_beat_db(mix["rms_db"], beat_frames)
    lo, hi = np.percentile(e_db, 5), np.percentile(e_db, 99)
    energy = np.clip((e_db - lo) / (hi - lo + 1e-9), 0, 1)

    # sections: sung ones from timing.json plus the instrumental stretches between them
    sections = []
    def add(name: str, kind: str, t0: float, t1: float) -> None:
        if t1 - t0 > 0.25:
            sections.append({"name": name, "kind": kind, "t0": round(t0, 3), "t1": round(t1, 3)})
    if timing:
        sung = timing["sections"]
        add("Intro", "instrumental", 0.0, sung[0]["t0"])
        for i, s in enumerate(sung):
            end = sung[i + 1]["t0"] if i + 1 < len(sung) else s["t1"]
            gap = (sung[i + 1]["t0"] - s["t1"]) if i + 1 < len(sung) else 0
            if gap > 2 * 4 * beat_s:  # two bars or more with no voice: a break of its own
                add(s["name"], "sung", s["t0"], s["t1"] + beat_s)
                add(f"Break after {s['name']}", "instrumental", s["t1"] + beat_s, sung[i + 1]["t0"])
            else:
                add(s["name"], "sung", s["t0"], end)
        add("Ending", "instrumental", sung[-1]["t1"], duration)
    else:
        add("Whole song", "unknown", 0.0, duration)

    # stems: level per section, playing or not, entries
    stem_env = {k: envelopes(load(p)) for k, p in stems.items()}
    stem_peak = {k: float(np.percentile(e["rms_db"], 99.5)) for k, e in stem_env.items()}
    for s in sections:
        a0, a1 = int(s["t0"] * FPS), max(int(s["t0"] * FPS) + 1, int(s["t1"] * FPS))
        m = (beats >= s["t0"]) & (beats < s["t1"])
        s["energy"] = round(float(energy[m].mean()) if m.any() else 0.0, 3)
        s["bars"] = round((s["t1"] - s["t0"]) / (4 * beat_s), 1)
        db = before = None  # noqa: F841
        downs_in = downbeats[(downbeats >= s["t0"] - 4 * beat_s) & (downbeats <= s["t0"] + 0.05)]
        s["barStart"] = round(float(downs_in[-1]), 3) if downs_in.size else None
        playing, partly = [], []
        for k, e in stem_env.items():
            act = e["rms_db"][a0:a1] > max(stem_peak[k] - 20, -60)
            cover = float(act.mean()) if act.size else 0.0
            if cover >= 0.5:
                playing.append(k)
            elif cover >= 0.15:
                partly.append(k)
        s["playing"] = playing
        s["partly"] = partly
    changes = []
    for p, n in zip(sections, sections[1:]):
        added = sorted(set(n["playing"]) - set(p["playing"]))
        dropped = sorted(set(p["playing"]) - set(n["playing"]))
        changes.append({"at": n["t0"], "from": p["name"], "to": n["name"], "energy": round(n["energy"] - p["energy"], 3),
                        "added": added, "dropped": dropped})
    entries = []
    for k, e in stem_env.items():
        if "vocal" in k:
            continue
        act = e["rms_db"] > max(stem_peak[k] - 24, -60)
        bar = int(2 * 4 * beat_s * FPS)  # two bars of silence before it counts as coming in
        i = 0
        while i < act.size:
            if act[i] and (i == 0 or not act[max(0, i - bar):i].any()):
                entries.append({"t": round(float(i / FPS), 3), "stem": k})
                i += bar
            i += 1
    entries.sort(key=lambda x: x["t"])

    accents = []
    for k, e in [("mix", mix)] + list(stem_env.items()):
        if "vocal" in k:
            continue
        for fr, strength in onset_peaks(e["env"]):
            if strength >= (0.75 if k == "mix" else 0.6):
                accents.append({"t": round(float(frame_time(fr)), 3), "stem": k, "strength": round(strength, 2)})
    accents.sort(key=lambda x: x["t"])

    peak_sec = max(sections, key=lambda s: s["energy"])
    biggest = sorted(changes, key=lambda c: -(abs(c["energy"]) + 0.15 * (len(c["added"]) + len(c["dropped"]))))[:3]
    data = {
        "master": master.name, "duration": round(duration, 3), "bpm": round(bpm, 2), "beat": round(beat_s, 4),
        "bar": round(4 * beat_s, 4), "midiBpm": midi_bpm, "gridFrom": drums_key or "mix", "downbeatPhase": phase,
        "beats": [round(float(b), 3) for b in beats], "downbeats": [round(float(b), 3) for b in downbeats],
        "energy": [round(float(x), 3) for x in energy], "sections": sections, "changes": changes,
        "entries": entries, "accents": accents, "peak": peak_sec["name"], "biggestChanges": biggest,
    }
    write_json(out / "map.json", data)

    def sec_row(s: dict) -> str:
        bar = "█" * int(round(s["energy"] * 10))
        return (f"| {s['name']} | {clock(s['t0'])}–{clock(s['t1'])} | {s['bars']} | {bar} {s['energy']:.2f} | "
                f"{', '.join(s['playing']) or '—'}{'; part of it: ' + ', '.join(s['partly']) if s['partly'] else ''} |")
    md = [f"# The song's map\n",
          f"Tempo {bpm:.1f} BPM (beat {beat_s:.3f} s, bar {4 * beat_s:.3f} s), from the {drums_key or 'mix'}"
          + (f"; Suno's MIDI says {midi_bpm}" if midi_bpm else "") + f". {len(beats)} beats, {len(downbeats)} bars. "
          f"Length {clock(duration)}.\n",
          "## Sections\n", "| Section | Time | Bars | Energy | Playing |", "|---|---|---|---|---|",
          *[sec_row(s) for s in sections],
          f"\nThe loudest section is **{peak_sec['name']}**.\n",
          "## The biggest changes (candidates for the turning point and the film's biggest moments)\n",
          *[f"- {clock(c['at'])} {c['from']} → {c['to']}: energy {c['energy']:+.2f}"
            + (f"; in: {', '.join(c['added'])}" if c["added"] else "") + (f"; out: {', '.join(c['dropped'])}" if c["dropped"] else "")
            for c in biggest],
          "\n## Instruments coming in (after two bars or more of silence)\n",
          *[f"- {clock(e['t'])} {e['stem']}" for e in entries if e["t"] > 0.5][:40],
          "\n## Strong accents by section (time, stem, strength)\n"]
    for s in sections:
        acc = [x for x in accents if s["t0"] <= x["t"] < s["t1"]]
        top = sorted(acc, key=lambda x: -x["strength"])[:8]
        md.append(f"- **{s['name']}**: " + (", ".join(f"{clock(x['t'])} {x['stem']} {x['strength']:.2f}"
                                                        for x in sorted(top, key=lambda x: x['t'])) or "none"))
    (out / "map.md").write_text("\n".join(md) + "\n")
    print(json.dumps({"bpm": data["bpm"], "midiBpm": midi_bpm, "beats": len(beats), "bars": len(downbeats),
                      "sections": [f"{s['name']} {clock(s['t0'])} e{s['energy']:.2f}" for s in sections],
                      "peak": data["peak"], "accents": len(accents), "wrote": [str(out / "map.json"), str(out / "map.md")]},
                     indent=1))


if __name__ == "__main__":
    try:
        main()
    except ToolError as e:
        fail(str(e))
