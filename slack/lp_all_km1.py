"""lp_all_km1.py — the ceiling of ALL rank-1 (cover) certificates for P_{-1} = (H(1) ∪ H(-1)) ∩ box:
LP over EVERY line with >= 3 points (not just rows/columns/±1), value = max fractional lawful set = min cover.
Compares with LP(1) (rows/columns/±1 lines only) and the trivial 4(p-1).  usage: lp_all_km1.py p [p ...]"""
import sys, time
sys.path.insert(0, 'slack')
from lp_curve import lines, solve
from sdp_lawful import points_pm1
for p in map(int, sys.argv[1:]):
    t0 = time.time()
    pts = points_pm1(p); n = len(pts)
    L_all = lines(pts, 'all'); L_pm1 = lines(pts, 'pm1')
    v_all = solve(pts, L_all); v_pm1 = solve(pts, L_pm1)
    print(f"p={p:4d}: n={n:5d} lines(all>=3)={len(L_all):6d} lines(pm1>=3)={len(L_pm1):5d}  "
          f"LP(all)={v_all:8.2f} = {v_all/(p-1):.4f}(p-1)   LP(1)={v_pm1:8.2f} = {v_pm1/(p-1):.4f}(p-1)  [{time.time()-t0:.0f}s]", flush=True)
