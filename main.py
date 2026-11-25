#!/usr/bin/env python3
"""Funniest One-Line Out-of-Office Reply — make.fun entry.

Writes one out-of-office auto-reply line to /output/entry.txt.

The line is the winner of a scored candidate tournament (specificity /
surprise / freshness, each 1-5). The winning line turns the standard
"if urgent, contact..." convention against itself: it asks the sender
to define urgent, then tells them to wait until Monday anyway.
"""
import os
import sys

# Candidate tournament: (line, specificity, surprise, freshness).
CANDIDATES = [
    (
        "Out of office until Monday. My inbox is now a wildlife reserve: "
        "please do not feed the emails.",
        3, 3, 3,
    ),
    (
        "Out of office. I have set my status to 'away' and my brain to "
        "'also away'. They are in sync for the first time all year.",
        3, 3, 3,
    ),
    (
        "I'm away until Monday. My auto-reply is the only thing in this "
        "company working overtime this week.",
        4, 4, 4,
    ),
    (
        "I'm away until Monday. If this is urgent, please define urgent, "
        "then wait until Monday anyway.",
        4, 5, 4,
    ),
    (
        "Out of office until Monday. I am not ignoring you. I am ignoring "
        "everyone, equally, with a system in place.",
        4, 4, 4,
    ),
    (
        "I'm away until Monday. This message was written by me, in advance, "
        "which is the most organised I have been all year.",
        4, 4, 4,
    ),
]

# The gate: 1-160 UTF-8 characters, a single line, not only whitespace.
MIN_CHARS = 1
MAX_CHARS = 160


def tournament_winner(candidates):
    """Pick the highest total score; ties break to the shorter line."""
    best = None
    best_score = -1
    for line, spec, surp, fresh in candidates:
        score = spec + surp + fresh
        if score > best_score or (
            score == best_score and len(line) < len(best)
        ):
            best = line
            best_score = score
    return best, best_score


def validate(line):
    """Check the entry against the competition gate."""
    if not line or not line.strip():
        raise ValueError("entry is empty or only whitespace")
    chars = len(line)
    if chars < MIN_CHARS or chars > MAX_CHARS:
        raise ValueError(
            f"entry is {chars} chars, gate is {MIN_CHARS}-{MAX_CHARS}"
        )
    # The gate counts UTF-8 characters, but the leaderboard's Size column
    # shows bytes, so keep the byte count visible in the check output.
    nbytes = len(line.encode("utf-8"))
    if nbytes > MAX_CHARS:
        raise ValueError(
            f"entry is {nbytes} bytes, over the {MAX_CHARS} byte budget"
        )
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    return chars, nbytes


def main(argv):
    line, score = tournament_winner(CANDIDATES)
    chars, nbytes = validate(line)
    if "--check" in argv:
        print(f"OK: {chars} chars, {nbytes} bytes, "
              f"tournament score {score}/15, single line")
        print(line)
        return 0
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != line:
        raise ValueError("round-trip mismatch: file differs from entry")
    print(f"Wrote {chars} chars to {path} (tournament score {score}/15)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
