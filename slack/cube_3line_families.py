"""cube_3line_families.py — 3-point lines of the permutation-cubic lift by 'span' J (number of primitive steps between the extreme points):
per J: #lines, #good (all three points W4-uncovered), max/avg degree of points in the good lines with span ≤ J0, greedy matching restricted to span ≤ J0,
and the rigorous greedy bound |good|/(3Δ−2).  usage: cube_3line_families.py p [x0 y0]"""
import sys, math
sys.path.insert(0, 'slack')
from lp_curve import curve_points, lines
p = int(sys.argv[1]); x0 = int(sys.argv[2]) if len(sys.argv) > 2 else 0; y0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0
pts = curve_points(p, 'cube', x0, y0); n = len(pts)
allL = lines(pts, 'all')
def is_pm1(s):
    (a, b), (c, d) = pts[s[0]], pts[s[1]]; dx, dy = c - a, d - b
    return dx == 0 or dy == 0 or abs(dx) == abs(dy)
rich = [s for s in allL if is_pm1(s) and len(s) >= 4]
S0 = set(range(n)) - set(i for s in rich for i in s)
three = [s for s in allL if not is_pm1(s) and len(s) == 3]
def span(s):
    P = sorted((pts[i] for i in s))
    (a, b), (c, d) = P[0], P[-1]; dx, dy = c - a, d - b
    return math.gcd(abs(dx), abs(dy))
byJ = {}
for s in three:
    J = span(s); byJ.setdefault(J, []).append(s)
print(f"p={p} box=({x0},{y0}): |S0|={len(S0)}, 3-lines={len(three)}; W4 cost={2*len(rich)+len(S0)} = {(2*len(rich)+len(S0))/(2*p):.4f} N")
print(" J   lines  lines/p  good  good/lines  cum_good/p")
cum = 0
for J in sorted(byJ)[:14]:
    L = byJ[J]; g = [s for s in L if all(i in S0 for i in s)]; cum += len(g)
    print(f"{J:3d} {len(L):6d} {len(L)/p:8.3f} {len(g):5d} {len(g)/max(1,len(L)):10.3f} {cum/p:10.3f}")
for J0 in (2, 3, 4, 6, 8, 12, 10**9):
    good = [s for J, L in byJ.items() if J <= J0 for s in L if all(i in S0 for i in s)]
    deg = {}
    for s in good:
        for i in s: deg[i] = deg.get(i, 0) + 1
    Dmax = max(deg.values()) if deg else 0; Davg = sum(deg.values()) / max(1, len(deg))
    # greedy matching (low-degree first)
    used = set(); m = 0
    for s in sorted(good, key=lambda s: sum(deg[i] for i in s)):
        if all(i not in used for i in s): used.update(s); m += 1
    bound = len(good) / (3 * Dmax - 2) if Dmax else 0
    print(f"J<= {J0 if J0<10**9 else 'all':>4}: good={len(good):5d} ({len(good)/p:.3f}p) Dmax={Dmax:3d} Davg={Davg:.2f} greedy matching={m:4d} ({m/p:.3f}p) rigorous |good|/(3Dmax-2)={bound/p:.4f}p  -> cost {(2*len(rich)+len(S0)-m)/(2*p):.4f} N (greedy)")

# --- second-moment bound: matching >= |good| - #intersecting pairs (pairs sharing >=1 point), for span <= J0
print("second-moment bound (span<=J0): |good| - #pairs sharing a point")
for J0 in (3, 4, 5, 6, 8):
    good = [s for J, L in byJ.items() if J <= J0 for s in L if all(i in S0 for i in s)]
    inc = {}
    for k, s in enumerate(good):
        for i in s: inc.setdefault(i, []).append(k)
    pairs = set()
    for i, ks in inc.items():
        for a in range(len(ks)):
            for b in range(a + 1, len(ks)): pairs.add((ks[a], ks[b]))
    lb = len(good) - len(pairs)
    print(f"  J<={J0}: good={len(good)} ({len(good)/p:.3f}p) pairs={len(pairs)} ({len(pairs)/p:.3f}p) -> matching >= {lb} ({lb/p:.3f}p) -> cost <= {(2*len(rich)+len(S0)-lb)/(2*p):.4f} N  [4/3 needs matching >= {(2*len(rich)+len(S0)-8*p/3)/p:.3f}p]")
