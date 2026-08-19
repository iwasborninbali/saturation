"""cell_volumes.py — Task C (t221 agents): exact 3-dim volumes of the sign cells for the 4-class residue-group
classification at k = -1 (pair_bound_notes.md sec. "24. T2.18", addendum "B.19"), and empirical validation by
direct enumeration of 4-class groups for p in {1009, 2003, 4001} (+ larger bonus primes).

MODEL.  A 4-class group of residue d (both quadratics solvable and non-degenerate) corresponds to a pair
(a,b) in F_p^* x F_p^* on the curve C0: a - 1/a + b + 1/b = 0 (mod p), with a^2 != -1, b^2 != 1
(hjsw_window.tex, Proposition prop:m8, proof; pair_bound_notes.md sec. 24, sec. 12).  Write X(u) in [-h,h]
(h=(p-1)/2) for the centred least-residue of u mod p, and set
    A1 = X(a),  A2 = X(1/a),  B1 = X(b),  B2 = X(1/b).
Fact (sec. 24, F1 / hjsw_window.tex Prop. prop:m8, proof): L := A1 - A2 + B1 + B2 is an EXACT multiple of p
with |L| <= 2p-2, hence L in {-p, 0, p}; put c := L/p.  The sigma-pair (a,-1/a) shares its centre iff
sign(A1) != sign(A2); the tau-pair (b,1/b) shares iff sign(B1) = sign(B2).  BOTH shared => the group is
(4,8,4) with one 8-point line (counted by m8); exactly ONE shared => (3,7,5,1) or (1,5,7,3) (m7); NEITHER
shared => (2,6,6,2) (m6) [pair_bound_notes.md sec. 24, "CLASSIFICATION"].

HEURISTIC VOLUME MODEL and its correct normalisation (see hjsw_window.tex, proof of Proposition
prop:m8asym, Steps 2-4).  That proof shows: as (a,b) ranges over C0(F_p) (a curve with |C0(F_p)| = p+O(sqrt p)
points, absolutely irreducible, Weil/Bombieri), the point x = (a, 1/a, b)/p mod 1 is equidistributed on the
3-torus (character sums S(h) = O(sqrt p) for every nonzero h, via Bombieri's bound on the non-constant
rational functions h.x restricted to C0).  Writing (u1,u2,u3) for the centred representative of x in the
open cube (-1/2,1/2)^3, this is *equidistribution w.r.t. the ordinary Lebesgue probability measure of the
cube (total mass 1)* -- NOT normalised to any single slice.  Every point of that open cube determines a
UNIQUE c in {-1,0,1} with u4 := c - u1 + u2 - u3 landing in (-1/2,1/2) (the three "which c" events tile the
cube up to a measure-zero boundary: this is exactly the L in {-p,0,p} trichotomy read on the torus), so
"equidistributed on the cube with mass 1" and "equidistributed on the union of the 3 hyperplane slices with
the SAME density on every slice, total mass 1" are the same statement -- no extra normalisation choice is
needed or available.  Proposition prop:m8asym only evaluates the sub-case "both shared" (4 of the 16 sign
patterns, volume 1/3 of the cube) because that's what m8 needs; this script evaluates the OTHER 12 patterns
(the "one shared" and "neither shared" cells) with the same exactness, to see whether the model predicts the
empirical (1/3,1/3,1/3) law of sec. 24 or something else ("the polytope volumes are computable — I have not
done it", sec. 24, last sentence).

EXACT COMPUTATION.  For a sign pattern s=(s1,s2,s3,s4) in {+1,-1}^4 and c in {-1,0,1},
  V(s,c) := 3-dim volume of { (u1,u2,u3) in (-1/2,1/2)^3 : sign(u_i)=s_i (i=1,2,3),
                              u4 := c-u1+u2-u3 has sign s4 and |u4| < 1/2 }        (measure du1 du2 du3).
Write u_i = s_i p_i (p_i = |u_i| in (0,1/2)) and eps = (-s1, s2, -s3) (coefficients of p1,p2,p3 in u4 - c):
u4 = c + eps.p, so the u4-condition is an interval condition alpha < eps.p < beta with
  (alpha,beta) = (-c, 1/2-c)   if s4 = +1
  (alpha,beta) = (-1/2-c, -c) if s4 = -1.
Substituting q_i = p_i if eps_i=+1, else q_i = 1/2-p_i (so q_i in (0,1/2) always and eps_i p_i = q_i - [eps_i=-1]/2)
turns eps.p into (sum q_i) - m/2 with m = #{i: eps_i=-1}, reducing V(s,c) to the volume of
{q in (0,1/2)^3 : sum(q) in J} for an interval J -- the CDF of a sum of 3 iid Uniform(0,1/2) variables, a
scaled Irwin-Hall distribution with the standard closed form (function F3 below).  Computed throughout with
fractions.Fraction: EXACT rational arithmetic, no floating point anywhere in the volume computation.

Self-checks built in (asserted at runtime): total volume over all 48 (pattern,c) cells is exactly 1; the
"both shared" total is exactly 1/3 (must match Proposition prop:m8asym / the proven m8 ~ p/12, N4 ~ p/4); each
of the four individual "both shared" volumes is exactly 1/12 (these are the four polytopes W_1..W_4 of the
Proposition's proof, Step 2, whose volumes 1/8 * Pr[...] = 1/8 * 2/3 = 1/12 are given explicitly there).

EMPIRICAL VALIDATION.  For a prime p: loop a in 1..p-1 (skip a^2 = -1, the degenerate case), d = a - 1/a mod p
(each valid non-degenerate d is hit by exactly two values of a, namely a and -1/a mod p; dedupe via a "seen d"
set so each residue/group is processed once); solve b^2+d*b+1=0 (i.e. b+1/b=-d) via Tonelli-Shanks, skipping
the degenerate discriminant (d=+-2) and the non-solvable case (discriminant a non-residue: this a does NOT
give a 4-class group at all -- only a 2-class one).  For every surviving group: compute (A1,A2,B1,B2), L, c,
sign pattern, and the (both/one/neither) cell; tabulate the joint (cell,c) distribution over N4 groups, and
(separately, using all 4 representative pairs (a,b) <-> (a,1/a) x (b,1/b) per group, matching Prop. prop:m8's
"each line arises from exactly four pairs") the full 16-pattern x 3-c distribution over 4*N4 pairs, for
comparison against the exact V(s,c) table.

usage: python3 slack/t221_agents/cell_volumes.py [p1 p2 p3 ...]      (default: 1009 2003 4001 20011 100003)
"""
import sys
import itertools
import math
from fractions import Fraction as Fr

