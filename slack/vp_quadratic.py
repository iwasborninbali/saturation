"""vp_quadratic.py — k=-1 vertical-pair model: T(eps) = E + eps^T C eps (odd degrees vanish by the symmetry R'); compute E, the matrix C,
lambda_min(C), the spectral lower bound E + (p-1) lambda_min, and (p<=19) the true min.  usage: python3 slack/vp_quadratic.py p [p2 ...]"""
import sys, itertools
import numpy as np
from collections import defaultdict
def analyse(p, brute=False):
    h = (p - 1) // 2
    def X(u): u %= p; return u if u <= h else u - p
    def Y(u): u %= p; return u if u else p
    classes = [(hyp, a) for a in range(1, p) for hyp in (1, -1)]
    base = {}
    for hyp, a in classes:
        ia = pow(a, -1, p); base[(hyp, a)] = (X(a), Y(ia if hyp == 1 else -ia))
    def col(cls, ra):
        hyp, a = cls; return base[cls][0] + (ra if hyp == 1 else 1 - ra) * p
    coef = defaultdict(float)
    for c1, c2, c3 in itertools.combinations(classes, 3):
        avars = sorted({c1[1], c2[1], c3[1]})
        for bits in itertools.product((0, 1), repeat=len(avars)):
            rmap = dict(zip(avars, bits))
            xs = [col(c, rmap[c[1]]) for c in (c1, c2, c3)]
            if len(set(xs)) < 3: continue
            for s in itertools.product((0, 1), repeat=3):
                (x1, y1), (x2, y2), (x3, y3) = [(xs[i], base[(c1, c2, c3)[i]][1] + s[i] * p) for i in range(3)]
                if (x2 - x1) * (y3 - y1) == (x3 - x1) * (y2 - y1):
                    items = list(rmap.items()); n = len(items)
                    for mask in range(1 << n):
                        mono = tuple(sorted(items[i][0] for i in range(n) if mask >> i & 1)); sign = 1
                        for i in range(n):
                            if mask >> i & 1 and items[i][1] == 1: sign = -sign
                        coef[mono] += sign / (1 << n)
    E = coef.get((), 0.0); n = p - 1; idx = {a: a - 1 for a in range(1, p)}
    C = np.zeros((n, n))
    for m, v in coef.items():
        if len(m) == 2: C[idx[m[0]], idx[m[1]]] += v / 2; C[idx[m[1]], idx[m[0]]] += v / 2
        elif len(m) in (1, 3) and abs(v) > 1e-9: print("  odd-degree term!", m, v)
    lam = np.linalg.eigvalsh(C); lmin = lam[0]
    out = f"p={p}: E={E:.1f} ({E/n:.3f}(p-1)); lambda_min(C)={lmin:.3f}, spectral bound E+(p-1)lambda_min = {E + n*lmin:.1f} ({(E+n*lmin)/n:.3f}(p-1)); nnz(C)={int((np.abs(C)>1e-9).sum()//2)}"
    if brute:
        best = None
        for r in range(1 << n):
            eps = np.array([1 if (r >> i) & 1 == 0 else -1 for i in range(n)], float)
            T = E + eps @ C @ eps
            if best is None or T < best: best = T
        out += f"; true min {best:.1f}"
    return out
for a in sys.argv[1:]:
    p = int(a); print(analyse(p, brute=(p <= 19)), flush=True)
