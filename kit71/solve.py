"""solve.py — the solver's own module. Ontology: saturation (+ stdlib). Nothing else.

Every object that leaves this module for the report is re-entered through the law:
Foothold(...) runs the_law on construction, canon() names it, certify() is the only
door for a Submission. Fast code (fast/*.c) only proposes; this module decides.
"""

from __future__ import annotations

import json
import os
import random
import sys
import time
from math import gcd

from saturation import (TARGET, Book, Degenerate, Foothold, canon, certify,
                        exact, in_space_only, motions, space, the_law)

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
LEDGER = os.path.join(RESULTS, "ledger.json")


# --- tokens <-> registers -------------------------------------------------

def tok(u: int, v: int, n: int) -> int:
    return u * n + v


def uv(t: int, n: int) -> tuple[int, int]:
    return divmod(t, n)


# --- fast (quadratic) legality tools; the law itself stays cubic ------------

def _dir(du: int, dv: int) -> tuple[int, int]:
    g = gcd(abs(du), abs(dv))
    du //= g
    dv //= g
    if du < 0 or (du == 0 and dv < 0):
        du, dv = -du, -dv
    return du, dv


def triples_through(p, others) -> int:
    """number of collinear triples {p, q, r} with q, r in others (registers)."""
    cnt: dict = {}
    t = 0
    for q in others:
        if q == p:
            continue
        d = _dir(q[0] - p[0], q[1] - p[1])
        k = cnt.get(d, 0)
        t += k
        cnt[d] = k + 1
    return t


def admissible(pts: list, p) -> bool:
    """may register-pair p join pts (a lawful set) without a collinear triple?"""
    seen = set()
    for q in pts:
        if q == p:
            return False
        d = _dir(q[0] - p[0], q[1] - p[1])
        if d in seen:
            return False
        seen.add(d)
    return True


def repair(pts: set, n: int) -> set:
    """greedy: drop the point sitting in most collinear triples until none remain."""
    pts = set(pts)
    while True:
        lst = list(pts)
        worst, worst_t = None, 0
        for p in lst:
            t = triples_through(p, lst)
            if t > worst_t:
                worst, worst_t = p, t
        if worst is None:
            return pts
        pts.discard(worst)


def greedy_fill(pts: set, n: int, rng: random.Random) -> set:
    """add admissible cells in random order until stuck (rows/cols cap at 2 implicitly)."""
    pts = set(pts)
    cells = [(u, v) for u in range(n) for v in range(n)]
    changed = True
    while changed:
        changed = False
        rng.shuffle(cells)
        lst = list(pts)
        for c in cells:
            if c in pts:
                continue
            if admissible(lst, c):
                pts.add(c)
                lst.append(c)
                changed = True
    return pts


# --- algebraic seeds -----------------------------------------------------------

def conic_points(n: int, q: int, a: int, b: int, c: int, d: int, e: int, f: int) -> set:
    """all cells (x, y) of the n x n box with a x^2 + b xy + c y^2 + d x + e y + f = 0 (mod q)."""
    out = set()
    for x in range(n):
        for y in range(n):
            if (a * x * x + b * x * y + c * y * y + d * x + e * y + f) % q == 0:
                out.add((x, y))
    return out


# --- certified I/O ---------------------------------------------------------------

def to_book(pts, n: int) -> Book:
    return frozenset(tok(u, v, n) for u, v in pts)


def from_book(book: Book, n: int) -> set:
    return {uv(t, n) for t in book}


def load_tokens(path: str) -> list:
    with open(path) as fh:
        txt = fh.read().replace(",", " ")
    return [int(x) for x in txt.split()]


def _load_ledger() -> dict:
    if os.path.exists(LEDGER):
        with open(LEDGER) as fh:
            return json.load(fh)
    return {"n": TARGET, "entries": [], "best": None}


def _save_ledger(led: dict) -> None:
    os.makedirs(RESULTS, exist_ok=True)
    tmp = LEDGER + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(led, fh)
    os.replace(tmp, LEDGER)


def record(book: Book, n: int, principle: str, note: str = "") -> Foothold:
    """re-enter through the law, name by canon, remember. Returns the Foothold."""
    book = in_space_only(exact(frozenset(book)), n)
    fh = Foothold(n=n, book=book)          # the_law runs here
    key = canon(book, n)
    led = _load_ledger()
    keys = {tuple(e["canon"]) for e in led["entries"]}
    fresh = key not in keys
    entry = {"size": fh.size, "shortfall": fh.shortfall, "principle": principle,
             "note": note, "time": time.strftime("%Y-%m-%d %H:%M:%S"),
             "tokens": sorted(book), "canon": list(key)}
    if fresh:
        led["entries"].append(entry)
        led["entries"].sort(key=lambda e: -e["size"])
        led["entries"] = led["entries"][:200]
    if led["best"] is None or fh.size > led["best"]["size"]:
        led["best"] = entry
    _save_ledger(led)
    if fresh:
        os.makedirs(RESULTS, exist_ok=True)
        import hashlib
        digest = hashlib.sha1(repr(key).encode()).hexdigest()[:10]
        fn = os.path.join(RESULTS, f"foothold_n{n}_size{fh.size}_{digest}.json")
        with open(fn, "w") as out:
            json.dump(entry, out)
    print(f"{fh!r} fresh={fresh} principle={principle} {note}")
    return fh


def best_report(n: int = TARGET) -> None:
    led = _load_ledger()
    b = led["best"]
    if b is None:
        print("ledger empty")
        return
    book = frozenset(b["tokens"])
    fh = Foothold(n=n, book=book)          # law re-run at report time
    print(f"BEST {fh!r}")
    print("principle:", b["principle"], b.get("note", ""))
    print("canon key:", tuple(canon(book, n)))
    print("sorted tokens:", sorted(book))
    if len(book) == 2 * n:
        print("CERTIFICATE:", certify(book, n))


# --- CLI ------------------------------------------------------------------------

def _cli(argv: list) -> None:
    if not argv:
        print(__doc__)
        return
    cmd, *rest = argv
    if cmd == "verify":                    # verify n files... proposed by fast code
        n = int(rest[0])
        for path in rest[1:]:
            book = frozenset(load_tokens(path))
            try:
                if n == TARGET:
                    fh = record(book, n, principle=f"file:{os.path.basename(path)}")
                else:
                    fh = Foothold(n=n, book=in_space_only(exact(book), n))
                print(path, "->", fh, "| canon", canon(book, n)[:6], "...")
                if len(book) == 2 * n:
                    print("   ", certify(book, n))
            except Degenerate as no:
                print(path, "-> REFUSED, witness", no.args[0])
    elif cmd == "report":
        best_report()
    else:
        print("unknown command", cmd)


if __name__ == "__main__":
    _cli(sys.argv[1:])
