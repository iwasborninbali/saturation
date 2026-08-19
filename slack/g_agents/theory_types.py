"""theory_types.py — G3.5: the exact interval condition for slope-(+-1) residue-group patterns of the
permutation cubic y = x^3 (p = 2 mod 3), the curve of root triples that governs it, and the limiting
densities of the two group shapes.  Companion to docs/research/g_agents/theory_types.md (full derivation);
this file only re-derives the needed facts computationally and checks them against direct enumeration.

Two independent computations for each c in a residue class with 3 roots of x^3 + eps*x = c (eps = +-1):
  (i) ALGEBRAIC  : classify c via the interval condition on least residues (fast, O(p) total per prime);
  (ii) GEOMETRIC  : brute-force the actual box lift of y = x^3 and bucket every point by its slope-(-eps)
       line (X+Y=const for eps=+1 [antidiagonal, "x^3+x"], X-Y=const for eps=-1... — see note in code)
       and report the realised sizes on each of the 4 lines of the group, compared to the algebraic
       prediction (k, k+3, 6-k, 3-k).
Also: (iii) point count of the "root-pair" conic curve C_eps: x1^2+x1*x2+x2^2 = -eps (Vieta for
x^3+eps*x-c, x3=-x1-x2), a smooth (hence absolutely irreducible) conic -- sanity count |C_eps(F_p)| = p+O(1);
(iv) Monte-Carlo + a from-scratch exact derivation of the limiting densities of the group shapes under the
"least residues jointly uniform subject to x1+x2+x3 = 0, c0 independent uniform" model.

usage:
  theory_types.py                      # default check: p in (401, 797), both slopes, full report
  theory_types.py densities            # continuum-model Monte Carlo + exact check only
  theory_types.py small                # small-p geometric cross-checks (11..197) against lp_curve.txt
"""
import sys
import random
from collections import defaultdict, Counter


# ---------------------------------------------------------------------------
# (i) ALGEBRAIC classification: for each c with 3 roots, the shift-bit / interval condition.
# ---------------------------------------------------------------------------

def roots_by_class(p, eps):
    """eps=+1: x^3+x = c (antidiagonal / slope -1 lines X+Y=const).
       eps=-1: x^3-x = c (diagonal / slope +1 lines X-Y=const).
    Returns dict c -> sorted list of roots (least residues in [0,p))."""
    roots = defaultdict(list)
    for x in range(p):
        c = (x * x * x + eps * x) % p
        roots[c].append(x)
    return roots


def classify_class(p, eps, c, xs):
    """xs: sorted roots of x^3+eps*x=c (len 3).  Returns (k, shape, predicted_sizes_dict).
    shift bit of root x_i (integer y_i = x_i^3 mod p, taken in [0,p)):
      eps=+1 (antidiagonal): bit_i = 0 iff x_i <= c0   (c0 := c, already in [0,p))
      eps=-1 (diagonal)    : bit_i = 0 iff x_i >= p-c0  (equivalently p-c0 = (-c) % p)
    k = #{bit_i = 0}; sizes on the group's 4 consecutive lines (base, base+p, base+2p, base+3p) are
    (k, k+3, 6-k, 3-k) where base = c0 (eps=+1) or base = -3p+... -- see md for the base-line bookkeeping;
    here we only need k and the *shape* (multiset of nonzero sizes), which is base-independent.
    """
    c0 = c
    if eps == 1:
        k = sum(1 for x in xs if x <= c0)
    else:
        thr = (-c0) % p
        k = sum(1 for x in xs if x >= thr)
    sizes = (k, k + 3, 6 - k, 3 - k)
    shape = tuple(sorted(s for s in sizes if s > 0))
    return k, shape


def algebraic_report(p, eps):
    roots = roots_by_class(p, eps)
    n_by_len = Counter(len(v) for v in roots.values())
    n_by_len[0] = p - sum(n_by_len.values())  # classes with 0 roots never appear as dict keys
    k_hist = Counter()
    shape_hist = Counter()
    for c, xs in roots.items():
        if len(xs) != 3:
            continue
        k, shape = classify_class(p, eps, c, xs)
        k_hist[k] += 1
        shape_hist[shape] += 1
    return n_by_len, k_hist, shape_hist


