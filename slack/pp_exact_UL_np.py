"""pp_exact_UL_np.py — vectorized exact U/p, L/p for the box lift of x^k (lift-accounting formula), O(p) with numpy.  usage: p k [x0 y0]"""
import sys, numpy as np
p = int(sys.argv[1]); k = int(sys.argv[2]); x0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0; y0 = int(sys.argv[4]) if len(sys.argv) > 4 else 0
assert (p - 1) % k != 0
t = np.arange(p, dtype=np.int64)
f = t.copy()
for _ in range(k - 1): f = (f * t) % p          # t^k mod p (k small)
pos = (t - x0) % p
res = {}
for sig in (+1, -1):
    c = (f - sig * t) % p
    kc = np.bincount(c, minlength=p)              # roots per residue
    kk = kc[c]                                    # k of x's residue
    if sig > 0:
        gp = (c - y0 + x0) % p
        cl = (pos + gp >= p).astype(np.int64) ^ 1  # class 1 iff pos+gp < p ; class 0 iff pos+gp >= p  -> cl = 1 if pos+gp<p
        cl = (pos + gp < p).astype(np.int64)
    else:
        gp = (c - x0 - y0) % p
        cl = (pos > gp).astype(np.int64)          # class 0 iff pos <= gp
    key = 2 * c + cl
    cnt2 = np.bincount(key, minlength=2 * p)
    n_x = cnt2[key]                               # roots in x's class (incl x)
    n0 = cnt2[0::2]; n1 = cnt2[1::2]              # per residue c
    L = int(((n0 >= 4).astype(np.int64) + (kc + n0 >= 4) + (kc + n1 >= 4) + (n1 >= 4))[kc > 0].sum())
    res[sig] = (kk, n_x, L)
kp, npl, Lp = res[+1]; km, nmi, Lm = res[-1]
U = int((((kp + npl) <= 3) * (((nmi <= 3).astype(np.int64)) + ((2 * km - nmi) <= 3)) + ((km + nmi) <= 3) * (((npl <= 3).astype(np.int64)) + ((2 * kp - npl) <= 3))).sum())
L = Lp + Lm
print(f"p={p} k={k} box=({x0},{y0}): L/p={L/p:.5f} U/p={U/p:.5f} cost/p={(2*L+U)/p:.5f} = {(2*L+U)/(2*p):.5f} N", flush=True)
