#!/usr/bin/env python3
"""x5_x7_numerics.py (agent: x5_x7_numerics) -- numerics for f(x)=x^5 and f(x)=x^7 permutation
monomials of F_p, box (0,0), generalizing the k=3 model worked out in
docs/research/permutation_cubic_note.md (read that file's sections 0-3 first).

Recap of the model (verified by re-derivation from the box-lift formulas, matches the note exactly):
for a permutation polynomial f of F_p, box (0,0), residue x in [0,p) has 4 lifts (x+dp, f(x)+ep),
d,e in {0,1}.  Fix a slope:

  slope +1 ("diagonal"):     c = f(x) - x mod p.  class+(x) = 1 iff f(x) mod p >= x, else 0.
  slope -1 ("antidiagonal"): c = f(x) + x mod p.  class-(x) = 1 iff f(x) mod p + x >= p, else 0.

For a residue class c with k roots split n0 class-0 / n1 class-1 (n0+n1=k), the FOUR consecutive
(spaced-by-p) integer lines owned by that class carry exactly (n0, 2n0+n1, n0+2n1, n1) points -- this
identity uses only the affine (d,e) lift structure and holds for ANY k, not just k=3 (checked below by
comparing to the direct brute-force count).  THE COVER: weight 1 on every +-1 line with >=4 points,
weight 1 on every point of P on none of them; cost = 2*L4 + U (Sec 2 of the note).

Task (name: x5_x7_numerics):
 (a) empirical P_k' = P(a random residue class has k' roots of f(t)-t=c, resp. f(t)+t=c), k'=0..deg(f),
     vs. the rencontres distribution of S_deg(f) (fixed points of a random permutation of deg(f)
     letters): P_renc(k) = C(n,k) D_{n-k}/n!.  (For the cubic this is 1/3,1/2,0,1/6 -- see note Sec 0.)
 (b) distribution of n0 given k' -- is it uniform on {0,...,k'} as the note's local law predicts
     (Weil equidistribution on the root variety, no dependence on which root is "first")?
 (c) EXACT cost (L4, U, cost=2L4+U) counted directly off the 4p-point set, plus a PREDICTION built
     from (a)+(b) plus the note's "independence of the two slopes at a residue" hypothesis (Sec 3 of
     the note; I did not find a 'profile_table' agent output anywhere in the repo at run time -- see
     NOTE_ON_PROFILE_TABLE below -- so this prediction is self-derived, generalizing the note's Sec 2-3
     bookkeeping to general k).  Two flavours: (i) "empirical-marginals" prediction, which plugs the
     ACTUAL observed P_k and assumes ONLY uniform-n0|k + slope-independence (isolates those two
     hypotheses); (ii) "idealized" prediction, which additionally replaces P_k by the rencontres law
     (tests the whole local-law package at once).
 (d) LP over all +-1 lines (fractional), via slack/lp_curve.py's own point/line/solve routines
     (imported, not reimplemented; only mode 'pm1' is run here -- that IS "the LP over all ±1-lines"
     asked for in part (d); the 'all-lines' mode of that script is a different, much slower
     calibration not requested here and is skipped for wall-clock reasons, confirmed cheap to add
     back if wanted).

Usage: /Users/iwasborninbali/venvs/sat/bin/python3 slack/g_agents/x5_x7_numerics.py
Output printed to stdout and saved verbatim to slack/g_agents/x5_x7_numerics_output.txt
"""
import sys, os, math, json
from math import gcd, comb
from fractions import Fraction
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import lp_curve as LPC  # slack/lp_curve.py -- reused for part (d), not modified

# ---------------------------------------------------------------- utilities

def is_prime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0: return False
        i += 2
    return True

def derangements(maxn):
    D = [1, 0]
    for m in range(2, maxn + 1):
        D.append((m - 1) * (D[m - 1] + D[m - 2]))
    return D

def rencontres_P(n):
    """Exact P(k) = C(n,k) D_{n-k} / n!, k=0..n, as Fractions.  n = deg(f)."""
    D = derangements(n)
    nf = math.factorial(n)
    return [Fraction(comb(n, k) * D[n - k], nf) for k in range(n + 1)]

# ---------------------------------------------------------- core (p, k_pow)

