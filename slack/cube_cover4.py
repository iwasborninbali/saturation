"""cube_cover4.py — explicit cover for permutation-cubic graphs y = a x^3 (p ≡ 2 mod 3): weight 1 on every slope-±1 line with ≥ 4 lifted
points + singletons elsewhere.  cost = 2·L4 + (#points on no such line) ≥ α.  Prints cost/N (N=2p) for several boxes; also LP(±1) for comparison.
usage: cube_cover4.py p [a] [nboxes]"""
import sys, random
sys.path.insert(0, 'slack')
from lp_curve import curve_points, lines
p = int(sys.argv[1]); a = int(sys.argv[2]) if len(sys.argv) > 2 else 1; nb = int(sys.argv[3]) if len(sys.argv) > 3 else 6
assert p % 3 == 2
curve = f"poly:{a},0,0,0"
rng = random.Random(p)
boxes = [(0, 0), (-(p - 1) // 2, 0), (-(p - 1) // 2, -(p - 1) // 2)] + [(rng.randrange(-p, p), rng.randrange(-p, p)) for _ in range(nb - 3)]
for (x0, y0) in boxes:
    pts = curve_points(p, curve, x0, y0); n = len(pts)
    ls = lines(pts, 'pm1')
    big = [s for s in ls if len(s) >= 4]
    covered = set(i for s in big for i in s)
    L4 = len(big); cost = 2 * L4 + (n - len(covered))
    sizes = {}
    for s in big: sizes[len(s)] = sizes.get(len(s), 0) + 1
    print(f"p={p} a={a} box=({x0},{y0}): L4={L4} sizes={dict(sorted(sizes.items()))} covered={len(covered)}/{n} cost={cost} = {cost/(2*p):.3f} N", flush=True)
