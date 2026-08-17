"""perturb.py — same-size perturbations of known rot2-symmetric books: exchange the columns of two
half-turn pairs (row and column counts and the half-turn symmetry are preserved), keep the result iff lawful.
Reports lawful neighbours and their exact class (web/stab.py).   usage: python3 perturb.py FILE [maxconfigs]"""
import sys, os
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/web'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decode import decode
from stab import classify, encode
import saturation as S

def dirs_ok(p, others):
    """no two of `others` collinear with p (others: list of (u,v) not containing p)"""
    seen = set()
    for (u, v) in others:
        du, dv = u - p[0], v - p[1]
        if du == 0 and dv == 0: return False
        g = gcd(abs(du), abs(dv)); du //= g; dv //= g
        if du < 0 or (du == 0 and dv < 0): du, dv = -du, -dv
        if (du, dv) in seen: return False
        seen.add((du, dv))
    return True

def lawful_after(pts_set, removed, added):
    base = [q for q in pts_set if q not in removed]
    new = list(added)
    for i, p in enumerate(new):
        if p in pts_set and p not in removed: return False
        others = base + [q for j, q in enumerate(new) if j != i]
        if not dirs_ok(p, others): return False
    return True

def main():
    path = sys.argv[1]; maxc = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
    found = {}
    lines = [l for l in open(path) if l.strip()][:maxc]
    tried = 0
    for li, line in enumerate(lines):
        cls, n, book = decode(line)
        m = n - 1
        pts = sorted(divmod(t, n) for t in book); pset = set(pts)
        pairs = sorted({tuple(sorted([(u, v), (m - u, m - v)])) for (u, v) in pts})
        for i in range(len(pairs)):
            for j in range(i + 1, len(pairs)):
                (a, b), _ = pairs[i]; (c, d), _ = pairs[j]
                for (d1, b1) in ((d, b), (m - d, m - b)):        # exchange columns, or with the image
                    newP = [(a, d1), (m - a, m - d1), (c, b1), (m - c, m - b1)]
                    if len(set(newP)) < 4: continue
                    removed = {(a, b), (m - a, m - b), (c, d), (m - c, m - d)}
                    tried += 1
                    if lawful_after(pset, removed, newP):
                        newbook = frozenset(u * n + v for (u, v) in (pset - removed) | set(newP))
                        S.certify(newbook, n)
                        k = classify(newbook, n)
                        enc = encode(newbook, n)
                        if enc not in found:
                            found[enc] = k
                            print(f"config {li}: pairs {pairs[i][0]}x{pairs[j][0]} variant {(d1,b1)} -> lawful, class {k}: {enc}", flush=True)
    print(f"tried {tried} exchanges over {len(lines)} configurations; lawful neighbours: {len(found)}; classes: {sorted(set(found.values()))}")

main()
