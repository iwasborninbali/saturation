"""runs_chain.py — the type chain along a run of consecutive quadratic residues (k=-1, §30 of pair_bound_notes).
KEY REDUCTION.  A vertex t (edge of the neighbour graph joins t,t+1 when both are QR) carries the H(1)-pair {a,1/a} with
    a = u_t + u_{t+1},  1/a = u_{t+1} - u_t,   u_s := a square root of s   (indeed a*(1/a) = u_{t+1}^2 - u_t^2 = 1),
and the pair is SHARED iff X(a)X(1/a) < 0 (X = centred representative).  So the chain of "shared" bits along a run is
    xi_i = [ X(u_i + u_{i+1}) * X(u_{i+1} - u_i) < 0 ],
invariant under the sign choices of the u's.  The vertex between edges i-1 and i is of type
    "8" (4,8,4) iff xi_{i-1} = 0 and xi_i = 1;  "6" (2,6,6,2) iff xi_{i-1} = 1 and xi_i = 0;  "7" otherwise.
MODEL: positions v_i = X(u_i)/p are i.i.d. uniform on (-1/2,1/2)  (Weil on the curve u_{i+1}^2 = u_i^2 + 1, as in prop m8asym).
This script (a) computes the model's laws by Monte-Carlo/quadrature and (b) checks them against real p.
usage: runs_chain.py model [samples]   |   runs_chain.py real p [p ...]"""
import sys, random
import numpy as np

def model(N=4_000_000, seed=1):
    rng = np.random.default_rng(seed)
    v = rng.random(N + 4) - 0.5
    def c(x):  # centred representative of x mod 1
        return (x + 0.5) % 1.0 - 0.5
    xi = ((c(v[:-1] + v[1:]) * c(v[1:] - v[:-1])) < 0).astype(np.int8)
    P1 = xi.mean()
    a, b = xi[:-1], xi[1:]
    p00 = ((a == 0) & (b == 0)).mean(); p01 = ((a == 0) & (b == 1)).mean()
    p10 = ((a == 1) & (b == 0)).mean(); p11 = ((a == 1) & (b == 1)).mean()
    print(f"MODEL (N={N}): P(xi=1) = {P1:.5f} (expect 1/2)")
    print(f"  pair law: P(00)={p00:.5f} P(01)={p01:.5f} P(10)={p10:.5f} P(11)={p11:.5f}")
    print(f"  vertex types: 8 = P(0,1) = {p01:.5f} (expect 1/3), 6 = P(1,0) = {p10:.5f} (expect 1/3), 7 = {p00+p11:.5f} (expect 1/3)")
    # triples (two consecutive vertices)
    trip = {}
    A, B, C = xi[:-2], xi[1:-1], xi[2:]
    for x in (0, 1):
        for y in (0, 1):
            for z in (0, 1):
                trip[(x, y, z)] = ((A == x) & (B == y) & (C == z)).mean()
    print("  triple law:", {k: round(v_, 5) for k, v_ in trip.items()})
    typ = lambda l, r: '8' if (l == 0 and r == 1) else ('6' if (l == 1 and r == 0) else '7')
    tt = {}
    for k_, v_ in trip.items():
        key = typ(k_[0], k_[1]) + typ(k_[1], k_[2])
        tt[key] = tt.get(key, 0) + v_
    print("  two-vertex type law:", {k: round(x, 5) for k, x in sorted(tt.items())})

def real(p):
    sq = np.zeros(p, dtype=bool); root = np.zeros(p, dtype=np.int64)
    for r in range(p):
        s = r * r % p
        if not sq[s]: sq[s] = True; root[s] = r
    isqr = sq.copy(); isqr[0] = False
    h = (p - 1) // 2
    X = lambda u: u - p if u > h else u
    # runs of consecutive QRs among t = 1..p-1 (t and t+1 both QR -> edge)
    xis = []; types = []
    t = 1
    runs = 0; lens = {}
    while t < p - 1:
        if not isqr[t]: t += 1; continue
        j = t
        while j + 1 < p and isqr[(j + 1) % p]: j += 1
        L = j - t + 1
        if L >= 2:
            runs += 1; lens[L] = lens.get(L, 0) + 1
            u = [int(root[s]) for s in range(t, j + 1)]
            chain = []
            for i in range(L - 1):
                a = (u[i] + u[i + 1]) % p; b = (u[i + 1] - u[i]) % p
                chain.append(1 if X(a) * X(b) < 0 else 0)
            xis.append(chain)
            for i in range(1, len(chain)):
                l, r = chain[i - 1], chain[i]
                types.append('8' if (l == 0 and r == 1) else ('6' if (l == 1 and r == 0) else '7'))
        t = j + 1
    flat = [x for c in xis for x in c]
    n1 = sum(flat); tot = len(flat)
    from collections import Counter
    ct = Counter(types); nt = sum(ct.values())
    pairs = Counter()
    for c in xis:
        for i in range(len(c) - 1): pairs[(c[i], c[i + 1])] += 1
    np_ = sum(pairs.values())
    print(f"p={p}: runs>=2: {runs}, edges: {tot}, P(xi=1)={n1/max(tot,1):.4f}; "
          f"pair law: " + " ".join(f"{k}:{v/max(np_,1):.4f}" for k, v in sorted(pairs.items())) +
          f"; types: " + " ".join(f"{k}:{v/max(nt,1):.4f}" for k, v in sorted(ct.items())) +
          f"; run lengths: {dict(sorted(lens.items()))}", flush=True)

if __name__ == '__main__':
    if sys.argv[1] == 'model':
        model(int(sys.argv[2]) if len(sys.argv) > 2 else 4_000_000)
    else:
        for p in map(int, sys.argv[2:]): real(p)
