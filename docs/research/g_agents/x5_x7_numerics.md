# x5_x7_numerics — box-lift numerics for f(x) = x⁵, x⁷ (permutation monomials), box (0,0)

*(agent `x5_x7_numerics`, 2026-08-19; code `slack/g_agents/x5_x7_numerics.py`, `x5_x7_numerics_pooled.py`,
`x5_x7_numerics_exact_constant.py`; raw output `slack/g_agents/x5_x7_numerics_output.txt` (453 lines, all
13 primes in full detail), `..._pooled_output.txt`, `..._exact_constant_output.txt`; data
`slack/g_agents/x5_x7_numerics_results.json`; reuses `slack/lp_curve.py` unmodified for part (d))*

Model: `docs/research/permutation_cubic_note.md` §0–3 (the k=3 case, proved rigorously there). This
note redoes its numerics for f(x) = x⁵ and x⁷, and checks how far its k=3 local law (rencontres marginal
+ uniform n0|k + slope-independence) extends empirically to these higher odd degrees.

## 0. Headline numbers

| f | mean cost/(2p) (explicit cover) | mean LP/(2p) (±1-lines, fractional) | idealized-model constant (exact) |
|---|---|---|---|
| x³ (note, rigorous) | 1.35–1.38 at p≤401 | 1.317–1.355 at p≤197 | **11/8 = 1.375000** |
| x⁵ (7 primes, 197–887) | **1.3884** (1.3618–1.4068) | **1.3241** (1.2867–1.3553) | **12059/8640 = 1.395718** |
| x⁷ (6 primes, 263–887) | **1.4151** (1.3940–1.4340) | **1.3432** (1.3156–1.3641) | **203347/145152 = 1.400925** |

The "idealized-model constant" is a p-independent exact rational number, computed by generalizing the
note's own §2–3 bookkeeping to general k under its own three hypotheses (H1)–(H3) below; run on k=3 it
reproduces the note's proven **11/8 exactly**, which is a strong correctness check on the whole
machinery (§5). For k=5, 7 the same hypotheses are only checked numerically here (§§2–3), not proved, so
those two constants are conjectural, not theorems. Both increase mildly with degree, and the finite-p
means sit close to (a bit above, as expected from `+O(√p)` fluctuations pulling either way at these
sizes) the corresponding constant.

**I did not find any output from a `profile_table` agent anywhere in the repo at run time** (checked
`docs/research/g_agents/`, `slack/g_agents/`, and `grep -r profile_table .`); part (c)'s prediction is
therefore self-derived rather than a cross-check against that agent's numbers.

## 1. Setup

f(x) = xᵏ mod p is a permutation of F_p iff gcd(k, p−1) = 1. Checking the task's example prime lists
against this condition turns up two entries that don't satisfy it:

- **p = 401 is in the task's x⁵ list, but gcd(5, 400) = 5 ≠ 1** — x⁵ is *not* a permutation of F₄₀₁ (400 =
  16·25). Dropped from the x⁵ sweep; kept for x⁷ (gcd(7,400)=1).
- **p = 449 is in the task's x⁷ list, but gcd(7, 448) = 7 ≠ 1** — x⁷ is *not* a permutation of F₄₄₉ (448 =
  2⁶·7). Dropped from the x⁷ sweep; kept for x⁵ (gcd(5,448)=1).

Final prime lists used (candidates {197,263,293,401,449,599,797,887}, filtered by the gcd condition; 797
and 887 added beyond the task's examples to get more classes per k′ bin and a longer p-range for trend/
fluctuation visibility — all runs together take under 5 seconds of wall-clock, so this was free):

- **x⁵** (gcd(5,p−1)=1): 197, 263, 293, 449, 599, 797, 887
- **x⁷** (gcd(7,p−1)=1): 263, 293, 401, 599, 797, 887

Box is (0,0) throughout, per the task. All class/root/line bookkeeping (roots of f(t)∓t=c, class-0/1 of
a root, the four line sizes (n₀, 2n₀+n₁, n₀+2n₁, n₁) owned by a class) was **re-derived from scratch**
from the affine lift structure (not copied from the note) and matches the note's formulas exactly for
general k, not just k=3 — see the module docstring of `x5_x7_numerics.py` for the derivation.

