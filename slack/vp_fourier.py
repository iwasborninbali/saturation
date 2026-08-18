"""vp_fourier.py — k=-1 vertical-pair model: T(eps) = number of collinear triples of S(r) as a polynomial of degree <= 3 in eps_a = (-1)^{r_a},
computed exactly from the collinear lift patterns of class triples (no enumeration of orientations).  Reports E[T], the Fourier
coefficients by degree (l1, l2, max), the number of nonzero coefficients, and (for p <= 19) the exact min over all r by brute force.
usage: python3 slack/vp_fourier.py p [bruteforce]"""
import sys, itertools
from collections import defaultdict
p = int(sys.argv[1]); h = (p - 1) // 2; brute = len(sys.argv) > 2
def X(u): u %= p; return u if u <= h else u - p
def Y(u): u %= p; return u if u else p          # residue in [1,p-1] for u != 0
# classes: (hyp, a) with hyp in {+1,-1}; H(1)_a: base (X(a), Y(1/a)); H(-1)_a: base (X(a), Y(-1/a))
classes = [(hyp, a) for a in range(1, p) for hyp in (1, -1)]
base = {}
for hyp, a in classes:
    ia = pow(a, -1, p); base[(hyp, a)] = (X(a), Y(ia if hyp == 1 else -ia))
# in orientation r: H(1)_a uses column X(a) + r_a p, H(-1)_a uses X(a) + (1 - r_a) p; both lifts s=0,1
def col(cls, ra):
    hyp, a = cls; return base[cls][0] + (ra if hyp == 1 else 1 - ra) * p
# T(eps) = sum over unordered class triples {c1,c2,c3} and orientation bits (r_a for the distinct a's involved) and lifts (s1,s2,s3):
#   [collinear] * prod_a [(r_a == rho_a)]  where rho are the bits realising the pattern; note H(1)_a and H(-1)_a share the bit r_a.
coef = defaultdict(float)     # monomial (sorted tuple of a's) -> coefficient in the eps-expansion; [r_a==0] = (1+eps)/2, [r_a==1] = (1-eps)/2
def add_indicator(assign):     # assign: dict a -> required bit; expands prod (1 +- eps_a)/2 into monomials
    items = list(assign.items()); n = len(items)
    for mask in range(1 << n):
        mono = tuple(sorted(items[i][0] for i in range(n) if mask >> i & 1))
        sign = 1
        for i in range(n):
            if mask >> i & 1 and items[i][1] == 1: sign = -sign
        coef[mono] += sign / (1 << n)
count_constraints = 0
for c1, c2, c3 in itertools.combinations(classes, 3):
    avars = sorted({c1[1], c2[1], c3[1]})
    for bits in itertools.product((0, 1), repeat=len(avars)):
        rmap = dict(zip(avars, bits))
        xs = [col(c, rmap[c[1]]) for c in (c1, c2, c3)]
        if len(set(xs)) < 3: continue        # two in one column: never collinear with a third (vertical line has 2)
        for s in itertools.product((0, 1), repeat=3):
            pts = [(xs[i], base[(c1, c2, c3)[i]][1] + s[i] * p) for i in range(3)]
            (x1, y1), (x2, y2), (x3, y3) = pts
            if (x2 - x1) * (y3 - y1) == (x3 - x1) * (y2 - y1):
                add_indicator(rmap); count_constraints += 1
coef = {m: v for m, v in coef.items() if abs(v) > 1e-12}
E = coef.get((), 0.0)
bydeg = defaultdict(list)
for m, v in coef.items(): bydeg[len(m)].append(v)
print(f"p={p}: collinear (class-triple, orientation, lifts) patterns: {count_constraints}; E[T] = {E:.2f} = {E/(p-1):.3f}(p-1)")
for d in sorted(bydeg):
    vs = bydeg[d]; print(f"  degree {d}: {len(vs)} coefficients, l1 = {sum(abs(v) for v in vs):.1f}, l2 = {sum(v*v for v in vs)**0.5:.2f}, max|.| = {max(abs(v) for v in vs):.2f}")
tot_l1 = sum(abs(v) for m, v in coef.items() if m)
print(f"  trivial Fourier lower bound: min T >= E - l1(nonconst) = {E - tot_l1:.1f}")
if brute:
    n = p - 1; avals = list(range(1, p)); best = None; bestr = None
    import math
    for r in range(1 << n):
        eps = {avals[i]: (1 if (r >> i) & 1 == 0 else -1) for i in range(n)}
        T = 0.0
        for m, v in coef.items():
            prod = v
            for a in m: prod *= eps[a]
            T += prod
        if best is None or T < best - 1e-9: best, bestr = T, r
    print(f"  brute-force min over 2^{n} orientations: {best:.1f}")
