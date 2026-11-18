"""Shared helpers for the tools: paths, settings, the film folder, audio, lyrics, word alignment, Whisper."""
from __future__ import annotations

import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILMS = ROOT / "films"

DEFAULT_SETTINGS = {
    "wip": {"config": None, "bin": None, "projectPrefix": "one-shot-"},
    "gpu": {"wrapper": None},
    "whisper": {"backend": "auto", "model": None},
    "pickWindowMinutes": 30,
}


class ToolError(Exception):
    """A problem the person running the tool can fix; printed as one line."""


def fail(msg: str, code: int = 1) -> None:
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def settings() -> dict:
    """settings.local.json over the defaults (one level deep)."""
    merged = json.loads(json.dumps(DEFAULT_SETTINGS))
    p = Path(os.environ.get("ONE_SHOT_SETTINGS") or ROOT / "settings.local.json")
    if p.exists():
        local = json.loads(p.read_text())
        for k, v in local.items():
            if isinstance(v, dict) and isinstance(merged.get(k), dict):
                merged[k].update(v)
            else:
                merged[k] = v
    return merged


# ---------- the film folder ----------

def film_dir(name: str | os.PathLike) -> Path:
    """A film by slug (films/<slug>) or by path."""
    p = Path(name)
    if p.is_dir() and (p / "run.json").exists():
        return p.resolve()
    q = FILMS / str(name)
    if q.is_dir() and (q / "run.json").exists():
        return q.resolve()
    raise ToolError(f"no film called {name!r} (expected films/<slug>/run.json; make one with tools/new_film.py)")


def load_run(film: Path) -> dict:
    return json.loads((film / "run.json").read_text())


def save_run(film: Path, run: dict) -> None:
    tmp = film / "run.json.tmp"
    tmp.write_text(json.dumps(run, indent=2) + "\n")
    tmp.replace(film / "run.json")


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")


# ---------- processes and audio ----------

def need(cmd: str, hint: str) -> str:
    found = shutil.which(cmd)
    if not found:
        raise ToolError(f"{cmd} isn't installed. {hint}")
    return found


def run(args: list[str], **kw) -> subprocess.CompletedProcess:
    r = subprocess.run(args, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        tail = (r.stderr or r.stdout).strip().splitlines()[-3:]
        raise ToolError(f"{Path(args[0]).name} failed: {' | '.join(tail)}")
    return r


def probe_seconds(path: Path) -> float:
    need("ffprobe", "Install ffmpeg (it includes ffprobe).")
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)])
    return float(r.stdout.strip())


