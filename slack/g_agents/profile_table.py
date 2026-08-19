#!/usr/bin/env python3
"""profile_table.py (agent: profile_table) -- per-residue lift-coverage profile for the +-1-line
cover of a permutation-polynomial box lift, and the expected cost of that cover under the note's
limit law, for GENERAL root-count distributions P_k (not just the cubic's).  Model / background:
docs/research/permutation_cubic_note.md secs 0-3 (read first; this file is built directly on its
formulas and is cross-checked against its numbers throughout).

Setup (recap). p prime, f a permutation polynomial of F_p, box lift
    P = {(X,Y) in [0,2p)^2 : Y == f(X) mod p},  4p points,
4 lifts (r_x+d*p, s_x+e*p), d,e in {0,1}, per residue x.  THE COVER: weight 1 on every +-1 line
(Y-X=const or X+Y=const) with >=4 points of P, weight 1 on every point of P on none of them
("singletons"); cost = 2*L4 + U bounds alpha(f,B) for every box, because a lawful S (no 3
collinear) meets ANY line in <=2 points, so a weight-1 line costs <=2 (2*L4 total) and a singleton
point costs <=1 (U total).

Slope +1: for c = f(x)-x, the roots t of f(t)-t=c split into "class 0" (s_t-r_t = c') and "class 1"
(s_t-r_t = c'+p); with n0 class-0 and n1=k-n0 class-1 roots (k = #roots of that c) the 4 consecutive
integer lines Y-X in {c'-p, c', c'+p, c'+2p} carry (n0, 2n0+n1, n0+2n1, n1) points -- line_counts().
Slope -1 is analogous with lines X+Y in {c'',c''+p,c''+2p,c''+3p} carrying the SAME 4 numbers as a
function of (n0,n1) (note sec 1).  Which of a root's 4 lifts (d,e) sit on which of the 4 lines is a
k-INDEPENDENT rule (note sec 1, "which lifts of a root lie on which line"): only the root's own
class (0 or 1) decides the mapping -- SLOPE_PLUS_MAP / SLOPE_MINUS_MAP below, taken verbatim from
the note's prose.  So "is this a >=4 line" depends on (k,n0) of t's class (via line_counts /
covered_lines), but "which lift lands on which of the 4 lines" is universal in k -- this is exactly
what makes part (1) below a finite, k-independent LOOKUP TABLE composed with a k,n0-dependent
threshold.

PART 1 -- covered_by_slope(...) / lift_profile(...): exact per-residue lift coverage, tabulated for
          k=0..5, all n0, both classes, both slopes; verified against the cubic note's k=3 rule.
PART 2 -- beta(k), q_of(...), expected_cost(...): E[2L4]/p, E[U]/p as explicit functions of the
          P_k's under the limit law (n0|k ~ Uniform{0..k}; x's own class uniform among the k roots;
          the two slopes independent); rencontres(d) for S_d; evaluated at d=3,4,5,6.
PART 3 -- fixed_point_distribution(perms,d): P_k for ANY transitive permutation group (any Galois
          group), so non-S_d cases plug into the exact same expected_cost(); demoed on C_4 (regular
          rep), A_4 and D_5 (natural actions) vs. the S_4/S_5 baselines.

usage:  /Users/iwasborninbali/venvs/sat/bin/python3 slack/g_agents/profile_table.py
(pure Python + fractions, no deps; runs in well under a second)
"""
from fractions import Fraction
from itertools import permutations
import random

# ================================================================================================
# PART 1 -- exact per-residue lift-coverage profile
# ================================================================================================

LIFTS = [(0, 0), (0, 1), (1, 0), (1, 1)]


def line_counts(k, n0):
    """(k,n0) -> the 4 consecutive-line point counts (n0, 2n0+n1, n0+2n1, n1), n1=k-n0.  Identical
    formula for both slopes (note sec 1: slope+ lines Y-X in {c'-p,c',c'+p,c'+2p} and slope- lines
    X+Y in {c'',c''+p,c''+2p,c''+3p} carry the same 4 numbers as a function of (n0,n1))."""
    n1 = k - n0
    return (n0, 2 * n0 + n1, n0 + 2 * n1, n1)


