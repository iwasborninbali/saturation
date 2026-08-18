"""block_cover2.py — k=-1: LP(1) (rows, columns, ±1 lines, single points; line cost 2, point cost 1) versus forced-block covers.
A residue group = all slope-±1 lines with x-y ≡ c (resp. x+y ≡ c) mod p; a block = the group's lines all taken (cost 2 per non-empty line).
Forcing rule: take (greedily, disjoint in points) every group whose largest line has ≥ t points, for t = 8, 7, 6, 5; cover the rest by LP.
Also reports the anatomy of the LP(1) optimum: weight mass on ±1 lines by (group max size), on rows/cols, on points.
usage: python3 slack/block_cover2.py p [p2 ...]"""
import sys
import numpy as np
from scipy.optimize import linprog
from collections import defaultdict
def setup(p):
    h = (p - 1) // 2
    pts = [(x, y) for x in range(-h, 3 * h + 2) for y in range(0, 2 * p) if (x * y) % p in (1, p - 1)]
    idx = {q: i for i, q in enumerate(pts)}; n = len(pts)
    dia = defaultdict(list); ant = defaultdict(list); rows = defaultdict(list); cols = defaultdict(list)
    for (x, y) in pts:
        dia[x - y].append(idx[(x, y)]); ant[x + y].append(idx[(x, y)]); rows[y].append(idx[(x, y)]); cols[x].append(idx[(x, y)])
    return pts, n, dia, ant, rows, cols
def lp_cover(n, lines, rest):
    """min sum 2 y_l + sum z_q covering the points in rest; returns (value, y, z)"""
    m = len(lines); pos = {q: r for r, q in enumerate(rest)}
    A = np.zeros((len(rest), m + len(rest)))
    for li, mem in enumerate(lines):
        for q in mem:
            if q in pos: A[pos[q], li] = 1
    for r in range(len(rest)): A[r, m + r] = 1
    c = np.concatenate([2 * np.ones(m), np.ones(len(rest))])
    res = linprog(c, A_ub=-A, b_ub=-np.ones(len(rest)), bounds=[(0, None)] * (m + len(rest)), method='highs')
    return res.fun, res.x[:m], res.x[m:]
def run(p):
    pts, n, dia, ant, rows, cols = setup(p)
    lines = []; tags = []
    for name, fam in (('row', rows), ('col', cols), ('dia', dia), ('ant', ant)):
        for c, mem in fam.items():
            lines.append(mem); tags.append((name, c))
    val, y, z = lp_cover(n, lines, list(range(n)))
    # anatomy of LP(1): group max size for ±1 lines
    gmax = {}
    for name, fam in (('dia', dia), ('ant', ant)):
        byres = defaultdict(list)
        for c, mem in fam.items(): byres[c % p].append(len(mem))
        for c in fam: gmax[(name, c)] = max(byres[c % p])
    mass = defaultdict(float)
    for li, (name, c) in enumerate(tags):
        if y[li] > 1e-9:
            key = name if name in ('row', 'col') else f"{name}:gmax{gmax[(name,c)]}:len{len(lines[li])}"
            mass[key] += 2 * y[li]
    mass['points'] = float(z.sum())
    out = [f"p={p}: LP(1) = {val:.2f} = {val/(p-1):.3f}(p-1); 4(p-1) = {4*(p-1)}"]
    out.append("  LP(1) cost by piece: " + ", ".join(f"{k}={v:.1f}" for k, v in sorted(mass.items(), key=lambda kv: -kv[1])))
    for t in (8, 7, 6, 5):
        covered = np.zeros(n, bool); blocks = 0; cost = 0; sizes = defaultdict(int)
        for name, fam in (('dia', dia), ('ant', ant)):
            byres = defaultdict(list)
            for c, mem in fam.items(): byres[c % p].append(c)
            for r, cs in byres.items():
                mx = max(len(fam[c]) for c in cs)
                if mx < t: continue
                grp = [q for c in cs for q in fam[c]]
                if any(covered[q] for q in grp): continue
                for q in grp: covered[q] = True
                nl = sum(1 for c in cs if fam[c]); blocks += 1; cost += 2 * nl; sizes[(mx, len(grp), nl)] += 1
        rest = [q for q in range(n) if not covered[q]]
        rv, _, _ = lp_cover(n, lines, rest) if rest else (0.0, None, None)
        out.append(f"  force groups with max line >= {t}: {blocks} blocks (types (max,pts,lines):count {dict(sizes)}) cost {cost}, rest {len(rest)} pts at {rv:.2f} "
                   f"({rv/max(1,len(rest)):.3f}/pt) -> total {cost+rv:.2f} = {(cost+rv)/(p-1):.3f}(p-1)  [{'=' if abs(cost+rv-val)<1e-6 else '>'} LP(1)]")
    return "\n".join(out)
for a in sys.argv[1:]:
    print(run(int(a)), flush=True)
