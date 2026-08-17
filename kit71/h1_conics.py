"""H1: modular conics in the 71-box. Question: which (q, conic) after greedy repair
and greedy fill gives the largest lawful book? Usage: python3 h1_conics.py [q ...]"""
from __future__ import annotations

import random
import sys

from saturation import TARGET
from solve import conic_points, greedy_fill, record, repair, to_book

N = TARGET


def primes(lo, hi):
    return [p for p in range(lo, hi + 1) if p > 1 and all(p % d for d in range(2, int(p ** .5) + 1))]


def run(q: int, rng: random.Random):
    fams = []
    # parabola y = x^2 + t
    for t in range(0, q, max(1, q // 6)):
        fams.append((f"parab y=x^2+{t} mod {q}", (1, 0, 0, 0, -1, t)))
    # hyperbola x*y = k
    for k in range(1, q, max(1, q // 6)):
        fams.append((f"hyper xy={k} mod {q}", (0, 1, 0, 0, 0, -k)))
    # ellipse/circle x^2 + y^2 = k
    for k in range(1, q, max(1, q // 6)):
        fams.append((f"circle x^2+y^2={k} mod {q}", (1, 0, 1, 0, 0, -k)))
    # a few random conics
    for _ in range(4):
        co = tuple(rng.randrange(q) for _ in range(6))
        fams.append((f"conic {co} mod {q}", co))
    best = None
    for name, co in fams:
        raw = conic_points(N, q, *co)
        rep = repair(raw, N)
        filled = greedy_fill(rep, N, rng)
        line = f"q={q:2d} {name:34s} raw={len(raw):3d} repaired={len(rep):3d} filled={len(filled):3d}"
        print(line, flush=True)
        if best is None or len(filled) > len(best[1]):
            best = (name, filled, len(raw), len(rep))
    name, filled, r, p = best
    record(to_book(filled, N), N, principle=name,
           note=f"raw={r} repaired={p} greedy-filled={len(filled)}")


if __name__ == "__main__":
    qs = [int(a) for a in sys.argv[1:]] or primes(29, 71)
    rng = random.Random(1)
    for q in qs:
        run(q, rng)
