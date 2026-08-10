#!/usr/bin/env python3
"""Temporal evidence for the four-state rule (SKILL.md Pass 4).

Does the mechanical half of the tense audit in references/temporal-clarity.md:
per-section counts of future markers, present-state markers, and past-tense claims,
plus the two greps the audit prescribes (future markers stranded in current-state
sections, current-state markers stranded in design/rollout sections), undated
past-tense sentences, and gate-clause coverage for flag mentions.

Steps 1 to 3 of the audit need a reader. This surfaces evidence and does not grade.

Usage: python3 tense_report.py FILE [FILE ...]
"""
import re
import sys

FUTURE = [r"\bwill\b", r"\bwe plan\b", r"\bonce we\b", r"\bgoing to\b", r"\bwe'll\b"]
CONDITIONAL = [r"\bwould\b"]
MODAL_NOSTATE = [r"\bshould\b"]
PRESENT_STATE = [r"\bcurrently\b", r"\btoday\b", r"\bat present\b", r"\balready\b",
                 r"\bright now\b", r"\bnow\b"]
PAST = [r"\bused to\b", r"\bwe moved\b", r"\bwe shipped\b", r"\bwas written\b",
        r"\bwas reported\b", r"\bwas accepted\b", r"\bhas not changed\b",
        r"\bwe changed\b", r"\bwas excluded\b", r"\bshipped\b", r"\bmoved\b"]
DATE = [r"\b(19|20)\d{2}\b", r"\b(?:January|February|March|April|May|June|July|"
        r"August|September|October|November|December)\b", r"\bQ[1-4]\b",
        r"\b\d{4}-\d{2}-\d{2}\b"]
VAGUE_DATE = [r"\brecently\b", r"\ba while ago\b", r"\bhistorically\b",
              r"\bin the past\b", r"\bpreviously\b"]
GATE = [r"\bbehind\b", r"\bflag\b", r"\boff in production\b", r"\bnot enabled\b",
        r"\bstaging only\b", r"\bunmerged\b", r"\bundeployed\b", r"\bno-op\b"]

CURRENT_SECTION = ["where we are", "current", "background", "today", "status",
                   "problem", "context"]
FUTURE_SECTION = ["will build", "proposed", "design", "rollout", "plan",
                  "what we will", "migration"]


def hits(pats, s):
    return sum(len(re.findall(p, s, re.I)) for p in pats)


def split_sentences(s):
    s = re.sub(r"\s+", " ", s)
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+", s) if x.strip()]


def sections(text):
    out, cur, buf = [], "(preamble)", []
    for line in text.split("\n"):
        m = re.match(r"^#{1,3} (.+)", line)
        if m:
            out.append((cur, "\n".join(buf)))
            cur, buf = m.group(1).strip(), []
        else:
            buf.append(line)
    out.append((cur, "\n".join(buf)))
    return [(t, b) for t, b in out if b.strip()]


def prose_only(body):
    keep = []
    for line in body.split("\n"):
        s = line.strip()
        if s.startswith(("|", "```", ">")):
            continue
        keep.append(line)
    return "\n".join(keep)


def main(paths):
    for path in paths:
        text = open(path, encoding="utf-8").read()
        print("=" * 78)
        print(f"### {path}")

        undated, leaked_future, leaked_present, ungated = [], [], [], []
        rows = []

        for title, body in sections(text):
            p = prose_only(body)
            f, c, m = hits(FUTURE, p), hits(CONDITIONAL, p), hits(MODAL_NOSTATE, p)
            pr, pa = hits(PRESENT_STATE, p), hits(PAST, p)
            rows.append((title, f, c, m, pr, pa))

            tl = title.lower()
            in_current = any(k in tl for k in CURRENT_SECTION)
            in_future = any(k in tl for k in FUTURE_SECTION)

            for sent in split_sentences(p):
                if hits(FUTURE, sent) or hits(MODAL_NOSTATE, sent):
                    if in_current:
                        leaked_future.append((title, sent))
                if hits(PRESENT_STATE, sent) and in_future:
                    leaked_present.append((title, sent))
                if hits(PAST, sent) and not hits(DATE, sent):
                    if hits(VAGUE_DATE, sent) or hits(PAST, sent):
                        undated.append((title, sent))
                if hits(GATE, sent) == 0 and re.search(r"\bflag\b", sent, re.I):
                    ungated.append((title, sent))

        print(f"{'section':<42}{'will':>5}{'would':>6}{'should':>7}"
              f"{'now':>5}{'past':>6}")
        for t, f, c, m, pr, pa in rows:
            print(f"  {t[:40]:<40}{f:>5}{c:>6}{m:>7}{pr:>5}{pa:>6}")

        print(f"\n[1] future markers in current-state sections: {len(leaked_future)}")
        for t, s in leaked_future[:8]:
            print(f"    ({t[:26]}) {s[:92]}")
        print(f"\n[2] present-state markers in design/rollout sections: "
              f"{len(leaked_present)}")
        for t, s in leaked_present[:8]:
            print(f"    ({t[:26]}) {s[:92]}")
        print(f"\n[3] past-tense sentences with no date: {len(undated)}")
        for t, s in undated[:10]:
            print(f"    ({t[:26]}) {s[:92]}")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1:])
