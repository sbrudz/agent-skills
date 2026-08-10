#!/usr/bin/env python3
"""Structural evidence for the spine / slot-claim / typography rules.

Counts what the Before-Pass-1, heading, and Pass 2 typography rules make checkable:
heading depth (a flat H2 list with zero H3 is the v3 failure), sequential numbering
(which disguises a 3-5 violation), bolded lead-in paragraphs (hierarchy carried by
typography), conventional slot names (what a reader navigates by), and inline
verification tags (analysis narration leaking onto the page).

Surfaces evidence; does not grade.

Usage: python3 structure_report.py FILE [FILE ...]
"""
import re
import sys

SLOTS = [
    "context", "background", "problem", "proposal", "proposed", "design",
    "alternatives", "risk", "rollout", "migration", "open question",
    "timeline", "impact", "appendix", "evidence", "gotcha", "summary",
    "decision", "scope", "cost", "security", "testing", "estimate",
]


def analyze(path):
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")

    h1 = [l for l in lines if re.match(r"^# ", l)]
    h2 = [l for l in lines if re.match(r"^## ", l)]
    h3 = [l for l in lines if re.match(r"^### ", l)]

    numbered = [l for l in h2 if re.match(r"^## \d+[.)]\s", l)]
    with_colon = [l for l in h2 + h3 if ":" in l.split(" ", 1)[-1]]
    slotted = [
        l for l in h2 + h3
        if any(s in l.lower() for s in SLOTS)
    ]

    # paragraphs: blank-line separated blocks that are not headings, tables,
    # code fences, or list items
    blocks = re.split(r"\n\s*\n", text)
    paras, bolded = [], []
    for b in blocks:
        s = b.strip()
        if not s or s.startswith(("#", "|", "```", ">", "---")):
            continue
        if re.match(r"^[-*+]\s|^\d+\.\s", s):
            continue
        paras.append(s)
        if s.startswith("**"):
            bolded.append(s)

    tags = re.findall(r"\[(?:VERIFIED|UNMEASURED|UNVERIFIED|TODO|ASSUMED)[^\]]*\]", text)
    words = len(text.split())

    return {
        "path": path, "words": words,
        "h1": len(h1), "h2": len(h2), "h3": len(h3),
        "numbered_h2": len(numbered),
        "headings_with_colon": len(with_colon),
        "headings_with_slot": len(slotted),
        "paragraphs": len(paras),
        "bolded_leadins": len(bolded),
        "inline_tags": len(tags),
        "h2_list": [l[3:].strip() for l in h2],
    }


def main(paths):
    for p in paths:
        r = analyze(p)
        print("=" * 70)
        print(f"### {r['path']}")
        print(f"total: {r['words']} words")
        print(f"  headings          H2={r['h2']}  H3={r['h3']}"
              f"   (H3=0 with many H2 means hierarchy by typography)")
        print(f"  numbered H2       {r['numbered_h2']}"
              f"   (numbering is not grouping)")
        print(f"  slot in heading   {r['headings_with_slot']}/{r['h2'] + r['h3']}"
              f"   (what the reader navigates by)")
        print(f"  slot+claim form   {r['headings_with_colon']}/{r['h2'] + r['h3']}"
              f"   (colon-separated slot then claim)")
        print(f"  bolded lead-ins   {r['bolded_leadins']}/{r['paragraphs']} paragraphs")
        print(f"  inline tags       {r['inline_tags']}"
              f"   (analysis narration; belongs in an appendix)")
        print("  H2 headings:")
        for h in r["h2_list"]:
            print(f"    - {h[:88]}")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1:])