def covered_lines(k, n0):
    """Which of the 4 candidate lines of a (k,n0) class have >=4 points of P (the cover's
    threshold: weight 1 on every +-1 line with >=4 points)."""
    return tuple(c >= 4 for c in line_counts(k, n0))


# lift (d,e) -> line-index (0..3) carrying it, for a root of the given class; k-independent, taken
# verbatim from note sec 1 ("Which lifts of a root lie on which line"):
#   slope +1, class-0 root: lifts d=e (i.e. (0,0),(1,1)) on line c' (idx1);
#                            lift (0,1) on c'+p (idx2); lift (1,0) on c'-p (idx0).
#   slope +1, class-1 root: lifts d=e on line c'+p (idx1->2 shifted, i.e. idx2 in our 0..3 indexing... )
# -- rather than renarrate, the two dicts below just ARE the note's four bullet points, one entry
#    per (lift -> which of the 4 lines {idx0,idx1,idx2,idx3} it lands on).
SLOPE_PLUS_MAP = {
    0: {(1, 0): 0, (0, 0): 1, (1, 1): 1, (0, 1): 2},   # class-0 root of a t3-t=c type equation
    1: {(1, 0): 1, (0, 0): 2, (1, 1): 2, (0, 1): 3},   # class-1 root
}
SLOPE_MINUS_MAP = {
    0: {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 2},   # class-0 root of a t3+t=c type equation
    1: {(0, 0): 1, (0, 1): 2, (1, 0): 2, (1, 1): 3},   # class-1 root
}
MAPS = {'+': SLOPE_PLUS_MAP, '-': SLOPE_MINUS_MAP}


def covered_by_slope(slope, k, n0, cls):
    """Subset of {(0,0),(0,1),(1,0),(1,1)} = the lifts of a class-`cls` root (root of a class of
    size k, n0 of whose k roots are class-0) that lie on a >=4-point line of the given slope ALONE."""
    assert 0 <= n0 <= k and cls in (0, 1)
    big = covered_lines(k, n0)
    m = MAPS[slope][cls]
    return frozenset(lift for lift in LIFTS if big[m[lift]])


def lift_profile(k_p, n0_p, cls_p, k_m, n0_m, cls_m):
    """PART (1) deliverable.  Given, for the SAME residue x: slope+1's (k,n0) of x's own c+(x)
    class and x's own class cls_p within it, and the analogous (k_m,n0_m,cls_m) for slope-1's
    c-(x) class -- return (covered, singles, covered_set):
        covered = #{x's 4 lifts lying on a >=4-point line of EITHER slope}
        singles = 4 - covered = the number of singleton points x contributes to the cover's cost
                  (covered and singles are complementary: covered + singles == 4 always)."""
    cp = covered_by_slope('+', k_p, n0_p, cls_p)
    cm = covered_by_slope('-', k_m, n0_m, cls_m)
    union = cp | cm
    return len(union), 4 - len(union), union


def _fmt_set(s):
    order = {(0, 0): '00', (0, 1): '01', (1, 0): '10', (1, 1): '11'}
    return '{' + ','.join(order[l] for l in LIFTS if l in s) + '}'


