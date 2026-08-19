# profile_table — per-residue lift-coverage profile and expected ±1-line-cover cost for general permutation-polynomial degrees

Agent: `profile_table`. Code: `slack/g_agents/profile_table.py` (self-contained, pure Python +
`fractions`, no deps; run with
`/Users/iwasborninbali/venvs/sat/bin/python3 slack/g_agents/profile_table.py`, ~2s total). Full run
log: `slack/g_agents/profile_table_output.txt`. Model / background:
`docs/research/permutation_cubic_note.md` secs 0–3 (the G3.5 cubic theorem — read first; this file
generalizes its cover-cost computation from `deg f = 3` to arbitrary degree / arbitrary root-count law).

## Task recap

(1) A function that, given `(k,n0)` for slope +1 and the analogous `(k,n0)` for slope −1 through the
*same* residue `x`, plus `x`'s own class in each group, returns exactly how many of `x`'s 4 lifts lie
on a ≥4-point line of either slope — tabulated for `k=0..5`, verified against the cubic note's k=3
rule. (2) Assuming the limit law (`P_k` for the root count, `n0 | k` uniform, `x`'s own class uniform
among the `k` roots, slopes independent), an explicit formula for `E[U]/p` and `E[2·L4]/p`, evaluated
at the rencontres distribution of `S_d`, `d=3,4,5,6`, reporting `cost/(2p)` (11/8 = 1.375 for `d=3`)
and whether it stays below 3/2. (3) The general formula so any root-count distribution (e.g. from a
different Galois group) can be plugged in.

## Part 1 — the per-residue lift-coverage function

Every residue `x` sits in one class of the slope-+1 equation `f(t)−t = c₊(x)` (size `k₊`, `n0₊`
class-0 roots) and one class of the slope-−1 equation `f(t)+t = c₋(x)` (size `k₋`, `n0₋` class-0
roots); `x` itself has a class `cls₊∈{0,1}` in the first and `cls₋∈{0,1}` in the second. **Which of
`x`'s 4 lifts `(δ,ε)` a given slope covers is a lookup table that depends only on `x`'s own class**
(taken verbatim from note sec. 1); **whether a given line clears the ≥4 threshold** is the only place
`(k,n0)` enters, through the line-count formula:

```
line_counts(k,n0) = (n0, 2n0+n1, n0+2n1, n1),   n1 = k − n0      (identical formula, both slopes)
```

| slope +1, root class | `(0,0)` & `(1,1)` → | `(0,1)` → | `(1,0)` → |
|---|---|---|---|
| 0 | `c′`  [count `2n0+n1`] | `c′+p` [count `n0+2n1`] | `c′−p` [count `n0`] |
| 1 | `c′+p` [count `n0+2n1`] | `c′+2p` [count `n1`] | `c′`  [count `2n0+n1`] |

| slope −1, root class | `(0,0)` → | `(0,1)` & `(1,0)` → | `(1,1)` → |
|---|---|---|---|
| 0 | `c″` [count `n0`] | `c″+p` [count `2n0+n1`] | `c″+2p` [count `n0+2n1`] |
| 1 | `c″+p` [count `2n0+n1`] | `c″+2p` [count `n0+2n1`] | `c″+3p` [count `n1`] |

`covered_by_slope(slope,k,n0,cls)` returns the subset of `x`'s 4 lifts covered by that slope alone
(look up the line for each lift, keep it iff its count ≥ 4); `lift_profile(k₊,n0₊,cls₊,k₋,n0₋,cls₋)`
takes the union over both slopes and returns `(covered, singles, covered_set)` with
`covered + singles == 4` always — `covered` is literally "how many of x's four lifts lie on a ≥4-point
line of either slope" and `singles = 4 − covered` is "the number of singletons `x` contributes" (the
task's own phrasing conflates these two complementary numbers; the code reports both so there is no
ambiguity). Full table for `k=0..5`, all `n0`, both classes, both slopes is in the run log (84 rows);
excerpt:

