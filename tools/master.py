"""Trim and master a take: −14 LUFS integrated, −1 dBTP, 48 kHz 24-bit WAV and a 320k MP3. Stems trimmed the same way.

    python3 tools/master.py <take.wav> <outDir> <name> [--start S] [--end S] [--tail S] [--stems <dir>]

  --start S   cut everything before S seconds, with a 6 ms fade-in (a cold open: start one beat before the first word)
  --end S     end at S seconds, with a 10 ms fade-out (or let --tail ring on from there)
  --tail S    after --end (or the take's end), a reverb tail of about S seconds grown from the last moment, fading out
  --stems D   write D's stems, cut the same way (no level change), into <outDir>/stems/ so they line up with the master

Writes <outDir>/<name>.wav, <name>.mp3 and <name>.json (what was done, the loudness before and after). The timing and
beat tools read <name>.json to line the stems up with the master.
"""
from __future__ import annotations

import _env  # noqa: F401
import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

import numpy as np

from common import ToolError, fail, need, run, write_json

SR = 48000


def load_stereo(path: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()


def write_f32(path: Path, y: np.ndarray) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-c:a", "pcm_f32le", str(path)], input=y.astype(np.float32).tobytes(), check=True)


def edit(y: np.ndarray, start: float | None, end: float | None, tail: float | None) -> np.ndarray:
    a = int(round((start or 0) * SR))
    b = int(round(end * SR)) if end is not None else len(y)
    if not 0 <= a < b <= len(y):
        raise ToolError(f"--start/--end outside the take (it's {len(y) / SR:.2f} s)")
    out = y[a:b].copy()
    if start:
        n = int(0.006 * SR)
        out[:n] *= np.linspace(0, 1, n)[:, None]
    if tail:
        # a tail grown from the last 0.75 s: decorrelated noise with an exponential decay (RT60 = tail), convolved
        from scipy.signal import fftconvolve
        rng = np.random.default_rng(7)
        n_ir = int(tail * SR)
        decay = np.exp(-6.91 * np.arange(n_ir) / n_ir)  # -60 dB over the tail
        ir = rng.standard_normal((n_ir, 2)) * decay[:, None]
        ir /= np.sqrt((ir ** 2).sum(axis=0))
        src = out[-int(0.75 * SR):]
        wet = np.stack([fftconvolve(src[:, c], ir[:, c]) for c in range(2)], axis=1)
        wet_after = wet[len(src):]
        # level: the tail starts about 6 dB under the dry signal's last moment
        dry_rms = np.sqrt((out[-int(0.1 * SR):] ** 2).mean()) + 1e-9
        wet_rms = np.sqrt((wet_after[:int(0.1 * SR)] ** 2).mean()) + 1e-9
        wet_after *= 0.5 * dry_rms / wet_rms
        fade = np.ones(len(wet_after))  # the decay is the IR's own; only the last 15% fades to silence
        k = int(0.15 * len(wet_after))
        fade[-k:] = np.linspace(1, 0, k)
        out = np.concatenate([out, wet_after * fade[:, None]])
    elif end is not None:
        n = int(0.010 * SR)
        out[-n:] *= np.linspace(1, 0, n)[:, None]
    return out


def loudness(path: Path) -> dict:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af",
                        "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    if not m:
        raise ToolError("couldn't measure loudness: " + r.stderr.strip().splitlines()[-1])
    return json.loads(m.group(0))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("take", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("name")
    ap.add_argument("--start", type=float)
    ap.add_argument("--end", type=float)
    ap.add_argument("--tail", type=float)
    ap.add_argument("--stems", type=Path)
    a = ap.parse_args()
    need("ffmpeg", "Install ffmpeg.")
    a.out.mkdir(parents=True, exist_ok=True)
    y = load_stereo(a.take)
    edited = edit(y, a.start, a.end, a.tail)
    wav, mp3 = a.out / f"{a.name}.wav", a.out / f"{a.name}.mp3"
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "edited.wav"
        write_f32(tmp, edited)
        m = loudness(tmp)
        af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
              f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
        run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-af", af, "-ar", str(SR), "-c:a", "pcm_s24le", str(wav)])
    run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-c:a", "libmp3lame", "-b:a", "320k", str(mp3)])
    after = loudness(wav)
    stems_out = []
    if a.stems:
        sd = a.out / "stems"
        sd.mkdir(exist_ok=True)
        for f in sorted(a.stems.iterdir()):
            if f.suffix.lower() not in (".wav", ".flac", ".mp3", ".m4a", ".aif", ".aiff"):
                continue
            s = edit(load_stereo(f), a.start, a.end, None)
            if a.tail:  # pad so every stem is as long as the master
                s = np.concatenate([s, np.zeros((len(edited) - len(s), 2), dtype=np.float32)])
            target = sd / (f.stem + ".wav")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                            "-c:a", "pcm_s24le", str(target)], input=s.astype(np.float32).tobytes(), check=True)
            stems_out.append(target.name)
    info = {
        "source": str(a.take), "start": a.start or 0.0, "end": a.end, "tail": a.tail,
        "seconds": round(len(edited) / SR, 3), "sampleRate": SR,
        "before": {"lufs": float(m["input_i"]), "truePeak": float(m["input_tp"]), "lra": float(m["input_lra"])},
        "after": {"lufs": float(after["input_i"]), "truePeak": float(after["input_tp"]), "lra": float(after["input_lra"])},
        "wav": wav.name, "mp3": mp3.name, "stems": stems_out,
        "note": "Song time 0 in this master is the source take's `start` seconds.",
    }
    write_json(a.out / f"{a.name}.json", info)
    print(json.dumps(info, indent=1))


if __name__ == "__main__":
    try:
        main()
    except ToolError as e:
        fail(str(e))