def print_single_slope_table():
    print("=" * 100)
    print("PART 1a. Single-slope profile table: covered_by_slope(slope,k,n0,cls) for k=0..5, all n0, both classes.")
    print("Lift labels 'de' mean (delta,epsilon).  #cov = number of x's 4 lifts covered by THIS slope alone.")
    print("=" * 100)
    header = f"{'k':>2} {'n0':>3} {'n1':>3} {'counts':>16} {'cls':>3}  {'slope+ covered':<14} #  {'slope- covered':<14} #"
    print(header)
    for k in range(0, 6):
        for n0 in range(0, k + 1):
            n1 = k - n0
            counts = line_counts(k, n0)
            for cls in ((0, 1) if k >= 1 else (0,)):
                # cls=0 is vacuous once n0==0 (no class-0 roots exist) and cls=1 vacuous once n1==0;
                # we still print them (the lookup is well-defined) but mark the vacuous side with '-'.
                cp = covered_by_slope('+', k, n0, cls)
                cm = covered_by_slope('-', k, n0, cls)
                vac = (cls == 0 and n0 == 0) or (cls == 1 and n1 == 0)
                tag = '  (no such root)' if vac else ''
                print(f"{k:>2} {n0:>3} {n1:>3} {str(counts):>16} {cls:>3}  {_fmt_set(cp):<14} {len(cp)}  {_fmt_set(cm):<14} {len(cm)}{tag}")
        print("-" * 100)


def verify_k3_cubic_rule():
    """Reproduce the cubic note's own words exactly (note sec 1):
    'in a same group the two lifts with delta=epsilon [covered by slope+]'
    'in a split group all lifts except one -- the lift (1,0) if class 0, (0,1) if class 1' [slope+]
    'slope -1: same group: the two mixed lifts; split: all but (0,0) if class0, all but (1,1) if class1'."""
    same_deq = frozenset({(0, 0), (1, 1)})
    same_mixed = frozenset({(0, 1), (1, 0)})
    checks = []
    # SAME groups: n0 in {0,3} (all-class-1 or all-class-0), k=3.
    checks.append(("slope+ same (n0=3,cls=0)", covered_by_slope('+', 3, 3, 0), same_deq))
    checks.append(("slope+ same (n0=0,cls=1)", covered_by_slope('+', 3, 0, 1), same_deq))
    checks.append(("slope- same (n0=3,cls=0)", covered_by_slope('-', 3, 3, 0), same_mixed))
    checks.append(("slope- same (n0=0,cls=1)", covered_by_slope('-', 3, 0, 1), same_mixed))
    # SPLIT groups: n0 in {1,2}, k=3.
    for n0 in (1, 2):
        all4 = frozenset(LIFTS)
        checks.append((f"slope+ split (n0={n0},cls=0) misses (1,0)", covered_by_slope('+', 3, n0, 0), all4 - {(1, 0)}))
        checks.append((f"slope+ split (n0={n0},cls=1) misses (0,1)", covered_by_slope('+', 3, n0, 1), all4 - {(0, 1)}))
        checks.append((f"slope- split (n0={n0},cls=0) misses (0,0)", covered_by_slope('-', 3, n0, 0), all4 - {(0, 0)}))
        checks.append((f"slope- split (n0={n0},cls=1) misses (1,1)", covered_by_slope('-', 3, n0, 1), all4 - {(1, 1)}))
    print("=" * 100)
    print("PART 1b. Verification vs. the cubic note's k=3 rule (verbatim quotes above each block).")
    print("=" * 100)
    ok = True
    for name, got, want in checks:
        status = "PASS" if got == want else "FAIL"
        ok = ok and (got == want)
        print(f"  [{status}] {name}: got {_fmt_set(got)}  want {_fmt_set(want)}")
    assert ok, "k=3 verification against the cubic note FAILED"
    print("All k=3 checks PASS: covered_by_slope reproduces the cubic note's rule exactly.\n")


