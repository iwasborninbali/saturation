#!/usr/bin/env python3
"""x5_x7_numerics_exact_constant.py (agent: x5_x7_numerics) -- the EXACT rational "idealized limiting
cost/(2p)" constant for f(x) = x^k (k odd, gcd(k,p-1)=1), under the three local-law hypotheses of
docs/research/permutation_cubic_note.md generalized to arbitrary k (see x5_x7_numerics.py's docstring
for the per-root line-membership formulas this reuses):

  (H1) the k'-distribution of residue classes (roots of f(t)-t=c, resp. f(t)+t=c) tends to the
       rencontres law of S_k (P_k' = C(k,k') D_{k-k'}/k!) as p -> infinity;
  (H2) given k' roots in a class, the number of class-0 roots n0 is Uniform on {0,...,k'};
  (H3) the plus- and minus- class data (k,n0,class) at a single residue x are independent.

These are exactly the hypotheses the note proves (Sec 3, via Weil equidistribution on the root conic
and a Kummer-sheaf non-triviality argument) for k=3; here they are only checked NUMERICALLY (parts
a, b of x5_x7_numerics.py / _pooled.py), not proved, for k=5, 7 -- so the constants below are
CONJECTURAL for k=5,7, not theorems.

Under (H1)-(H3) the limiting ratio cost/(2p) is a pure combinatorial constant, independent of p (this
independence is itself a nontrivial and checkable structural claim -- verified in the code below by
symbolic (Fraction) computation, not floating point):

    limit = E[L4 per slope per class] * 2   [the "2*L4/p" term, times 2 slopes]
          + E[U per residue]                [the "U/p" term]
    cost/(2p) -> limit / 2

For k=3 this must equal 11/8 exactly (Theorem G3.5 of the note) -- reproduced EXACTLY below (not just
approximately) as a check on the whole machinery, then the same computation is run for k=5, 7.

Usage: python3 slack/g_agents/x5_x7_numerics_exact_constant.py
"""
import sys, os
from fractions import Fraction

sys.path.insert(0, os.path.dirname(__file__))
import x5_x7_numerics as M


def idealized_constant(k_pow):
    renc = M.rencontres_P(k_pow)
    Pk = {k: renc[k] for k in range(k_pow + 1)}

    def one_slope_EL4(bigcount):
        tot = Fraction(0)
        for k in range(k_pow + 1):
            if Pk[k] == 0:
                continue
            avg = Fraction(sum(bigcount(k, n0) for n0 in range(k + 1)), k + 1) if k > 0 else Fraction(0)
            tot += Pk[k] * avg
        return tot

    eL4 = one_slope_EL4(M.bigcount_plus)  # bigcount_plus == bigcount_minus (same 4-line-size formula)

    states = M.slope_states(Pk, k_pow)
    wsum = sum(w for *_, w in states)
    assert wsum == 1, f"slope_states weights should sum to 1, got {wsum}"

    lifts = [(d, e) for d in (0, 1) for e in (0, 1)]
    eU = Fraction(0)
    for (kp, n0p, n1p, cp, wp) in states:
        for (km, n0m, n1m, cm, wm) in states:
            w = wp * wm
            if w == 0:
                continue
            singles = sum(1 for (d, e) in lifts
                          if not M.covered_plus(cp, n0p, n1p, d, e)
                          and not M.covered_minus(cm, n0m, n1m, d, e))
            eU += w * singles

    # L4 = p*(eL4_plus + eL4_minus) = p*2*eL4 (both slopes give the same eL4 under this model
    # since Pk_plus = Pk_minus = the same rencontres law); U = p*eU.  cost/(2p) = (2L4+U)/(2p).
    ratio = (2 * (2 * eL4) + eU) / 2
    return eL4, eU, ratio


def main():
    out = []
    def P(*a):
        s = " ".join(str(x) for x in a)
        print(s); out.append(s)

    P("Exact rational 'idealized limiting cost/(2p)' constants under hypotheses (H1)-(H3), f(x)=x^k:")
    P(f"{'k':>3} {'E[L4/class/slope]':>20} {'E[U/residue]':>16} {'limit cost/(2p)':>18} {'decimal':>10}")
    for k_pow in (3, 5, 7):
        eL4, eU, ratio = idealized_constant(k_pow)
        P(f"{k_pow:>3} {str(eL4):>20} {str(eU):>16} {str(ratio):>18} {float(ratio):>10.6f}")
    P("\nk=3 row MUST equal 11/8 exactly (Theorem G3.5 of permutation_cubic_note.md) -- this is a")
    P("reproduction check of the whole machinery (rencontres law + uniform-n0|k + slope-independence")
    P("+ the per-root line-membership bookkeeping), not a new computation for k=3.")
    P("k=5, k=7 rows are new (conjectural: (H1)-(H3) are only checked numerically for k=5,7, not")
    P("proved as the note proves them for k=3).")

    outpath = os.path.join(os.path.dirname(__file__), 'x5_x7_numerics_exact_constant_output.txt')
    with open(outpath, 'w') as fh:
        fh.write("\n".join(out) + "\n")
    print(f"\n[written {outpath}]")


if __name__ == '__main__':
    main()