# ---------------------------------------------------------------------------
# (ii) GEOMETRIC cross-check: brute-force box lift, bucket by actual line, compare to (k,k+3,6-k,3-k).
# ---------------------------------------------------------------------------

def geometric_lines(p, direction):
    """direction='anti' -> key = X+Y (slope -1 lines); direction='diag' -> key = X-Y (slope +1 lines).
    Box [0,2p) x [0,2p), curve Y = X^3 mod p.  Returns dict key -> count."""
    lines = defaultdict(int)
    for x in range(p):
        y = (x * x * x) % p
        for X in (x, x + p):
            for Y in (y, y + p):
                key = X + Y if direction == 'anti' else X - Y
                lines[key] += 1
    return lines


def geometric_vs_algebraic(p, eps, direction, verbose=False):
    """eps/direction pairing: eps=+1 <-> direction='anti' (x^3+x, antidiagonals);
                               eps=-1 <-> direction='diag' (x^3-x, diagonals)."""
    roots = roots_by_class(p, eps)
    lines = geometric_lines(p, direction)
    mismatches = []
    checked = 0
    for c, xs in roots.items():
        if len(xs) != 3:
            continue
        k, shape = classify_class(p, eps, c, xs)
        if direction == 'anti':
            base_lines = [c, c + p, c + 2 * p, c + 3 * p]
        else:
            # diagonals: X-Y ranges over (-2p,2p); base chosen so the group sits at
            # c-eps*... use the same 4 consecutive multiples-of-p-apart lines containing all points:
            # every point of this class has X-Y in {-c-2p,...}; simplest robust check: just gather
            # every line key with key % p == (base residue) among keys actually present.
            base_res = (-c) % p
            base_lines = [base_res - 2 * p, base_res - p, base_res, base_res + p]
        actual = [lines.get(L, 0) for L in base_lines]
        predicted = list((k, k + 3, 6 - k, 3 - k))
        checked += 1
        if sorted(actual) != sorted(predicted) or sum(actual) != 12:
            mismatches.append((c, xs, k, predicted, base_lines, actual))
        if verbose and len(mismatches) <= 5 and (sorted(actual) != sorted(predicted)):
            print(f"    MISMATCH c={c} xs={xs} k={k} predicted={predicted} lines={base_lines} actual={actual}")
    return checked, mismatches


# ---------------------------------------------------------------------------
# (iii) the conic C_eps : x1^2 + x1*x2 + x2^2 = -eps  (point count, irreducibility sanity)
# ---------------------------------------------------------------------------