def demo_lift_profile():
    print("=" * 100)
    print("PART 1c. lift_profile(k_p,n0_p,cls_p, k_m,n0_m,cls_m) usage examples (combining BOTH slopes' data).")
    print("=" * 100)
    examples = [
        # (k_p,n0_p,cls_p, k_m,n0_m,cls_m, label)
        (3, 3, 0, 3, 3, 0, "cubic, same+same (x is the class-0 root of a (3,3) group on both slopes)"),
        (3, 1, 0, 3, 1, 1, "cubic, split+split, class0 on slope+, class1 on slope- (max double coverage)"),
        (3, 0, 1, 1, 1, 0, "cubic, same on slope+ (all-class1 group) but a k=1 singleton residue on slope-"),
        (1, 1, 0, 1, 1, 0, "x isolated on BOTH slopes (k=1 each): the purest singleton, 0 lifts covered"),
        (5, 4, 0, 4, 1, 1, "quintic/quartic mix: k=5,n0=4 (split, cls0) on +; k=4,n0=1 (split, cls1) on -"),
    ]
    for k_p, n0_p, cls_p, k_m, n0_m, cls_m, label in examples:
        covered, singles, uset = lift_profile(k_p, n0_p, cls_p, k_m, n0_m, cls_m)
        print(f"  {label}")
        print(f"    (k+,n0+,cls+)=({k_p},{n0_p},{cls_p})  (k-,n0-,cls-)=({k_m},{n0_m},{cls_m})"
              f"  -> covered={covered} singles={singles}  covered_set={_fmt_set(uset)}")
    print()


# ================================================================================================
# PART 2 -- expected cost per residue under the limit law, as a function of the P_k's
# ================================================================================================
#
# Limit law (as given): for EACH slope independently, the number of roots k of x's own class has
# P(k roots) = P_k; given k, n0 (# class-0 roots) is Uniform{0,...,k} (this is exactly the discrete
# uniform marginal of Binomial(k,theta) mixed over theta~Uniform(0,1), the "mixture of Binomial(k,
# theta) over uniform theta" of the background, i.e. the Beta(1,1)-Binomial identity
#   integral_0^1 C(k,n0) theta^n0 (1-theta)^(k-n0) dtheta = 1/(k+1)  for every n0 = 0..k);
# and x's own class is uniform among the k roots of its class (so P(cls(x)=0 | k,n0) = n0/k); the
# two slopes are independent for the same x.
#
# 2*L4 is a sum over LINES (equivalently over residue CLASSES c, one per slope): a class of size k
# with n0 class-0 roots contributes B(k,n0) := #{of its 4 candidate lines with >=4 points} big
# lines, each counted with weight 2 (a lawful set meets ANY line in <=2 points).  Since classes are
# drawn from P_k UNBIASED over c (P_k is defined as "proportion of residue CLASSES", i.e. of the p
# values of c, that's already exactly the right averaging -- no size-bias correction needed here):
#
#   E[2*L4]/p  =  2 * sum_over_slopes  sum_{k=0}^{d}  P_k^sigma * beta(k),
#   beta(k) := (1/(k+1)) * sum_{n0=0}^{k} B(k,n0)                                     ... (*)
#
# U is a sum over RESIDUES x (sec 2 of the note literally defines it that way).  A uniformly random
# residue x lands in a class of size k with probability proportional to k*P_k (size-biased: classes
# with more roots contain more residues) -- but conveniently this size bias exactly cancels against
# the "1/k" of splitting a class's roots by class label, see the derivation in q_of() below, leaving
# again a clean sum weighted by P_k/(k+1).  With q_sigma(lift) := P(a given lift of x is covered by
# slope sigma ALONE), independence of the two slopes gives
#
#   E[U]/p  =  sum_{lift in the 4 lifts}  (1 - q_+(lift)) * (1 - q_-(lift))            ... (**)
#
# and cost/p = E[2L4]/p + E[U]/p, cost/(2p) = cost/p / 2.  (*) and (**) are the GENERAL FORMULA of
# part (3): plug in ANY sequence(s) of P_k (summing to 1, with sum_k k*P_k = 1 -- see note below)
# for either or both slopes.


def B(k, n0):
    """#{of the 4 candidate lines of a (k,n0) class that carry >=4 points}."""
    return sum(1 for c in line_counts(k, n0) if c >= 4)


def beta(k):
    """beta(k) = E_{n0 ~ Uniform{0..k}}[ B(k,n0) ], exact Fraction."""
    return Fraction(sum(B(k, n0) for n0 in range(k + 1)), k + 1)