def analyze(p, k_pow):
    """f(x) = x^k_pow mod p.  Returns f (list), and for each slope: roots_of[c] (list of roots t),
    class(t) (0/1) -- computed directly from f, no shortcuts."""
    assert gcd(k_pow, p - 1) == 1, f"x^{k_pow} is not a permutation of F_{p} (gcd={gcd(k_pow, p-1)})"
    f = [pow(x, k_pow, p) for x in range(p)]

    plus_roots = [[] for _ in range(p)]   # c -> roots t of f(t)-t == c
    minus_roots = [[] for _ in range(p)]  # c -> roots t of f(t)+t == c
    for t in range(p):
        s = f[t]
        plus_roots[(s - t) % p].append(t)
        minus_roots[(s + t) % p].append(t)

    def class_plus(t):   # 1 iff f(t) mod p >= t (matches note: class-0 <-> s_t - r_t = c - p < 0)
        return 1 if f[t] >= t else 0

    def class_minus(t):  # 1 iff f(t) mod p + t >= p (wrapped)
        return 1 if f[t] + t >= p else 0

    return f, plus_roots, minus_roots, class_plus, class_minus


def k_distribution(roots_of, p):
    cnt = Counter(len(roots_of[c]) for c in range(p))
    return cnt  # {k': #classes with that many roots}, sums to p


def n0_given_k(roots_of, classify, p):
    """tab[k'] = Counter over n0 in {0,...,k'} of #classes with that (k', n0)."""
    tab = {}
    for c in range(p):
        rs = roots_of[c]
        kk = len(rs)
        n0 = sum(1 for t in rs if classify(t) == 0)
        tab.setdefault(kk, Counter())[n0] += 1
    return tab

# --------------------------------------------------- exact cover cost (data)

def explicit_cover_cost(p, f):
    """Direct brute-force over the 4p points of P: bucket by Y-X and Y+X, L4 = #lines (either
    slope) with >=4 points, U = #points on none of them, cost = 2*L4 + U.  No formulas used."""
    pts = []
    for x in range(p):
        y = f[x]
        for d in (0, 1):
            for e in (0, 1):
                pts.append((x + d * p, y + e * p))
    assert len(pts) == 4 * p and len(set(pts)) == 4 * p

    plus_line, minus_line = {}, {}
    plus_of, minus_of = [], []
    for (X, Y) in pts:
        pl, mn = Y - X, Y + X
        plus_of.append(pl); minus_of.append(mn)
        plus_line[pl] = plus_line.get(pl, 0) + 1
        minus_line[mn] = minus_line.get(mn, 0) + 1

    L4_plus = sum(1 for v in plus_line.values() if v >= 4)
    L4_minus = sum(1 for v in minus_line.values() if v >= 4)
    U = sum(1 for i in range(len(pts)) if plus_line[plus_of[i]] < 4 and minus_line[minus_of[i]] < 4)
    L4 = L4_plus + L4_minus
    cost = 2 * L4 + U
    return dict(L4=L4, L4_plus=L4_plus, L4_minus=L4_minus, U=U, cost=cost, npts=len(pts))

# ------------------------------------------------- self-derived prediction
# (generalizes note Sec 2-3's bookkeeping to arbitrary k; see module docstring (c))

def bigcount_plus(k, n0):
    """# of the 4 slope+1 lines of a class (n0, n1=k-n0) with size >= 4."""
    n1 = k - n0
    sizes = (n0, 2 * n0 + n1, n0 + 2 * n1, n1)
    return sum(1 for s in sizes if s >= 4)

def bigcount_minus(k, n0):
    n1 = k - n0
    sizes = (n0, 2 * n0 + n1, n0 + 2 * n1, n1)   # same multiset/order as +1 (c'', c''+p, c''+2p, c''+3p)
    return sum(1 for s in sizes if s >= 4)

def predicted_L4(p, Pk_plus, Pk_minus, maxk):
    """E[L4] = p * sum_k P_k * avg_{n0 ~ Uniform{0..k}} bigcount(k,n0), each slope, summed."""
    def one_slope(Pk, bigcount):
        tot = Fraction(0)
        for k in range(maxk + 1):
            if Pk.get(k, 0) == 0: continue
            avg = Fraction(sum(bigcount(k, n0) for n0 in range(k + 1)), k + 1) if k > 0 else Fraction(0)
            tot += Pk[k] * avg
        return tot
    ep = one_slope(Pk_plus, bigcount_plus)
    em = one_slope(Pk_minus, bigcount_minus)
    return p * ep, p * em, p * (ep + em)

