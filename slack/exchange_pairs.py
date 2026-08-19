"""exchange_pairs.py — mechanism for the exchange lemma (H4): every point q of H(-1) taken into a lawful set FORBIDS at least one point of
each "blocking pair" {a,b} subset H(1) collinear with q.  If the bipartite graph (q -> its blocking pairs) has a system of distinct
representatives, then |S ∩ H(-1)| <= #(points of H(1) missing from S), i.e. |S| <= alpha(H(1)) + O(1) = 3(p-1) + O(1).
This script measures: the number of blocking pairs per q, the degree distribution, and (Hall) the maximum matching between the
H(-1) points and the H(1) points they can block (each q matched to one point of one of its pairs).  usage: exchange_pairs.py p [p ...]"""
import sys
from collections import defaultdict
from itertools import combinations
import networkx as nx
def pts(p):
    h = (p - 1) // 2; x0, y0 = -h, 0
    P1 = []; Pm = []
    for x in range(1, p):
        ix = pow(x, -1, p)
        for (y, L) in ((ix, P1), ((-ix) % p, Pm)):
            for X in (x0 + ((x - x0) % p), x0 + ((x - x0) % p) + p):
                for Y in (y0 + ((y - y0) % p), y0 + ((y - y0) % p) + p):
                    L.append((X, Y))
    return sorted(set(P1)), sorted(set(Pm))
for p in map(int, sys.argv[1:]):
    P1, Pm = pts(p)
    S1 = set(P1)
    pairs = defaultdict(set)      # q -> set of frozenset({a,b}) collinear with q
    for q in Pm:
        byslope = defaultdict(list)
        for a in P1:
            dx, dy = a[0] - q[0], a[1] - q[1]
            g = abs(dx) if dy == 0 else (abs(dy) if dx == 0 else __import__('math').gcd(abs(dx), abs(dy)))
            d = (dx // g, dy // g)
            if d[0] < 0 or (d[0] == 0 and d[1] < 0): d = (-d[0], -d[1])
            byslope[d].append(a)
        for d, L in byslope.items():
            if len(L) >= 2:
                for a, b in combinations(L, 2): pairs[q].add(frozenset((a, b)))
    deg = [len(pairs[q]) for q in Pm]
    G = nx.Graph()
    for q in Pm:
        for pr in pairs[q]:
            for a in pr: G.add_edge(('q', q), ('a', a))
    M = nx.algorithms.bipartite.maximum_matching(G, top_nodes=[('q', q) for q in Pm]) if G else {}
    matched = sum(1 for k in M if k[0] == 'q')
    print(f"p={p}: |H(1)|=|H(-1)|={len(P1)}; blocking pairs per q: min {min(deg)}, mean {sum(deg)/len(deg):.1f}, max {max(deg)}; "
          f"q with 0 pairs: {sum(1 for d in deg if d == 0)}; maximum matching q->H(1): {matched}/{len(Pm)}", flush=True)
