"""dir11_groups.py — k=-1, slope +1: classify residue groups by class composition and centre pattern; count distinct-class collinear triples
per group type; verify Sum = dir_count(1,1).  usage: python3 slack/dir11_groups.py p1 [p2 ...]"""
import sys, itertools
from collections import defaultdict, Counter
for a_ in sys.argv[1:]:
    p = int(a_); h = (p - 1) // 2
    def X(t): t %= p; return t if t <= h else t - p
    def Y(t): t %= p; return t if t else p
    # slope +1 lines: x - y = w; collect points per w with class labels; group by residue w mod p
    lines = defaultdict(list)
    for a in range(1, p):
        ia = pow(a, -1, p)
        for hyp, yb in ((1, Y(ia)), (-1, Y(-ia))):
            for r in (0, 1):
                for s in (0, 1):
                    x, y = X(a) + r * p, yb + s * p
                    lines[x - y].append((hyp, a))
    groups = defaultdict(list)
    for w, mem in lines.items(): groups[w % p].append((w, mem))
    types = Counter(); tri_by_type = Counter(); total = 0
    for d, ls in groups.items():
        classes = set(c for w, mem in ls for c in mem)
        n1 = sum(1 for c in classes if c[0] == 1); n2 = len(classes) - n1
        # centres: for each class its 2-copy line
        centre = {}
        for w, mem in ls:
            cnt = Counter(mem)
            for c, k in cnt.items():
                if k == 2: centre[c] = w
        centres = sorted(set(centre.values()))
        cvals = tuple(sorted(Counter(centre.values()).values()))     # partition of classes by centre
        t = 0
        for w, mem in ls:
            cnt = Counter(mem); cls = list(cnt)
            for tri in itertools.combinations(cls, 3): t += cnt[tri[0]] * cnt[tri[1]] * cnt[tri[2]]
        key = (n1, n2, cvals); types[key] += 1; tri_by_type[key] += t; total += t
    print(f"p={p}: slope+1 distinct-class triples {total} = {total/(p-1):.3f}(p-1); group types (n_H1, n_H-1, centre partition): count, triples/group:")
    for key in sorted(types, key=lambda k: -types[k]):
        print(f"    {key}: {types[key]} groups, {tri_by_type[key]/types[key]:.1f} triples each")
