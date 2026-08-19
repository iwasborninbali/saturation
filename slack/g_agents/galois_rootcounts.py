#!/usr/bin/env python3
"""galois_rootcounts.py (agent: galois_rootcounts) -- checks supporting the theory report
docs/research/g_agents/galois_rootcounts.md.  Read that file for the full derivations; this
script only contains the numerical/symbolic-rational verifications cited there.

Five independent checks, all for f(t) = t^k, k in {5,7} odd prime (background: read
docs/research/permutation_cubic_note.md sections 0-3 first -- this script assumes that model).

  (1) TRINOMIAL DISCRIMINANT / SIMPLE-BRANCHING CHECK.  Claim: disc_x(x^k - x - T), as a
      polynomial in T, equals +-(k^k T^{k-1} - (k-1)^{k-1}) exactly (trinomial discriminant
      formula), so its k-1 roots (= the critical values of x -> x^k-x) are exactly the
      (k-1)-th roots of (k-1)^{k-1}/k^k, hence PAIRWISE DISTINCT whenever p does not divide
      k(k-1) (separability of x^{k-1} = const).  Checked directly and more strongly than via
      the discriminant formula: compute the k-1 critical points (roots of k x^{k-1} = 1 mod p)
      by brute force, verify they are k-1 DISTINCT field elements, verify each critical value
      c_i = x_i^k - x_i satisfies c_i^{k-1} == (k-1)^{k-1} * k^{-k} (mod p) exactly, and verify
      the k-1 critical VALUES are pairwise distinct.  This is the fact that feeds Jordan's
      theorem (transitive + primitive [k prime] + a transposition [simple branch point] = S_k).

  (2) CHEBOTAREV / CYCLE-TYPE CHECK (the strong form of "Galois group = S_k").  For random c,
      factor x^k - x - c over F_p via distinct-degree factorization (Cantor-Zassenhaus DDF,
      implemented from scratch below -- no external CAS), recording the cycle type (partition
      of k given by the degrees of the irreducible factors).  By the standard dictionary
      between factorization patterns and Frobenius cycle type, if Gal = S_k acting naturally,
      the empirical cycle-type distribution over random c should match the S_k conjugacy-class
      distribution (rencontres numbers are just the "number of 1's in the cycle type" marginal
      of this same check -- this is a strictly stronger test).

  (3) ROOT-COUNT DISTRIBUTION (the rencontres-numbers marginal of (2)), direct O(p) count, for
      completeness / cross-reference with agent x5_x7_numerics's independent numerics.

  (4) COST CONSTANT C(P) = lim cost/(2p) for the generalized ">=4-line + singletons" cover of
      section 2 of the background note, computed EXACTLY (fractions.Fraction) from the local
      law (rencontres P_k' + uniform n0|k' + slope-independence).  Verified to reproduce 11/8
      exactly at k=3 (Theorem G3.5), then evaluated at k=5,7.  Derived independently in this
      file (see docs/research/g_agents/galois_rootcounts.md Part 3 for the derivation); the
      numbers are cross-checked against slack/g_agents/x5_x7_numerics_exact_constant.py's
      independently-coded version of the same computation (not imported -- this file does not
      read or modify that one; the match is reported as a consistency check only).

  (5) GENUS OF THE PAIRWISE FIBRE PRODUCT X_2 = {(t1,t2,c): t_i^k-t_i=c, t1!=t2} (the curve
      whose Weil bound drives the pairwise equidistribution of Part 2 of the report; the k=3
      case is the conic Q_+ of the background note).  Riemann-Hurwitz formula genus computed
      by hand in the report: g_2 = (k-2)(k-3)/2.  Checked here by directly counting F_p-points
      of the affine model and comparing |N - p| to the Weil-bound order of magnitude 2*g_2*sqrt(p)
      (a consistency check, not a proof -- affine point counts differ from the smooth projective
      model by O(1) boundary terms which the check absorbs into a generous constant).

Usage: /Users/iwasborninbali/venvs/sat/bin/python3 slack/g_agents/galois_rootcounts.py
Output printed to stdout and saved verbatim to slack/g_agents/galois_rootcounts_output.txt
"""
import sys
import random
from fractions import Fraction
from math import comb, gcd, isqrt

random.seed(20260819)

OUT_LINES = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT_LINES.append(s)


# ============================================================== basic utilities

