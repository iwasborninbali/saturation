#!/usr/bin/env python3
"""x5_x7_numerics_pooled.py (agent: x5_x7_numerics) -- pooled versions of parts (a),(b) of
x5_x7_numerics.py: single-prime samples are tiny for k'>=4 (e.g. only 0-8 classes out of p), so pool
counts across ALL usable primes (for each k_pow) before comparing to the rencontres / uniform laws.
Also verifies the plus<->minus symmetry noticed in the raw output: for f=x^k (k odd), t -> mu*t with
mu^(k-1) = -1 sends roots of f(t)+t=c bijectively to roots of f(s)-s=-mu*c (elementary: f(mu t) - mu t
= mu^k t^k - mu t = mu*(mu^(k-1) t^k - t) = mu*(-t^k - t) = -mu*(f(t)+t)), so such a mu exists iff -1 is
a (k-1)-th power mod p, and existence forces the plus- and minus- class-size multisets to be EXACT
rearrangements of one another (hence identical P_k), independent of the local-law/equidistribution
heuristics of (a)-(b) -- checked exactly (not just approximately) below.

Usage: python3 slack/g_agents/x5_x7_numerics_pooled.py
Output printed to stdout and saved to slack/g_agents/x5_x7_numerics_pooled_output.txt
"""
import sys, os, math
from math import gcd
from fractions import Fraction
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
import x5_x7_numerics as M

CANDIDATES = [197, 263, 293, 401, 449, 599, 797, 887]

def mu_pow_km1_eq_neg1_solvable(k, p):
    """Is x^(k-1) = -1 solvable mod p?  (elementary Euler-criterion style check, no discrete log)."""
    d = gcd(k - 1, p - 1)
    # -1 is a d-th-power-residue-class question: x^(k-1)=-1 solvable iff (-1)^((p-1)/d) == 1
    return pow(p - 1, (p - 1) // d, p) == 1  # (p-1) mod p == -1 mod p, correct representative

def main():
    out = []
    def P(*a):
        s = " ".join(str(x) for x in a)
        print(s); out.append(s)

    for k_pow in (5, 7):
        plist = sorted(p for p in CANDIDATES if gcd(k_pow, p - 1) == 1)
        P(f"\n{'='*78}\nf(x) = x^{k_pow}   primes: {plist}   (pooled over {len(plist)} primes)")

        # -------- symmetry check (exact, elementary) --------
        P(f"\n-- symmetry check: does mu^{k_pow-1} = -1 have a solution mod p? (predicts exact plus<->minus")
        P(f"   class-size rearrangement, hence identical P_k, via t -> mu*t) --")
        pooled_cnt_p = Counter(); pooled_cnt_m = Counter()
        pooled_n0_p = {}; pooled_n0_m = {}
        sym_flags = {}
        for p in plist:
            solvable = mu_pow_km1_eq_neg1_solvable(k_pow, p)
            f, pr, mr, cp, cm = M.analyze(p, k_pow)
            cnt_p = M.k_distribution(pr, p); cnt_m = M.k_distribution(mr, p)
            identical = (cnt_p == cnt_m)
            sym_flags[p] = (solvable, identical)
            P(f"  p={p:5d}  mu^{k_pow-1}=-1 solvable: {str(solvable):5}  observed P_k(plus)==P_k(minus): {identical}"
              f"  {'<-- MATCH' if solvable==identical else '<-- MISMATCH!!'}")
            for k, c in cnt_p.items(): pooled_cnt_p[k] += c
            for k, c in cnt_m.items(): pooled_cnt_m[k] += c
            tp = M.n0_given_k(pr, cp, p); tm = M.n0_given_k(mr, cm, p)
            for k, cc in tp.items():
                pooled_n0_p.setdefault(k, Counter())
                for n0, v in cc.items(): pooled_n0_p[k][n0] += v
            for k, cc in tm.items():
                pooled_n0_m.setdefault(k, Counter())
                for n0, v in cc.items(): pooled_n0_m[k][n0] += v
        all_match = all(s == i for (s, i) in sym_flags.values())
        P(f"  ==> prediction matches observation at all {len(plist)} primes: {all_match}")

        # -------- pooled (a): k-distribution vs rencontres --------
        P(f"\n-- pooled (a): k'-distribution over {sum(pooled_cnt_p.values())} classes (plus) / "
          f"{sum(pooled_cnt_m.values())} (minus), vs rencontres law of S_{k_pow} --")
        renc = M.rencontres_P(k_pow)
        Np = sum(pooled_cnt_p.values()); Nm = sum(pooled_cnt_m.values())
        P(f"{'k':>3} {'renc P_k':>10} {'#plus':>7} {'pooled P+':>10} {'#minus':>7} {'pooled P-':>10}")
        for k in range(k_pow + 1):
            cp_, cm_ = pooled_cnt_p.get(k, 0), pooled_cnt_m.get(k, 0)
            P(f"{k:>3} {float(renc[k]):>10.4f} {cp_:>7} {cp_/Np:>10.4f} {cm_:>7} {cm_/Nm:>10.4f}")
        # chi-square (float is fine here, small numbers)
        chi2_p_f = sum(((pooled_cnt_p.get(k,0) - float(renc[k])*Np)**2)/(float(renc[k])*Np)
                        for k in range(k_pow+1) if renc[k] > 0)
        chi2_m_f = sum(((pooled_cnt_m.get(k,0) - float(renc[k])*Nm)**2)/(float(renc[k])*Nm)
                        for k in range(k_pow+1) if renc[k] > 0)
        dof = sum(1 for k in range(k_pow+1) if renc[k] > 0) - 1
        P(f"  chi^2 (dof={dof}): plus={chi2_p_f:.2f}  minus={chi2_m_f:.2f}  "
          f"(rough guide: dof={dof} 95th-pctile chi^2 ~ {dof + 2*math.sqrt(2*dof):.1f})")

        # -------- pooled (b): n0 | k vs uniform --------
        P(f"\n-- pooled (b): n0 | k' distribution vs Uniform{{0,...,k'}} --")
        for slope, pooled_n0 in (('plus', pooled_n0_p), ('minus', pooled_n0_m)):
            for k in sorted(pooled_n0):
                if k < 2: continue
                cc = pooled_n0[k]
                n = sum(cc.values())
                if n < 5: continue  # too few pooled classes to say anything
                exp = n / (k + 1)
                row = " ".join(f"n0={j}:{cc.get(j,0)}({cc.get(j,0)/n:.3f})" for j in range(k + 1))
                chi2 = sum((cc.get(j,0) - exp) ** 2 / exp for j in range(k + 1))
                P(f"  {slope:5} k={k}  n_classes={n:4d}  uniform-expected={exp:.2f}/cell  chi2(dof={k})={chi2:.2f}")
                P(f"        {row}")

    outpath = os.path.join(os.path.dirname(__file__), 'x5_x7_numerics_pooled_output.txt')
    with open(outpath, 'w') as fh:
        fh.write("\n".join(out) + "\n")
    print(f"\n[written {outpath}]")

if __name__ == '__main__':
    main()