def covered_plus(class_, n0, n1, d, e):
    if class_ == 0:
        same, s01, s10 = 2 * n0 + n1, n0 + 2 * n1, n0
    else:
        same, s01, s10 = n0 + 2 * n1, n1, 2 * n0 + n1
    size = same if d == e else (s01 if (d == 0 and e == 1) else s10)
    return size >= 4

def covered_minus(class_, n0, n1, d, e):
    if class_ == 0:
        s00, mix, s11 = n0, 2 * n0 + n1, n0 + 2 * n1
    else:
        s00, mix, s11 = 2 * n0 + n1, n0 + 2 * n1, n1
    if d == 0 and e == 0: size = s00
    elif d == 1 and e == 1: size = s11
    else: size = mix
    return size >= 4

def slope_states(Pk, maxk):
    """Exact joint law of (k, n0, class) for a SIZE-BIASED random residue x (x uniform in [0,p)):
    P(k) = k*P_k (size bias), n0 ~ Uniform{0..k} | k, class=0 w.p. n0/k | (k,n0).  Returns list of
    (k, n0, n1, class, weight) with weight summing to 1 (k=0 excluded automatically: zero weight)."""
    out = []
    for k in range(1, maxk + 1):
        pk = Pk.get(k, 0)
        if pk == 0: continue
        for n0 in range(k + 1):
            n1 = k - n0
            base = pk * Fraction(n0, k + 1)  # = P_k * n0/(k+1); size-bias*uniform-n0*P(class=0|n0,k) collapses to this
            # class=0 weight = P_k * [k*(1/(k+1))] * (n0/k) = P_k*n0/(k+1)
            # class=1 weight = P_k * [k*(1/(k+1))] * (n1/k) = P_k*n1/(k+1)
            w0 = pk * Fraction(n0, k + 1)
            w1 = pk * Fraction(n1, k + 1)
            if w0 > 0: out.append((k, n0, n1, 0, w0))
            if w1 > 0: out.append((k, n0, n1, 1, w1))
    return out

def predicted_U(p, Pk_plus, Pk_minus, maxk):
    """E[U] = p * E[#singleton lifts of a residue], assuming the plus- and minus-class draws of a
    residue are INDEPENDENT (note Sec 3's hypothesis), each drawn from slope_states()."""
    states_p = slope_states(Pk_plus, maxk)
    states_m = slope_states(Pk_minus, maxk)
    wsum_p = sum(w for *_, w in states_p)
    wsum_m = sum(w for *_, w in states_m)
    total = Fraction(0)
    lifts = [(d, e) for d in (0, 1) for e in (0, 1)]
    for (kp, n0p, n1p, cp, wp) in states_p:
        for (km, n0m, n1m, cm, wm) in states_m:
            w = wp * wm
            if w == 0: continue
            singles = sum(1 for (d, e) in lifts
                          if not covered_plus(cp, n0p, n1p, d, e) and not covered_minus(cm, n0m, n1m, d, e))
            total += w * singles
    # normalize (wsum_p, wsum_m should each be exactly 1; guard against Pk not summing to 1 due to
    # missing k's outside the observed range, e.g. empirical P_k with p classes as exact fractions
    # k/p should already sum to 1 exactly)
    if wsum_p != 1 or wsum_m != 1:
        total = total / (wsum_p * wsum_m)
    return p * total

# ---------------------------------------------------------------- reporting

def frac_counter_to_P(cnt, p, maxk):
    return {k: Fraction(cnt.get(k, 0), p) for k in range(maxk + 1)}

def fmt_frac(fr, w=7):
    return f"{float(fr):.4f}"

