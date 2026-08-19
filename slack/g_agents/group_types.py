#!/usr/bin/env python3
"""group_types.py (agent: group_types) -- classify residue classes of the two depressed cubics

    x^3 + x == c (mod p)   antidiagonal grouping: slope -1 lines X+Y = const
    x^3 - x == c (mod p)   diagonal grouping:     slope +1 lines X-Y = const

by the pattern of point-counts on the 4 consecutive integer lines of their "group" in the box lift
L = {(X,Y) in [0,2p)^2 : Y == X^3 (mod p)} of the permutation cubic (p prime, p == 2 mod 3).

Derivation (see docs/research/g_agents/group_types.md for the write-up). Fix a slope and a residue
class c with roots x_1,x_2,x_3 in [0,p). Each root x_i has an actual curve point (x_i, y_i),
y_i = x_i^3 mod p, and an integer "shift bit" b_i in {0,1}:

    antidiagonal (x^3+x):  b_i = 1  iff  x_i + y_i >= p        (the sum wraps)
    diagonal     (x^3-x):  b_i = 1  iff  x_i >= y_i             (the difference does not go negative)

b_i=0 ("low") contributes counts (1,2,1,0) to the group's 4 consecutive lines (spaced by p); b_i=1
("high") contributes (0,1,2,1). With k = #{i : b_i=0} in {0,1,2,3}, the total group pattern is exactly

    (k, k+3, 6-k, 3-k)

so: k=0 -> (0,3,6,3) ~ shape (3,6,3); k=3 -> (3,6,3,0) ~ shape (3,6,3); k=1 -> (1,4,5,2); k=2 -> (2,5,4,1).
A class with 1 root always gives shape (1,2,1) regardless of that root's bit (no ambiguity). A class
with 0 roots contributes nothing. Classes with 2 roots (a genuine double root, i.e. ramification of the
cubic) are also tabulated; elementary QR theory predicts n2 = 0 for the antidiagonal slope always
(since p==2 mod 3 forces -1/3 to be a non-residue, so x^3+x has no critical points over F_p), and for
the diagonal slope n2 = 0 when p==5 (mod 12) but n2 > 0 is possible when p==11 (mod 12) (3 is then a QR,
so x^3-x has 2 critical points) -- this is checked numerically below.

usage:  python3 slack/g_agents/group_types.py [p1 p2 ...]
default p list: 101 197 401 599 797 1097   (all run in well under a second: O(p) per prime per slope,
direct bucketing, no O(p^2) pair search anywhere in this file).

Output is printed to stdout and also written verbatim to slack/g_agents/group_types_output.txt.
"""
import sys
from collections import Counter, defaultdict

DEFAULT_PS = [101, 197, 401, 599, 797, 1097]


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def build(p, sign):
    """sign=+1 -> antidiagonal classes c=(x^3+x) mod p ; sign=-1 -> diagonal classes c=(x^3-x) mod p.
    Returns roots_of: dict c -> sorted list of roots x in [0,p).  O(p)."""
    roots_of = defaultdict(list)
    for x in range(p):
        c = (x * x * x + sign * x) % p
        roots_of[c].append(x)
    return roots_of


def bit_of(x, p, sign):
    """Shift bit of root x for the given slope: 0='low', 1='high' (see module docstring)."""
    y = pow(x, 3, p)
    if sign == 1:
        return 1 if (x + y) >= p else 0
    else:
        return 1 if x >= y else 0


SHAPE_OF_K = {0: '(3,6,3)', 3: '(3,6,3)', 1: '(1,4,5,2)', 2: '(2,5,4,1)'}


def analyze_slope(p, sign):
    roots_of = build(p, sign)
    n_by_size = Counter()
    for c in range(p):
        n_by_size[len(roots_of.get(c, ()))] += 1
    assert n_by_size[0] == p - len(roots_of)
    assert sum(sz * n for sz, n in n_by_size.items()) == p  # every residue x counted exactly once

    records = []  # (c, roots(tuple), bits(tuple), k)
    k_counter = Counter()
    shape_counter = Counter()
    bits_counter = Counter()
    for c, roots in roots_of.items():
        if len(roots) == 3:
            bits = tuple(bit_of(x, p, sign) for x in roots)  # root order = ascending x
            k = bits.count(0)
            records.append((c, tuple(roots), bits, k))
            k_counter[k] += 1
            shape_counter[SHAPE_OF_K[k]] += 1
            bits_counter[bits] += 1
    records.sort()

    # sanity check on 1-root classes: shape is always (1,2,1) regardless of the root's bit
    for c, roots in roots_of.items():
        if len(roots) == 1:
            b = bit_of(roots[0], p, sign)
            pat = (1, 2, 1, 0) if b == 0 else (0, 1, 2, 1)
            assert tuple(v for v in pat if v) == (1, 2, 1)

    return dict(roots_of=roots_of, n_by_size=n_by_size, records=records,
                k_counter=k_counter, shape_counter=shape_counter, bits_counter=bits_counter)