def is_prime(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31):
        if n % q == 0:
            return n == q
    i = 37
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def primes_in_range(lo, hi):
    return [n for n in range(lo, hi) if is_prime(n)]


# ============================================================== (0) rencontres numbers

def derangements(n):
    D = [1, 0]
    for i in range(2, n + 1):
        D.append((i - 1) * (D[-1] + D[-2]))
    return D


def rencontres_P(k):
    """Exact Fraction list P[0..k]: P[j] = P(uniform random permutation of k letters has
    exactly j fixed points) = C(k,j) D_{k-j} / k! ."""
    D = derangements(k)
    fact_k = 1
    for i in range(1, k + 1):
        fact_k *= i
    return [Fraction(comb(k, j) * D[k - j], fact_k) for j in range(k + 1)]


def partitions(n):
    """All integer partitions of n, as sorted tuples (descending)."""
    def helper(n, maxpart):
        if n == 0:
            yield ()
            return
        for p in range(min(n, maxpart), 0, -1):
            for rest in helper(n - p, p):
                yield (p,) + rest
    return list(helper(n, n))


def conjugacy_class_prob(k, parts):
    """Probability a uniform random permutation of k letters has cycle type `parts`
    (a partition of k, as a tuple of part sizes, multiplicities counted from the tuple)."""
    from collections import Counter
    cnt = Counter(parts)
    fact_k = 1
    for i in range(1, k + 1):
        fact_k *= i
    denom = 1
    for part, mult in cnt.items():
        denom *= (part ** mult)
        f = 1
        for i in range(1, mult + 1):
            f *= i
        denom *= f
    return Fraction(fact_k, denom * fact_k)  # class size / k!  == 1/denom


# ============================================================== (1) critical points / discriminant check

def modinv(a, p):
    return pow(a, p - 2, p)


def kth_power_roots_of_unity_like(k, invk, p):
    """Brute-force roots of x^(k-1) == invk (mod p), i.e. the critical points of x -> x^k-x
    (roots of k*x^(k-1) = 1).  O(p); k,p small enough here that this is instant and has zero
    room for a factoring bug (unlike a Tonelli-Shanks-type root extractor)."""
    target = invk
    e = k - 1
    return [x for x in range(1, p) if pow(x, e, p) == target]


def check_discriminant(k, primes):
    P(f"\n=== (1) Trinomial-discriminant / simple-branching check, k={k} ===")
    P(f"Claim: disc_x(x^{k}-x-T) = +-(k^k T^(k-1) - (k-1)^(k-1)), so the k-1 critical values")
    P(f"of x -> x^{k}-x are exactly the (k-1)=th roots of (k-1)^(k-1)/k^k, pairwise distinct")
    P(f"whenever p does not divide k*(k-1) = {k*(k-1)}.")
    all_ok = True
    for p in primes:
        invk = modinv(k, p)
        const = (pow(k - 1, k - 1, p) * pow(invk, k, p)) % p  # (k-1)^(k-1) / k^k mod p
        crit_pts = kth_power_roots_of_unity_like(k, invk, p)
        n_expected = k - 1
        distinct_pts_ok = (len(crit_pts) == n_expected) and (len(set(crit_pts)) == n_expected)
        crit_vals = [(pow(x, k, p) - x) % p for x in crit_pts]
        vals_distinct = (len(set(crit_vals)) == n_expected)
        formula_ok = all(pow(v, k - 1, p) == const for v in crit_vals)
        ok = distinct_pts_ok and vals_distinct and formula_ok
        all_ok &= ok
        P(f"  p={p:5d}: #critical points={len(crit_pts)} (want {n_expected}, distinct={distinct_pts_ok});"
          f" #distinct critical VALUES={len(set(crit_vals))} (distinct={vals_distinct});"
          f" formula v^(k-1)==(k-1)^(k-1)/k^k for all v: {formula_ok}   -> {'OK' if ok else 'FAIL'}")
    P(f"  ALL {'PASS' if all_ok else 'FAIL'} for k={k} at primes {primes}")
    return all_ok


# ============================================================== (2) polynomial arithmetic mod p, DDF

def pdeg(a):
    for i in range(len(a) - 1, -1, -1):
        if a[i] % 1 != 0:
            pass
        if a[i]:
            return i
    return -1  # zero polynomial


def ptrim(a, p):
    a = [c % p for c in a]
    d = pdeg(a)
    return a[:d + 1] if d >= 0 else [0]


