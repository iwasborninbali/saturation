"""cube_matching_fast.py — fast (O(p)) enumeration of 3-point lines of small span for the lift of y=x^3 (p≡2 mod 3), box (x0,y0),
via the family parametrisation: steps 0<i<j (gcd 1), base residue x ≡ −(i+j)u/3, points x, x+iu, x+ju, integer direction (u*,v*) ≡ (u,v),
v ≡ (f(x+iu)−f(x))/i.  W4-uncovered set from the lift-accounting lemma.  Reports per span: lines, good lines, and for span ≤ J0 the matching bounds
(greedy; |good|−#pairs; Caro–Wei Σ_e 1/(1+n_e)).   usage: cube_matching_fast.py p J0 [x0 y0]"""
import sys, math
from math import gcd
import numpy as np
p = int(sys.argv[1]); J0 = int(sys.argv[2]); x0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0; y0 = int(sys.argv[4]) if len(sys.argv) > 4 else 0
assert p % 3 == 2
inv3 = pow(3, -1, p)
t = np.arange(p, dtype=np.int64); f = (t * t % p) * t % p
pos = (t - x0) % p                                # r_t - x0
# --- ±1 structure: k, class, n for each residue on both slopes
def slope_data(sig):
    c = (f - sig * t) % p
    kc = np.bincount(c, minlength=p); kk = kc[c]
    if sig > 0:
        gp = (c - y0 + x0) % p; cl = (pos + gp < p).astype(np.int64)     # class 1 iff pos+gp<p (class 0 iff pos >= 1-g)
    else:
        gp = (c - x0 - y0) % p; cl = (pos > gp).astype(np.int64)         # class 0 iff pos <= gp
    key = 2 * c + cl; cnt2 = np.bincount(key, minlength=2 * p); n_x = cnt2[key]
    return kk, cl, n_x
kp, ap, npl = slope_data(+1); km, bm, nmi = slope_data(-1)
# covered lifts: sizes through the four lifts (δ,ε) of x
def covered_table():
    cov = np.zeros((p, 2, 2), dtype=bool)
    # slope +
    eq = kp + npl                                  # (0,0),(1,1)
    s01 = np.where(ap == 0, 2 * kp - npl, npl)     # (0,1)
    s10 = np.where(ap == 0, npl, 2 * kp - npl)     # (1,0)
    # slope -
    m00 = np.where(bm == 0, nmi, 2 * km - nmi); m11 = np.where(bm == 0, 2 * km - nmi, nmi); mmix = km + nmi
    cov[:, 0, 0] = (eq >= 4) | (m00 >= 4); cov[:, 1, 1] = (eq >= 4) | (m11 >= 4)
    cov[:, 0, 1] = (s01 >= 4) | (mmix >= 4); cov[:, 1, 0] = (s10 >= 4) | (mmix >= 4)
    return cov
cov = covered_table()
nunc = int((~cov).sum()); Lrich = None
# lifts: X = r_x + δp with r_x = x0 + pos, Y = s_x + εp with s_x = y0 + ((f - y0) % p)
rx = x0 + pos; sx = y0 + (f - y0) % p
def lift_index(X, Y):
    """return (residue x, δ, ε) if (X,Y) is a lattice point of the lift, else None"""
    x = X % p
    d = (X - rx[x]); e = (Y - sx[x])
    if d % p or e % p: return None
    d //= p; e //= p
    if d not in (0, 1) or e not in (0, 1): return None
    if (Y - sx[x]) % p: return None
    return (x, d, e)
