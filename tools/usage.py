"""What a film's run has used so far: tokens and API-equivalent cost per model, per agent, per hour, from Claude Code's
own transcripts on this machine.

    python3 tools/usage.py <film> [--session <id> …] [--json] [--out <file.md>]

Sessions are found in ~/.claude/projects/<this repo>/: every transcript that mentions films/<slug> and started after the
film's run.json "started" (minus ten minutes), with its subagents (critic, researchers) counted in. --session picks
sessions by id instead. Each API response is counted once (Claude Code writes a message's blocks as separate lines).

Costs are at the API's list prices (USD per million tokens; cache writes at 1.25× input for 5 minutes, 2× for an hour).
On a subscription this is a measure of size, not a bill. Claude Code's web search and fetch run on a small model that
doesn't appear in the transcript lines; their exact cost shows up in the session's own totals ("cost-state") when the
session ends, and is reported here when present. Until then they show as a count of searches and fetches.
"""
from __future__ import annotations

import _env  # noqa: F401
import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from common import ROOT, ToolError, fail, film_dir, load_run

PRICES = {  # input, output, 5-minute cache write, 1-hour cache write, cache read (USD per million tokens)
    "claude-fable-5-2": (8.0, 40.0, 10.0, 16.0, 0.20),
    "claude-mythos-5-2": (8.0, 40.0, 10.0, 16.0, 0.20),
    "claude-opus-5-5": (4.0, 20.0, 5.0, 8.0, 0.20),
    "claude-sonnet-5-5": (2.0, 10.0, 2.5, 4.0, 0.10),
    "claude-haiku-5-5": (0.10, 0.50, 0.125, 0.20, 0.01),
}


def project_dir() -> Path:
    key = re.sub(r"[^A-Za-z0-9]", "-", str(ROOT))
    return Path.home() / ".claude" / "projects" / key