def padd(a, b, p):
    n = max(len(a), len(b))
    r = [0] * n
    for i, c in enumerate(a):
        r[i] = (r[i] + c) % p
    for i, c in enumerate(b):
        r[i] = (r[i] + c) % p
    return ptrim(r, p)


def psub(a, b, p):
    n = max(len(a), len(b))
    r = [0] * n
    for i, c in enumerate(a):
        r[i] = (r[i] + c) % p
    for i, c in enumerate(b):
        r[i] = (r[i] - c) % p
    return ptrim(r, p)


def pmul(a, b, p):
    da, db = pdeg(a), pdeg(b)
    if da < 0 or db < 0:
        return [0]
    r = [0] * (da + db + 1)
    for i in range(da + 1):
        if a[i] == 0:
            continue
        ai = a[i]
        for j in range(db + 1):
            r[i + j] = (r[i + j] + ai * b[j]) % p
    return ptrim(r, p)


def pdivmod(a, b, p):
    """Return (q, r) with a = q*b + r, deg r < deg b.  b must be nonzero."""
    a = ptrim(a, p)
    b = ptrim(b, p)
    db = pdeg(b)
    if db < 0:
        raise ZeroDivisionError
    inv_lead = modinv(b[db], p)
    rem = a[:]
    q = [0] * max(1, pdeg(a) - db + 1) if pdeg(a) >= db else [0]
    while True:
        dr = pdeg(rem)
        if dr < db:
            break
        coeff = (rem[dr] * inv_lead) % p
        shift = dr - db
        if shift >= len(q):
            q += [0] * (shift - len(q) + 1)
        q[shift] = (q[shift] + coeff) % p
        # rem -= coeff * x^shift * b
        for i in range(db + 1):
            if b[i]:
                idx = i + shift
                rem[idx] = (rem[idx] - coeff * b[i]) % p
        rem = ptrim(rem, p)
        if pdeg(rem) < 0:
            rem = [0]
            break
    return ptrim(q, p), ptrim(rem, p)


def pmod(a, b, p):
    return pdivmod(a, b, p)[1]


def pgcd(a, b, p):
    a, b = ptrim(a, p), ptrim(b, p)
    while pdeg(b) >= 0:
        a, b = b, pmod(a, b, p)
    d = pdeg(a)
    if d < 0:
        return [0]
    inv_lead = modinv(a[d], p)
    return ptrim([c * inv_lead % p for c in a], p)


def ppowmod(base, e, mod_poly, p):
    """base^e mod (mod_poly, p), square-and-multiply."""
    result = [1]
    b = pmod(base, mod_poly, p)
    while e > 0:
        if e & 1:
            result = pmod(pmul(result, b, p), mod_poly, p)
        b = pmod(pmul(b, b, p), mod_poly, p)
        e >>= 1
    return ptrim(result, p)