def conic_point_count(p, eps):
    target = (-eps) % p
    cnt = 0
    for x1 in range(p):
        # x2^2 + x1*x2 + (x1^2 - target) = 0 ; solve quadratic in x2 mod p
        a, b, c = 1, x1, (x1 * x1 - target) % p
        disc = (b * b - 4 * a * c) % p
        # count square roots of disc mod p (0,1, or 2)
        if disc == 0:
            cnt += 1
        else:
            # Euler's criterion
            if pow(disc, (p - 1) // 2, p) == 1:
                cnt += 2
    return cnt


def discriminant_check(eps, primes):
    """The conic x1^2+x1x2+x2^2=-eps has 3x3 matrix det = -eps*(1-1/4) = -eps*3/4 (mod p);
    nonzero for p != 2,3 for either sign of eps -> smooth (hence absolutely irreducible) conic."""
    out = []
    for p in primes:
        det_num = (-eps * 3) % p  # numerator of -eps*3/4 up to the unit 1/4 (4 invertible for p>2)
        out.append((p, det_num != 0))
    return out


# ---------------------------------------------------------------------------
# (iv) continuum density model: u1,u2 iid U(0,1) free; u3 forced so u1+u2+u3 in {1,2};
#      gamma iid U(0,1) independent.  k = #{u_i <= gamma}.  Predict P(k=j) for j=0,1,2,3.
# ---------------------------------------------------------------------------

def density_model_montecarlo(n=2_000_000, seed=0):
    rnd = random.Random(seed)
    k_hist = Counter()
    for _ in range(n):
        u1 = rnd.random()
        u2 = rnd.random()
        s = u1 + u2
        u3 = (1 - s) if s < 1 else (2 - s)
        gamma = rnd.random()
        k = (u1 <= gamma) + (u2 <= gamma) + (u3 <= gamma)
        k_hist[k] += 1
    return {j: k_hist[j] / n for j in range(4)}


def density_model_exact():
    """Exact closed form via the two branches (sum=1 simplex, sum=2 reflected simplex), each with
    probability 1/2, using the classical uniform-spacings order-statistic means for m=3 spacings:
    E[D_(1)] = 1/9 (min), E[D_(2)] = 5/18 (median), E[D_(3)] = 11/18 (max) on the sum=1 branch;
    the sum=2 branch is the reflection 1-D, swapping min<->1-max etc.
    E[min]_full  = 1/2*(1/9)   + 1/2*(1 - 11/18) = 1/2*(2/18 + 7/18) = 9/36 = 1/4
    E[max]_full  = 1/2*(11/18) + 1/2*(1 - 1/9)   = 1/2*(11/18+16/18) = 27/36 = 3/4
    P(k=0) = P(gamma < min) = E[min] = 1/4 ;  P(k=3) = P(gamma > max) = 1 - E[max] = 1/4
    P(k=1) = P(k=2) = (1 - P(k=0) - P(k=3)) / 2 = 1/4   (by the (gamma,u)->(1-gamma,1-u) symmetry)
    """
    from fractions import Fraction as F
    Emin_branch1 = F(1, 9)
    Emax_branch1 = F(11, 18)
    Emin = F(1, 2) * Emin_branch1 + F(1, 2) * (1 - Emax_branch1)
    Emax = F(1, 2) * Emax_branch1 + F(1, 2) * (1 - Emin_branch1)
    p0 = Emin
    p3 = 1 - Emax
    p1 = p2 = (1 - p0 - p3) / 2
    return {0: p0, 1: p1, 2: p2, 3: p3, 'Emin': Emin, 'Emax': Emax}


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def shape_label(shape):
    return {(3, 3, 6): 'A (3,6,3)', (1, 2, 4, 5): 'B {1,2,4,5}'}.get(shape, str(shape))


def full_report(p):
    print(f"\n=== p={p} ===")
    for eps, name in ((1, 'antidiagonal x^3+x'), (-1, 'diagonal x^3-x')):
        n_by_len, k_hist, shape_hist = algebraic_report(p, eps)
        n3 = n_by_len.get(3, 0)
        n1 = n_by_len.get(1, 0)
        n0 = n_by_len.get(0, 0)
        print(f"  {name}: n0={n0} ({n0/p:.4f}) n1={n1} ({n1/p:.4f}) n3={n3} ({n3/p:.4f})  "
              f"[predicted 1/3,1/2,1/6 = {p/3:.1f},{p/2:.1f},{p/6:.1f}]")
        khist_frac = {j: (k_hist[j], round(k_hist[j] / n3, 4) if n3 else None) for j in range(4)}
        print(f"    k-histogram (count, frac of n3={n3}): {khist_frac}   [predicted 1/4 each]")
        shape_frac = {shape_label(s): (cnt, round(cnt / n3, 4)) for s, cnt in shape_hist.items()}
        print(f"    shapes: {shape_frac}   [predicted A: 1/2, B: 1/4+1/4=1/2]")


def small_p_crosscheck():
    print("=== small-p geometric cross-check (algebraic k-formula vs brute-force box lift) ===")
    for p in (11, 13, 17, 19, 101, 131, 167, 197):
        tot_mismatch = 0
        tot_checked = 0
        sizes_combined = Counter()
        for eps, direction in ((1, 'anti'), (-1, 'diag')):
            checked, mism = geometric_vs_algebraic(p, eps, direction)
            tot_checked += checked
            tot_mismatch += len(mism)
            lines = geometric_lines(p, direction)
            for v in lines.values():
                if v >= 3:
                    sizes_combined[v] += 1
            if mism:
                print(f"  p={p} eps={eps} dir={direction}: {len(mism)}/{checked} MISMATCHES, e.g. {mism[0]}")
        six = sizes_combined.get(6, 0)
        three = sizes_combined.get(3, 0)
        four = sizes_combined.get(4, 0)
        five = sizes_combined.get(5, 0)
        print(f"  p={p}: checked={tot_checked} mismatches={tot_mismatch}  "
              f"sizes(pm1, rows/cols excluded since always=2)={dict(sorted(sizes_combined.items()))}  "
              f"3==2*6? {three}=={2*six}: {three == 2*six}   4==5? {four}=={five}: {four==five}")


def double_root_diagnostic():
    """Explains the small residual mismatches in the small-p cross-check: classes with a DOUBLE root
    (2 distinct residue points, one with multiplicity 2) are excluded from the len==3 classification but
    still contribute a rich line when their own 2-root k in {0,1,2} lands on k=1 (an extra 3+3 split, no
    6-line) or k in {0,2} (an extra lone 4-line, no matching 5-line) -- an O(1) correction (<=2 classes
    total per prime, from g'(x)=0 / h'(x)=0), negligible next to n3 ~ p/6."""
    print("=== double-root (ramification) classes: source of the O(1) residual in the small-p check ===")
    for p in (11, 131, 167):
        for eps, name in ((1, 'antidiag'), (-1, 'diag')):
            roots = roots_by_class(p, eps)
            doubles = [(c, xs) for c, xs in roots.items() if len(xs) == 2]
            for c, xs in doubles:
                if eps == 1:
                    k2 = sum(1 for x in xs if x <= c)
                else:
                    thr = (-c) % p
                    k2 = sum(1 for x in xs if x >= thr)
                extra = '(1,3,3,1): +2 to the 3-count, +0 to 6' if k2 == 1 else \
                        '(0,2,4,2) or (2,4,2,0): +1 to the 4-count, +0 to 5'
                print(f"    p={p} {name}: double-root class c={c} roots={xs} k2={k2}  -> {extra}")


def conic_check():
    print("=== conic C_eps: x1^2+x1x2+x2^2 = -eps  (point count vs p, discriminant nonzero check) ===")
    for eps in (1, -1):
        print(f"  eps={eps} (curve for x^3{'+' if eps==1 else '-'}x-c):")
        print(f"    discriminant nonzero (irreducible) for p in {{401,797,101,131,167,197}}: "
              f"{discriminant_check(eps, (401, 797, 101, 131, 167, 197))}")
        for p in (101, 197, 401, 797):
            n = conic_point_count(p, eps)
            n3 = sum(1 for c, xs in roots_by_class(p, eps).items() if len(xs) == 3)
            print(f"    p={p}: |C_eps(F_p)|={n}  (p{'+' if n>=p else '-'}{abs(n-p)}, i.e. p+O(1)); "
                  f"6*n3(3-root classes)={6*n3}  ratio |C|/(6*n3)={n/(6*n3):.4f}")


def density_check():
    print("=== continuum density model: exact vs Monte Carlo ===")
    exact = density_model_exact()
    print(f"  exact: P(k=0)={exact[0]} P(k=1)={exact[1]} P(k=2)={exact[2]} P(k=3)={exact[3]}  "
          f"(E[min]={exact['Emin']}, E[max]={exact['Emax']})")
    mc = density_model_montecarlo(2_000_000)
    print(f"  Monte Carlo (n=2e6): {{{', '.join(f'{j}: {v:.4f}' for j, v in mc.items())}}}")


if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == 'densities':
        density_check()
    elif args and args[0] == 'small':
        small_p_crosscheck()
        double_root_diagnostic()
        conic_check()
    else:
        ps = [int(a) for a in args] if args and args[0].isdigit() else [401, 797]
        density_check()
        print()
        small_p_crosscheck()
        print()
        double_root_diagnostic()
        print()
        conic_check()
        for p in ps:
            full_report(p)