def correlation(p, A_res, B_res):
    """A_res, B_res: dict x -> #roots of x's class, for the antidiagonal (A) and diagonal (B) slope."""
    A3 = sum(1 for x in range(p) if A_res[x] == 3)
    B3 = sum(1 for x in range(p) if B_res[x] == 3)
    both3 = sum(1 for x in range(p) if A_res[x] == 3 and B_res[x] == 3)
    pA, pB = A3 / p, B3 / p
    pAB = both3 / p
    contingency = Counter((A_res[x], B_res[x]) for x in range(p))
    return pA, pB, pAB, pA * pB, contingency


def verify_involution(p, roots_of):
    """The map x -> (p-x)%p sends the class c to the class (p-c)%p (since (-x)^3 +- (-x) = -(x^3 +- x)
    for both signs). For 3-root classes with c != 0 this pairs classes exactly (roots negate and swap
    order, bits complement and reverse, so k -> 3-k); the unique fixed class c=0 has no partner and is
    reported separately. Returns (#classes checked as an exact pair, list of any mismatches, roots of
    the c=0 class). A clean run (no mismatches) is an exact, non-heuristic confirmation of the pairing
    that forces n(k=1)=n(k=2) and n(k=0)=n(k=3) among the OTHER classes."""
    mismatches = []
    checked = 0
    for c, roots in roots_of.items():
        if len(roots) != 3 or c == 0:
            continue
        cp = (-c) % p
        roots2 = roots_of.get(cp, [])
        expected = sorted((p - x) % p for x in roots)
        if list(roots2) != expected:
            mismatches.append((c, cp, list(roots2), expected))
        else:
            checked += 1
    return checked, mismatches, roots_of.get(0, [])


def class_sizes_by_x(p, sign, roots_of):
    if sign == 1:
        return {x: len(roots_of[(x ** 3 + x) % p]) for x in range(p)}
    else:
        return {x: len(roots_of[(x ** 3 - x) % p]) for x in range(p)}


def run(p, out):
    def w(s=''):
        print(s)
        out.append(s)

    assert is_prime(p), f"{p} not prime"
    assert p % 3 == 2, f"{p} not == 2 mod 3"
    w(f"\n==================== p = {p}  (p mod 12 = {p % 12}, p mod 3 = {p % 3}) ====================")
    slope_data = {}
    for name, sign in (('antidiagonal  x^3+x=c  (slope -1 lines X+Y=const)', 1),
                        ('diagonal      x^3-x=c  (slope +1 lines X-Y=const)', -1)):
        d = analyze_slope(p, sign)
        slope_data[sign] = d
        nb = d['n_by_size']
        n0, n1, n2, n3 = nb.get(0, 0), nb.get(1, 0), nb.get(2, 0), nb.get(3, 0)
        w(f"\n-- {name} --")
        w(f"  classes by #roots: 0:{n0} ({n0/p:.4f})  1:{n1} ({n1/p:.4f})  2:{n2} ({n2/p:.4f})  3:{n3} ({n3/p:.4f})"
          f"   [n1+2n2+3n3={n1+2*n2+3*n3} == p={p}]")
        if n2:
            w(f"  ** {n2} double-root (ramification) classes -- excluded from the 3-root tabulation below **")
        kc, sc = d['k_counter'], d['shape_counter']
        w("  3-root classes by k = #{roots with bit=0}:  " +
          "  ".join(f"k={k}: {kc.get(k,0):4d} ({kc.get(k,0)/n3:.4f})" for k in (0, 1, 2, 3)))
        w("  3-root classes by shape:                    " +
          "  ".join(f"{s}: {sc.get(s,0):4d} ({sc.get(s,0)/n3:.4f})"
                     for s in ('(3,6,3)', '(1,4,5,2)', '(2,5,4,1)')))
        bc = d['bits_counter']
        w("  full (b1,b2,b3) bit-tuple counts (root order = ascending x): " +
          ", ".join(f"{bt}:{bc.get(bt,0)}" for bt in
                     ((0,0,0),(0,0,1),(0,1,0),(1,0,0),(0,1,1),(1,0,1),(1,1,0),(1,1,1))))
        checked, mism, c0roots = verify_involution(p, d['roots_of'])
        n3 = nb.get(3, 0)
        n3_excl_c0 = n3 - (1 if len(c0roots) == 3 else 0)
        status = "OK (exact)" if not mism else f"MISMATCH x{len(mism)}"
        c0info = f"c=0 has {len(c0roots)} root(s) {tuple(c0roots)}"
        if len(c0roots) == 3:
            c0info += (f", bits={tuple(bit_of(x, p, sign) for x in c0roots)}"
                       f", k={sum(1 for x in c0roots if bit_of(x, p, sign) == 0)}")
        w(f"  involution c<->-c check: {checked}/{n3_excl_c0} paired 3-root classes verified exact ({status}); {c0info}")
    # correlation between the two slopes at the same residue point x
    A_res = class_sizes_by_x(p, 1, slope_data[1]['roots_of'])
    B_res = class_sizes_by_x(p, -1, slope_data[-1]['roots_of'])
    pA, pB, pAB, prod, cont = correlation(p, A_res, B_res)
    w("\n-- correlation of the two slope-groups through the same residue point x (exact, full population x=0..p-1) --")
    w(f"  P(antidiag class has 3 roots) = {pA:.4f}    P(diag class has 3 roots) = {pB:.4f}")
    w(f"  P(both 3 roots) = {pAB:.4f}   P(A3)*P(B3) = {prod:.4f}   ratio P(both)/product = {pAB/prod if prod else float('nan'):.4f}")
    w("  contingency (size_antidiag,size_diag) -> count(x): " + ", ".join(f"{k}:{v}" for k, v in sorted(cont.items())))
    return slope_data


