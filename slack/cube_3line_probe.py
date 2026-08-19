"""cube_3line_probe.py — after the ±1 cover W4 (weight 1 on rich ±1-lines), how much can 3-point lines of other slopes save?
For y=x^3 (p≡2 mod 3), box (x0,y0): uncovered set S0 = points on no rich ±1 line; 3-lines with all 3 points in S0 ('good'), with exactly 2 in S0;
greedy matching among good lines (each saves 1); LP over rich ±1 lines + good 3-lines + singletons; LP over everything (reference).
usage: cube_3line_probe.py p [x0 y0]"""
import sys, math, numpy as np
sys.path.insert(0, 'slack')
from lp_curve import curve_points, lines
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
p = int(sys.argv[1]); x0 = int(sys.argv[2]) if len(sys.argv) > 2 else 0; y0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0
pts = curve_points(p, 'cube', x0, y0); n = len(pts); N = 2 * p
def slope_of(s):
    (a, b), (c, d) = pts[s[0]], pts[s[1]]
    dx, dy = c - a, d - b
    return 'pm1' if (dx == 0 or dy == 0 or abs(dx) == abs(dy)) else 'other'
allL = lines(pts, 'all')
rich = [s for s in allL if slope_of(s) == 'pm1' and len(s) >= 4]
covered = set(i for s in rich for i in s)
S0 = set(range(n)) - covered
three = [s for s in allL if slope_of(s) == 'other']
good = [s for s in three if all(i in S0 for i in s)]
two = [s for s in three if sum(i in S0 for i in s) == 2]
costW4 = 2 * len(rich) + len(S0)
# greedy matching among good lines (prefer lines through low-degree points)
deg = {}
for s in good:
    for i in s: deg[i] = deg.get(i, 0) + 1
order = sorted(good, key=lambda s: sum(deg[i] for i in s))
used = set(); matched = 0
for s in order:
    if all(i not in used for i in s):
        used.update(s); matched += 1
def solve(lines_list, point_set):
    idx = {P: k for k, P in enumerate(sorted(point_set))}; m = len(lines_list); nn = len(idx)
    A = lil_matrix((nn, m + nn))
    for k, s in enumerate(lines_list):
        for i in s:
            if i in idx: A[idx[i], k] = 1
    for i in range(nn): A[i, m + i] = 1
    c = np.concatenate([2 * np.ones(m), np.ones(nn)])
    res = linprog(c, A_ub=-A.tocsr(), b_ub=-np.ones(nn), bounds=(0, None), method='highs')
    return res.fun
lp_good = solve([s for s in good], S0)                       # cover S0 by good 3-lines + singletons
lp_all3 = solve([[i for i in s if i in S0] for s in three if sum(i in S0 for i in s) >= 2], S0)  # allow 3-lines with ≥2 uncovered pts (cost 2 each)
lp_full = solve(allL, set(range(n)))
print(f"p={p} box=({x0},{y0}) N={N}: |S0|={len(S0)} ({len(S0)/n:.3f} of {n}); 3-lines: {len(three)} (avg deg {3*len(three)/n:.1f}); good(3 in S0)={len(good)} "
      f"({len(good)/p:.2f}p), 2-in-S0={len(two)}")
print(f"  W4 cost={costW4} = {costW4/N:.4f} N; greedy matching on good lines: {matched} lines -> cost {costW4-matched} = {(costW4-matched)/N:.4f} N (saving {matched/p:.3f} p)")
print(f"  LP(S0 by good 3-lines+singletons): {lp_good:.1f} -> total {2*len(rich)+lp_good:.1f} = {(2*len(rich)+lp_good)/N:.4f} N")
print(f"  LP(S0 by 3-lines with >=2 pts in S0, cost 2 each): total {2*len(rich)+lp_all3:.1f} = {(2*len(rich)+lp_all3)/N:.4f} N")
print(f"  LP(all lines, reference): {lp_full:.1f} = {lp_full/N:.4f} N", flush=True)
