"""defects3.py — all directed 3-cycle orbit defects for odd n, INCLUDING the central row/column class, one representative per
D4-orbit (as cell sets).  Output: PAIRS strings "a,b;c,d;e,f" (each pair {(a,b),(m-a,m-b)}); a trailing comment gives counts.
An arc from class X to class Y is a half-turn pair {(a,b),(m-a,m-b)} with a in X, b in Y; a 3-cycle X->Y->Z->X uses three
distinct classes among {0..h-1} and the central class {h} (n=2h+1); the balance lemma allows the central class (only the
central cell (h,h) is excluded, and it never occurs in a 3-cycle).
    python3 bench/defects3.py N [--central-only|--noncentral-only]
"""
import sys, itertools

def motions(n):
    m = n - 1
    return [lambda u, v: (u, v), lambda u, v: (v, m - u), lambda u, v: (m - u, m - v), lambda u, v: (m - v, u),
            lambda u, v: (v, u), lambda u, v: (m - u, v), lambda u, v: (u, m - v), lambda u, v: (m - v, m - u)]

def canon(cells, n):
    return min(tuple(sorted(f(u, v) for (u, v) in cells)) for f in motions(n))

def pair_cells(a, b, n):
    m = n - 1
    return {(a, b), (m - a, m - b)}

def main():
    n = int(sys.argv[1]); m = n - 1; h = m // 2
    mode = sys.argv[2] if len(sys.argv) > 2 else ""
    classes = list(range(h + 1))                      # h = central class
    reps = {c: ([c, m - c] if c != h else [h]) for c in classes}
    seen = {}; out = []
    for X, Y, Z in itertools.permutations(classes, 3):  # ordered = directed cycle X->Y->Z->X (cyclic rotations give same set)
        for a1 in reps[X]:
            for b1 in reps[Y]:
                for b2 in reps[Z]:
                    for a3 in reps[X]:
                        # arcs: X->Y as (a1,b1); Y->Z as (y2, b2) with y2 in reps[Y]; Z->X as (z3, a3) with z3 in reps[Z]
                        for y2 in reps[Y]:
                            for z3 in reps[Z]:
                                pairs = [(a1, b1), (y2, b2), (z3, a3)]
                                cells = set()
                                for (a, b) in pairs:
                                    cells |= pair_cells(a, b, n)
                                if len(cells) != 6:
                                    continue
                                key = canon(cells, n)
                                if key in seen:
                                    continue
                                central = (h in (X, Y, Z))
                                if mode == "--central-only" and not central: 
                                    seen[key] = None; continue
                                if mode == "--noncentral-only" and central:
                                    seen[key] = None; continue
                                seen[key] = pairs
                                out.append((central, ";".join(f"{a},{b}" for a, b in pairs)))
    for c, s in out:
        print(s)
    nc = sum(1 for c, _ in out if c); nn = len(out) - nc
    from math import comb
    print(f"# n={n}: {len(out)} defect sets mod D4 (central class: {nc}, expected C(h,2)={comb(h,2)}; others: {nn}, expected 4*C(h,3)={4*comb(h,3)})", file=sys.stderr)

if __name__ == "__main__":
    main()