```
 k  n0  n1           counts cls  slope+ covered #  slope- covered #
 3   1   2     (1, 4, 5, 2)   0  {00,01,11}     3  {01,10,11}     3
 3   1   2     (1, 4, 5, 2)   1  {00,10,11}     3  {00,01,10}     3
 4   4   0     (4, 8, 4, 0)   0  {00,01,10,11}  4  {00,01,10,11}  4
 5   2   3     (2, 7, 8, 3)   0  {00,01,11}     3  {01,10,11}     3
```

(the last row shows a class whose *own* slope's lines are all < 4 points on slope −1 for a class-0
root of that shape, yet 3 lifts are still covered by slope +1 alone — `k` needn't be ≥3 for coverage,
it only needs enough roots for `2n0+n1` etc. to clear 4, which is why `k=2` already produces coverage:
`line_counts(2,0)=(0,2,4,2)`, one line hits exactly 4).

**k=3 verification** (`verify_k3_cubic_rule()`, 12 checks, all PASS): reproduces the cubic note's
prose exactly — "same group: the two `δ=ε` lifts covered by slope +[1]" (`n0∈{0,3}` ⇒
`covered_by_slope('+',3,n0,cls) == {(0,0),(1,1)}`), "split group: all lifts but one, `(1,0)` if class
0, `(0,1)` if class 1" (`n0∈{1,2}`), and the analogous slope −1 rule (same ⇒ the two mixed lifts;
split ⇒ all but `(0,0)`/`(1,1)`).

## Part 2 — expected cost per residue as an explicit function of the `P_k`'s

