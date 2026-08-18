"""dir_count.py — k=-1: for a fixed primitive direction (u,v), count the collinear distinct-class point-triples of P_{-1} on lines of that
direction, and describe them by residue-line groups: on the mod-p line ux+vy ≡ w (mod p)... we simply enumerate: for each integer line
of direction (u,v) with >= 3 candidates, the distinct-class triples; report count, count/(p-1), and the distribution of the number of
classes per rich line.  usage: python3 slack/dir_count.py u v p1 [p2 ...]"""
import sys, itertools
from collections import defaultdict, Counter
u, v = int(sys.argv[1]), int(sys.argv[2])
for a_ in sys.argv[3:]:
    p = int(a_); h = (p - 1) // 2
    def X(t): t %= p; return t if t <= h else t - p
    def Y(t): t %= p; return t if t else p
    pts = []
    for a in range(1, p):
        ia = pow(a, -1, p)
        for hyp, yb in ((1, Y(ia)), (-1, Y(-ia))):
            for r in (0, 1):
                for s in (0, 1): pts.append(((X(a) + r * p, yb + s * p), (hyp, a)))
    lines = defaultdict(list)
    for (x, y), c in pts:
        lines[v * x - u * y].append(((x, y), c))          # lines of direction (u,v): v x - u y = const
    tri = 0; sizes = Counter(); ncls = Counter()
    for key, mem in lines.items():
        if len(mem) < 3: continue
        sizes[len(mem)] += 1; ncls[len({c for _, c in mem})] += 1
        for t in itertools.combinations(mem, 3):
            if len({c for _, c in t}) == 3: tri += 1
    print(f"dir ({u},{v}) p={p}: rich lines {sum(sizes.values())} (sizes {dict(sorted(sizes.items()))}), classes per rich line {dict(sorted(ncls.items()))}, distinct-class triples {tri} = {tri/(p-1):.3f}(p-1)")