def ddf_cycle_type(f, p):
    """Distinct-degree factorization of squarefree monic f mod p.  Returns sorted tuple of
    irreducible-factor degrees (= cycle type of Frobenius at this point, if f = char. poly of
    Frobenius acting on the k roots of the defining trinomial). f must be squarefree; caller
    checks via gcd(f,f')==1 and skips degenerate c."""
    k = pdeg(f)
    f_cur = ptrim(f, p)
    degs = []
    d = 1
    xpoly = [0, 1]
    while pdeg(f_cur) >= 1 and d <= k:
        h = ppowmod(xpoly, p ** d, f, p)          # x^(p^d) mod ORIGINAL f (see docstring: valid)
        diff = psub(h, xpoly, p)
        g = pgcd(f_cur, diff, p)
        dg = pdeg(g)
        if dg >= 1:
            assert dg % d == 0, (dg, d, g)
            degs += [d] * (dg // d)
            f_cur, r = pdivmod(f_cur, g, p)
            assert pdeg(r) < 0 or r == [0]
        d += 1
    if pdeg(f_cur) >= 1:
        degs.append(pdeg(f_cur))  # leftover factor of its own (necessarily prime, unreached) degree
    return tuple(sorted(degs))


def is_squarefree(f, p):
    d = [i * f[i] % p for i in range(1, len(f))]
    d = ptrim([0] + d[1:], p) if False else ptrim(d, p)
    # derivative: coeff of x^(i-1) in f' is i*f[i]
    fp = ptrim([(i * f[i]) % p for i in range(1, len(f))], p)
    if pdeg(fp) < 0:
        return False
    g = pgcd(f, fp, p)
    return pdeg(g) <= 0


def check_chebotarev_cycletype(k, p, n_samples, rng):
    """Sample n_samples random c in F_p, factor x^k - x - c via DDF, tabulate cycle type,
    compare to S_k conjugacy-class distribution."""
    from collections import Counter
    parts_all = partitions(k)
    theory = {parts: conjugacy_class_prob(k, parts) for parts in parts_all}
    emp = Counter()
    used = 0
    skipped = 0
    cs = rng.sample(range(p), min(n_samples, p))
    for c in cs:
        f = [(-c) % p, (p - 1) % p] + [0] * (k - 2) + [1]  # -c - x + 0*x^2+...+x^k  (coeff of x^1 is -1)
        f = ptrim(f, p)
        if not is_squarefree(f, p):
            skipped += 1
            continue
        ct = ddf_cycle_type(f, p)
        assert sum(ct) == k, (ct, k, c)
        emp[ct] += 1
        used += 1
    P(f"  p={p}: sampled {len(cs)} c-values, {used} squarefree (skipped {skipped} with a repeated root)")
    P(f"  {'cycle type':<18}{'theory P':>12}{'theory %':>10}{'empirical':>12}{'emp %':>10}")
    total_abs_err = Fraction(0)
    for parts in sorted(parts_all, key=lambda t: (-len(t), t)):
        th = theory[parts]
        e = emp.get(parts, 0)
        emp_frac = Fraction(e, used) if used else Fraction(0)
        total_abs_err += abs(th - emp_frac)
        P(f"  {str(parts):<18}{str(th):>12}{float(th)*100:>9.2f}%{e:>12}{float(emp_frac)*100:>9.2f}%")
    P(f"  sum |theory - empirical| over all {len(parts_all)} cycle types = {float(total_abs_err):.4f}"
      f"  (statistical noise scale ~ 1/sqrt({used}) = {1/max(used,1)**0.5:.3f})")
    return used, total_abs_err


# ============================================================== (3) root-count distribution (direct)

def root_count_distribution(k, p):
    from collections import Counter
    cnt = Counter()
    for x in range(p):
        c = (pow(x, k, p) - x) % p
        cnt[c] += 1
    dist = Counter()
    for c in range(p):
        dist[cnt.get(c, 0)] += 1
    return dist  # dist[j] = #{c : exactly j roots}


def check_root_counts(k, primes):
    P(f"\n=== (3) Root-count distribution vs rencontres law, k={k} ===")
    renc = rencontres_P(k)
    P(f"  rencontres P_j (S_{k}, exact): " + ", ".join(f"{j}:{renc[j]}({float(renc[j]):.4f})" for j in range(k + 1)))
    for p in primes:
        dist = root_count_distribution(k, p)
        P(f"  p={p}: " + ", ".join(f"{j}:{dist.get(j,0)}({dist.get(j,0)/p:.4f})" for j in range(k + 1))
          + f"   [check sum j*n_j == p: {sum(j*dist.get(j,0) for j in range(k+1))} == {p}]")


# ============================================================== (4) exact cost constant C(P)

def bigcounts(j, m):
    """L1..L4 = counts on the four consecutive +-1 lines owned by a class with j roots,
    n0=m of class 0, n1=j-m of class 1: (n0, 2n0+n1, n0+2n1, n1)."""
    n0, n1 = m, j - m
    return (n0, 2 * n0 + n1, n0 + 2 * n1, n1)


def E_lines_per_class(k):
    """E[# of the 4 lines owned by a random class that have >=4 points], ONE slope."""
    renc = rencontres_P(k)
    tot = Fraction(0)
    for j in range(0, k + 1):
        if renc[j] == 0 or j == 0:
            continue
        s = 0
        for m in range(0, j + 1):
            L = bigcounts(j, m)
            s += sum(1 for v in L if v >= 4)
        tot += renc[j] * Fraction(s, j + 1)
    return tot


def slope_states(k):
    """All (j, m, class, weight) states for ONE slope at a size-biased ("owned by residue x")
    random residue x: weight = P(x's class has j roots) * P(that class has n0=m | j) *
    P(x itself is class `class` | j, m).  Sums to 1.  j ranges 1..k (x is always a root of its
    own class, so j=0 never occurs at a residue)."""
    renc = rencontres_P(k)
    states = []
    for j in range(1, k + 1):
        if renc[j] == 0:
            continue
        sb = renc[j] * j  # size-biased weight for this j (sum_j j*P_j == 1 always, E[fixed pts]=1)
        for m in range(0, j + 1):
            w_jm = sb * Fraction(1, j + 1)
            if m > 0:
                states.append((j, m, 0, w_jm * Fraction(m, j)))
            if j - m > 0:
                states.append((j, m, 1, w_jm * Fraction(j - m, j)))
    return states


def covered_plus(cls, n0, n1, d, e):
    """slope +1 lines L1..L4 = (n0, 2n0+n1, n0+2n1, n1).  Returns whether the lift (d,e) of a
    root of this class (class `cls`) lies on a line with >=4 points."""
    L1, L2, L3, L4 = n0, 2 * n0 + n1, n0 + 2 * n1, n1
    if cls == 0:
        # (0,0)&(1,1) -> L2 ; (0,1) -> L3 ; (1,0) -> L1
        if d == e:
            return L2 >= 4
        return (L3 >= 4) if (d, e) == (0, 1) else (L1 >= 4)
    else:
        # (0,0)&(1,1) -> L3 ; (0,1) -> L4 ; (1,0) -> L2
        if d == e:
            return L3 >= 4
        return (L4 >= 4) if (d, e) == (0, 1) else (L2 >= 4)


def covered_minus(cls, n0, n1, d, e):
    """slope -1 lines M1..M4 = (n0, 2n0+n1, n0+2n1, n1) (same formula, different routing)."""
    M1, M2, M3, M4 = n0, 2 * n0 + n1, n0 + 2 * n1, n1
    if cls == 0:
        # (0,0) -> M1 ; mixed (0,1)&(1,0) -> M2 ; (1,1) -> M3
        if (d, e) == (0, 0):
            return M1 >= 4
        if (d, e) == (1, 1):
            return M3 >= 4
        return M2 >= 4
    else:
        # (0,0) -> M2 ; mixed -> M3 ; (1,1) -> M4
        if (d, e) == (0, 0):
            return M2 >= 4
        if (d, e) == (1, 1):
            return M4 >= 4
        return M3 >= 4


def E_singleton_lifts_per_residue(k):
    """E[# of x's 4 lifts covered by NEITHER slope's >=4-line set], combining independent
    slope+/slope- states."""
    states = slope_states(k)
    wsum = sum(w for *_, w in states)
    assert wsum == 1, (k, wsum)
    lifts = [(d, e) for d in (0, 1) for e in (0, 1)]
    total = Fraction(0)
    for (jp, mp, cp, wp) in states:
        n0p, n1p = mp, jp - mp
        for (jm, mm, cm, wm) in states:
            n0m, n1m = mm, jm - mm
            w = wp * wm
            survive = sum(1 for (d, e) in lifts
                          if not covered_plus(cp, n0p, n1p, d, e)
                          and not covered_minus(cm, n0m, n1m, d, e))
            total += w * survive
    return total


def cost_constant(k):
    eL = E_lines_per_class(k)
    eU = E_singleton_lifts_per_residue(k)
    C = 2 * eL + eU / 2   # = (4*eL + eU)/2 ; L4=2p*eL both slopes, U=p*eU, cost=2L4+U=p(4eL+eU)
    return eL, eU, C


def run_cost_constant():
    P("\n=== (4) Exact cost constant C(P) = lim cost/(2p), own independent derivation ===")
    P("  cost = 2*L4 + U ; L4 = 2p*E[lines/class] (both slopes) ; U = p*E[singleton lifts/residue]")
    P("  C(P) = 2*E[lines/class] + E[singleton lifts/residue]/2")
    for k in (3, 5, 7):
        eL, eU, C = cost_constant(k)
        tag = "  <- must equal 11/8 exactly (Theorem G3.5)" if k == 3 else ""
        P(f"  k={k}: E[lines/class]={eL}  E[singletons/residue]={eU}  C(P)={C} = {float(C):.6f}{tag}")
    return {k: cost_constant(k) for k in (3, 5, 7)}


# ============================================================== (5) genus of pairwise fibre product

def genus_X2(k):
    return Fraction((k - 2) * (k - 3), 2)


def count_X2_points(k, p):
    """N2 = #{(t1,t2) in F_p^2 : t1 != t2, t1^k - t1 == t2^k - t2}.  O(p) via bucketing."""
    from collections import Counter
    cnt = Counter()
    for t in range(p):
        cnt[(pow(t, k, p) - t) % p] += 1
    N2 = sum(v * (v - 1) for v in cnt.values())  # ordered pairs, v choose ordered-distinct-pairs
    return N2


def check_genus(k, primes):
    P(f"\n=== (5) Genus of pairwise fibre product X_2, k={k}: g_2=(k-2)(k-3)/2 = {genus_X2(k)} ===")
    g2 = genus_X2(k)
    for p in primes:
        N2 = count_X2_points(k, p)
        dev = N2 - p * (p - 1) // p * 1  # placeholder, real comparison below
        # X_2 affine point count ~ k(k-1)/k * p... actually leading term: for each of the p
        # values of c, expected #ordered pairs of distinct roots ~ E[j(j-1)] over rencontres j.
        renc = rencontres_P(k)
        Ejj1 = sum(renc[j] * j * (j - 1) for j in range(k + 1))
        pred_leading = float(Ejj1) * p
        bound = 2 * float(g2) * (p ** 0.5) + 6 * k * (p ** 0.5)  # generous slack for affine/infinity terms
        P(f"  p={p}: N2={N2}  E[j(j-1)]*p (leading term)={pred_leading:.1f}  "
          f"|N2-pred|={abs(N2-pred_leading):.1f}  generous O(sqrt p) budget~{bound:.1f}  "
          f"{'OK' if abs(N2-pred_leading) <= bound else 'CHECK'}")


# ============================================================== main

def main():
    rng = random.Random(20260819)

    # sanity: k=3 rencontres must match the note's stated (1/3, 1/2, 0, 1/6)
    renc3 = rencontres_P(3)
    P("=== (0) sanity: rencontres numbers of S_3 vs background note's stated cubic law ===")
    P(f"  computed: {renc3}  (note states 1/3, 1/2, 0, 1/6 for k=0,1,2,3)")
    assert renc3 == [Fraction(1, 3), Fraction(1, 2), Fraction(0), Fraction(1, 6)]
    P("  MATCH.")

    for k in (5, 7):
        renc = rencontres_P(k)
        P(f"\nRencontres numbers of S_{k} (exact): " + ", ".join(f"P_{j}={renc[j]}" for j in range(k + 1)))

    primes5 = [p for p in primes_in_range(500, 2001) if gcd(5, p - 1) == 1 and p % 5 != 0]
    primes7 = [p for p in primes_in_range(500, 2001) if gcd(7, p - 1) == 1 and p % 7 != 0]
    sample5 = [primes5[0], primes5[len(primes5)//2], primes5[-1]]
    sample7 = [primes7[0], primes7[len(primes7)//2], primes7[-1]]
    P(f"\n#primes in [500,2000] usable for k=5 (gcd(5,p-1)=1): {len(primes5)}; sample used: {sample5}")
    P(f"#primes in [500,2000] usable for k=7 (gcd(7,p-1)=1): {len(primes7)}; sample used: {sample7}")

    ok5 = check_discriminant(5, sample5)
    ok7 = check_discriminant(7, sample7)

    P("\n=== (2) Chebotarev cycle-type check (Galois group = S_k, strong form) ===")
    for k, sample in ((5, sample5[:2]), (7, sample7[:2])):
        P(f"\n-- k={k} --")
        for p in sample:
            check_chebotarev_cycletype(k, p, n_samples=min(400, p), rng=rng)

    check_root_counts(5, sample5)
    check_root_counts(7, sample7)

    consts = run_cost_constant()

    check_genus(5, sample5)
    check_genus(7, sample7)

    P("\n=== SUMMARY ===")
    P(f"  discriminant/simple-branching check: k=5 {'PASS' if ok5 else 'FAIL'}, k=7 {'PASS' if ok7 else 'FAIL'}")
    for k in (5, 7):
        eL, eU, C = consts[k]
        P(f"  k={k}: C(P) = {C}  ~= {float(C):.6f}")
    P("  (cross-check target, from slack/g_agents/x5_x7_numerics_exact_constant.py, computed")
    P("   independently by a different agent: k=5 -> 12059/8640 ~= 1.395718; k=7 -> 203347/145152 ~= 1.400925)")

    with open(__file__.replace(".py", "_output.txt"), "w") as f:
        f.write("\n".join(OUT_LINES) + "\n")


if __name__ == "__main__":
    main()
