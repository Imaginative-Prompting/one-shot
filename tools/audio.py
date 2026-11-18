"""Audio analysis shared by timing.py and beats.py: onset envelopes, tempo, a beat tracker, onset peaks, RMS, MIDI.

numpy and scipy only. The beat tracker is Ellis's dynamic-programming tracker (2007): the onset envelope's tempo from its
autocorrelation, then the best-scoring beat sequence near that spacing, so the grid follows small drift.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.ndimage import median_filter
from scipy.signal import stft

from common import load_audio

SR = 22050
HOP = SR // 100  # the envelopes run at 100 frames a second
FPS = 100


def envelopes(y: np.ndarray) -> dict:
    """Half-wave-rectified log-spectral flux per band, at 100 frames a second, and the RMS level."""
    f, _, Z = stft(y, fs=SR, nperseg=2048, noverlap=2048 - HOP, boundary=None, padded=False)
    mag = np.log1p(1000 * np.abs(Z))
    flux = np.maximum(0, np.diff(mag, axis=1))

    def band(lo: float, hi: float) -> np.ndarray:
        return np.concatenate([[0], flux[(f >= lo) & (f <= hi)].sum(axis=0)])

    env = band(30, 8000)
    t = (np.arange(env.size) * HOP + 1024) / SR
    # the level in dBFS, from the samples, on the same 100-a-second clock (frame k centred on sample k*HOP + 1024)
    centres = np.arange(env.size) * HOP + 1024
    win = 1024
    padded = np.pad(y.astype(np.float64) ** 2, (win, win))
    csum = np.concatenate([[0.0], np.cumsum(padded)])
    lo = np.clip(centres - win // 2 + win, 0, padded.size)
    hi = np.clip(centres + win // 2 + win, 0, padded.size)
    rms_db = 10 * np.log10((csum[hi] - csum[lo]) / win + 1e-12)
    return {"t": t, "env": env, "low": band(30, 150), "bright": band(2000, 8000), "voice": band(150, 4000),
            "rms_db": rms_db}


def tempo(env: np.ndarray, lo_bpm: float = 75, hi_bpm: float = 165) -> float:
    e = env - env.mean()
    ac = np.correlate(e, e, mode="full")[e.size - 1:]
    lo, hi = int(FPS * 60 / hi_bpm), int(FPS * 60 / lo_bpm) + 1
    k = lo + int(np.argmax(ac[lo:hi]))
    a, b, c = ac[k - 1], ac[k], ac[k + 1]
    denom = a - 2 * b + c
    k_ref = k + (0.5 * (a - c) / denom if denom != 0 else 0)
    return 60 * FPS / k_ref


def track(env: np.ndarray, bpm: float, tightness: float = 400.0) -> np.ndarray:
    period = FPS * 60 / bpm
    o = env / (env.std() + 1e-9)
    score = o.copy()
    back = -np.ones(o.size, dtype=int)
    lags = np.arange(int(round(period / 2)), int(round(period * 2)) + 1)
    penalty = -tightness * np.log(lags / period) ** 2
    for t in range(lags[0], o.size):
        prev = t - lags
        ok = prev >= 0
        if not ok.any():
            continue
        cand = score[prev[ok]] + penalty[ok]
        j = int(np.argmax(cand))
        if cand[j] > 0:
            score[t] = o[t] + cand[j]
            back[t] = prev[ok][j]
    tail = slice(max(0, o.size - int(period)), o.size)
    t = tail.start + int(np.argmax(score[tail]))
    beats = []
    while t >= 0:
        beats.append(t)
        t = back[t]
    return np.array(beats[::-1])


def refine(frames: np.ndarray, env: np.ndarray, reach: int = 2) -> np.ndarray:
    out = []
    for k in frames:
        a, b = max(1, k - reach), min(env.size - 2, k + reach)
        j = a + int(np.argmax(env[a:b + 1]))
        y0, y1, y2 = env[j - 1], env[j], env[j + 1]
        d = y0 - 2 * y1 + y2
        out.append(j + (0.5 * (y0 - y2) / d if d < 0 else 0))
    return np.array(out, dtype=float)


def frame_time(k) -> np.ndarray:
    return (np.asarray(k, dtype=float) * HOP + 1024) / SR


def onset_peaks(env: np.ndarray, min_gap_frames: int = 9, median_frames: int = 201) -> list[tuple[int, float]]:
    """Local peaks of the envelope over its running median, strongest kept first, at least min_gap apart:
    [(frame, strength 0-1)] in time order."""
    base = median_filter(env, size=median_frames)
    rel = env - base
    peaks = [k for k in range(1, env.size - 1) if rel[k] > 0 and env[k] >= env[k - 1] and env[k] > env[k + 1]]
    keep: list[int] = []
    for k in sorted(peaks, key=lambda k: -rel[k]):
        if all(abs(k - j) >= min_gap_frames for j in keep):
            keep.append(k)
    keep.sort()
    if not keep:
        return []
    strong = float(np.percentile(rel[keep], 99)) or 1.0
    return [(k, float(min(1.0, rel[k] / strong))) for k in keep]


def load(path: Path) -> np.ndarray:
    return load_audio(path, SR)


# ---------- MIDI (Suno's, for cross-checks only) ----------

def midi_notes(path: Path) -> list[tuple[float, float, int]]:
    """[(start s, end s, pitch)] of a MIDI file, tolerating the malformed key signatures some exports carry."""
    import mido
    from mido.midifiles import meta
    spec = meta._META_SPEC_BY_TYPE.get("key_signature")  # noqa: SLF001
    if spec is not None and not getattr(spec, "_one_shot_safe", False):
        original = spec.decode

        def safe(message, data, _orig=original):
            try:
                _orig(message, data)
            except Exception:  # noqa: BLE001  (a key signature mido can't read: irrelevant to timing)
                message.key = "C"

        spec.decode = safe
        spec._one_shot_safe = True
    mf = mido.MidiFile(str(path))
    notes: list[tuple[float, float, int]] = []
    t = 0.0
    on: dict[tuple[int, int], float] = {}
    for msg in mf:  # iterating a MidiFile yields messages with delta times in seconds, tempo map applied
        t += msg.time
        if msg.type == "note_on" and msg.velocity > 0:
            on[(msg.channel, msg.note)] = t
        elif msg.type in ("note_off", "note_on"):
            s = on.pop((msg.channel, msg.note), None)
            if s is not None:
                notes.append((s, t, msg.note))
    return sorted(notes)
