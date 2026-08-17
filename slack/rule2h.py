"""rule2h.py — candidate explicit construction from the p=13 witness: two hyperbolas H(1,p), H(2,p) in the HJSW window;
each residue class keeps a horizontal pair (x, x+p) on one row: side = right if xm <= (p-1)/2 else left; row band
b = ym mod 2 for c=1, 1 - (ym mod 2) for c=2.  Reports |R|, collinear triples, and greedy/exact lawful subset size."""
import sys, os, subprocess, tempfile
from itertools import combinations
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import saturation as S

def rule(p, cs=(1, 2), band=None):
    h = (p - 1) // 2; N = 2 * p; pts = set()
    for c in cs:
        for xm in range(1, p):
            ym = (c * pow(xm, -1, p)) % p
            b = (ym % 2) if c == cs[0] else 1 - (ym % 2)
            if band: b = band(c, xm, ym)
            y = ym + p * b
            xs_pair = (xm, xm + p) if xm <= h else (xm - p, xm)      # HJSW window coordinate xs in [-(p-1)/2, (3p-1)/2]
            for xs in xs_pair:
                x = xs + h                                            # grid coordinate 0..2p-1
                assert 0 <= x < N and 0 <= y < N, (p, c, xm, ym, xs, y)
                pts.add((x, y))
    return pts

def collinear_triples(pts):
    L = sorted(pts); bad = []
    for a, b, c in combinations(L, 3):
        if (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]) == 0: bad.append((a, b, c))
    return bad

def greedy_repair(pts):
    pts = set(pts)
    while True:
        bad = collinear_triples(pts)
        if not bad: return pts
        cnt = {}
        for t in bad:
            for q in t: cnt[q] = cnt.get(q, 0) + 1
        worst = max(cnt, key=cnt.get); pts.discard(worst)

if __name__ == "__main__":
    for p in [int(a) for a in sys.argv[1:]] or [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        R = rule(p); N = 2 * p
        bad = collinear_triples(R)
        rep = greedy_repair(R)
        print(f"p={p:3d} N={N:3d} |R|={len(R):4d} ({len(R)/N:.3f} N)  collinear triples={len(bad):4d}  greedy lawful={len(rep):4d} ({len(rep)/N:.3f} N)   HJSW={3*(p-1)} ({3*(p-1)/N:.3f})", flush=True)
