"""What the ear would catch in a lyric: line ends that rhyme with nothing near them, rhymes that only match on the vowel,
lines that are long or dense with names and numbers, identical rhymes; plus syllables and stresses per line, the
end-rhyme scheme, and rhyme families inside lines. Prints a table; --html writes a rhyme map that colours each family.

    python3 tools/lyric.py <lyric.txt> [--html <out.html>] [--json <out.json>]

Pronunciations come from the CMU dictionary (the `pronouncing` package). Words it doesn't know are counted by spelling
and marked with "?"; respell or check those by ear. Numbers are what to look at, not verdicts: a long line can be right.
"""
from __future__ import annotations

import _env  # noqa: F401
import argparse
import html
import json
import re
import statistics
from collections import defaultdict
from pathlib import Path

from common import ToolError, fail, read_lyric

import pronouncing

VOWELS = {"AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY", "IH", "IY", "OW", "OY", "UH", "UW"}
FUNCTION = set("a an the and or but of to in on at by for with from as is am are was were be been it its i me my you "
               "your we our they them their he him his she her this that these those not no so do does did".split())
# Okabe–Ito plus a few distinguishable extras: readable for most colour-blind viewers on light and dark backgrounds.
PALETTE = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#999999",
           "#8C6BB1", "#A6761D", "#66C2A5", "#E7298A"]


def phones(word: str) -> tuple[str | None, bool]:
    w = word.lower().strip("'")
    ps = pronouncing.phones_for_word(w)
    if not ps and w.endswith("in'"):
        ps = pronouncing.phones_for_word(w[:-1] + "g")
    if not ps and w.endswith("'s"):
        ps = pronouncing.phones_for_word(w[:-2])
    return (ps[0], True) if ps else (None, False)


def guess_syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and not w.endswith(("le", "ee", "ye")) and n > 1:
        n -= 1
    return max(1, n)


def tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z']*|\d+", text.replace("’", "'"))


