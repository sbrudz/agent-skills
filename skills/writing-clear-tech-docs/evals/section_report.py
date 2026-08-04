#!/usr/bin/env python3
"""Section balance report: per-H2 word counts, largest first.

Grades the walkthrough-budget rule ("when the walkthrough carries the central
claim, no other section should be longer") and the hierarchy red flag about six
H2 sections of equal weight. Usage:

    python3 section_report.py <file.md> [<file.md> ...]

Word counts exclude the heading line itself. Table rows are counted, since a
risk table is content the section is spending budget on.
"""
import re
import sys
from pathlib import Path


def sections(text: str):
    """[(heading, word_count)] for every H2 and H3, plus a leading '(preamble)' entry.

    H3s are reported separately and their words are NOT folded into the parent H2.
    Measuring H2 alone lets a revision hide an underfed walkthrough by nesting an
    unrelated subsection beneath its heading, which inflates the parent's count
    while the walkthrough itself stays as thin as it was.
    """
    parts = re.split(r"^(##+)\s+(.*)$", text, flags=re.M)
    out = [("(preamble)", len(parts[0].split()))]
    for i in range(1, len(parts) - 2, 3):
        depth, heading, body = parts[i], parts[i + 1], parts[i + 2]
        prefix = "  " * (len(depth) - 2)
        out.append((f"{prefix}{heading.strip()}", len(body.split())))
    return out


def main():
    for arg in sys.argv[1:]:
        p = Path(arg)
        if not p.exists():
            print(f"{arg}: MISSING")
            continue
        text = p.read_text()
        secs = sections(text)
        total = len(text.split())
        print(f"\n{'=' * 70}\n### {p}\ntotal: {total} words | H2 sections: {len(secs) - 1}")
        for heading, words in sorted(secs, key=lambda s: -s[1]):
            bar = "#" * round(words / max(total, 1) * 60)
            print(f"  {words:5d}  {bar:<20} {heading}")


if __name__ == "__main__":
    main()