HALF = Fr(1, 2)
PATTERNS = list(itertools.product((1, -1), repeat=4))   # (s1,s2,s3,s4), each +-1
CVALS = (-1, 0, 1)


# ---------------------------------------------------------------------------------------------------------
# Part 1: EXACT volumes
# ---------------------------------------------------------------------------------------------------------

def F3(t):
    """Exact 3-dim volume of {q in (0,HALF)^3 : sum(q) <= t}, for t a Fraction (any value; clipped)."""
    if t <= 0:
        return Fr(0)
    if t >= 3 * HALF:
        return HALF ** 3
    total = Fr(0)
    k = 0
    while k <= 3 and k * HALF <= t:
        total += Fr((-1) ** k * math.comb(3, k)) * (t - k * HALF) ** 3
        k += 1
    return total / 6


def slab_volume(eps, alpha, beta):
    """Volume of {p in (0,HALF)^3 : alpha < eps1*p1+eps2*p2+eps3*p3 < beta}, eps_i in {+1,-1}."""
    m = sum(1 for e in eps if e == -1)
    shift = m * HALF
    return F3(beta + shift) - F3(alpha + shift)


def cell_volume(s, c):
    """s=(s1,s2,s3,s4) sign pattern (each +-1), c in {-1,0,1}. Exact V(s,c), a Fraction."""
    s1, s2, s3, s4 = s
    eps = (-s1, s2, -s3)
    cF = Fr(c)
    if s4 == 1:
        alpha, beta = -cF, HALF - cF
    else:
        alpha, beta = -HALF - cF, -cF
    return slab_volume(eps, alpha, beta)