def q_of(lift, slope, Pk):
    """q_sigma(lift) = P(this lift of a uniformly random residue x is covered by slope `slope`
    alone), under the limit law, as an explicit function of Pk = [P_0, P_1, ..., P_d].

    Derivation: P(k(x)=k) = k*P_k (size-biased -- classes with k roots hold k of the p residues);
    given k, n0 ~ Uniform{0..k}; given (k,n0), P(cls(x)=0)=n0/k, P(cls(x)=1)=(k-n0)/k.  So
        q(lift) = sum_k [k*P_k] * (1/(k+1)) * sum_{n0=0}^k (1/k)*[n0*cov(lift|k,n0,0) + (k-n0)*cov(lift|k,n0,1)]
                = sum_k [P_k/(k+1)] * sum_{n0=0}^k [n0*cov(lift|k,n0,0) + (k-n0)*cov(lift|k,n0,1)]
    (the size-bias factor k and the 1/k of averaging over the k roots cancel exactly, for every
    k>=1; the k=0 term contributes 0 either way since no residue is ever a member of a 0-root
    class)."""
    total = Fraction(0)
    for k, Pk_k in enumerate(Pk):
        if Pk_k == 0 or k == 0:
            continue
        inner = 0
        for n0 in range(k + 1):
            n1 = k - n0
            c0 = 1 if lift in covered_by_slope(slope, k, n0, 0) else 0
            c1 = 1 if lift in covered_by_slope(slope, k, n0, 1) else 0
            inner += n0 * c0 + n1 * c1
        total += Pk_k * Fraction(inner, k + 1)
    return total


def _check_Pk(Pk, name):
    s = sum(Pk)
    assert s == 1, f"{name}: sum(P_k) = {s} != 1"
    ek = sum(k * pk for k, pk in enumerate(Pk))
    assert ek == 1, f"{name}: sum(k*P_k) = {ek} != 1 (violates sum_c k(c) = p)"


def expected_cost(Pk_plus, Pk_minus=None, check=True, label_plus="+", label_minus="-"):
    """PART (2)/(3) deliverable.  Pk_plus, Pk_minus: sequences of Fraction/int, index k=0..d,
    summing to 1, with sum_k k*P_k = 1 (automatic for ANY transitive permutation-group action by
    Burnside/orbit-counting -- see fixed_point_distribution below).  Pk_minus defaults to Pk_plus
    (both slopes share one Galois group / root-count law, the situation in the task and in the
    cubic note).  Returns a dict of exact Fractions: E_2L4, E_U, E_cost (all "per p"), and
    E_cost_over_2p = the reported constant (11/8 for the cubic)."""
    if Pk_minus is None:
        Pk_minus = Pk_plus
    if check:
        _check_Pk(Pk_plus, f"Pk_{label_plus}")
        _check_Pk(Pk_minus, f"Pk_{label_minus}")
    E_L4_plus = sum(Pk_plus[k] * beta(k) for k in range(len(Pk_plus)))
    E_L4_minus = sum(Pk_minus[k] * beta(k) for k in range(len(Pk_minus)))
    E_2L4 = 2 * (E_L4_plus + E_L4_minus)
    q_plus = {lift: q_of(lift, '+', Pk_plus) for lift in LIFTS}
    q_minus = {lift: q_of(lift, '-', Pk_minus) for lift in LIFTS}
    E_U = sum((1 - q_plus[l]) * (1 - q_minus[l]) for l in LIFTS)
    E_cost = E_2L4 + E_U
    return {
        "E_2L4": E_2L4, "E_U": E_U, "E_cost": E_cost, "E_cost_over_2p": E_cost / 2,
        "q_plus": q_plus, "q_minus": q_minus,
    }


# ---- rencontres numbers for S_d (P_k = #{permutations of d with exactly k fixed points} / d!) ----

def derangements_upto(m):
    D = [1, 0]
    for i in range(2, m + 1):
        D.append((i - 1) * (D[i - 1] + D[i - 2]))
    return D  # D[i] = number of derangements of i elements


def comb(n, r):
    num = 1
    for i in range(r):
        num = num * (n - i) // (i + 1)
    return num