**Validation against the note's own numbers** (before trusting anything new): running the same
machinery at k=3, p=197, box (0,0) gives `L4=97 (47+50), U=350, cost=544` — **exactly** the note's
reported value (§4: "p=197 ... cost 544 ... "), and the k=3 class count is 33 = N₃ = (197+1)/6 on both
slopes, also exact. This is a strong sanity check that the general-k code is correct.

## 2. Part (a): the k′-distribution vs the rencontres law of S_k

For a permutation polynomial f of degree k, t^k − t − c is a degree-k polynomial in t for a "generic"
irreducible-Galois-group trinomial family; if its Galois group (as c varies) is the full symmetric group
S_k, Chebotarev predicts the number of roots k′ in F_p to be asymptotically distributed as the number of
fixed points of a uniform random permutation of k letters — the **rencontres numbers**
P(k′) = C(k,k′)·D_{k−k′}/k! (D_m = derangements of m). This is exactly what the note found for k=3
(1/3, 1/2, 0, 1/6, §0). The alternative the task asks to weigh against is a **smaller Galois group** for
the trinomial family (which would skew the k′-distribution away from rencontres).

**Pooled counts** (all usable primes combined, 3485 classes for x⁵, 3240 for x⁷ — pooling matters because
a single prime gives only 0–8 classes with k′≥4):

x⁵, S₅ rencontres vs pooled empirical (χ² with 4 dof, since renc(4)=0 is excluded):

| k′ | renc P(k′) | # plus (of 3485) | pooled P₊ | # minus | pooled P₋ |
|---|---|---|---|---|---|
| 0 | 0.3667 | 1286 | 0.3690 | 1318 | 0.3782 |
| 1 | 0.3750 | 1276 | 0.3661 | 1240 | 0.3558 |
| 2 | 0.1667 | 612 | 0.1756 | 602 | 0.1727 |
| 3 | 0.0833 | 285 | 0.0818 | 292 | 0.0838 |
| 4 | 0.0000 | 0 | 0.0000 | 0 | 0.0000 |
| 5 | 0.0083 | 26 | 0.0075 | 33 | 0.0095 |

χ²(dof=4): plus = 2.87, minus = 6.00 (95th-percentile guide ≈ 9.7) — **no evidence against rencontres**.

x⁷, S₇ rencontres vs pooled empirical (χ² with 6 dof):

| k′ | renc P(k′) | # plus (of 3240) | pooled P₊ | # minus | pooled P₋ |
|---|---|---|---|---|---|
| 0 | 0.3679 | 1178 | 0.3636 | 1170 | 0.3611 |
| 1 | 0.3681 | 1228 | 0.3790 | 1239 | 0.3824 |
| 2 | 0.1833 | 566 | 0.1747 | 576 | 0.1778 |
| 3 | 0.0625 | 208 | 0.0642 | 193 | 0.0596 |
| 4 | 0.0139 | 44 | 0.0136 | 44 | 0.0136 |
| 5 | 0.0042 | 16 | 0.0049 | 16 | 0.0049 |
| 6 | 0.0000 | 0 | 0.0000 | 0 | 0.0000 |
| 7 | 0.0002 | 0 | 0.0000 | 2 | 0.0006 |