def sigma_shared(s):
    return s[0] != s[1]


def tau_shared(s):
    return s[2] == s[3]


def cell_name(s):
    sh, ta = sigma_shared(s), tau_shared(s)
    if sh and ta:
        return "both"
    if (not sh) and (not ta):
        return "neither"
    return "one"


def build_table():
    table = {}
    for s in PATTERNS:
        for c in CVALS:
            table[(s, c)] = cell_volume(s, c)
    return table


def aggregate(table):
    agg = {"both": Fr(0), "one": Fr(0), "neither": Fr(0)}
    agg_c = {(cell, c): Fr(0) for cell in ("both", "one", "neither") for c in CVALS}
    for (s, c), v in table.items():
        cell = cell_name(s)
        agg[cell] += v
        agg_c[(cell, c)] += v
    return agg, agg_c


def run_exact_checks(table, agg, agg_c):
    """Assertions tying the computation back to the proven facts; raises AssertionError on failure."""
    total = sum(table.values())
    assert total == Fr(1), f"total volume {total} != 1"
    assert agg["both"] == Fr(1, 3), f"V_both = {agg['both']} != 1/3 (contradicts Prop. prop:m8asym)"
    both_patterns = [s for s in PATTERNS if sigma_shared(s) and tau_shared(s)]
    assert len(both_patterns) == 4
    for s in both_patterns:
        nz = [(c, table[(s, c)]) for c in CVALS if table[(s, c)] != 0]
        assert len(nz) == 1, f"pattern {s} should be supported at exactly one c, got {nz}"
        c0, v0 = nz[0]
        assert v0 == Fr(1, 12), f"pattern {s} at c={c0}: volume {v0} != 1/12 (Prop. prop:m8, proof, Step 2)"
    # sanity: marginal over s4 at fixed (s1,s2,s3) and summed over c must recover 1/8 (one octant of the cube)
    for s123 in itertools.product((1, -1), repeat=3):
        tot = sum(table[((*s123, s4), c)] for s4 in (1, -1) for c in CVALS)
        assert tot == Fr(1, 8), f"octant {s123} total {tot} != 1/8"


# ---------------------------------------------------------------------------------------------------------
# Part 2: EMPIRICAL enumeration of 4-class groups
# ---------------------------------------------------------------------------------------------------------

