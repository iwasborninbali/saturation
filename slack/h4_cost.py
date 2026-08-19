"""h4_cost.py — the cost of taking points of H(-1) against a rigid maximum M of H(1) (H4', after the stability lemma).
For a maximum M (orbit-wise optimum) and each q in H(-1): F(q) = the set of pairs {x,y} in M collinear with q (all must be broken to take q).
Measures: (i) #free q (F(q) empty) -- these are the O(1) term; (ii) tau(G_Q) = min #deletions from M breaking all pairs of all q in Q
(vertex cover, ILP) for Q = all of H(-1) and for random Q; (iii) how many q a single deletion can unblock.
usage: h4_cost.py p [p ...]"""
import sys, random
from collections import defaultdict
from itertools import combinations
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def build(p):
    h = (p - 1) // 2; x0, y0 = -h, 0
    X = lambda u: u if u <= h else u - p
    H1 = []; own = {}
    for a in range(1, p):
        ia = pow(a, -1, p)
        bx = x0 + ((a - x0) % p); by = y0 + ((ia - y0) % p)
        for r in (0, 1):
            for s in (0, 1):
                q = (bx + r * p, by + s * p); H1.append(q); own[q] = a
    Hm = []
    for a in range(1, p):
        ia = (-pow(a, -1, p)) % p
        bx = x0 + ((a - x0) % p); by = y0 + ((ia - y0) % p)
        for r in (0, 1):
            for s in (0, 1): Hm.append((bx + r * p, by + s * p))
    H1 = sorted(set(H1)); Hm = sorted(set(Hm))
    orb = {}
    for a in range(1, p):
        ia = pow(a, -1, p); orb[a] = frozenset({a, ia, (p - a) % p, (p - ia) % p})
    return H1, Hm, own, orb

def maximum_M(H1, own, orb):
    """orbit-wise maximum by brute force inside each orbit"""
    groups = defaultdict(list)
    for q in H1: groups[orb[own[q]]].append(q)
    def lawful(S):
        c = defaultdict(int)
        for (x, y) in S:
            for k in (('r', y), ('c', x), ('d', x - y), ('a', x + y)):
                c[k] += 1
                if c[k] > 2: return False
        return True
    M = []
    for O, P in groups.items():
        best = None
        for m in range(len(P), 0, -1):
            for S in combinations(P, m):
                if lawful(S): best = S; break
            if best: break
        M.extend(best)
    return M

def run(p):
    H1, Hm, own, orb = build(p)
    M = maximum_M(H1, own, orb); Ms = set(M); idx = {q: i for i, q in enumerate(M)}
    F = {}
    for q in Hm:
        byd = defaultdict(list)
        for a in M:
            dx, dy = a[0] - q[0], a[1] - q[1]
            g = np.gcd(abs(dx), abs(dy)) or 1
            d = (dx // g, dy // g)
            if d[0] < 0 or (d[0] == 0 and d[1] < 0): d = (-d[0], -d[1])
            byd[d].append(a)
        pr = [(a, b) for L in byd.values() if len(L) >= 2 for a, b in combinations(L, 2)]
        F[q] = pr
    free = [q for q in Hm if not F[q]]
    # vertex cover ILP over the union graph
    edges = sorted({(idx[a], idx[b]) if idx[a] < idx[b] else (idx[b], idx[a]) for q in Hm for a, b in F[q]})
    A = np.zeros((len(edges), len(M)))
    for i, (u, v) in enumerate(edges): A[i, u] = A[i, v] = 1
    r = milp(c=np.ones(len(M)), constraints=LinearConstraint(A, 1, np.inf), bounds=Bounds(0, 1), integrality=np.ones(len(M)))
    tau_all = round(r.fun) if r.success else None
    # single-deletion power: for how many q does one deletion break ALL pairs
    power = defaultdict(int)
    for q in Hm:
        if not F[q]: continue
        common = set(F[q][0])
        for a, b in F[q][1:]: common &= {a, b}
        for a in common: power[a] += 1
    print(f"p={p}: |M|={len(M)} (3(p-1)={3*(p-1)}), |H(-1)|={len(Hm)}; free q (no blocking pair): {len(free)}; "
          f"pairs per q: mean {np.mean([len(F[q]) for q in Hm]):.1f}; distinct blocked pairs: {len(edges)}; "
          f"tau(all) = {tau_all} (= {tau_all/len(Hm):.2f}|H(-1)|, {tau_all/len(M):.2f}|M|); "
          f"max #q unblocked by ONE deletion: {max(power.values()) if power else 0}; q unblockable by one deletion: {sum(power.values())}", flush=True)

for p in map(int, sys.argv[1:]): run(p)

def union_max(p):
    """max lawful subset of M ∪ R(M') where M, M' are rigid maxima of the two hyperbolae (R(x,y) = (p-x, y) maps H(1) -> H(-1))"""
    H1, Hm, own, orb = build(p)
    M = maximum_M(H1, own, orb)
    M2 = [(p - x, y) for (x, y) in M]              # R-image: a maximum of H(-1)
    U = sorted(set(M) | set(M2))
    idx = {q: i for i, q in enumerate(U)}
    lines = defaultdict(list)
    for (x, y) in U:
        for k in (('r', y), ('c', x), ('d', x - y), ('a', x + y)): lines[k].append(idx[(x, y)])
    L = [v for v in lines.values() if len(v) >= 3]
    # add general 3-point lines
    for i in range(len(U)):
        for j in range(i + 1, len(U)):
            pass
    A = np.zeros((len(L), len(U)))
    for i, m in enumerate(L):
        for j in m: A[i, j] = 1
    r = milp(c=-np.ones(len(U)), constraints=LinearConstraint(A, -np.inf, 2), bounds=Bounds(0, 1), integrality=np.ones(len(U)))
    v_axis = round(-r.fun)
    # now with ALL lines (>=3 points) of U
    from lp_curve import lines as alllines
    L2 = alllines(U, 'all')
    A2 = np.zeros((len(L2), len(U)))
    for i, m in enumerate(L2):
        for j in m: A2[i, j] = 1
    r2 = milp(c=-np.ones(len(U)), constraints=LinearConstraint(A2, -np.inf, 2), bounds=Bounds(0, 1), integrality=np.ones(len(U)))
    print(f"p={p}: |M ∪ R(M)| = {len(U)} (2*3(p-1) = {6*(p-1)}); max lawful inside it: rows/cols/±1 only {v_axis}, ALL lines {round(-r2.fun)}"
          f"  (3(p-1) = {3*(p-1)}, alpha(P_-1) known = {{11:32,13:40,17:54,19:59}}.get(p))", flush=True)