χ²(dof=6): plus = 3.82, minus = 6.56 (95th-percentile guide ≈ 12.9) — again **no evidence against
rencontres**; k=4 (the rarest nonzero bin) matches to 3 decimal places on both slopes at both k_pow.
k′=6 never occurs in any of the 6725 pooled classes across both degrees, matching renc(6)=0 exactly for
both S₅ and S₇ (a permutation can't fix exactly n−1 of n points). **Verdict: x⁵ and x⁷ behave like generic
trinomials with full symmetric Galois group S₅, S₇ — no sign of the "smaller Galois group" alternative** at
these primes; per-prime tables (noisier, single-p samples) are in the raw output file, L1-distances to
rencontres range 0.01–0.17 per prime, shrinking in the pooled data as expected.

## 3. Part (b): the n₀ | k′ distribution — is it Uniform{0,...,k′}?

Pooled counts, cells with <5 pooled classes omitted (too little signal):

**x⁵:** plus k=2 (612 classes): n₀ = 206/200/206 (expect 204 each, χ²=0.12, dof2). plus k=3 (285): 72/72/
72/69 (expect 71.25, χ²=0.09). plus k=5 (26, small): 9/3/3/3/3/5 (χ²=6.77, dof5 — largest deviation, but
n=26 is a tiny sample and 9 total independent-ish comparisons were run in this table, so one χ²≈6.8 is not
surprising). minus k=2 (602): 199/204/199 (χ²=0.08). minus k=3 (292): 71/75/75/71 (χ²=0.22). minus k=5
(33): 5/7/5/5/6/5 (χ²=0.64).

**x⁷:** plus k=2 (566): 179/208/179 (χ²=2.97). plus k=3 (208): 64/43/43/58 (χ²=6.58, dof3). plus k=4 (44):
9/9/8/9/9 (χ²=0.09, very uniform). plus k=5 (16, small): 1/4/3/3/4/1 (χ²=3.50). minus k=2 (576): 180/216/
180 (χ²=4.50). minus k=3 (193): 49/49/46/49 (χ²=0.14). minus k=4 (44): 4/13/10/13/4 (χ²=9.41, dof4 —
largest deviation in the whole sweep, p≈0.05 territory on its own, but again one flagged cell out of ~18
tested is squarely consistent with multiple-comparison noise, not a systematic bias — it isn't repeated at
the corresponding plus-slope k=4 row, which is the most uniform row in the table). minus k=5 (16): 4/2/2/
2/2/4 (χ²=2.00).

**Verdict: no systematic departure from Uniform{0,...,k′}** — every k with a reasonably-sized pooled
sample (k=2,3, and k=4 for x⁷) looks close to flat, the two mildly elevated χ² cells (plus-k=3 and
minus-k=4 for x⁷) don't point in a consistent direction across the sister slope/degree, and the exactly-0
or barely-elevated cells (k=2,3 mostly) carry the bulk of the mass. Consistent with the note's Weil-
equidistribution argument (§3: "the roots' positions are jointly equidistributed... n₀ is UNIFORM on
{0,...,k} in the limit") having no obstruction at k=5,7 either.

## 4. Part (c): exact cover cost vs. self-derived prediction

The cover: weight 1 on every ±1-line (either slope) with ≥4 points of P, weight 1 on every point of P on
none of them; cost = 2·L4 + U (note §2). Computed two ways:

1. **EXACT**, brute-force over the actual 4p points of P (bucket by Y−X and Y+X, count line sizes
   directly, no formulas) — this is ground truth, no modeling assumptions.
2. **PREDICTED**, built from parts (a)+(b) plus the note's third hypothesis, **slope-independence**
   (§3: "the two slopes' groups of a residue x are independent in the limit") — generalizing the note's
   §2 bookkeeping (which lines a class's roots land on, given class label + n₀,n₁) to arbitrary k, then
   combining plus- and minus-class draws at a residue as *independent* to get the singleton count U.
   Two flavours: **pred_emp** plugs the *actual observed* P_k at this p (isolates hypotheses (H2)
   uniform-n₀|k and (H3) independence, since (H1) is fed the true data); **pred_ideal** additionally
   replaces P_k by the rencontres law (tests all of H1–H3 as a single asymptotic package — this is the one
   that gives a p-independent exact constant, §5).

Full per-prime table (all 13 (p,k) runs; L4± = #big lines per slope, U = #singleton points):

| k | p | L4₊ | L4₋ | L4 | U | cost | cost/2p | pred_emp/2p | pred_ideal/2p | LP(pm1) | LP/2p | LP/p |
|---|---|-----|-----|----|----|------|---------|-------------|---------------|---------|-------|------|
| 5 | 197 | 41 | 54 | 95 | 360 | 550 | 1.3959 | 1.4355 | 1.3957 | 534 | 1.3553 | 2.7107 |
| 5 | 263 | 71 | 58 | 129 | 482 | 740 | 1.4068 | 1.3924 | 1.3957 | 708 | 1.3460 | 2.6920 |
| 5 | 293 | 77 | 84 | 161 | 476 | 798 | 1.3618 | 1.3440 | 1.3957 | 754 | 1.2867 | 2.5734 |
| 5 | 449 | 119 | 125 | 244 | 770 | 1258 | 1.4009 | 1.3799 | 1.3957 | 1176 | 1.3096 | 2.6192 |
| 5 | 599 | 157 | 166 | 323 | 1020 | 1666 | 1.3907 | 1.3906 | 1.3957 | 1582 | 1.3205 | 2.6411 |
| 5 | 797 | 227 | 212 | 439 | 1296 | 2174 | 1.3639 | 1.3864 | 1.3957 | 2090 | 1.3112 | 2.6223 |
| 5 | 887 | 221 | 230 | 451 | 1580 | 2482 | 1.3991 | 1.3944 | 1.3957 | 2376 | 1.3393 | 2.6787 |
| 7 | 263 | 69 | 56 | 125 | 484 | 734 | 1.3954 | 1.4036 | 1.4009 | 692 | 1.3156 | 2.6312 |
| 7 | 293 | 67 | 76 | 143 | 544 | 830 | 1.4164 | 1.3971 | 1.4009 | 788 | 1.3447 | 2.6894 |
| 7 | 401 | 107 | 110 | 217 | 710 | 1144 | 1.4264 | 1.4217 | 1.4009 | 1084 | 1.3516 | 2.7032 |
| 7 | 599 | 153 | 138 | 291 | 1124 | 1706 | 1.4240 | 1.4068 | 1.4009 | 1624 | 1.3556 | 2.7112 |
| 7 | 797 | 203 | 210 | 413 | 1396 | 2222 | 1.3940 | 1.3844 | 1.4009 | 2116 | 1.3275 | 2.6550 |
| 7 | 887 | 201 | 204 | 405 | 1734 | 2544 | 1.4340 | 1.4159 | 1.4009 | 2420 | 1.3641 | 2.7283 |

`pred_emp` tracks `cost` closely (typically within 1–2%, e.g. p=599,k=5: 1.3906 predicted vs 1.3907
exact — a near-perfect hit; mean absolute relative error across all 13 rows ≈ 1.3%), which is a decent
numeric confirmation of (H2)+(H3) at these sizes given they're doing real work (U is ~3–4× L4 in every
row, and U is exactly the part that depends on cross-slope independence).

### The exact idealized constant

Because `pred_ideal` plugs in the p-independent rencontres law for P_k, the whole prediction becomes an
*exact rational number times p* — i.e. cost/(2p) → a fixed constant as p → ∞ *under hypotheses
(H1)-(H3)*, computed symbolically (Python `Fraction`, no floating point) in
`x5_x7_numerics_exact_constant.py`:

| k | E[L4 per class per slope] | E[U per residue] | **idealized limit of cost/(2p)** | decimal |
|---|---|---|---|---|
| 3 | 1/4 | 7/4 | **11/8** | 1.375000 |
| 5 | 31/120 | 1519/864 | **12059/8640** | 1.395718 |
| 7 | 877/3360 | 637871/362880 | **203347/145152** | 1.400925 |

The k=3 row reproduces the note's *proven* Theorem G3.5 constant (11/8) **exactly** — not approximately,
bit-for-bit as a fraction — which is a strong correctness check on the general-k generalization (rencontres
marginal + uniform-n₀|k + slope-independence + the per-root line-membership bookkeeping, all re-derived
independently of the note for this task). The k=5, 7 values are new: **conjectural** limiting constants for
this specific explicit cover, valid if (H1)-(H3) extend to x⁵, x⁷ the way the note proves them for x³ (its
proof uses Weil equidistribution on the genus-0 root conic of a *cubic* trinomial specifically — that
argument doesn't immediately transfer to quintic/septic trinomials, whose root varieties have larger genus,
so proving (H1)-(H3) at k=5,7 is genuinely open; here they are only checked numerically, §§2-3, and pass).
The empirical means (1.3884 for x⁵ over 7 primes, 1.4151 for x⁷ over 6 primes) bracket their respective
idealized constants (1.3957, 1.4009) from both sides across the individual primes, consistent with
`O(√p)`-scale fluctuations around a genuine limit rather than a systematic offset.

## 5. Part (d): LP over all ±1-lines (fractional), for calibration

Using `slack/lp_curve.py`'s own `curve_points`/`lines`/`solve` (imported, not reimplemented; only mode
`'pm1'` was run — "the LP over all ±1-lines" the task asks for; that script's separate `'all'`-lines mode is
a different, much more expensive calibration (O(p²) line-pair enumeration into a ~30× larger LP — 93s at
p=599 vs 0.34s for pm1-only) that is not part of this task and was skipped for wall-clock reasons after
confirming the pm1-only path is fast; see LP/(2p), LP/p columns in the §4 table above). Every LP value
sits strictly below the exact combinatorial-cover cost at the same (p,k) — LP/(2p) averages 1.3241 (x⁵) and
1.3432 (x⁷), vs cost/(2p) averages 1.3884 and 1.4151 — confirming the ≥4-line+singleton cover is not tight
even restricted to ±1-lines, same qualitative picture as the note's own remark for k=3 ("the LP over all
±1-lines is a little better, 1.32–1.36 N" vs the cover's 11/8 = 1.375, §0/§4). The x⁵, x⁷ LP ranges
(1.29–1.36, 1.32–1.36) sit right alongside the note's reported cubic range at comparable p, with a mild
upward drift with degree, same direction as the exact-cost trend.

## 6. A genuine structural finding: exact plus/minus symmetry at special primes

Three (p, k) rows above show **P_k(plus) identically equal to P_k(minus)**, not just close: x⁵ at p=449,
and x⁷ at p=293, 401, 797 (visible in the raw per-prime tables, e.g. p=449 x⁵: plus and minus k′-counts
176/140/100/28/0/5 on *both* slopes, matching digit-for-digit; the LP/cost tables above show these are
otherwise unremarkable primes, not larger deviations). This is not noise: for f(x) = x^k with k odd,

  f(μt) − μt = μ^k t^k − μt = μ(μ^{k−1}t^k − t) = μ(−t^k − t) = −μ(f(t) + t)     whenever μ^{k−1} = −1,

so t ↦ μt is a bijection sending every root of f(t)+t=c to a root of f(s)−s = −μc — an **exact
rearrangement** of the minus-class sizes into the plus-class sizes (not merely an asymptotic coincidence),
whenever F_p contains a solution to μ^{k−1} = −1. Checked this prediction exactly (elementary Euler-
criterion test, no discrete log) against all 13 runs in `x5_x7_numerics_pooled.py`: **13/13 correct** —
every predicted-solvable prime shows exact P_k equality, every predicted-unsolvable prime shows unequal
P_k. (The *finer* n₀|k breakdown also matched exactly at p=449/x⁵, but not at p=293,401,797/x⁷ — e.g.
p=293,x⁷,k=2: plus n₀-counts 12/28/12 vs minus 17/18/17, same total 52 but different split — so the
finer symmetry is not implied by the argument above and is presumably a further coincidence specific to
which of the several μ-solutions was used implicitly by the k=5 case; not chased further here.) This is
worth flagging because it is a clean, deterministic alternative explanation for why P_k(plus) and
P_k(minus) sometimes match "too well" to be attributed to (H1) alone — it isn't evidence of a *smaller*
Galois group either way, just an artifact of F_p containing an appropriate root of −1, orthogonal to the
Chebotarev question in §2.

## 7. Files

- `slack/g_agents/x5_x7_numerics.py` — main script: parts (a)(b)(c)(d) for all 13 (p, k_pow) runs, prints
  and saves `x5_x7_numerics_output.txt` (453 lines, full per-prime detail for every k, n₀|k cell, and
  cover-cost breakdown) and `x5_x7_numerics_results.json` (machine-readable).
- `slack/g_agents/x5_x7_numerics_pooled.py` — pooled (a)/(b) tables + the μ^{k−1}=−1 symmetry check (§6),
  saves `x5_x7_numerics_pooled_output.txt`.
- `slack/g_agents/x5_x7_numerics_exact_constant.py` — the symbolic idealized-constant derivation (§4),
  saves `x5_x7_numerics_exact_constant_output.txt`; reproduces the note's 11/8 exactly at k=3.
- All three import `slack/lp_curve.py` for part (d) rather than reimplementing it; that file was not
  modified.
- Runtime: the whole sweep (all three scripts, 13 primes × 2 exponents, all four parts) runs in about 5
  seconds total on this machine — negligible against the ~50-minute budget.
