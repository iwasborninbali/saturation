"""crosslines.py — fast (O(|U|^2)) count of collinear triples in the union H(1,p) ∪ H(1,q) in the N×N window
(same conventions as crosstriples.py: HJSW x-shift −(p−1)/2 for each modulus, points (x,y) in [0,N)^2), classified:
  within_p / within_q : all three points on one hyperbola;
  cross               : points on both hyperbolas, split by the slope of the line: horizontal/vertical, ±1, other;
  and, for cross triples, whether the two points of the same hyperbola are congruent (same class) or not.
usage: crosslines.py p q N [p q N ...]"""
import sys
from math import gcd
from itertools import combinations
from collections import defaultdict


def cands(p, N):
    out = []
    for x in range(N):
        xp = (x - (p - 1) // 2) % p
        if xp == 0: continue
        for y in range(N):
            if y % p and (xp * y - 1) % p == 0: out.append((x, y))
    return out


def lines_of(U):
    """dict: canonical line -> list of point indices (all lines with ≥2 points)"""
    L = defaultdict(set)
    n = len(U)
    for i in range(n):
        x1, y1 = U[i]
        for j in range(i + 1, n):
            x2, y2 = U[j]
            dx, dy = x2 - x1, y2 - y1; g = gcd(abs(dx), abs(dy)); dx //= g; dy //= g
            if dx < 0 or (dx == 0 and dy < 0): dx, dy = -dx, -dy
            key = (dx, dy, dx * y1 - dy * x1)
            s = L[key]; s.add(i); s.add(j)
    return L


def slope_class(dx, dy):
    if dy == 0: return "hor"
    if dx == 0: return "ver"
    if abs(dx) == abs(dy): return "diag"
    return "other"


def count(p, q, N):
    Hp, Hq = cands(p, N), cands(q, N)
    sp = set(Hp); U = sorted(sp | set(Hq)); inp = [u in sp for u in U]
    L = lines_of(U)
    res = defaultdict(int)
    for (dx, dy, _), mem in L.items():
        m = len(mem)
        if m < 3: continue
        a = sum(1 for i in mem if inp[i]); b = m - a
        sc = slope_class(dx, dy)
        # triples: within p: C(a,3); within q: C(b,3); cross: C(a,2)*b + a*C(b,2)
        res["within_p"] += a * (a - 1) * (a - 2) // 6
        res["within_q"] += b * (b - 1) * (b - 2) // 6
        cr = a * (a - 1) // 2 * b + a * b * (b - 1) // 2
        res["cross"] += cr; res["cross_" + sc] += cr
        # same-class pairs among the p-points (resp. q-points) on this line
        if cr:
            pp = [U[i] for i in mem if inp[i]]; qq = [U[i] for i in mem if not inp[i]]
            same_p = sum(1 for u, v in combinations(pp, 2) if (u[0] - v[0]) % p == 0 and (u[1] - v[1]) % p == 0)
            same_q = sum(1 for u, v in combinations(qq, 2) if (u[0] - v[0]) % q == 0 and (u[1] - v[1]) % q == 0)
            res["cross_samepair"] += same_p * b + same_q * a
    res["|Hp|"], res["|Hq|"], res["|U|"] = len(Hp), len(Hq), len(U)
    return res


if __name__ == "__main__":
    args = list(map(int, sys.argv[1:]))
    print("  p   q    N  |Hp| |Hq|  |U| | within_p within_q   cross | hor+ver   diag  other | samepair | cross/N^2 cross/(N lnN)")
    for i in range(0, len(args), 3):
        p, q, N = args[i:i + 3]
        r = count(p, q, N)
        import math
        print(f"{p:3d} {q:3d} {N:4d} {r['|Hp|']:4d} {r['|Hq|']:4d} {r['|U|']:5d} | {r['within_p']:8d} {r['within_q']:8d} {r['cross']:7d} |"
              f" {r['cross_hor'] + r['cross_ver']:7d} {r['cross_diag']:6d} {r['cross_other']:6d} | {r['cross_samepair']:8d} |"
              f" {r['cross'] / N**2:9.3f} {r['cross'] / (N * math.log(N)):9.2f}", flush=True)