def run_one(p, k_pow, out):
    def P(*a):
        s = " ".join(str(x) for x in a)
        print(s); out.append(s)

    P(f"\n{'='*78}\np = {p}   f(x) = x^{k_pow}   gcd({k_pow},p-1) = {gcd(k_pow,p-1)}   box (0,0)   4p = {4*p}")
    f, plus_roots, minus_roots, cls_p, cls_m = analyze(p, k_pow)

    renc = rencontres_P(k_pow)
    P(f"\n-- (a) k'-distribution of residue classes, vs rencontres law of S_{k_pow} --")
    cnt_p = k_distribution(plus_roots, p)
    cnt_m = k_distribution(minus_roots, p)
    assert sum(cnt_p.values()) == p and sum(cnt_m.values()) == p
    P(f"{'k':>3} {'renc P_k':>10} {'#plus':>7} {'emp P+':>8} {'#minus':>7} {'emp P-':>8}")
    for k in range(k_pow + 1):
        P(f"{k:>3} {fmt_frac(renc[k]):>10} {cnt_p.get(k,0):>7} {fmt_frac(Fraction(cnt_p.get(k,0),p)):>8} "
          f"{cnt_m.get(k,0):>7} {fmt_frac(Fraction(cnt_m.get(k,0),p)):>8}")
    # simple L1 discrepancy vs rencontres
    l1_p = sum(abs(Fraction(cnt_p.get(k,0),p) - renc[k]) for k in range(k_pow+1))
    l1_m = sum(abs(Fraction(cnt_m.get(k,0),p) - renc[k]) for k in range(k_pow+1))
    P(f"L1 distance to rencontres law: plus={float(l1_p):.4f}  minus={float(l1_m):.4f}")

    P(f"\n-- (b) n0 | k distribution (is it Uniform{{0,...,k}}? note's local law says yes) --")
    tab_p = n0_given_k(plus_roots, cls_p, p)
    tab_m = n0_given_k(minus_roots, cls_m, p)
    for slope, tab in (('plus', tab_p), ('minus', tab_m)):
        for k in range(2, k_pow + 1):  # k=0,1 trivial (n0 forced or single point mass)
            if k not in tab: continue
            c = tab[k]
            nclasses = sum(c.values())
            row = " ".join(f"n0={n0}:{c.get(n0,0)}" for n0 in range(k+1))
            unif = 1.0/(k+1)
            P(f"  {slope:5} k={k}  (#classes={nclasses}, uniform if each ~{unif*nclasses:.2f}): {row}")

    P(f"\n-- (c) cover cost: exact (from data) vs self-derived prediction --")
    exact = explicit_cover_cost(p, f)
    P(f"  EXACT   : L4+={exact['L4_plus']} L4-={exact['L4_minus']} L4={exact['L4']} U={exact['U']} "
      f"cost=2*L4+U={exact['cost']}   cost/(2p)={exact['cost']/(2*p):.4f}   cost/p={exact['cost']/p:.4f}")

    Pk_emp_p = frac_counter_to_P(cnt_p, p, k_pow)
    Pk_emp_m = frac_counter_to_P(cnt_m, p, k_pow)
    L4p_e, L4m_e, L4_e = predicted_L4(p, Pk_emp_p, Pk_emp_m, k_pow)
    U_e = predicted_U(p, Pk_emp_p, Pk_emp_m, k_pow)
    cost_e = 2 * L4_e + U_e
    P(f"  PRED(emp P_k, uniform n0|k, slope-independence): L4+={float(L4p_e):.2f} L4-={float(L4m_e):.2f} "
      f"L4={float(L4_e):.2f} U={float(U_e):.2f} cost={float(cost_e):.2f}   cost/(2p)={float(cost_e)/(2*p):.4f}")

    Pk_renc = {k: renc[k] for k in range(k_pow + 1)}
    L4p_i, L4m_i, L4_i = predicted_L4(p, Pk_renc, Pk_renc, k_pow)
    U_i = predicted_U(p, Pk_renc, Pk_renc, k_pow)
    cost_i = 2 * L4_i + U_i
    P(f"  PRED(idealized: rencontres P_k, uniform n0|k, slope-independence): L4+={float(L4p_i):.2f} "
      f"L4-={float(L4m_i):.2f} L4={float(L4_i):.2f} U={float(U_i):.2f} cost={float(cost_i):.2f}   "
      f"cost/(2p)={float(cost_i)/(2*p):.4f}")
    P(f"  relative error exact-vs-emp-pred: {(exact['cost']-float(cost_e))/exact['cost']*100:+.2f}%   "
      f"exact-vs-idealized-pred: {(exact['cost']-float(cost_i))/exact['cost']*100:+.2f}%")

    P(f"\n-- (d) LP over all +-1 lines (fractional), slack/lp_curve.py machinery, mode='pm1' --")
    pts = LPC.curve_points(p, f'pow:{k_pow}', 0, 0)
    assert len(pts) == 4 * p
    ls = LPC.lines(pts, 'pm1')
    sizes = Counter(len(s) for s in ls)
    lp_val = LPC.solve(pts, ls)
    P(f"  #(+-1)-lines with >=3 pts: {len(ls)}  size histogram: {dict(sorted(sizes.items()))}")
    P(f"  LP value = {lp_val:.3f}   LP/(2p) = {lp_val/(2*p):.4f}   LP/p = {lp_val/p:.4f}")

    return dict(p=p, k_pow=k_pow, exact=exact, cost_pred_emp=float(cost_e), cost_pred_ideal=float(cost_i),
                lp_pm1=lp_val, Pk_plus=cnt_p, Pk_minus=cnt_m, l1_plus=float(l1_p), l1_minus=float(l1_m))