def parse_time(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def read_lines(path: Path):
    with open(path) as fh:
        for line in fh:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def cost_of(model: str, u: dict) -> float | None:
    p = PRICES.get(model)
    if not p:
        return None
    return (u["input"] * p[0] + u["output"] * p[1] + u["cache5m"] * p[2] + u["cache1h"] * p[3]
            + u["cacheRead"] * p[4]) / 1e6


def collect(paths: list[tuple[Path, str]]) -> tuple[dict, list[dict]]:
    """Usage per message id across transcript files: {id: row}, plus tool-call rows."""
    msgs: dict[str, dict] = {}
    tools: list[dict] = []
    for path, agent in paths:
        for d in read_lines(path):
            if d.get("type") != "assistant":
                continue
            m = d.get("message") or {}
            u = m.get("usage")
            mid = m.get("id") or d.get("requestId")
            if not u or not mid:
                continue
            cc = u.get("cache_creation") or {}
            five = cc.get("ephemeral_5m_input_tokens")
            hour = cc.get("ephemeral_1h_input_tokens")
            if five is None and hour is None:
                five, hour = u.get("cache_creation_input_tokens", 0), 0
            msgs[mid] = {  # the last line of a message carries its final usage
                "model": m.get("model"), "agent": agent, "t": d.get("timestamp"),
                "input": u.get("input_tokens", 0) or 0, "output": u.get("output_tokens", 0) or 0,
                "cache5m": five or 0, "cache1h": hour or 0, "cacheRead": u.get("cache_read_input_tokens", 0) or 0,
                "thinking": (u.get("output_tokens_details") or {}).get("thinking_tokens", 0) or 0,
            }
            for block in m.get("content") or []:
                if block.get("type") == "tool_use" and block.get("name") in ("WebSearch", "WebFetch", "Agent", "Task"):
                    tools.append({"id": block.get("id"), "name": block["name"], "agent": agent})
    uniq = {t["id"]: t for t in tools}
    return msgs, list(uniq.values())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("film", nargs="?")
    ap.add_argument("--session", nargs="*")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    pdir = project_dir()
    if not pdir.is_dir():
        raise ToolError(f"no Claude Code transcripts for this repo at {pdir}")
    sessions: list[Path] = []
    title = "sessions " + ", ".join(a.session or [])
    if a.session:
        sessions = [pdir / f"{s}.jsonl" for s in a.session]
    else:
        if not a.film:
            ap.error("give a film or --session")
        film = film_dir(a.film)
        run = load_run(film)
        title = run["slug"]
        start = parse_time(run["started"]) - timedelta(minutes=10)
        needle = f"films/{run['slug']}"
        for f in sorted(pdir.glob("*.jsonl")):
            first = next((d.get("timestamp") for d in read_lines(f) if d.get("timestamp")), None)
            if first and parse_time(first) >= start and needle in f.read_text(errors="ignore"):
                sessions.append(f)
    if not sessions:
        raise ToolError("no transcripts found for this film yet")

    paths: list[tuple[Path, str]] = []
    exact: list[dict] = []
    for s in sessions:
        paths.append((s, "main"))
        sub = s.with_suffix("") / "subagents"
        for j in sorted(sub.glob("*.jsonl")) if sub.is_dir() else []:
            meta = j.with_suffix(".meta.json")
            kind = json.loads(meta.read_text()).get("agentType", "subagent") if meta.exists() else "subagent"
            paths.append((j, kind))
        states = [d for d in read_lines(s) if d.get("type") == "cost-state"]
        if states:
            exact.append({"session": s.stem, **{k: states[-1].get(k) for k in ("totalCostUSD", "modelUsage")}})
    msgs, tools = collect(paths)

    zero = lambda: {"input": 0, "output": 0, "cache5m": 0, "cache1h": 0, "cacheRead": 0, "thinking": 0, "calls": 0}  # noqa: E731
    by_model, by_agent, by_hour = defaultdict(zero), defaultdict(zero), defaultdict(zero)
    cost_model, cost_agent, cost_hour = defaultdict(float), defaultdict(float), defaultdict(float)
    first_t = last_t = None
    for r in msgs.values():
        c = cost_of(r["model"], r) or 0.0
        hour = parse_time(r["t"]).astimezone().strftime("%m-%d %H:00") if r["t"] else "?"
        for key, bucket, costs in ((r["model"], by_model, cost_model), (r["agent"], by_agent, cost_agent),
                                   (hour, by_hour, cost_hour)):
            b = bucket[key]
            for k in ("input", "output", "cache5m", "cache1h", "cacheRead", "thinking"):
                b[k] += r[k]
            b["calls"] += 1
            costs[key] += c
        if r["t"]:
            t = parse_time(r["t"])
            first_t = t if first_t is None or t < first_t else first_t
            last_t = t if last_t is None or t > last_t else last_t
    total = sum(cost_model.values())
    tool_counts = defaultdict(int)
    for t in tools:
        tool_counts[t["name"]] += 1
    # search and fetch on the small model, estimated from a measured run: $10 per 1,000 searches, plus about $0.002 of
    # small-model tokens per search or fetch call
    web_est = tool_counts["WebSearch"] * 0.010 + (tool_counts["WebSearch"] + tool_counts["WebFetch"]) * 0.0019
    out = {
        "film": title, "sessions": [s.stem for s in sessions], "transcripts": len(paths), "apiCalls": len(msgs),
        "from": first_t.astimezone().isoformat(timespec="minutes") if first_t else None,
        "to": last_t.astimezone().isoformat(timespec="minutes") if last_t else None,
        "costUSD": round(total, 2), "webEstimateUSD": round(web_est, 2), "totalEstimateUSD": round(total + web_est, 2),
        "byModel": {k: {**v, "costUSD": round(cost_model[k], 2)} for k, v in by_model.items()},
        "byAgent": {k: {**v, "costUSD": round(cost_agent[k], 2)} for k, v in by_agent.items()},
        "byHour": {k: {"calls": v["calls"], "output": v["output"], "costUSD": round(cost_hour[k], 2)}
                   for k, v in sorted(by_hour.items())},
        "toolCalls": dict(tool_counts),
        "exactAtSessionEnd": exact,
    }
    if a.json:
        print(json.dumps(out, indent=1))
    else:
        M = lambda n: f"{n / 1e6:.2f}M" if n >= 1e5 else f"{n / 1e3:.1f}k"  # noqa: E731
        lines = [f"# Usage: {title}", "",
                 f"{out['apiCalls']} API calls in {len(sessions)} session(s) and {len(paths) - len(sessions)} subagent(s), "
                 f"{out['from']} to {out['to']}. **${total + web_est:.2f}** at API list prices: ${total:.2f} for the "
                 f"models in the transcript, about ${web_est:.2f} for web search and fetch (estimated).", "",
                 "| Model | Calls | Input | Cache write 5m | Cache write 1h | Cache read | Output (thinking) | $ |",
                 "|---|---|---|---|---|---|---|---|"]
        for k, v in sorted(by_model.items(), key=lambda kv: -cost_model[kv[0]]):
            lines.append(f"| {k} | {v['calls']} | {M(v['input'])} | {M(v['cache5m'])} | {M(v['cache1h'])} | "
                         f"{M(v['cacheRead'])} | {M(v['output'])} ({M(v['thinking'])}) | {cost_model[k]:.2f} |")
        lines += ["", "| Agent | Calls | Output | $ |", "|---|---|---|---|"]
        for k, v in sorted(by_agent.items(), key=lambda kv: -cost_agent[kv[0]]):
            lines.append(f"| {k} | {v['calls']} | {M(v['output'])} | {cost_agent[k]:.2f} |")
        lines += ["", "| Hour | Calls | Output | $ |", "|---|---|---|---|"]
        for k, v in sorted(by_hour.items()):
            lines.append(f"| {k} | {v['calls']} | {M(v['output'])} | {cost_hour[k]:.2f} |")
        lines += ["", f"Web searches/fetches and subagent launches: {dict(tool_counts) or 'none'} (searches and fetches "
                      "run on a small model not in the transcript lines)."]
        for e in exact:
            lines.append(f"\nExact totals written by session {e['session']} when it ended: ${e['totalCostUSD']:.2f} "
                         + ", ".join(f"{m} ${u.get('costUSD', 0):.2f}" for m, u in (e["modelUsage"] or {}).items()))
        text = "\n".join(lines) + "\n"
        if a.out:
            a.out.write_text(text)
        print(text)


if __name__ == "__main__":
    try:
        main()
    except ToolError as e:
        fail(str(e))