def analyse(path: Path) -> dict:
    lines = read_lyric(path)
    out_lines = []
    for ln in lines:
        words = []
        for t in tokens(ln.text):
            ph, known = phones(t)
            if ph:
                stresses = pronouncing.stresses(ph)
                rp = pronouncing.rhyming_part(ph)
                perfect = re.sub(r"\d", "", rp)
                vowels = [re.sub(r"\d", "", p) for p in rp.split() if re.sub(r"\d", "", p) in VOWELS]
                all_vowels = [re.sub(r"\d", "", p) for p in ph.split() if re.sub(r"\d", "", p) in VOWELS]
                ps = ph.split()
                k = len(ps) - len(rp.split())  # index of the last stressed vowel
                onset = " ".join(re.sub(r"\d", "", p) for p in ps[max(0, k - 1):]) if k > 0 else None
                words.append({"w": t, "syl": len(stresses), "stress": stresses, "perfect": perfect,
                              "slant": " ".join(vowels), "vowels": all_vowels, "known": True, "onset": onset,
                              "final": re.sub(r"\d", "", ps[-1])})
            else:
                n = guess_syllables(t)
                words.append({"w": t, "syl": n, "stress": "?" * n, "perfect": None, "slant": None, "vowels": [],
                              "known": False, "onset": None, "final": None})
        out_lines.append({"id": ln.id, "section": ln.section, "text": ln.text, "words": words,
                          "syllables": sum(w["syl"] for w in words),
                          "stress": " ".join(w["stress"] for w in words)})

    # families inside each section: perfect keys shared by 2+ content words (or line ends), then slant keys
    by_section: dict[str, list[dict]] = defaultdict(list)
    for L in out_lines:
        by_section[L["section"]].append(L)
    fam_id = 0
    families: list[dict] = []
    for sec, ls in by_section.items():
        def candidates(key: str):
            groups = defaultdict(list)
            for L in ls:
                for i, w in enumerate(L["words"]):
                    if not w["known"] or w.get("family") is not None:
                        continue
                    end = i == len(L["words"]) - 1
                    if w["w"].lower() in FUNCTION and not end:
                        continue
                    k = w[key]
                    if k:
                        groups[k].append((L, i))
            return groups
        for key, kind in (("perfect", "rhyme"), ("slant", "slant")):
            for k, members in candidates(key).items():
                lines_in = {L["id"] for L, _ in members}
                distinct = {L["words"][i]["w"].lower() for L, i in members}
                if len(distinct) < 2:  # the same word again is repetition, not rhyme
                    continue
                if kind == "slant" and len(k.split()) == 1 and k in ("AH", "IH"):  # schwa-ish vowels match everything
                    continue
                fid = fam_id
                fam_id += 1
                families.append({"id": fid, "section": sec, "kind": kind, "key": k,
                                 "words": sorted(distinct), "lines": sorted(lines_in)})
                for L, i in members:
                    L["words"][i]["family"] = fid

    # the end scheme per section, multisyllabic endings, identical rhymes
    flags: list[str] = []
    for sec, ls in by_section.items():
        letters: dict[str, str] = {}
        for L in ls:
            if not L["words"]:
                continue
            last = L["words"][-1]
            key = last["perfect"] or last["w"].lower()
            letter = letters.setdefault(key, chr(ord("A") + len(letters)) if len(letters) < 26 else "?")
            L["end"] = letter
            L["tail"] = [v for w in L["words"] for v in w["vowels"]][-3:]
        for a, b in zip(ls, ls[1:]):
            wa, wb = a["words"][-1], b["words"][-1]
            if a.get("end") == b.get("end") and (wa["w"].lower() == wb["w"].lower() or
                                                 (wa["onset"] and wa["onset"] == wb["onset"])):
                flags.append(f"identical rhyme: line {a['id']} '{wa['w']}' / line {b['id']} '{wb['w']}'"
                             " (the same sounds from the consonant before the stressed vowel)")
        for i, a in enumerate(ls):
            for b in ls[i + 1:i + 4]:
                ta, tb = a.get("tail", []), b.get("tail", [])
                n = 0
                while n < min(len(ta), len(tb)) and ta[-1 - n] == tb[-1 - n]:
                    n += 1
                if n >= 2:
                    a.setdefault("multi", []).append(b["id"])
                    b.setdefault("multi", []).append(a["id"])
        syl = [L["syllables"] for L in ls]
        med = statistics.median(syl) if syl else 0
        for L in ls:
            if med and (L["syllables"] > med * 1.4 or L["syllables"] < med * 0.6) and abs(L["syllables"] - med) >= 3:
                flags.append(f"line {L['id']} has {L['syllables']} syllables; its section's median is {med:g}")
    # what the ear catches: line ends that rhyme with nothing near them, vowel-only rhymes, long lines, dense lines
    groups = [{"M", "N", "NG"}, {"P", "B", "T", "D", "K", "G"}, {"F", "V", "TH", "DH", "S", "Z", "SH", "ZH", "CH", "JH"},
              {"L", "R"}]

    def strength(a: dict, b: dict) -> str:
        if not a["known"] or not b["known"]:
            return "unknown"
        if a["w"].lower() == b["w"].lower():
            return "same word"
        if a["onset"] and a["onset"] == b["onset"]:
            return "identical"
        if a["perfect"] and a["perfect"] == b["perfect"]:
            return "perfect"
        if a["slant"] and a["slant"] == b["slant"]:
            fa, fb = a["final"], b["final"]
            if fa == fb or (fa in VOWELS and fb in VOWELS) or any(fa in g and fb in g for g in groups):
                return "close"
            return "vowel only"
        return "none"

    rank = {"perfect": 4, "close": 3, "same word": 2, "identical": 2, "vowel only": 1, "unknown": 1, "none": 0}
    ends = {"perfect": 0, "close": 0, "repeated": 0, "vowel only": 0, "none": 0}
    number_words = set("hundred thousand million billion trillion percent per cent zero one two three four five six "
                       "seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen "
                       "twenty thirty forty fifty sixty seventy eighty ninety".split())
    for sec, ls in by_section.items():
        for i, L in enumerate(ls):
            if not L["words"]:
                continue
            best, partner = "none", None
            for j in range(max(0, i - 2), min(len(ls), i + 3)):
                if j == i or not ls[j]["words"]:
                    continue
                st = strength(L["words"][-1], ls[j]["words"][-1])
                if rank[st] > rank[best]:
                    best, partner = st, ls[j]["id"]
            L["endRhyme"] = {"strength": best, "with": partner}
            key = "repeated" if best in ("same word", "identical") else ("vowel only" if best in ("vowel only", "unknown") else best)
            ends[key] += 1
            if len(ls) >= 3 and best == "none":
                flags.append(f"line {L['id']} ('{L['words'][-1]['w']}') rhymes with no line near it")
            elif best == "vowel only":
                flags.append(f"line {L['id']} ('{L['words'][-1]['w']}') rhymes only on the vowel with line {partner}")
        for L in ls:
            toks = [w["w"] for w in L["words"]]
            names = [t for k, t in enumerate(toks) if k > 0 and t[0].isupper() and t not in ("I", "I'm", "I've", "I'll", "I'd")]
            nums = [t for t in toks if t.isdigit() or t.lower() in number_words]
            L["dense"] = len(names) + len(nums)
            if L["dense"] >= 2:
                flags.append(f"line {L['id']} carries {len(names)} name(s) and {len(nums)} number word(s): "
                             f"{', '.join(names + nums)}")
            if L["syllables"] > 13:
                flags.append(f"line {L['id']} is {L['syllables']} syllables: long for a sung line")
    unknown = sorted({w["w"] for L in out_lines for w in L["words"] if not w["known"]})
    in_family = sum(1 for L in out_lines for w in L["words"] if w.get("family") is not None)
    total_words = sum(len(L["words"]) for L in out_lines)
    return {"file": str(path), "lines": out_lines, "families": families, "flags": flags, "unknown": unknown,
            "summary": {"lines": len(out_lines), "words": total_words, "characters": len(Path(path).read_text()),
                        "syllables_median": statistics.median([L["syllables"] for L in out_lines]),
                        "words_in_rhyme_families": in_family,
                        "line_ends": ends,
                        "lines_over_13_syllables": sum(1 for L in out_lines if L["syllables"] > 13),
                        "dense_lines": sum(1 for L in out_lines if L.get("dense", 0) >= 2),
                        "multisyllabic_endings": sum(1 for L in out_lines if L.get("multi")),
                        "sections": list(by_section)}}


