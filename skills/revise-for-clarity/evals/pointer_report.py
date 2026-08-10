#!/usr/bin/env python3
"""Pointer audit: extract every label-style reference with its containing sentence.

Grades the revise-for-clarity evals, and reproduces the "external labels" column
in RESULTS.md. Usage:

    python3 pointer_report.py <file.md> [<file.md> ...]
    python3 pointer_report.py --summary <file.md> [...]   # one line per file

A pointer is "resolved" when the sentence containing it also states what the referent
says. That call needs a reader, so this script surfaces evidence rather than guessing:
the substance heuristic below is deliberately loose and over-flags. Grade by reading the
printed sentences, not by trusting the counts.

INTERNAL_KINDS are references a document defines itself (its own phase list, track table,
or enumerated options). Those are self-contained and excluded from the external count.
Everything else requires an artifact the reader does not have.
"""
import re
import sys
from pathlib import Path

POINTER_PATTERNS = [
    (r"\b[Dd]ecisions?\s+\d+(\s+and\s+\d+)?", "decision-number"),
    (r"\bv\d+(\s+(RFC|proposal))?('s)?\b", "version-doc"),
    (r"\bopen question \d+", "question-number"),
    (r"\b[Mm]ilestones?\s+\d+", "milestone"),
    (r"\b[A-Z]{3,6}-\d+", "ticket"),
    (r"\bthe council\b|\bcouncil's\b", "review-body"),
    (r"\bthe (incident )?review\b|\bin review\b", "review-artifact"),
    (r"\bthe runbook\b|\bthe mockup\b|\bthe prototype\b", "artifact"),
    (r"\b(indexing|write-path) RFCs\b", "doc-class"),
    (r"\bPhoenix migration\b", "project-name"),
    (r"\b(Dana|Priya|Wei|Frank|Thao)\b", "bare-person"),
    (r"\bTrack [A-E]\b", "track"),
    (r"\b[Pp]hases?\s+\d+", "phase"),
    (r"\bOption \d+", "option-number"),
    (r"§[\d.]+", "section-mark"),
]

INTERNAL_KINDS = {"track", "phase", "option-number", "section-mark"}

SUBSTANCE_HINTS = re.compile(
    r"(,\s*which\b|,\s*the\b|\bthat\s+\w+s\b|—|--|:\s|\bsequences?\b|\brequires?\b|"
    r"\bmeasures?\b|\bstates?\b|\bsays\b|\bcovers?\b|\bfound\b|\bproposed?\b|\(.*\))"
)


def sentences(text: str):
    body = re.sub(r"^\s*\|.*\|\s*$", "", text, flags=re.M)   # drop table rows
    body = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", body)      # unwrap md links
    body = re.sub(r"\s+", " ", body)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z*])", body) if s.strip()]


def audit(text: str):
    rows = []
    for sent in sentences(text):
        for pat, kind in POINTER_PATTERNS:
            for m in re.finditer(pat, sent):
                rows.append({
                    "label": m.group(0).strip(),
                    "kind": kind,
                    "sentence": sent[:300],
                    "external": kind not in INTERNAL_KINDS,
                    "has_substance_hint": bool(SUBSTANCE_HINTS.search(sent)),
                })
    return rows


def main():
    args = [a for a in sys.argv[1:] if a != "--summary"]
    summary_only = "--summary" in sys.argv

    for arg in args:
        p = Path(arg)
        if not p.exists():
            print(f"{arg}: MISSING")
            continue
        text = p.read_text()
        rows = audit(text)
        words = len(text.split())
        external = [r for r in rows if r["external"]]

        if summary_only:
            print(f"{words:5d} words  {len(external):3d} external label occurrences  "
                  f"{len(rows):3d} total  {p}")
            continue

        headings = re.findall(r"^#{1,3}\s+(.*)$", text, flags=re.M)
        print(f"\n{'='*70}\n### {p}")
        print(f"words: {words} | headings: {len(headings)} | "
              f"external label occurrences: {len(external)} | "
              f"all pointer occurrences: {len(rows)}")
        print("\nheadings:")
        for h in headings:
            print(f"  - {h}")
        print("\nexternal labels (grade each by reading the sentence):")
        for r in external:
            flag = " " if r["has_substance_hint"] else "!"
            print(f"  {flag} [{r['kind']}] {r['label']!r}")
            print(f"      {r['sentence']}")
        print("\n  ('!' = no substance hint in the sentence; heuristic, over-flags)")


if __name__ == "__main__":
    main()
