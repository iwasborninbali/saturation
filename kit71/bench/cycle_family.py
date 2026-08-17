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


def sample_cycles(n, length, k, rng, loops=False):
    """random odd cycles of the given length (5 or 3+loops variants), canonical-deduped; yields PAIRS strings"""
    m = n - 1; h = m // 2
    seen = set(); out = []
    classes = [i for i in range(h)]              # row classes 0..h-1 (h itself excluded: centre row)
    tries = 0
    while len(out) < k and tries < 50 * k:
        tries += 1
        cls = rng.sample(classes, length)
        # representatives: first vertex x in class cls[0] (x or m-x irrelevant up to D4), others random sign
        verts = [cls[0]] + [rng.choice((c, m - c)) for c in cls[1:]]
        pairs = [(verts[i], verts[(i + 1) % length]) for i in range(length)]
        # closing sign: replace last target by x or m-x
        if rng.random() < 0.5:
            pairs[-1] = (pairs[-1][0], m - pairs[-1][1])
        cells = set()
        for (a, b) in pairs:
            cells |= pair_cells(a, b, n)
        if len(cells) != 2 * length:
            continue
        if loops:
            used = {c for (a, b) in pairs for c in (a, m - a, b, m - b)}
            free = [c for c in classes if c not in used]
            if len(free) < 2:
                continue
            d, e = rng.sample(free, 2)
            pairs = pairs + [(d, d), (e, m - e)]
            cells |= pair_cells(d, d, n) | pair_cells(e, m - e, n)
            if len(cells) != 2 * length + 4:
                continue
        key = canon(cells, n)
        if key in seen:
            continue
        seen.add(key)
        out.append(";".join(f"{a},{b}" for a, b in pairs))
    return out


def main():
    n = int(sys.argv[1]); loops = "--loops" in sys.argv
    if "--sample" in sys.argv:
        import random
        k = int(sys.argv[sys.argv.index("--sample") + 1])
        length = int(sys.argv[sys.argv.index("--len") + 1]) if "--len" in sys.argv else 5
        seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 1
        for s_ in sample_cycles(n, length, k, random.Random(seed), loops):
            print(s_)
        return
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