def probe_video(path: Path) -> dict:
    r = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
             "-show_entries", "stream=width,height,r_frame_rate,nb_read_packets,color_space,color_transfer,color_primaries",
             "-of", "json", str(path)])
    s = json.loads(r.stdout)["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    s["fps"] = float(num) / float(den)
    s["frames"] = int(s.get("nb_read_packets", 0))
    return s


def load_audio(path: Path, sr: int = 22050, mono: bool = True):
    """Decode any audio file to float32 samples with ffmpeg."""
    import numpy as np
    need("ffmpeg", "Install ffmpeg.")
    args = ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1" if mono else "2", "-ar", str(sr), "-f", "f32le", "-"]
    raw = subprocess.run(args, check=True, capture_output=True).stdout
    y = np.frombuffer(raw, dtype=np.float32)
    return y if mono else y.reshape(-1, 2)


def clock(s: float) -> str:
    return f"{int(s // 60)}:{s % 60:05.2f}"


# ---------- lyrics ----------

@dataclass
class Line:
    id: int
    section: str
    text: str


def read_lyric(path: Path) -> list[Line]:
    """Sung lines of a lyric file with their sections. Section tags are lines like [Chorus] or [Bridge: half-time]."""
    raw_lines = Path(path).read_text().splitlines()
    tag_re = re.compile(r"\[(.+?)\]")
    names = [tag_re.fullmatch(r.strip()).group(1).split(":")[0].strip() for r in raw_lines if tag_re.fullmatch(r.strip())]
    total: dict[str, int] = {}
    for n in names:
        total[n] = total.get(n, 0) + 1
    lines: list[Line] = []
    section = "Intro"
    seen: dict[str, int] = {}
    for raw in raw_lines:
        t = raw.strip()
        if not t:
            continue
        tag = tag_re.fullmatch(t)
        if tag:
            name = tag.group(1).split(":")[0].strip()
            seen[name] = seen.get(name, 0) + 1
            # a tag used more than once without a number gets one: Chorus 1, Chorus 2
            section = f"{name} {seen[name]}" if total[name] > 1 and not re.search(r"\d", name) else name
            continue
        if re.fullmatch(r"\(.*\)", t):  # a stage direction in parentheses, not sung
            continue
        lines.append(Line(len(lines) + 1, section, t))
    if not lines:
        raise ToolError(f"{path}: no sung lines found")
    return lines


_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def number_words(n: int) -> list[str]:
    if n < 20:
        return [_ONES[n]]
    if n < 100:
        return [_TENS[n // 10]] + ([_ONES[n % 10]] if n % 10 else [])
    if n < 1000:
        return [_ONES[n // 100], "hundred"] + (number_words(n % 100) if n % 100 else [])
    if 1100 <= n <= 1999 or 2010 <= n <= 2099:  # read as a year: nineteen ninety, twenty twenty-six
        return number_words(n // 100) + (number_words(n % 100) if n % 100 else ["hundred"])
    if n < 1_000_000:
        return number_words(n // 1000) + ["thousand"] + (number_words(n % 1000) if n % 1000 else [])
    return [str(n)]


def words_of(text: str) -> list[str]:
    """Comparable tokens: lowercase, no punctuation, numbers spelled out, contractions kept whole."""
    t = text.lower().replace("’", "'").replace("&", " and ")
    t = re.sub(r"(\d),(\d)", r"\1\2", t)
    out: list[str] = []
    for tok in re.findall(r"[a-z0-9']+", t):
        tok = tok.strip("'")
        if not tok:
            continue
        if tok.isdigit():
            out.extend(number_words(int(tok)))
        else:
            out.append(tok)
    return out


def _close(a: str, b: str) -> bool:
    if a == b:
        return True
    strip = lambda w: re.sub(r"(in'|ing|s|'s|ed)$", "", w.replace("'", ""))  # noqa: E731
    return strip(a) == strip(b) and len(strip(a)) >= 3


def align(expected: list[str], heard: list[str]) -> list[tuple[str, int | None, int | None]]:
    """Levenshtein alignment: a list of (kind, i_expected, j_heard), kind in same/sub/missing/extra."""
    n, m = len(expected), len(heard)
    import numpy as np
    d = np.zeros((n + 1, m + 1), dtype=np.int32)
    d[:, 0] = np.arange(n + 1)
    d[0, :] = np.arange(m + 1)
    for i in range(1, n + 1):
        ei = expected[i - 1]
        for j in range(1, m + 1):
            cost = 0 if _close(ei, heard[j - 1]) else 1
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + cost)
    out = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and d[i, j] == d[i - 1, j - 1] + (0 if _close(expected[i - 1], heard[j - 1]) else 1):
            out.append(("same" if _close(expected[i - 1], heard[j - 1]) else "sub", i - 1, j - 1))
            i, j = i - 1, j - 1
        elif i > 0 and d[i, j] == d[i - 1, j] + 1:
            out.append(("missing", i - 1, None))
            i -= 1
        else:
            out.append(("extra", None, j - 1))
            j -= 1
    return out[::-1]


# ---------- Whisper ----------

def _apple_silicon() -> bool:
    return sys.platform == "darwin" and platform.machine() == "arm64"


def whisper_backend() -> str:
    want = settings()["whisper"].get("backend", "auto")
    if want != "auto":
        return want
    if _apple_silicon() and shutil.which("mlx_whisper"):
        return "mlx"
    try:
        import faster_whisper  # noqa: F401
        return "faster"
    except ImportError:
        pass
    if shutil.which("whisper"):
        return "openai"
    raise ToolError("no Whisper found. On Apple silicon: `uv tool install mlx-whisper`; elsewhere: "
                    "`.venv/bin/pip install faster-whisper`. Then run tools/check_setup.py.")


def transcribe(path: Path, language: str = "en", prompt: str | None = None) -> dict:
    """Word-timed transcript: {text, words: [{word, start, end, probability}], backend, model}.

    Runs ONCE per call: never retry in a loop. On macOS the MLX backend needs the GPU (run outside any sandbox).
    """
    backend = whisper_backend()
    model = settings()["whisper"].get("model")
    path = Path(path).resolve()
    if backend == "mlx":
        model = model or "mlx-community/whisper-large-v3-turbo"
        with tempfile.TemporaryDirectory() as td:
            args = ["mlx_whisper", str(path), "--model", model, "--output-format", "json", "--output-dir", td,
                    "--output-name", "t", "--word-timestamps", "True", "--verbose", "False",
                    "--condition-on-previous-text", "False", "--language", language]
            if prompt:
                args += ["--initial-prompt", prompt[:800]]
            run(args)
            j = json.loads((Path(td) / "t.json").read_text())
        words = [{"word": w["word"].strip(), "start": float(w["start"]), "end": float(w["end"]),
                  "probability": float(w.get("probability", 1))} for s in j.get("segments", []) for w in s.get("words", [])]
        return {"text": j.get("text", "").strip(), "words": words, "backend": backend, "model": model}
    if backend == "faster":
        from faster_whisper import WhisperModel
        model = model or "large-v3-turbo"
        wm = WhisperModel(model, compute_type="auto")
        segs, _ = wm.transcribe(str(path), language=language, word_timestamps=True, condition_on_previous_text=False,
                                initial_prompt=prompt[:800] if prompt else None)
        words, texts = [], []
        for s in segs:
            texts.append(s.text)
            for w in s.words or []:
                words.append({"word": w.word.strip(), "start": float(w.start), "end": float(w.end),
                              "probability": float(w.probability)})
        return {"text": " ".join(t.strip() for t in texts), "words": words, "backend": backend, "model": model}
    if backend == "openai":
        model = model or "turbo"
        with tempfile.TemporaryDirectory() as td:
            args = ["whisper", str(path), "--model", model, "--output_format", "json", "--output_dir", td,
                    "--word_timestamps", "True", "--condition_on_previous_text", "False", "--language", language]
            run(args)
            j = json.loads(next(Path(td).glob("*.json")).read_text())
        words = [{"word": w["word"].strip(), "start": float(w["start"]), "end": float(w["end"]),
                  "probability": float(w.get("probability", 1))} for s in j.get("segments", []) for w in s.get("words", [])]
        return {"text": j.get("text", "").strip(), "words": words, "backend": backend, "model": model}
    raise ToolError(f"unknown whisper backend {backend!r} in settings.local.json")