def rencontres(d):
    """Closed form: P_k = C(d,k) * D_{d-k} / d! for k=0..d."""
    D = derangements_upto(d)
    fact_d = 1
    for i in range(2, d + 1):
        fact_d *= i
    return [Fraction(comb(d, k) * D[d - k], fact_d) for k in range(d + 1)]


def rencontres_bruteforce(d):
    """Cross-check of rencontres(d): literally enumerate all d! permutations of range(d) and count
    fixed points -- 'P_k = number of permutations of d elements with exactly k fixed points / d!'
    exactly as worded in the task.  (720 permutations at d=6: trivial.)"""
    return fixed_point_distribution(permutations(range(d)), d)


# ================================================================================================
# PART 3 -- general root-count distributions from an arbitrary (transitive) permutation group
# ================================================================================================

def fixed_point_distribution(perms, d):
    """P_k for ANY finite list/iterable of permutations of range(d) (a subgroup G <= S_d, meant to
    be the Galois group of f(t)-t-C, resp. f(t)+t-C, over F_p(C), acting on its d roots): P_k =
    #{g in G : g has exactly k fixed points} / |G|.  For a TRANSITIVE G this automatically satisfies
    sum_k k*P_k = 1, by Burnside/orbit-counting ((1/|G|) sum_g fix(g) = #orbits = 1) -- i.e. the
    'sum_c k(c) = p' identity of the note is exactly the permutation-group-theoretic statement that
    G acts transitively on the d roots."""
    perms = list(perms)
    counts = [0] * (d + 1)
    for g in perms:
        assert len(g) == d
        fx = sum(1 for i in range(d) if g[i] == i)
        counts[fx] += 1
    n = len(perms)
    return [Fraction(c, n) for c in counts]


def is_even_permutation(perm):
    n = len(perm)
    seen = [False] * n
    cycles = 0
    for i in range(n):
        if not seen[i]:
            cycles += 1
            j = i
            while not seen[j]:
                seen[j] = True
                j = perm[j]
    return (n - cycles) % 2 == 0


def cyclic_regular_rep(d):
    """C_d acting on itself by translation (regular representation): perm_r(i) = (i+r) mod d."""
    return [tuple((i + r) % d for i in range(d)) for r in range(d)]


def alternating_group(d):
    """A_d = even permutations of S_d, natural action on d points."""
    return [p for p in permutations(range(d)) if is_even_permutation(p)]


def dihedral_natural_action(d):
    """D_d (order 2d) acting on the d vertices of a regular d-gon: d rotations + d reflections."""
    rot = [tuple((i + r) % d for i in range(d)) for r in range(d)]
    refl = [tuple((k - i) % d for i in range(d)) for k in range(d)]
    return rot + refl


# ================================================================================================
# Monte-Carlo cross-check of expected_cost(), sampling directly from the stated generative model
# (independent of the exact-Fraction machinery above -- a bug in one is unlikely to be masked by
# a matching bug in the other).  Mirrors the style of slack/cube_local_law.py.
# ================================================================================================

def monte_carlo_check(Pk, trials=400_000, seed=1):
    rng = random.Random(seed)
    ks = list(range(len(Pk)))
    weights = [float(p) for p in Pk]

    def sample_class_level():  # unbiased over c: used for the 2*L4 average
        k = rng.choices(ks, weights=weights)[0]
        n0 = rng.randint(0, k) if k > 0 else 0
        return k, n0

    def sample_x_level():  # size-biased over x: used for the U average
        xw = [k * w for k, w in zip(ks, weights)]
        k = rng.choices(ks, weights=xw)[0]
        n0 = rng.randint(0, k)
        cls = 0 if rng.random() < n0 / k else 1
        return k, n0, cls

    # E[2L4]/p, one slope (both slopes share Pk here; total is 2x this by symmetry of the model).
    tot_B = 0
    for _ in range(trials):
        k, n0 = sample_class_level()
        tot_B += B(k, n0)
    mc_L4_one_slope = tot_B / trials
    mc_2L4 = 2 * (2 * mc_L4_one_slope)  # x2 for the "2*" weight, x2 for the two (identical) slopes

    # E[U]/p: need BOTH slopes' independent (k,n0,cls) per trial x.
    tot_singles = 0
    for _ in range(trials):
        k_p, n0_p, cls_p = sample_x_level()
        k_m, n0_m, cls_m = sample_x_level()
        _, singles, _ = lift_profile(k_p, n0_p, cls_p, k_m, n0_m, cls_m)
        tot_singles += singles
    mc_U = tot_singles / trials

    return mc_2L4, mc_U


