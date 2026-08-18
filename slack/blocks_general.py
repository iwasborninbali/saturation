"""blocks_general.py — 8-point ±1 lines ('blocks') of P_1 ∪ P_k in the HJSW box for general k, and how many are 'closed'
(all four classes' row- and column-partners lie in blocks too).  usage: blocks_general.py k p1 p2 ..."""
import sys
from collections import defaultdict
k0 = int(sys.argv[1])
for p in map(int, sys.argv[2:]):
    h = (p - 1) // 2; k = k0 % p
    pts = [(x, y) for x in range(-h, 3 * h + 2) for y in range(0, 2 * p) if (x * y) % p in (1, k)]
    def cls(q):
        x, y = q; return (x % p, y % p)          # residue class (a,b) with ab ≡ 1 or k
    lines = defaultdict(list)
    for q in pts:
        x, y = q; lines[('d', x - y)].append(q); lines[('a', x + y)].append(q)
    eight = [(key, mem) for key, mem in lines.items() if len(mem) == 8]
    blocks = []
    inblock = set()
    for key, mem in eight:
        cs = {cls(q) for q in mem}
        blocks.append((key, cs)); inblock |= cs
    def row_partner(c):
        a, b = c; return ((k * pow(a, 1, p)) % p if (a * b) % p == 1 else pow(k, -1, p) * a % p, b)  # same b: x -> k/b or 1/b
    def col_partner(c):
        a, b = c; return (a, (k * b) % p if (a * b) % p == 1 else (pow(k, -1, p) * b) % p)      # same a: y -> k/a or 1/a
    # sanity: partners must be classes of the other hyperbola
    closed = 0; partial = 0
    for key, cs in blocks:
        ok = True
        for c in cs:
            for q in (row_partner(c), col_partner(c)):
                if q not in inblock: ok = False
        if ok: closed += 1
    nd = sum(1 for key, _ in blocks if key[0] == 'd'); na = len(blocks) - nd
    sizes = defaultdict(int)
    for key, mem in lines.items():
        if len(mem) >= 3: sizes[len(mem)] += 1
    print(f"p={p} k={k}: 8-lines={len(blocks)} (diag {nd}, anti {na}); classes in blocks {len(inblock)} of {2*(p-1)}; closed blocks {closed}; "
          f"per-p: 8-lines/p={len(blocks)/p:.3f}; rich ±1 lines by size {dict(sorted(sizes.items()))}", flush=True)