def tonelli_shanks(n, p):
    """A square root of n mod p (odd prime p), or None if n is a non-residue. n=0 -> 0."""
    n %= p
    if n == 0:
        return 0
    if pow(n, (p - 1) // 2, p) != 1:
        return None
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(n, q, p), pow(n, (q + 1) // 2, p)
    while t != 1:
        i, temp = 0, t
        while temp != 1:
            temp = (temp * temp) % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = (b * b) % p
        t = (t * c) % p
        r = (r * b) % p
    return r


def X(u, p, h):
    u %= p
    return u if u <= h else u - p


def classify(A1, A2, B1, B2):
    s1 = 1 if A1 > 0 else -1
    s2 = 1 if A2 > 0 else -1
    s3 = 1 if B1 > 0 else -1
    s4 = 1 if B2 > 0 else -1
    return (s1, s2, s3, s4)


def empirical(p, fine=True):
    h = (p - 1) // 2
    seen = set()
    N4 = 0
    cell_c_counts = {(cell, c): 0 for cell in ("both", "one", "neither") for c in CVALS}
    pair_hist = {(s, c): 0 for s in PATTERNS for c in CVALS} if fine else None
    total_pairs = 0
    inv2 = pow(2, p - 2, p)
    for a in range(1, p):
        if (a * a) % p == p - 1:
            continue  # degenerate a: a^2 = -1 (sigma-fixed class)
        inva = pow(a, p - 2, p)
        d = (a - inva) % p
        if d in seen:
            continue
        seen.add(d)
        Db = (d * d - 4) % p
        if Db == 0:
            continue  # degenerate b: d = +-2
        sq = tonelli_shanks(Db, p)
        if sq is None:
            continue  # b-quadratic not solvable: not a 4-class group
        b1 = ((-d + sq) * inv2) % p
        b2 = ((-d - sq) * inv2) % p
        assert (b1 * b2) % p == 1 and (b1 + b2) % p == (-d) % p
        invb1 = pow(b1, p - 2, p)
        assert invb1 == b2
        assert b1 * b1 % p != 1 and b2 * b2 % p != 1  # non-degenerate (should be automatic since Db != 0)
        N4 += 1
        A1, A2 = X(a, p, h), X(inva, p, h)
        B1, B2 = X(b1, p, h), X(invb1, p, h)
        L = A1 - A2 + B1 + B2
        assert L % p == 0 and abs(L) <= p
        c = L // p
        assert c in CVALS
        s = classify(A1, A2, B1, B2)
        cell_c_counts[(cell_name(s), c)] += 1
        if fine:
            neg_inv_a = (-inva) % p
            for aa in (a, neg_inv_a):
                inv_aa = pow(aa, p - 2, p)
                for bb in (b1, invb1):
                    inv_bb = pow(bb, p - 2, p)
                    x1, x2, x3, x4 = X(aa, p, h), X(inv_aa, p, h), X(bb, p, h), X(inv_bb, p, h)
                    Lp = x1 - x2 + x3 + x4
                    assert Lp % p == 0 and abs(Lp) <= p
                    cp = Lp // p
                    sp = classify(x1, x2, x3, x4)
                    pair_hist[(sp, cp)] += 1
                    total_pairs += 1
    return dict(p=p, h=h, N4=N4, cell_c_counts=cell_c_counts, pair_hist=pair_hist, total_pairs=total_pairs)


# ---------------------------------------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------------------------------------

def fmt(fr):
    return f"{fr.numerator}/{fr.denominator}"


def print_exact_report(table, agg, agg_c):
    print("=" * 100)
    print("EXACT VOLUMES  V(s,c) = vol{ u in (-1/2,1/2)^3-slice-param : sign(u)=s, u4=c-u1+u2-u3 in (-1/2,1/2) }")
    print("s = (sign A1, sign A2, sign B1, sign B2);  sigma-shared = sign(A1)!=sign(A2); tau-shared = sign(B1)=sign(B2)")
    print("=" * 100)
    header = f"{'s1':>3}{'s2':>3}{'s3':>3}{'s4':>3}  {'cell':8}  {'c=-1':>10}  {'c=0':>10}  {'c=1':>10}  {'sum_c':>10}  (float sum_c)"
    print(header)
    for s in PATTERNS:
        cell = cell_name(s)
        vals = [table[(s, c)] for c in CVALS]
        tot = sum(vals)
        row = "".join(f"{'+' if x==1 else '-':>3}" for x in s)
        print(f"{row}  {cell:8}  {fmt(vals[0]):>10}  {fmt(vals[1]):>10}  {fmt(vals[2]):>10}  {fmt(tot):>10}  ({float(tot):.6f})")
    print("-" * 100)
    print("Per (cell,c) aggregate:")
    for cell in ("both", "one", "neither"):
        row = "  ".join(f"c={c}: {fmt(agg_c[(cell,c)]):>7}" for c in CVALS)
        print(f"  {cell:8} {row}   | total {fmt(agg[cell])}  ({float(agg[cell]):.6f})")
    grand = sum(agg.values())
    print(f"  {'TOTAL':8} {'':38}   | total {fmt(grand)}  ({float(grand):.6f})   [must be 1]")
    print("-" * 100)
    Vb, Vo, Vn = agg["both"], agg["one"], agg["neither"]
    # express V_both:V_one:V_neither as an integer ratio via a common denominator
    denom = Vb.denominator
    denom = denom * Vo.denominator // math.gcd(denom, Vo.denominator)
    denom = denom * Vn.denominator // math.gcd(denom, Vn.denominator)
    ib, io, iN = int(Vb * denom), int(Vo * denom), int(Vn * denom)
    gg = math.gcd(math.gcd(ib, io), iN)
    print(f"V_both : V_one : V_neither  =  {fmt(Vb)} : {fmt(Vo)} : {fmt(Vn)}  =  {ib//gg} : {io//gg} : {iN//gg}")
    print(f"  as decimals: {float(Vb):.6f} : {float(Vo):.6f} : {float(Vn):.6f}   (equal thirds would be 0.333333 each)")
    print(f"  V_one/2 (sigma-only)  vs  V_one/2 (tau-only): see breakdown below")
    sigma_only = sum(table[(s, c)] for s in PATTERNS for c in CVALS if sigma_shared(s) and not tau_shared(s))
    tau_only = sum(table[(s, c)] for s in PATTERNS for c in CVALS if (not sigma_shared(s)) and tau_shared(s))
    print(f"  sigma-only-shared = {fmt(sigma_only)} ({float(sigma_only):.6f}),  tau-only-shared = {fmt(tau_only)} ({float(tau_only):.6f})  [sum = V_one]")
    print("=" * 100)


def print_empirical_report(res, table, agg, agg_c):
    p, N4 = res["p"], res["N4"]
    print(f"\np = {p}:  N4 (4-class groups, one slope) = {N4}   N4/p = {N4/p:.5f}  (model/proved: 1/4 = {0.25:.5f})")
    m8 = sum(res["cell_c_counts"][("both", c)] for c in CVALS)
    m7 = sum(res["cell_c_counts"][("one", c)] for c in CVALS)
    m6 = sum(res["cell_c_counts"][("neither", c)] for c in CVALS)
    assert m8 + m7 + m6 == N4
    print(f"  m8 (both) = {m8:6d}  frac of N4 = {m8/N4:.5f}  (model {float(agg['both']):.5f})   m8/p = {m8/p:.5f}  (model*1/4 = {float(agg['both'])/4:.5f}, proved limit 1/12 = {1/12:.5f})")
    print(f"  m7 (one)  = {m7:6d}  frac of N4 = {m7/N4:.5f}  (model {float(agg['one']):.5f})   m7/p = {m7/p:.5f}  (model*1/4 = {float(agg['one'])/4:.5f})")
    print(f"  m6 (neither)={m6:5d}  frac of N4 = {m6/N4:.5f}  (model {float(agg['neither']):.5f})   m6/p = {m6/p:.5f}  (model*1/4 = {float(agg['neither'])/4:.5f})")
    print(f"  (1/3,1/3,1/3) empirical check: {m8/N4:.4f}, {m7/N4:.4f}, {m6/N4:.4f}  vs 0.3333, 0.3333, 0.3333")
    print("  breakdown by c (fraction of N4):")
    for cell in ("both", "one", "neither"):
        parts = "  ".join(f"c={c}:{res['cell_c_counts'][(cell,c)]/N4:.5f}(model {float(agg_c[(cell,c)]):.5f})" for c in CVALS)
        print(f"    {cell:8} {parts}")
    if res["pair_hist"] is not None:
        tp = res["total_pairs"]
        print(f"  fine (16-pattern x 3c) check over all {tp} representative pairs (= 4*N4):")
        maxdev = 0.0
        for s in PATTERNS:
            for c in CVALS:
                emp = res["pair_hist"][(s, c)] / tp
                mod = float(table[(s, c)])
                maxdev = max(maxdev, abs(emp - mod))
        print(f"    max |empirical_fraction - exact_volume| over all 48 cells = {maxdev:.5f}")


def main(argv):
    primes = [int(x) for x in argv] if argv else [1009, 2003, 4001, 20011, 100003]
    table = build_table()
    agg, agg_c = aggregate(table)
    run_exact_checks(table, agg, agg_c)
    print("All exact self-checks passed (total volume = 1; V_both = 1/3; the four W_i = 1/12 each; octant totals = 1/8).")
    print_exact_report(table, agg, agg_c)
    for p in primes:
        res = empirical(p, fine=(p <= 20011))
        print_empirical_report(res, table, agg, agg_c)


if __name__ == "__main__":
    main(sys.argv[1:])