def main():
    ps = [int(a) for a in sys.argv[1:]] or DEFAULT_PS
    out = []

    def w(s=''):
        print(s)
        out.append(s)

    all_data = {}
    for p in ps:
        all_data[p] = run(p, out)

    w("\n\n==================== SUMMARY: shape proportions among 3-root classes vs p ====================")
    w(f"{'p':>6} | {'slope':<10} | {'n3':>5} | {'(3,6,3)':>9} | {'(1,4,5,2)':>10} | {'(2,5,4,1)':>10} || "
      f"{'n0/p':>7} {'n1/p':>7} {'n2/p':>7} {'n3/p':>7}")
    for p in ps:
        for sign, name in ((1, 'antidiag'), (-1, 'diag')):
            d = all_data[p][sign]
            nb = d['n_by_size']
            n0, n1, n2, n3 = nb.get(0, 0), nb.get(1, 0), nb.get(2, 0), nb.get(3, 0)
            sc = d['shape_counter']
            w(f"{p:>6} | {name:<10} | {n3:>5} | {sc.get('(3,6,3)',0)/n3:>9.4f} | {sc.get('(1,4,5,2)',0)/n3:>10.4f} | "
              f"{sc.get('(2,5,4,1)',0)/n3:>10.4f} || {n0/p:>7.4f} {n1/p:>7.4f} {n2/p:>7.4f} {n3/p:>7.4f}")
    w("\nnaive prediction if the 3 shift bits were i.i.d. fair coins:  (3,6,3): 0.2500   (1,4,5,2): 0.3750   (2,5,4,1): 0.3750")
    w("naive prediction for #roots (S3-Galois / random-cubic heuristic):  0-root: 0.3333   1-root: 0.5000   3-root: 0.1667")

    w("\n==================== SUMMARY: bit-tuple proportions among 3-root classes vs p ====================")
    tuples = ((0,0,0),(0,0,1),(0,1,0),(1,0,0),(0,1,1),(1,0,1),(1,1,0),(1,1,1))
    w(f"{'p':>6} | {'slope':<10} | " + " ".join(f"{str(t):>9}" for t in tuples))
    for p in ps:
        for sign, name in ((1, 'antidiag'), (-1, 'diag')):
            d = all_data[p][sign]
            n3 = d['n_by_size'].get(3, 0)
            bc = d['bits_counter']
            w(f"{p:>6} | {name:<10} | " + " ".join(f"{bc.get(t,0)/n3:>9.4f}" for t in tuples))
    w("naive i.i.d.-fair-coin prediction for EACH of the 8 tuples: 0.1250")

    w("\n==================== SUMMARY: cross-slope correlation vs p ====================")
    w(f"{'p':>6} | {'P(A3)':>7} {'P(B3)':>7} | {'P(both3)':>9} {'P(A3)*P(B3)':>12} {'ratio':>7}")
    for p in ps:
        A_res = class_sizes_by_x(p, 1, all_data[p][1]['roots_of'])
        B_res = class_sizes_by_x(p, -1, all_data[p][-1]['roots_of'])
        pA, pB, pAB, prod, cont = correlation(p, A_res, B_res)
        w(f"{p:>6} | {pA:>7.4f} {pB:>7.4f} | {pAB:>9.4f} {prod:>12.4f} {pAB/prod:>7.4f}")

    p0 = ps[0]
    w(f"\n\n==================== FULL PER-CLASS RECORDS, p={p0} (smallest p only; larger p summarised above) ====================")
    for sign, name in ((1, 'antidiagonal'), (-1, 'diagonal')):
        w(f"\n-- {name}, p={p0} -- (c, roots=ascending x, bits, k, shape)")
        for c, roots, bits, k in all_data[p0][sign]['records']:
            w(f"  c={c:4d}  roots={roots}  bits={bits}  k={k}  shape={SHAPE_OF_K[k]}")

    with open('slack/g_agents/group_types_output.txt', 'w') as f:
        f.write('\n'.join(out) + '\n')
    print("\n[wrote slack/g_agents/group_types_output.txt]")


if __name__ == '__main__':
    main()