def is_pm1(u, v): return u == 0 or v == 0 or abs(u) == abs(v)
lines_by_span = {}
fam = {}
seen = set()
steps = [(i, j) for j in range(2, J0 + 1) for i in range(1, j) if gcd(i, j) == 1]
for (i, j) in steps:
    ij_inv3 = (-(i + j) * inv3) % p
    ii = pow(i, -1, p)
    for u in range(1, p):
        x1 = ij_inv3 * u % p; x2 = (x1 + i * u) % p; x3 = (x1 + j * u) % p
        v = (f[x2] - f[x1]) * ii % p
        # consistency (family formula): (f[x3]-f[x1]) ≡ j v
        # if (f[x3] - f[x1] - j * v) % p: continue   # should not happen (x1+x2+x3≡0)
        for d0 in (0, 1):
            for e0 in (0, 1):
                X = rx[x1] + d0 * p; Y = sx[x1] + e0 * p
                # candidates u* with X + i u*, X + j u* in [x0, x0+2p)
                lo = math.ceil((x0 - X) / j) if j > 0 else None
                # u* ≡ u mod p; enumerate representatives in [ (x0-X)/j , (x0+2p-1-X)/i ] roughly; small ranges
                for us in range(u - 3 * p, u + 3 * p + 1, p):
                    if X + i * us < x0 or X + i * us >= x0 + 2 * p or X + j * us < x0 or X + j * us >= x0 + 2 * p: continue
                    for vs in range(v - 3 * p, v + 3 * p + 1, p):
                        if Y + i * vs < y0 or Y + i * vs >= y0 + 2 * p or Y + j * vs < y0 or Y + j * vs >= y0 + 2 * p: continue
                        if is_pm1(us, vs): continue
                        P2 = (X + i * us, Y + i * vs); P3 = (X + j * us, Y + j * vs)
                        # the points P2, P3 are automatically lattice points of the lift? their residues are x2,x3 and Y+i vs ≡ f(x2)? check
                        l2 = lift_index(*P2); l3 = lift_index(*P3)
                        if l2 is None or l3 is None: continue
                        key = tuple(sorted([(X, Y), P2, P3]))
                        if key in seen: continue
                        seen.add(key)
                        g = gcd(abs(P3[0] - key[0][0]) if False else abs(key[2][0] - key[0][0]), abs(key[2][1] - key[0][1]))
                        span = g
                        good = (not cov[x1, d0, e0]) and (not cov[l2[0], l2[1], l2[2]]) and (not cov[l3[0], l3[1], l3[2]])
                        lines_by_span.setdefault(span, []).append((key, good, j)); fam.setdefault((i, j), [0, 0]); fam[(i, j)][0] += 1; fam[(i, j)][1] += good
costW4 = None
# rich lines count L for cost: recompute L from residue profiles
def rich_count(sig):
    c = (f - sig * t) % p; kc = np.bincount(c, minlength=p)
    if sig > 0: gp = (c - y0 + x0) % p; cl = (pos + gp < p).astype(np.int64)
    else: gp = (c - x0 - y0) % p; cl = (pos > gp).astype(np.int64)
    key = 2 * c + cl; cnt2 = np.bincount(key, minlength=2 * p); n0 = cnt2[0::2]; n1 = cnt2[1::2]
    return int(((n0 >= 4).astype(np.int64) + (kc + n0 >= 4) + (kc + n1 >= 4) + (n1 >= 4))[kc > 0].sum())
L = rich_count(+1) + rich_count(-1); costW4 = 2 * L + nunc
print(f"p={p} box=({x0},{y0}) J0={J0}: uncovered={nunc} ({nunc/(4*p):.3f}), W4 cost={costW4} = {costW4/(2*p):.4f} N; 4/3 needs matching >= {(costW4-8*p/3)/p:.4f} p")
print("  per family (i,j): lines/p, good/p, good fraction")
for (i, j) in sorted(fam): print(f"    ({i},{j}): {fam[(i,j)][0]/p:.4f}p {fam[(i,j)][1]/p:.4f}p {fam[(i,j)][1]/max(1,fam[(i,j)][0]):.4f}")
tot = 0; totg = 0
for J in sorted(lines_by_span):
    L_ = lines_by_span[J]; g_ = sum(1 for _, gd, _j in L_ if gd); tot += len(L_); totg += g_
    print(f"  span {J:2d}: lines={len(L_):6d} ({len(L_)/p:.3f}p) good={g_:5d} ({g_/max(1,len(L_)):.3f})")
for Jc in sorted(set([3, 4, 5, 6, 8, J0])):
    good = [k for J, L_ in lines_by_span.items() for k, gd, jj in L_ if gd and 3 <= jj <= Jc]   # by FAMILY 3 <= j <= Jc (centre family (1,2) excluded)
    inc = {}
    for e, k in enumerate(good):
        for P in k: inc.setdefault(P, []).append(e)
    nbr = [set() for _ in good]
    for P, es in inc.items():
        for a in es:
            for b in es:
                if a != b: nbr[a].add(b)
    pairs = sum(len(s) for s in nbr) // 2
    cw = sum(1.0 / (1 + len(s)) for s in nbr)
    used = set(); m = 0
    for e in sorted(range(len(good)), key=lambda e: len(nbr[e])):
        if all(P not in used for P in good[e]): used.update(good[e]); m += 1
    print(f"  family j<={Jc}: good={len(good)} ({len(good)/p:.4f}p) pairs={pairs} ({pairs/p:.4f}p) |good|-pairs={(len(good)-pairs)/p:.4f}p  Caro-Wei={cw/p:.4f}p  greedy={m/p:.4f}p -> cost(greedy)={(costW4-m)/(2*p):.4f} N")
