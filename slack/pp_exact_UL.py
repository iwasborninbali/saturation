"""pp_exact_UL.py — exact U/p and L/p (lift-accounting formula, §1 of perm_poly_theorem_notes.md) for the box lift of f(x)=x^k in box (x0,y0),
computed in O(p) from root buckets (no line enumeration).  usage: pp_exact_UL.py p k [x0 y0]"""
import sys
p = int(sys.argv[1]); k = int(sys.argv[2]); x0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0; y0 = int(sys.argv[4]) if len(sys.argv) > 4 else 0
assert (p - 1) % k != 0
def pos(t): return (t - x0) % p           # r_t - x0 in [0,p)
buck = {+1: {}, -1: {}}
f = [pow(t, k, p) for t in range(p)]
for t in range(p):
    buck[+1].setdefault((f[t] - t) % p, []).append(t)
    buck[-1].setdefault((f[t] + t) % p, []).append(t)
# class of root t in residue c on slope σ: slope +: class0 iff s_t - r_t = c' (smaller) iff v_t < u_t iff pos(t) + gpos >= p, gpos = (c - y0 + x0) mod p
#                                          slope -: class0 iff u_t + v_t < 1 iff pos(t) <= gpos', gpos' = (c - x0 - y0) mod p
def classes(sig, c, roots):
    if sig > 0:
        gp = (c - y0 + x0) % p
        return [1 if pos(t) + gp < p else 0 for t in roots]      # 1 = class 1 (u < 1-g), 0 = class 0
    else:
        gp = (c - x0 - y0) % p
        return [0 if pos(t) <= gp else 1 for t in roots]
info = {+1: {}, -1: {}}   # per residue x: (k, n_x)  where n_x = #roots in x's class
L = 0
for sig in (+1, -1):
    for c, roots in buck[sig].items():
        kk = len(roots); cl = classes(sig, c, roots)
        n0 = cl.count(0); n1 = kk - n0
        L += (n0 >= 4) + (kk + n0 >= 4) + (kk + n1 >= 4) + (n1 >= 4)
        for t, cc in zip(roots, cl):
            info[sig][t] = (kk, n0 if cc == 0 else n1)
U = 0
for x in range(p):
    kp, npl = info[+1][x]; km, nmi = info[-1][x]
    U += (kp + npl <= 3) * ((nmi <= 3) + (2 * km - nmi <= 3)) + (km + nmi <= 3) * ((npl <= 3) + (2 * kp - npl <= 3))
print(f"p={p} k={k} box=({x0},{y0}): L/p={L/p:.5f} U/p={U/p:.5f} cost/p={(2*L+U)/p:.5f} = {(2*L+U)/(2*p):.5f} N")
