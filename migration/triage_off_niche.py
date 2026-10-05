#!/usr/bin/env python3
"""Phase 1c off-niche for Metaalhandel-gids.nl. bij twijfel → gesloten.

Important: Dutch *metalen* / English *metals* do NOT contain the substring
*metaal* — earlier pass over-closed real scrap yards. Fixed here.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT.parent / "src/content/metaalhandels"
NORM = ROOT / "scrape/normalized"
REPORT = ROOT / "OFF_NICHE_PASS.json"
MD = ROOT / "OFF_NICHE_TRIAGE.md"

STRONG = re.compile(
    r"metaalhandel|metaal\s*handel|oud[- ]?ijzer|schroot|"
    r"metaal\s*recycling|sloopmetaal|metaal\s*inname|"
    r"\bmetaal\b|\bmetalen\b|\bmetals\b|"
    r"\bferro\b|non[- ]?ferro|koperschroot|"
    r"ijzerhandel|ijzer\s*en\s*metalen|ijzer\s*&\s*metalen|"
    r"handel\s*in\s*oude\s*metalen|oude\s*metalen|"
    r"metaalrecy|schrootmetaal|\bijzerboer",
    re.I,
)
HARD_JUNK = re.compile(
    r"camping|hotel|restaurant|kapsalon|makelaar|tandarts|fysio|"
    r"hovenier|schilder|autobedrijf|\bgarage\b|sportschool|zwembad|"
    r"supermarkt|gemeente\b|architect|speelgoed|tuincentrum|"
    r"aannemer|bouwbedrijf|notaris|advocaat|dierenarts|"
    r"entertainment(?!\s*&\s*metals)",
    re.I,
)
IN_TEXT = re.compile(
    r"\bmetaal\b|\bmetalen\b|\bmetals\b|schroot|oud[- ]?ijzer|"
    r"metaal\s*recycling|metaalrecy|\bferro\b|non[- ]?ferro|"
    r"koper|aluminium|messing|\bijzer\b|scrap|"
    r"sloopmetaal|metaal\s*inname|ijzerhandel",
    re.I,
)


def name_blob(d: dict) -> str:
    return f"{d.get('naam') or ''} {d.get('slug') or ''}"


def host_blob(d: dict) -> str:
    w = d.get("website") or ""
    return re.sub(r"^https?://(www\.)?", "", w, flags=re.I).split("/")[0]


def full(d: dict) -> str:
    # Do NOT use meta_description — Django boilerplate always mentions oud ijzer.
    # Do NOT use kenmerken — category tags are site-wide defaults on junk too.
    # Website host is fair game (e.g. holtiesschrootmetaal.nl).
    return " ".join(
        [
            name_blob(d),
            d.get("omschrijving") or "",
            d.get("meta_title") or "",
            host_blob(d),
        ]
    )


def should_close(d: dict) -> str | None:
    nb, fb = name_blob(d), full(d)
    strong = bool(STRONG.search(nb) or STRONG.search(fb))
    if HARD_JUNK.search(nb) and not strong:
        return "hard junk name"
    if strong or IN_TEXT.search(fb):
        return None
    return "twijfel → gesloten (no metaal/schroot signal)"


def main() -> None:
    closed = []
    reasons = Counter()
    actief = 0
    for path in sorted(CONTENT.glob("*.json")):
        d = json.loads(path.read_text())
        reason = should_close(d)
        if not reason:
            if d.get("status") != "actief" or d.get("_triage"):
                d["status"] = "actief"
                d.pop("_triage", None)
                path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
                npath = NORM / path.name
                if npath.exists():
                    nd = json.loads(npath.read_text())
                    nd["status"] = "actief"
                    nd.pop("_triage", None)
                    npath.write_text(json.dumps(nd, ensure_ascii=False, indent=2) + "\n")
            actief += 1
            continue
        d["status"] = "gesloten"
        d["_triage"] = {"reason": reason, "pass": "off-niche-1c"}
        path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
        npath = NORM / path.name
        if npath.exists():
            nd = json.loads(npath.read_text())
            nd["status"] = "gesloten"
            nd["_triage"] = d["_triage"]
            npath.write_text(json.dumps(nd, ensure_ascii=False, indent=2) + "\n")
        closed.append({"naam": d.get("naam"), "reason": reason, "file": path.name})
        reasons[reason] += 1

    report = {
        "counts": {"twijfel": 0, "closed": len(closed), "actief": actief},
        "reasons": dict(reasons),
        "samples": closed[:30],
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    MD.write_text(
        "# Off-niche — Metaalhandel-gids.nl\n\n"
        f"Actief {actief} · Gesloten {len(closed)} · twijfel=0\n\n"
        + "\n".join(f"- {k}: {v}" for k, v in reasons.items())
        + "\n\nRe-run 2026-10-04: fixed metalen/metals false closes.\n"
    )
    print(json.dumps(report["counts"], indent=2))
    print("reasons", dict(reasons))


if __name__ == "__main__":
    main()