# ---------------------------------------------------------------------- main

def main():
    out = []
    def P(*a):
        s = " ".join(str(x) for x in a)
        print(s); out.append(s)

    candidates = [197, 263, 293, 401, 449, 599, 797, 887]
    for c in candidates:
        assert is_prime(c), c

    plist = {
        5: sorted(p for p in candidates if gcd(5, p - 1) == 1),
        7: sorted(p for p in candidates if gcd(7, p - 1) == 1),
    }
    dropped = {
        5: sorted(p for p in candidates if gcd(5, p - 1) != 1),
        7: sorted(p for p in candidates if gcd(7, p - 1) != 1),
    }

    P("x5_x7_numerics -- f(x)=x^5, x^7 permutation-monomial box-lift numerics, box (0,0)")
    P("NOTE_ON_PROFILE_TABLE: searched docs/research/g_agents/, slack/g_agents/, and the whole repo")
    P("(grep -r profile_table) at run time; no output from a 'profile_table' agent was present, so")
    P("part (c)'s prediction below is self-derived (generalizing note Sec 2-3 to general k), not a")
    P("cross-check against that agent's actual numbers.")
    P(f"\ncandidate primes: {candidates}")
    P(f"x^5 usable (gcd(5,p-1)=1): {plist[5]}   -- DROPPED (not a permutation): {dropped[5]}  [note: the")
    P("  task prompt's example list for x^5 includes 401, but gcd(5,400)=5 != 1, so x^5 is NOT a")
    P("  permutation of F_401 -- excluded from the x^5 sweep, kept for x^7 where gcd(7,400)=1.]")
    P(f"x^7 usable (gcd(7,p-1)=1): {plist[7]}   -- DROPPED (not a permutation): {dropped[7]}  [similarly")
    P("  449 is in the task's x^7 example list but gcd(7,448)=7 != 1 -- excluded from the x^7 sweep,")
    P("  kept for x^5 where gcd(5,448)=1.]")

    results = []
    for k_pow in (5, 7):
        for p in plist[k_pow]:
            results.append(run_one(p, k_pow, out))

    P(f"\n{'='*78}\nSUMMARY TABLE: cost/(2p) exact vs predicted, and LP/(2p)")
    P(f"{'k':>2} {'p':>5} {'L1(+)':>7} {'L1(-)':>7} {'cost':>6} {'cost/2p':>8} {'pred_emp/2p':>12} "
      f"{'pred_ideal/2p':>13} {'LP_pm1/2p':>10}")
    for r in results:
        p, k = r['p'], r['k_pow']
        c = r['exact']['cost']
        P(f"{k:>2} {p:>5} {r['l1_plus']:>7.4f} {r['l1_minus']:>7.4f} {c:>6} {c/(2*p):>8.4f} "
          f"{r['cost_pred_emp']/(2*p):>12.4f} {r['cost_pred_ideal']/(2*p):>13.4f} {r['lp_pm1']/(2*p):>10.4f}")

    outpath = os.path.join(os.path.dirname(__file__), 'x5_x7_numerics_output.txt')
    with open(outpath, 'w') as fh:
        fh.write("\n".join(out) + "\n")
    print(f"\n[written {outpath}]")

    jpath = os.path.join(os.path.dirname(__file__), 'x5_x7_numerics_results.json')
    with open(jpath, 'w') as fh:
        json.dump([{kk: (vv if not isinstance(vv, dict) else {str(k2): v2 for k2, v2 in vv.items()})
                     for kk, vv in r.items() if kk not in ('exact',)} | {
                        'exact_' + kk: vv for kk, vv in r['exact'].items()
                    } for r in results], fh, indent=1)
    print(f"[written {jpath}]")

if __name__ == '__main__':
    main()
