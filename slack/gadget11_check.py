"""gadget11_check.py — independent check of the (1,1)-gadget count 144 = 9 + 54 + 81 (Lemma 'gadget maxima').

For every prime p in the list, every c, and a sample of boxes W=[x0,x0+2p)x[y0,y0+2p): build P_W, find all rich lines by brute
force over pairs, group classes into V-orbits, and for every generic orbit of pattern (1,1) verify
  * the line/multiplicity structure used in the proof: the two 'distinguished' 3-lines through the shared class kappa carry
    one m=1 point and two m=2 points; the two other 3-lines carry two m=1 and one m=2; the two 4-lines carry three m=1 and one m=2;
  * the number of 10-point lawful subsets is 9 (t=0), 54 (t=1), 81 (t=2), where t = number of m=2 points used;
  * the maximum is 10.
Usage: python3 slack/gadget11_check.py [pmax] [boxes_per_p]
"""
import sys, itertools, random
from fractions import Fraction

def primes(pmax):
    return [q for q in range(3, pmax + 1) if all(q % d for d in range(2, int(q ** 0.5) + 1))]

def check(p, c, x0, y0):
    P = [(x, y) for x in range(x0, x0 + 2 * p) for y in range(y0, y0 + 2 * p) if (x * y - c) % p == 0]
    S = set(P)
    lines = {}
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            (x1, y1), (x2, y2) = P[i], P[j]
            dx, dy = x2 - x1, y2 - y1
            # canonical line: (a,b,c) with a x + b y = c, primitive, a>0 or (a==0 and b>0)
            a, b = dy, -dx
            g = abs(__import__('math').gcd(a, b)); a //= g; b //= g
            if a < 0 or (a == 0 and b < 0): a, b = -a, -b
            cc = a * x1 + b * y1
            lines.setdefault((a, b, cc), set()).update([(x1, y1), (x2, y2)])
    rich = [frozenset(v) for v in lines.values() if len(v) >= 3]
    mult = {q: 0 for q in P}
    for L in rich:
        for q in L: mult[q] += 1
    # orbits of classes
    def cls(q): return (q[0] % p, q[1] % p)
    def sig(k): return ((-k[1]) % p, (-k[0]) % p)
    def tau(k): return (k[1], k[0])
    seen = set(); results = []
    for q in P:
        k = cls(q)
        if k in seen: continue
        orbit = {k, sig(k), tau(k), sig(tau(k))}
        seen |= orbit
        if len(orbit) < 4: continue
        pts = [q for q in P if cls(q) in orbit]
        ls = [L for L in rich if any(cls(q) in orbit for q in L)]
        assert all(all(cls(q) in orbit for q in L) for L in ls), "rich line leaves the orbit"
        n3 = sum(1 for L in ls if len(L) == 3); n4 = sum(1 for L in ls if len(L) == 4)
        # pattern: e = split sigma pairs, f = split tau pairs; a split pair = two 3-lines of that slope, shared = one 4-line
        if not (n3 == 4 and n4 == 2): continue          # not (1,1): (0,0) has n4=4; (2,0)/(0,2) has n3=4,n4=2 too!
        # distinguish (1,1) from (2,0): in (2,0) all four 3-lines have the same slope
        def slope(L):
            (a, b), (cc, d) = sorted(L)[:2]; return 1 if (cc - a) == (d - b) else -1
        sl = [slope(L) for L in ls if len(L) == 3]
        if len(set(sl)) == 1: continue                   # (2,0) or (0,2)
        # structure
        m2 = [q for q in pts if mult[q] == 2]; assert len(m2) == 4
        assert all(mult[q] in (1, 2) for q in pts)
        three = [L for L in ls if len(L) == 3]; four = [L for L in ls if len(L) == 4]
        prof3 = sorted(tuple(sorted(mult[q] for q in L)) for L in three)
        prof4 = sorted(tuple(sorted(mult[q] for q in L)) for L in four)
        assert prof3 == [(1, 1, 2), (1, 1, 2), (1, 2, 2), (1, 2, 2)], prof3
        assert prof4 == [(1, 1, 1, 2), (1, 1, 1, 2)], prof4
        # the two (1,2,2)-lines are the diagonal and antidiagonal of one class kappa: their m=1 points are copies of one class
        dist = [L for L in three if sorted(mult[q] for q in L) == [1, 2, 2]]
        k1 = {cls(q) for L in dist for q in L if mult[q] == 1}
        assert len(k1) == 1, k1
        # count maximum lawful subsets by t
        best = 0; cnt = {}
        idx = {q: i for i, q in enumerate(pts)}
        lines_idx = [[idx[q] for q in L] for L in ls]
        for mask in range(1 << 16):
            ok = True
            for L in lines_idx:
                if sum((mask >> i) & 1 for i in L) > 2: ok = False; break
            if not ok: continue
            sz = bin(mask).count("1")
            if sz > best: best = sz; cnt = {}
            if sz == best:
                t = sum((mask >> idx[q]) & 1 for q in m2)
                cnt[t] = cnt.get(t, 0) + 1
        assert best == 10 and cnt == {0: 9, 1: 54, 2: 81}, (best, cnt)
        results.append(1)
    return len(results)

if __name__ == "__main__":
    pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 13
    nb = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    rnd = random.Random(1)
    tot = 0
    for p in primes(pmax):
        for c in range(1, p):
            boxes = [(x0, y0) for x0 in range(p) for y0 in range(p)]
            rnd.shuffle(boxes)
            for (x0, y0) in boxes[:nb]:
                tot += check(p, c, x0, y0)
        print(f"p={p}: ok, (1,1)-orbits checked so far: {tot}", flush=True)
    print("ALL OK: every (1,1) orbit has the stated line structure, maximum 10, and 9/54/81 maximum sets by t")