Recall the cover: weight 1 on every ±1-line with ≥4 points (cost 2 each, since a lawful set meets
*any* line in ≤2 points), weight 1 on every point on none of them; `cost = 2·L4 + U ≥ α`. Writing
`B(k,n0) = #{of the 4 candidate lines of a (k,n0) class with ≥4 points}` and averaging over the limit
law (`n0 | k ~ Uniform{0..k}`, independent slopes, `x` uniform among its class's roots):

```
β(k) := E_{n0~U{0..k}}[B(k,n0)] = (1/(k+1))·Σ_{n0=0}^k B(k,n0)

E[2·L4]/p = 2·Σ_σ Σ_k P_k^σ·β(k)                                                        ... (I)
     (L4 is a sum over CLASSES/lines, and P_k is already the unbiased fraction of classes with k
      roots — no size-bias correction needed)

q_σ(lift) := P(a uniformly random x's `lift` is covered by slope σ alone)
           = Σ_k [P_k^σ/(k+1)]·Σ_{n0=0}^k [n0·cov_σ(lift|k,n0,0) + (k−n0)·cov_σ(lift|k,n0,1)]    ... (II)
     (U is a sum over RESIDUES; a residue lands in a size-k class with size-biased probability
      k·P_k, but that factor of k exactly cancels the 1/k of splitting the class's roots by label,
      leaving the same clean P_k/(k+1) weight as in β — see the derivation in profile_table.py's
      q_of() docstring)

E[U]/p = Σ_{lift∈{00,01,10,11}} (1 − q_+(lift))·(1 − q_−(lift))                          ... (III)
     (independence of the two slopes turns "not covered by either" into a product)

cost/p = E[2·L4]/p + E[U]/p,      cost/(2p) = cost/p / 2
```

`β(k)` for `k=0..8`: `0, 0, 2/3, 3/2, 12/5, 8/3, 20/7, 3, 28/9` (monotone increasing, `β(k)→4` as
`k→∞` — every class eventually has all 4 of its lines ≥4 points).

**Exact cubic check.** Plugging `P_k = [1/3, 1/2, 0, 1/6]` (the note's own numbers, and independently
`rencontres(3)`, and independently the empirical proportions found by sibling agent `group_types`
converging to `(1/3, 1/2, 1/6)` by direct `O(p)` bucketing over real primes up to `p=100019` —
`docs/research/g_agents/group_types.md`) into (I)–(III) gives, **as an exact rational identity, not
merely a numerical match**:

```
E[2·L4]/p = 1        E[U]/p = 7/4        cost/p = 11/4        cost/(2p) = 11/8 = 1.375
```

— reproducing the note's sec. 3 closed form (`2L4/p → 1`, `U/p → 7/4`, `cost/(2p) → 11/8`) term by
term. A direct Monte-Carlo simulation of the generative model (300k trials, sampling `k,n0,cls`
independently for both slopes exactly as stated, `monte_carlo_check()`) lands within statistical
noise: `2L4/p ≈ 1.0018` (exact 1), `U/p ≈ 1.7474` (exact 7/4) — an independent, from-scratch
cross-check of formulas (I)–(III) against the definitions, not just against the note.

**`S_d` rencontres, `d=3..6`** (`P_k` = `C(d,k)·D_{d-k}/d!`, cross-checked against brute-force
enumeration of all `d!` permutations for every `d`):

| d | `P_k` (k=0..d) | E[2L4]/p | E[U]/p | cost/p | cost/(2p) | decimal | < 3/2? |
|---|---|---|---|---|---|---|---|
| 3 | 1/3, 1/2, 0, 1/6 | 1 | 7/4 | 11/4 | **11/8** | 1.3750 | YES |
| 4 | 3/8, 1/3, 1/4, 0, 1/24 | 16/15 | 53/30 | 17/6 | **17/12** | 1.4167 | YES |
| 5 | 11/30, 3/8, 1/6, 1/12, 0, 1/120 | 31/30 | 1519/864 | 12059/4320 | **12059/8640** | 1.3957 | YES |
| 6 | 53/144, 11/30, 3/16, 1/18, 1/48, 0, 1/720 | 661/630 | 295/168 | 7069/2520 | **7069/5040** | 1.4026 | YES |

All four stay comfortably below `3/2`, i.e. under this cover none of the degree-3..6 permutation-
polynomial graphs (with full `S_d` Galois group and the assumed equidistribution law) reach the HJSW
hyperbola value — the `d=3` case is exactly the proved theorem, `d=4,5,6` are the same computation run
on the next three rencontres laws. The ratio is *not* monotone in `d` (1.375 → 1.417 → 1.396 →
1.403), reflecting the non-monotone rencontres numbers themselves (`P_0` oscillates around `1/e`
before settling); as `d→∞` the law converges to Poisson(1) (`P_k → e⁻¹/k!`), for which the same
formula gives `cost/(2p) ≈ 1.4012` (float, not exact — `k` truncated at 40, negligible tail folded
in) — already close to the `d=6` value, i.e. the constant appears to converge quickly and stay well
under `3/2` in the limit too.

## Part 3 — the general formula for other root-count distributions

Formulas (I)–(III) only ever use the `P_k^σ` sequences (and the fixed, `k`-independent lookup tables
of Part 1) — nothing about them is specific to `S_d`. `fixed_point_distribution(perms, d)` computes
`P_k` for *any* finite permutation group `G ≤ S_d` given as a list of permutations of `range(d)`:
`P_k = #{g∈G : g has exactly k fixed points}/|G|`. This is the right general input whenever the
Galois group of `f(t)∓t−C` over `F_p(C)` (acting on the `d` roots) is `G` rather than the full
`S_d` — by the standard Chebotarev heuristic the fraction of `c` for which `f(t)∓t=c` has exactly `k`
roots in `F_p` tends to this same `P_k`. **The consistency identity `Σ_k k·P_k = 1`** (used silently
throughout, since it is what makes `p = Σ_c k(c)` exact) **holds automatically for any *transitive***
`G` — it is exactly Burnside/orbit-counting, `(1/|G|)Σ_g fix(g) = #orbits = 1`. `expected_cost()`
asserts both `Σ P_k=1` and `Σ k·P_k=1` on every call as a guard.

Demonstration — two slopes still assumed symmetric (same `G` on both), `d=4` and `d=5`, `S_d`
compared against non-symmetric-group actions on the same `d` points:

| group | `|G|` | `P_k` (k=0..d) | E[2L4]/p | E[U]/p | cost/(2p) | < 3/2? |
|---|---|---|---|---|---|---|
| `S_4` natural | 24 | 3/8, 1/3, 1/4, 0, 1/24 | 16/15 | 53/30 | 17/12 ≈ 1.4167 | YES |
| `A_4` natural | 12 | 1/4, 2/3, 0, 0, 1/12 | 4/5 | 92/45 | 64/45 ≈ 1.4222 | YES |
| `C_4` regular | 4 | 3/4, 0, 0, 0, 1/4 | 12/5 | 0 | 6/5 = 1.2000 | YES |
| `S_5` natural | 120 | 11/30, 3/8, 1/6, 1/12, 0, 1/120 | 31/30 | 1519/864 | 12059/8640 ≈ 1.3957 | YES |
| `D_5` natural | 10 | 2/5, 1/2, 0, 0, 0, 1/10 | 16/15 | 6/5 | 17/15 ≈ 1.1333 | YES |

`C_4`'s regular representation (only the identity has fixed points, and it fixes all 4 — a
free/fixed-point-free action off the identity) gives the *lowest* cost of the five, `6/5`; `A_4`
gives the *highest*, `64/45`. So the constant is genuinely sensitive to the Galois group, but in
every one of these five very different actions (cyclic-regular, alternating, dihedral, plus the two
symmetric baselines) it lands well inside `[6/5, 3/2)` — none of them reach `3/2`. (Five hand-picked
small groups is not a proof for all transitive `G ≤ S_d`; it is offered as evidence that the
sub-`3/2` behaviour is not a knife-edge coincidence of `S_d` specifically.)

