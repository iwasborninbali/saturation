"""cycle_family.py — unique defect sets for the odd-cycle families (balance lemma), modulo D4.

A defect is a set of half-turn pairs {(x,y),(m-x,m-y)} forming an Eulerian digraph on row-classes;
we enumerate 3-cycles (x,y),(y,z),(z,x') with x' in {x, m-x}, and (optionally) 3-cycle + two diagonal
loops, and print one representative per D4-orbit as a PAIRS string:  "x,y;y,z;z,x'".

    python3 kit71/bench/cycle_family.py N [--loops] > list.txt
"""
import sys


def motions(n):
    m = n - 1
    return [lambda u, v: (u, v), lambda u, v: (v, m - u), lambda u, v: (m - u, m - v), lambda u, v: (m - v, u),
            lambda u, v: (v, u), lambda u, v: (m - u, v), lambda u, v: (u, m - v), lambda u, v: (m - v, m - u)]


def canon(cells, n):
    ms = motions(n)
    return min(tuple(sorted(f(u, v) for (u, v) in cells)) for f in ms)


def pair_cells(x, y, n):
    m = n - 1
    return {(x, y), (m - x, m - y)}


def main():
    n = int(sys.argv[1]); loops = "--loops" in sys.argv
    m = n - 1; h = m // 2
    seen = set(); out = []
    for x in range(h):
        for y in range(n):
            if y in (h, x, m - x):
                continue
            for z in range(n):
                if z in (h, x, m - x, y, m - y):
                    continue
                for xp in (x, m - x):
                    pairs = [(x, y), (y, z), (z, xp)]
                    cells = set()
                    for (a, b) in pairs:
                        cells |= pair_cells(a, b, n)
                    if len(cells) != 6:
                        continue
                    if not loops:
                        key = canon(cells, n)
                        if key in seen:
                            continue
                        seen.add(key)
                        out.append(";".join(f"{a},{b}" for a, b in pairs))
                    else:
                        # add two diagonal loops: main-diagonal pair (d,d) and anti-diagonal pair (e, m-e), classes distinct from x,y,z
                        used = {x, m - x, y, m - y, z, m - z}
                        for d in range(h):
                            if d in used:
                                continue
                            for e in range(h):
                                if e in used or e == d:
                                    continue
                                cells2 = cells | pair_cells(d, d, n) | pair_cells(e, m - e, n)
                                if len(cells2) != 10:
                                    continue
                                key = canon(cells2, n)
                                if key in seen:
                                    continue
                                seen.add(key)
                                out.append(";".join(f"{a},{b}" for a, b in pairs + [(d, d), (e, m - e)]))
    for s in out:
        print(s)
    print(f"# n={n} unique defect sets: {len(out)}", file=sys.stderr)


if __name__ == "__main__":
    main()
