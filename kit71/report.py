"""report.py — end-of-session report. Everything printed here is re-entered through the law
at print time: the best Foothold is rebuilt from its token list (the_law runs), the canon key is
recomputed, and a Submission is attempted only if the size is 2n (certify decides)."""
from __future__ import annotations

import json
import os
import sys

from saturation import TARGET, Foothold, canon, certify, exact, in_space_only, the_law
from brief import Ledger, Submission

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "results", "ledger.json")
NOTES = os.path.join(HERE, "notes", "hypotheses.md")


def main() -> None:
    n = TARGET
    led = json.load(open(LEDGER))
    entries = sorted(led["entries"], key=lambda e: -e["size"])
    best = entries[0]
    book = in_space_only(exact(frozenset(best["tokens"])), n)
    fh = Foothold(n=n, book=book)                     # the law, again
    key = canon(book, n)
    assert list(key) == best["canon"], "canon key drifted"
    ledger = Ledger()
    for e in entries[:20]:
        ledger.log(Foothold(n=n, book=frozenset(e["tokens"])))   # brief.Ledger: re-verifies, dedups by canon
    print("=" * 78)
    print(f"RESOLUTION {n}  ceiling {2 * n}")
    print(f"BEST {fh!r}   (ledger.best = {ledger.best!r}, {len(ledger.keys)} distinct canon keys among top-20)")
    print("principle:", best["principle"], best.get("note", ""))
    if fh.size == 2 * n:
        sub = Submission(n=n, book=book)
        print("SUBMISSION:", sub.certificate)
    else:
        print(f"no Submission: size {fh.size} < {2 * n}; shortfall {fh.shortfall}")
    print("canon key:", key)
    print("sorted tokens:", sorted(book))
    print("as (row, col):", [divmod(t, n) for t in sorted(book)])
    print()
    print("distinct footholds by size (ledger):")
    sizes = {}
    for e in entries:
        sizes[e["size"]] = sizes.get(e["size"], 0) + 1
    print("  " + ", ".join(f"{s}:{c}" for s, c in sorted(sizes.items(), reverse=True)))
    print()
    if os.path.exists(NOTES):
        print(open(NOTES).read())


if __name__ == "__main__":
    main()