`expected_cost(Pk_plus, Pk_minus)` also accepts two genuinely different distributions per slope
(nothing forces `f(t)−t` and `f(t)+t` to share a Galois group in general); example, slope+ ~ `S_4`,
slope− ~ `A_4`: `cost/(2p) = 259/180 ≈ 1.4389`, still `< 3/2`.

## Scope note: this is not a claim about the hyperbola (`k=2`)

Note remark 2 states the hyperbola `x↦1/x` gives `α = 3(p−1)` *exactly*, i.e. `cost/(2p) → 3/2` — the
HJSW value itself. Plugging a matching root-count law into formulas (I)–(III) (quadratics have 0 or 2
roots, never 1, generically: `P_k=[1/2,0,1/2]`, which does satisfy `ΣP_k=1, Σk·P_k=1`) gives
`cost/(2p) = 4/3`, **not** `3/2`. This is not a contradiction of the note — `k=2` is a single
involution-like pairing `(t,t')`, and nothing in this task establishes that its `n0 | k=2` split is
`Uniform{0,1,2}` (the `n0 | k` uniform law here comes from a genuine `k`-fold equidistribution — a
mixture of `Binomial(k,θ)` over `θ~Uniform(0,1)` — that the note justifies via Weil on a genus-0
curve for `k=3`; whether the analogous statement holds, or holds with the same uniform mixing
measure, for a `k=2` pencil is a separate question this task does not address). It is reported here
only as a boundary-of-validity flag: the "assume `n0|k` uniform" hypothesis of Part 2 is doing real,
falsifiable work (changing the input law changes the output in a way that can be checked against
independently-known exact answers), not a tautology that always outputs something safely under
`3/2` — so the `< 3/2` verdicts above are genuine content, not an artifact of the formula being
unable to output anything else: `expected_cost()` does output `≥ 3/2` for some valid inputs, e.g.
`P_k=[0,1]` (every class deterministically has exactly 1 root — not realizable by an actual
transitive Galois-group action for `d≥2`, since the identity always fixes all `d` points, but a
mathematically legal input, `ΣP_k=1, Σk·P_k=1`) gives `E[2L4]/p=0, E[U]/p=4, cost/(2p)=2` — the
worst possible value (every point a singleton, `cost=4p` exactly). None of the *realizable*
distributions tried above (rencontres or genuine small transitive groups) came anywhere close to
that; they clustered in `[6/5, 3/2)`.

## Files

- `slack/g_agents/profile_table.py` — all three parts; `__main__` prints the full table, the k=3
  verification, usage examples, the `β(k)` table, the exact cubic check + Monte Carlo cross-check,
  the `d=3..6` table, the non-`S_d` group demonstrations, and the Poisson(1) limit.
- `slack/g_agents/profile_table_output.txt` — full run log (144 lines) referenced above.