def write_html(a: dict, out: Path) -> None:
    fams = {f["id"]: f for f in a["families"]}
    order: dict[int, int] = {}
    css_rules = []
    per_section: dict[str, int] = {}
    for f in a["families"]:
        idx = per_section.get(f["section"], 0)  # colours restart in each section
        per_section[f["section"]] = idx + 1
        order[f["id"]] = idx
        c = PALETTE[idx % len(PALETTE)]
        style = "solid" if f["kind"] == "rhyme" else "dashed"
        css_rules.append(f".f{f['id']}{{background:{c}33;border-bottom:3px {style} {c}}}")
    rows = []
    section = None
    for L in a["lines"]:
        if L["section"] != section:
            section = L["section"]
            rows.append(f'<tr class="sec"><td colspan="4">[{html.escape(section)}]</td></tr>')
        parts = []
        for w in L["words"]:
            t = html.escape(w["w"])
            cls = f' class="f{w["family"]}"' if w.get("family") is not None else ""
            title = f' title="{html.escape(fams[w["family"]]["kind"] + ": " + fams[w["family"]]["key"])}"' if cls else ""
            parts.append(f"<span{cls}{title}>{t}{'' if w['known'] else '<sup>?</sup>'}</span>")
        multi = f' <span class="multi">multi with {", ".join(map(str, L["multi"]))}</span>' if L.get("multi") else ""
        rows.append(f'<tr><td class="n">{L["id"]}</td><td class="line">{" ".join(parts)}{multi}</td>'
                    f'<td class="n">{L["syllables"]}</td><td class="st">{html.escape(L["stress"])} '
                    f'<b>{L.get("end", "")}</b></td></tr>')
    flags = "".join(f"<li>{html.escape(f)}</li>" for f in a["flags"]) or "<li>none</li>"
    unknown = html.escape(", ".join(a["unknown"])) or "none"
    page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rhyme map</title><style>