# ================================================================================================
if __name__ == "__main__":
    print_single_slope_table()
    verify_k3_cubic_rule()
    demo_lift_profile()

    print("=" * 100)
    print("PART 2. beta(k) = E_{n0~U{0..k}}[B(k,n0)] (expected # big lines per class of size k, one slope):")
    print("=" * 100)
    for k in range(0, 9):
        print(f"  beta({k}) = {beta(k)}  (= {float(beta(k)):.4f})")
    print()

    print("=" * 100)
    print("PART 2. Cubic sanity check: hardcoded P_k=[1/3,1/2,0,1/6] (the note's own numbers) must give 11/8.")
    print("=" * 100)
    Pk_cubic_hardcoded = [Fraction(1, 3), Fraction(1, 2), Fraction(0), Fraction(1, 6)]
    Pk_cubic_rencontres = rencontres(3)
    print(f"  hardcoded P_k = {[str(x) for x in Pk_cubic_hardcoded]}")
    print(f"  rencontres(3) = {[str(x) for x in Pk_cubic_rencontres]}")
    assert Pk_cubic_hardcoded == Pk_cubic_rencontres, "rencontres(3) does not match the note's cubic P_k!"
    res_cubic = expected_cost(Pk_cubic_hardcoded)
    print(f"  E[2L4]/p = {res_cubic['E_2L4']} = {float(res_cubic['E_2L4']):.6f}   (note: -> 1 exactly, sec 3)")
    print(f"  E[U]/p   = {res_cubic['E_U']}   = {float(res_cubic['E_U']):.6f}   (note: -> 7/4 exactly, sec 3)")
    print(f"  cost/p   = {res_cubic['E_cost']}  = {float(res_cubic['E_cost']):.6f}  (note: -> 11/4 exactly, sec 3)")
    print(f"  cost/(2p)= {res_cubic['E_cost_over_2p']} = {float(res_cubic['E_cost_over_2p']):.6f}"
          f"   <-- must equal 11/8 = {float(Fraction(11, 8)):.6f}")
    assert res_cubic["E_2L4"] == 1, res_cubic["E_2L4"]
    assert res_cubic["E_U"] == Fraction(7, 4), res_cubic["E_U"]
    assert res_cubic["E_cost_over_2p"] == Fraction(11, 8), res_cubic["E_cost_over_2p"]
    print("  EXACT MATCH to the cubic note's closed form (2L4/p->1, U/p->7/4, cost/(2p)->11/8). PASS\n")

    mc_2L4, mc_U = monte_carlo_check(Pk_cubic_hardcoded, trials=300_000, seed=2)
    print(f"  Monte Carlo (300000 trials, direct sampling of the generative model): "
          f"2L4/p~{mc_2L4:.4f} (exact {float(res_cubic['E_2L4']):.4f}), "
          f"U/p~{mc_U:.4f} (exact {float(res_cubic['E_U']):.4f})\n")

    print("=" * 100)
    print("PART 2. Rencontres distributions of S_d, d=3..6 -- cost/(2p) and comparison to 3/2.")
    print("=" * 100)
    print(f"{'d':>2} {'P_k (k=0..d)':<55} {'E[2L4]/p':>10} {'E[U]/p':>10} {'cost/p':>10} {'cost/(2p)':>12} {'<3/2?':>6}")
    for d in range(3, 7):
        Pk = rencontres(d)
        Pk_bf = rencontres_bruteforce(d)
        assert Pk == Pk_bf, f"d={d}: closed-form rencontres != brute-force enumeration ({Pk} vs {Pk_bf})"
        res = expected_cost(Pk)
        pk_str = "[" + ",".join(str(x) for x in Pk) + "]"
        below = res["E_cost_over_2p"] < Fraction(3, 2)
        print(f"{d:>2} {pk_str:<55} {float(res['E_2L4']):>10.6f} {float(res['E_U']):>10.6f} "
              f"{float(res['E_cost']):>10.6f} {str(res['E_cost_over_2p'])+' ':>7}{float(res['E_cost_over_2p']):>6.4f} "
              f"{'YES' if below else 'NO':>6}")
    print()
    print("  (d=3 row must read cost/(2p) = 11/8 = 1.375 exactly, matching the check above.)\n")

    print("=" * 100)
    print("PART 3. General formula plugged in with a DIFFERENT Galois group than S_d (same d).")
    print("Burnside check: sum_k k*P_k = 1 for every TRANSITIVE group action, printed as 'avg fix'.")
    print("=" * 100)
    groups = [
        ("S_4  (order 24, natural action)", list(permutations(range(4))), 4),
        ("A_4  (order 12, natural action)", alternating_group(4), 4),
        ("C_4  (order 4, regular rep.)   ", cyclic_regular_rep(4), 4),
        ("S_5  (order 120, natural action)", list(permutations(range(5))), 5),
        ("D_5  (order 10, natural action) ", dihedral_natural_action(5), 5),
    ]
    for name, perms, d in groups:
        Pk = fixed_point_distribution(perms, d)
        avg_fix = sum(k * pk for k, pk in enumerate(Pk))
        res = expected_cost(Pk)
        pk_str = "[" + ",".join(str(x) for x in Pk) + "]"
        print(f"  {name}  |G|={len(perms):>3}  P_k={pk_str}")
        print(f"    avg#fix(=sum k*P_k)={avg_fix}  E[2L4]/p={float(res['E_2L4']):.4f}  "
              f"E[U]/p={float(res['E_U']):.4f}  cost/(2p)={res['E_cost_over_2p']} = {float(res['E_cost_over_2p']):.4f}"
              f"  <3/2? {'YES' if res['E_cost_over_2p'] < Fraction(3,2) else 'NO'}")
    print()
    print("  Bonus: the two slopes need NOT share a Galois group -- expected_cost(Pk_plus, Pk_minus)")
    print("  accepts two independent distributions.  Example: slope+ ~ S_4, slope- ~ A_4:")
    res_mixed = expected_cost(fixed_point_distribution(permutations(range(4)), 4),
                               fixed_point_distribution(alternating_group(4), 4),
                               label_plus="S_4", label_minus="A_4")
    print(f"    cost/(2p) = {res_mixed['E_cost_over_2p']} = {float(res_mixed['E_cost_over_2p']):.4f}"
          f"  <3/2? {'YES' if res_mixed['E_cost_over_2p'] < Fraction(3,2) else 'NO'}")

    print()
    print("=" * 100)
    print("BONUS (floats, not exact -- for context only): the d->infinity limit of S_d's rencontres")
    print("law is Poisson(1), P_k -> e^-1/k! (fixed points of a 'random' large permutation).")
    print("=" * 100)
    import math
    K = 40
    Pk_pois = [math.exp(-1) / math.factorial(k) for k in range(K + 1)]
    Pk_pois[-1] += 1 - sum(Pk_pois)  # dump negligible tail (~1e-50) into the last bucket
    res_pois = expected_cost(Pk_pois, check=False)
    print(f"  Poisson(1): E[2L4]/p={float(res_pois['E_2L4']):.6f}  E[U]/p={float(res_pois['E_U']):.6f}  "
          f"cost/(2p)={float(res_pois['E_cost_over_2p']):.6f}  (d=6 was already {float(expected_cost(rencontres(6))['E_cost_over_2p']):.6f} "
          f"-- fast convergence, both comfortably < 3/2)")
