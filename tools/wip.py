"""Post a step's WIP entry, so the person can see what the run did (and write notes on it).

    python3 tools/wip.py <film> post <entry.json>
    python3 tools/wip.py <film> setup

With the WIP (https://github.com/Imaginative-Prompting/wip) set up in settings.local.json (wip.config, wip.bin), the
entry goes into the film's project through the WIP's own CLI: the project is made on first use, media paths relative to
the film folder become the WIP's /media/ URLs (the WIP's config needs a mount that contains the films folder), and an
entry id that already exists is refused: every pass is a new entry. Without the WIP, the entry is written as Markdown into
films/<slug>/wip/<id>.md.

Entry fields: id, title, tags (list), summary, body (Markdown), media ([{type: image|audio|video, src, title}]).
"""
from __future__ import annotations

import _env  # noqa: F401
import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

from common import ToolError, fail, film_dir, load_run, now_iso, settings


def wip_cfg() -> tuple[Path, Path] | None:
    s = settings()["wip"]
    if s.get("config") and s.get("bin") and Path(s["config"]).exists() and Path(s["bin"]).exists():
        return Path(s["config"]).resolve(), Path(s["bin"]).resolve()
    return None


def wip_cli(cfg: Path, binp: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["node", str(binp), *args, "--config", str(cfg)], capture_output=True, text=True)


def media_mount(cfg: Path, film: Path) -> tuple[str, Path]:
    conf = json.loads(cfg.read_text())
    for name, rel in (conf.get("mounts") or {}).items():
        root = (cfg.parent / rel).resolve()
        try:
            film.resolve().relative_to(root)
            return name, root
        except ValueError:
            continue
    raise ToolError(f"the WIP config {cfg} has no mount containing {film}; add one to its \"mounts\", e.g. "
                    f"\"oneshot\": \"{film.parent.resolve()}\", and restart the WIP server")


def project(film: Path) -> tuple[str, str]:
    run = load_run(film)
    return run.get("wipProject") or f"one-shot-{run['slug']}", f"One Shot: {run['slug']}"


def setup(film: Path) -> dict:
    w = wip_cfg()
    if not w:
        (film / "wip").mkdir(exist_ok=True)
        return {"wip": None, "fallback": str(film / "wip")}
    cfg, binp = w
    pid, title = project(film)
    r = wip_cli(cfg, binp, "project", "--id", pid, "--title", title)
    if r.returncode != 0 and "already exists" not in (r.stderr + r.stdout):
        raise ToolError(f"couldn't make the WIP project: {r.stderr.strip()}")
    port = json.loads(cfg.read_text()).get("port", 7353)
    return {"wip": str(cfg), "project": pid, "url": f"http://127.0.0.1:{port}/?project={pid}"}


def post(film: Path, entry_path: Path) -> dict:
    e = json.loads(entry_path.read_text())
    for k in ("id", "title", "body"):
        if not e.get(k):
            raise ToolError(f"the entry needs {k!r}")
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,119}", e["id"]):
        raise ToolError("an entry id is lowercase letters, digits, - and _ (at most 120)")
    e.setdefault("tags", [])
    e["updatedAt"] = now_iso()
    w = wip_cfg()
    if not w:
        out = film / "wip" / f"{e['id']}.md"
        if out.exists():
            raise ToolError(f"{out.name} exists: every pass is a new entry with a new id")
        out.parent.mkdir(exist_ok=True)
        media = "\n".join(f"- {m.get('type', 'file')}: [{m.get('title') or m['src']}](../{m['src']})" for m in e.get("media", []))
        out.write_text(f"# {e['title']}\n\n_{e['updatedAt']}_ · {', '.join(e['tags'])}\n\n{e.get('summary', '')}\n\n"
                       f"{e['body']}\n\n{media}\n")
        return {"posted": str(out)}
    cfg, binp = w
    setup(film)
    pid, _ = project(film)
    if wip_cli(cfg, binp, "get", "--project", pid, "--id", e["id"]).returncode == 0:
        raise ToolError(f"entry {e['id']} already exists in {pid}: every pass is a new entry with a new id")
    name, root = media_mount(cfg, film)
    for m in e.get("media", []):
        src = m["src"]
        if re.match(r"^(https?:|/media/)", src):
            continue
        p = (film / src).resolve()
        if not p.exists():
            raise ToolError(f"media not found: {p}")
        m["src"] = f"/media/{name}/{p.relative_to(root).as_posix()}"
        if m.get("poster") and not re.match(r"^(https?:|/media/)", m["poster"]):
            m["poster"] = f"/media/{name}/{(film / m['poster']).resolve().relative_to(root).as_posix()}"
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(e, fh)
        tmp = fh.name
    r = wip_cli(cfg, binp, "put", "--project", pid, "--file", tmp)
    Path(tmp).unlink(missing_ok=True)
    if r.returncode != 0:
        raise ToolError(f"the WIP refused the entry: {r.stderr.strip()}")
    port = json.loads(cfg.read_text()).get("port", 7353)
    return {"posted": e["id"], "project": pid, "url": f"http://127.0.0.1:{port}/?project={pid}"}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("film")
    ap.add_argument("cmd", choices=["post", "setup"])
    ap.add_argument("entry", nargs="?", type=Path)
    a = ap.parse_args()
    film = film_dir(a.film)
    if a.cmd == "setup":
        print(json.dumps(setup(film), indent=1))
    else:
        if not a.entry:
            ap.error("post needs <entry.json>")
        print(json.dumps(post(film, a.entry.resolve()), indent=1))


if __name__ == "__main__":
    try:
        main()
    except ToolError as e:
        fail(str(e))