:root{{--bg:#fbfaf7;--fg:#1d1d1d;--mute:#6b6b6b;--line:#e4e1da}}
@media (prefers-color-scheme:dark){{:root{{--bg:#16171a;--fg:#ececec;--mute:#9a9a9a;--line:#2b2d31}}}}
body{{background:var(--bg);color:var(--fg);font:16px/1.5 ui-sans-serif,system-ui,sans-serif;margin:0;padding:24px 16px;max-width:1000px}}
table{{border-collapse:collapse;width:100%}} td{{padding:4px 8px;border-bottom:1px solid var(--line);vertical-align:top}}
.n{{color:var(--mute);text-align:right;width:3em;font-variant-numeric:tabular-nums}} .st{{color:var(--mute);font:13px ui-monospace,monospace;white-space:nowrap}}
.sec td{{color:var(--mute);padding-top:18px;border:0}} .line span{{padding:0 1px;border-radius:2px}} .multi{{color:var(--mute);font-size:12px;margin-left:8px}}
{''.join(css_rules)}
</style></head><body>
<h1 style="font-size:20px">Rhyme map</h1>
<p style="color:var(--mute)">Each colour is one sound family inside its section: solid underline = rhyme (same vowel and ending),
dashed = slant (same vowel sounds). Columns: line, syllables, stresses per word (1 stressed, 0 unstressed, ? unknown) and the
end-rhyme letter. {a["summary"]["lines"]} lines, {a["summary"]["words"]} words, {a["summary"]["characters"]} characters.</p>
<table>{''.join(rows)}</table>
<h2 style="font-size:16px">To look at</h2><ul>{flags}</ul>
<p style="color:var(--mute)">Not in the dictionary (counted by spelling): {unknown}</p>
</body></html>"""
    out.write_text(page)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lyric", type=Path)
    ap.add_argument("--html", type=Path)
    ap.add_argument("--json", type=Path)
    a = ap.parse_args()
    res = analyse(a.lyric)
    if a.html:
        write_html(res, a.html)
    if a.json:
        a.json.write_text(json.dumps(res, indent=1))
    section = None
    for L in res["lines"]:
        if L["section"] != section:
            section = L["section"]
            print(f"\n[{section}]")
        er = L.get("endRhyme", {}).get("strength", "")
        mark = {"perfect": " ", "close": "~", "same word": "=", "identical": "=", "vowel only": "?", "unknown": "?", "none": "✕"}.get(er, " ")
        print(f"{L['id']:>3} {L['syllables']:>3}  {L.get('end', ' ')}{mark} {L['text']}")
    print("\nEnd marks: blank perfect rhyme, ~ close, = same word, ? vowel only, ✕ no rhyme near it.")
    print("To look at:" + ("".join(f"\n- {f}" for f in res["flags"]) or " nothing flagged"))
    if res["unknown"]:
        print("Not in the dictionary: " + ", ".join(res["unknown"]))
    print(json.dumps(res["summary"]))


if __name__ == "__main__":
    try:
        main()
    except ToolError as e:
        fail(str(e))
