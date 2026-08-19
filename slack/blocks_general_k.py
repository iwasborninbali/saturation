"""blocks_general_k.py — why the block decomposition is special to k = ±1.
For P_k = (H(1) ∪ H(k)) ∩ box: a point of H(c) has r_-^2 - r_+^2 = 4xy = 4c, so with t := r_+^2/4 it joins the vertex t to t+c.
Hence the neighbour graph on the vertex set {t : t is a QR} has TWO step types: t~t+1 (from H(1)) and t~t+k (from H(k)),
each present when both endpoints are QRs.  For k = ±1 the two coincide and the graph is a union of paths (runs of consecutive QRs);
for any other k the degree doubles and a giant component appears, so no finite block decomposition exists.
usage: blocks_general_k.py p k [k ...]"""
import sys
from collections import defaultdict
def comps(p, k):
    sq = [False]*p
    for r in range(p): sq[r*r % p] = True
    V = [t for t in range(p) if sq[t]]
    idx = set(V); par = {t: t for t in V}
    def find(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    def uni(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: par[ra] = rb
    E = 0
    for t in V:
        for step in {1 % p, k % p}:
            u = (t + step) % p
            if u in idx: uni(t, u); E += 1
    sizes = defaultdict(int)
    for t in V: sizes[find(t)] += 1
    hist = defaultdict(int)
    for s in sizes.values(): hist[s] += 1
    mx = max(sizes.values())
    return len(V), E, len(sizes), mx, dict(sorted(hist.items())[:6])
for p in (1009, 4001):
    for k in (-1, 2, 3, 5, 7):
        n, e, c, mx, hist = comps(p, k % p)
        print(f"p={p} k={k:3d}: vertices {n}, edges {e}, components {c}, largest {mx} ({100*mx/n:.1f}% of vertices), small sizes {hist}", flush=True)
