"""hjsw_window_check.py — independent check of the HJSW-window theorem (third solver).

P = H(c,p) ∩ G(p),  G(p) = [-(p-1)/2, (3p-1)/2] × [0, 2p-1]  (KNS 2.1; HJSW window, 2p × 2p).
Claim: every subset of P with no three collinear has ≤ 3(p-1) points, and the number of maximum
lawful subsets is 9^s, s = #{QR among c, -c}  (s = [c is a QR] + [-c is a QR]).

What this script verifies for each p (no theory trusted, everything recomputed from the point set):
  1. all lines carrying ≥ 3 points of P (found by brute force over pairs) have slope ±1 (never 0, ∞, other);
  2. every such line lies inside one V4-orbit of classes {κ, π+κ, π-κ, -κ}, hence the max decomposes over orbits;
  3. the double-counting identity  2·|L| + Z = 3(p-1)  (L = lines with ≥3 points, Z = points on no such line),
     which is the whole proof:  |S| ≤ Z + Σ_{ℓ∈L} |S∩ℓ| ≤ Z + 2|L|;
  4. exact maximum by brute force per orbit (≤ 16 points per orbit ⇒ 2^16 subsets), summed — must equal 3(p-1);
     an explicit maximum witness is assembled and passed through saturation.the_law (grid coordinates, N = 2p);
  5. the number of maximum lawful subsets (product over orbits) — must equal 9^s.
usage: python3 slack/hjsw_window_check.py p1 p2 ...   (default: all primes 3..101 with c=1, plus a spread of c)
"""
import sys, os
from math import gcd
from itertools import combinations
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import saturation as S


def points(p, c):
    """P = H(c,p) ∩ G(p) as (x,y) with x in [-(p-1)/2, (3p-1)/2], y in [0,2p-1]; only normal points lie on H."""
    h = (p - 1) // 2
    return [(x, y) for x in range(-h, 3 * h + 2) for y in range(2 * p) if x % p and y % p and (x * y - c) % p == 0]


def lines_ge3(P):
    """all lines with ≥ 3 points of P: dict (a,b,c0) -> sorted list of points, with a*y - b*x = c0, (a,b) primitive."""
    idx = set(P); seen = {}; L = {}
    Pl = sorted(P)
    for i in range(len(Pl)):
        for j in range(i + 1, len(Pl)):
            (x1, y1), (x2, y2) = Pl[i], Pl[j]
            dx, dy = x2 - x1, y2 - y1; g = gcd(abs(dx), abs(dy)); dx //= g; dy //= g
            if dx < 0 or (dx == 0 and dy < 0): dx, dy = -dx, -dy
            key = (dx, dy, dx * y1 - dy * x1)
            if key in seen: continue
            seen[key] = 1
            mem = [q for q in Pl if dx * q[1] - dy * q[0] == key[2]]
            if len(mem) >= 3: L[key] = mem
    return L


def cls(q, p): return (q[0] % p, q[1] % p)


def orbit_of(kappa, p):
    a, b = kappa
    return frozenset({(a, b), ((-b) % p, (-a) % p), (b, a), ((-a) % p, (-b) % p)})


def max_lawful_orbit(pts, L):
    """brute force: max lawful subset of the ≤16 points of one orbit, given the ≥3-lines restricted to it;
    returns (max, count of maximum subsets, one witness)."""
    n = len(pts); pos = {q: i for i, q in enumerate(pts)}
    masks = []
    for mem in L:
        m = 0
        for q in mem:
            if q in pos: m |= 1 << pos[q]
        if bin(m).count("1") >= 3: masks.append(m)
    best, cnt, wit = -1, 0, None
    for sub in range(1 << n):
        ok = True
        for m in masks:
            if bin(sub & m).count("1") >= 3: ok = False; break
        if not ok: continue
        k = bin(sub).count("1")
        if k > best: best, cnt, wit = k, 1, sub
        elif k == best: cnt += 1
    return best, cnt, [pts[i] for i in range(n) if wit >> i & 1]


def is_qr(a, p): return pow(a % p, (p - 1) // 2, p) == 1


def check(p, c, verbose=True):
    P = points(p, c); assert len(P) == 4 * (p - 1)
    L = lines_ge3(P)
    # 1. slopes
    for (dx, dy, _), mem in L.items():
        assert (dx, dy) in ((1, 1), (1, -1)), f"p={p} c={c}: line of slope {dy}/{dx} with {len(mem)} points {mem}"
        assert len(mem) in (3, 4)
    # 2. lines inside one orbit
    orbits = {}
    for q in P:
        o = orbit_of(cls(q, p), p); orbits.setdefault(o, []).append(q)
    for mem in L.values():
        os_ = {orbit_of(cls(q, p), p) for q in mem}
        assert len(os_) == 1, f"p={p} c={c}: a ≥3-line crosses orbits: {mem}"
    # 3. identity
    on = set(q for mem in L.values() for q in mem)
    Z = len(P) - len(on)
    ident = 2 * len(L) + Z
    assert ident == 3 * (p - 1), f"p={p} c={c}: 2|L|+Z = {ident} != {3*(p-1)}"
    # 4. exact max per orbit + witness through the law
    total, count, witness = 0, 1, []
    for o, pts in orbits.items():
        assert len(pts) in (8, 16)
        Lo = [mem for mem in L.values() if orbit_of(cls(mem[0], p), p) == o]
        m, cnt, w = max_lawful_orbit(pts, Lo)
        assert m == 3 * len(pts) // 4, f"p={p} c={c}: orbit {sorted(o)} max {m} of {len(pts)} points"
        total += m; count *= cnt; witness += w
    assert total == 3 * (p - 1)
    N = 2 * p; h = (p - 1) // 2
    S.the_law(frozenset((x + h) * N + y for (x, y) in witness), N)      # grid coordinates 0..2p-1
    # 5. number of maximum subsets
    s = int(is_qr(c, p)) + int(is_qr(-c, p))
    assert count == 9 ** s, f"p={p} c={c}: #max subsets {count} != 9^{s}"
    if verbose:
        print(f"p={p:3d} c={c:3d}: |P|={len(P):4d}  lines>=3: {len(L):4d} (all slope ±1)  Z={Z:2d}  "
              f"2|L|+Z={ident:4d}=3(p-1)  exact max={total:4d} (witness lawful)  #max subsets={count}=9^{s}")
    return total, count


if __name__ == "__main__":
    ps = [int(a) for a in sys.argv[1:]]
    if not ps:
        ps = [p for p in range(3, 102) if all(p % d for d in range(2, int(p ** 0.5) + 1))]
    for p in ps:
        cs = [1] if p > 31 else list(range(1, p))          # every c for small p, c=1 (plus a few) for larger
        if p > 31: cs = sorted({1, 2, p - 1, p - 2, 3 % p, (p + 1) // 2})
        for c in cs:
            check(p, c, verbose=(c in (1, 2, p - 1) or p <= 13))
    print("all checks passed")
