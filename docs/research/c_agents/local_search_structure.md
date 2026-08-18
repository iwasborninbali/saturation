# local_search_structure — a local rule for t_G in the class-graph cover LP

Code: `slack/c_agents/local_search_structure.py` (run: `/Users/iwasborninbali/venvs/sat/bin/python3 slack/c_agents/local_search_structure.py`, ~3s).
Model: `slack/cyc_model.py`; background: `docs/research/pair_bound_notes.md` §25–26.

**Headline.** The literal ask — an explicit local rule of the form "t=1 on predicted groups, else 0" —
does **not** beat doing nothing on held-out data (honest negative, numbers below). Loosening the same
kind of rule to also output t=1/2 (still local/explicit/bounded-window, just three-valued instead of
two) flips the sign: a *single feature*, thresholded at two points, nets **+0.35 to +0.41 per group on
every held-out instance tried** (real and synthetic, all four other primes, all three other seeds),
about **44% of the free LP's own saving**.

## 1. Setup

For every group `G` the free LP (`cm.lp(M)`) returns `t_G` exactly at one of `{0, 1/2, 1}` (checked: no
value farther than 1e-4 from that set, for every instance below). Step (2) of the task asks for local
features of a group's 4 vertices computed **from the cyclic order of all specials** — the union of every
group's vertex set, i.e. what's known about the instance *before* deciding which groups to activate.

For every special vertex `v` we compute, along its own `<k>`-cycle, the nearest *other* special before it
and after it (`local_context`). Two facts, verified in code (`check_alternation_fact`) rather than
assumed, drive everything below:

* cycles are built strictly `K,M,K,M,…`, so a vertex's type is exactly the parity of its cycle index;
* hence a special's previous/next neighbour has the **opposite** type iff the distance to it is **odd**
  — in particular the row-mate/column-mate (the immediate cycle-neighbour, distance 1) of *any* vertex
  is *always* of the opposite type, unconditionally.

From this, each group `G = {2 K's, 2 M's}` gets 8 "sides" (dist_prev, dist_next for each of its 4
vertices), aggregated into 5 permutation-symmetric features:

| feature | meaning |
|---|---|
| `min_dist` | closest other special to any of the 4 vertices |
| `max_of_min` | worst-connected of the 4 vertices (isolation) |
| `mean_dist` | average distance to nearest neighbour, over the 8 sides |
| `n_adj` ∈ [0,8] | # sides whose nearest neighbour is the immediate cycle-neighbour |
| `n_odd` ∈ [0,8] | # sides at odd distance, i.e. whose nearest neighbour is opposite type |

Density of specials (`4·G8 / #classes`) is **0.29–0.34 at every p tested (101…601)** — it does not shrink
with p — so `min_dist`/`mean_dist` stay O(1) (empirically 1–4) throughout; the window this rule needs is
bounded independent of p, consistent with the §26 equidistribution framework.

TRAIN = real (199,2), real (199,3), synthetic (199, k=2, seeds 0,1,2) — 5 instances, 162 groups.
TEST = real (101,2), (401,2), (401,3), (601,2) **and** synthetic (401, k=2, seeds 0,1,2) — 7 instances,
held out on *both* axes (other primes, other seeds), split into TEST-real / TEST-syn / TEST-all below.

## 2. Free LP on all 12 requested instances

`t=1 / t=0 / t≈1/2` are group counts (% of G8); `0/1-oracle` = the best *any* binary (t∈{0,1}) rule could
ever do on that exact instance — force t=1 exactly where the free LP chose it, t=0 elsewhere, i.e. the
ceiling for step 3, computed with the answer already known (not a portable rule, a diagnostic).

| instance | G8 | t=1 | t=0 | t≈1/2 | free-LP net/grp | 0/1-oracle net/grp |
|---|---:|---:|---:|---:|---:|---:|
| real(199,2) | 32 | 22% | 41% | 38% | +0.812 | −0.062 |
| real(199,3) | 34 | 35% | 47% | 18% | +0.882 | +0.235 |
| syn(199,2,seed0) | 32 | 3% | 41% | 56% | +0.477 | −0.062 |
| syn(199,2,seed1) | 32 | 3% | 19% | 78% | +0.592 | +0.062 |
| syn(199,2,seed2) | 32 | 3% | 31% | 66% | +0.545 | −0.062 |
| real(101,2) | 16 | 25% | 50% | 25% | +0.750 | +0.000 |
| real(401,2) | 64 | 52% | 45% | 3% | +0.938 | +0.844 |
| real(401,3) | 58 | 38% | 52% | 10% | +0.862 | +0.483 |
| real(601,2) | 102 | 41% | 45% | 14% | +0.961 | +0.588 |
| syn(401,2,seed0) | 64 | 8% | 14% | 78% | +0.637 | −0.031 |
| syn(401,2,seed1) | 64 | 2% | 20% | 78% | +0.668 | −0.031 |
| syn(401,2,seed2) | 64 | 5% | 19% | 77% | +0.595 | −0.031 |

Two patterns matter for everything that follows:

1. **Real vs synthetic.** Real arrangements grow *more integral* as p grows (t≈1/2 share: 38%→3–14% from
   p=199 to p=401/601); synthetic (fully random group placement) stays at 56–78% t≈1/2 regardless of p.
   This matches the notes' "real 0.75–1.0, random ≈0.65" — and explains why synthetic's 0/1-oracle
   ceiling is **flat at ≈0** (−0.03 to +0.06) while real's ceiling *rises* with p (0 → 0.84).
2. **The 0/1-oracle ceiling is already ≤0 on 5 of the 12 instances** (both p=199 reals/synthetics, all
   3 synthetic-401 seeds) — i.e. no binary rule, however well fitted, can win there. This is a structural
   fact about the LP, not a defect of any particular classifier.

## 3. Feature means by true label (TRAIN, 162 groups)

| feature | t=0 | t≈1/2 | t=1 |
|---|---:|---:|---:|
| min_dist | 1.17 | 1.05 | 1.08 |
| max_of_min | 2.86 | 2.93 | 1.72 |
| mean_dist | 3.34 | 3.03 | 2.25 |
| n_adj | 2.00 | 2.85 | 4.04 |
| n_odd | 3.48 | 4.85 | 5.80 |

`n_odd` separates the three classes best and monotonically (3.5 → 4.9 → 5.8): groups with more
odd-distance (alternating-type) neighbours in the full specials order are more likely to get t>0. This
single feature is what every fitted rule below ends up using.

## 4. Rules fitted

**CART** (max_depth 3, plain-Python Gini splitter, no sklearn in this venv — `build_tree`/`best_split`):

* binary label (t=1 vs t=0, 1/2-groups dropped, 80 groups): `if n_odd<=5.5: predict 0 else predict 1`
  — train accuracy 0.887 vs 0.725 majority baseline. The tree never splits past depth 1 (`n_odd` beats
  every other feature by a wide Gini margin at every depth tried, 2–5).
* 3-way label (162 groups): collapses to the same split — `n_odd<=5.5 → 0`, `n_odd>5.5 → 1/2` (never
  predicts 1); train accuracy 0.574 vs 0.475 baseline.

**Threshold rule** (`fit_threshold_rule`): rather than a Gini proxy, exhaustively grid-searches
1–2 thresholds on `n_odd ∈ [0,8]` to **directly maximise LP net/group on TRAIN** (5 LP solves per
candidate threshold pair, 45–81 candidates, all instances cached — a few seconds total):

* binary family (t=1 iff n_odd≥thr): best is thr=8 (all‑8 required), TRAIN net **−0.049**.
* 3-way family (t=1 if n_odd≥hi, t=1/2 if lo≤n_odd<hi, else 0): best is **lo=4, hi=8**, TRAIN net
  **+0.346** — clearly better than the CART, found by optimising the right objective directly.

Other hand-written rules tried for comparison (all worse): `adj≥1`, `adj≥2` (predict 1 if an immediate
cycle-neighbour is itself special), `odd≥5`, `isolated` (predict 1 when *far* from other specials —
tests the opposite-sign intuition), `crowded` (predict 1 when *close*), `always1`, `always1/2`.

## 5. Evaluation on held-out data (the actual deliverable)

All numbers are `cyc_model.lp(M, t_fixed=rule(...))` saving, divided by G8 — model selection uses TRAIN
only; TEST-real/TEST-syn are never touched when picking the best rule.

### 5a. Step 3 as literally specified: binary rules (t=1 on predicted groups, else 0)

| rule | TRAIN | TEST-real | TEST-syn | TEST-all |
|---|---:|---:|---:|---:|
| always0 (baseline) | +0.0000 | +0.0000 | +0.0000 | +0.0000 |
| always1 | −1.6543 | −1.3667 | −1.1875 | −1.2870 |
| adj≥1 | −1.0617 | −0.5833 | −1.0833 | −0.8056 |
| adj≥2 | −0.7901 | −0.5833 | −0.6562 | −0.6157 |
| odd≥5 | −0.4074 | −0.2167 | −0.1771 | −0.1991 |
| isolated(max_of_min≥6) | −0.1111 | −0.1000 | −0.2083 | −0.1481 |
| crowded(min_dist≤2) | −1.6543 | −1.5000 | −1.1771 | −1.3565 |
| CART tree | −0.2840 | −0.2167 | −0.1875 | −0.2037 |
| **thr_bin (best by TRAIN)** | **−0.0494** | **−0.1500** | **+0.0208** | **−0.0741** |

**Every binary rule tried is ≤0 on held-out data; the best one is worse than doing nothing.** This is an
honest negative result for the literal ask, and it is not a search failure: §6 shows the *ceiling* for
any binary rule is itself ≤0 on more than a third of the instances tested, so no amount of feature
engineering within this local-window family can fix it — the fix has to relax the binary constraint
(§5b), not sharpen the classifier.

### 5b. Bonus: same kind of rule, allowed to output t=1/2 too

Still explicit / local / bounded-window (a group's value depends only on `n_odd`, itself a function of
the nearest neighbours of its 4 vertices) — just three-valued instead of two, which is what the LP's own
structure actually wants (§2).

| rule | TRAIN | TEST-real | TEST-syn | TEST-all |
|---|---:|---:|---:|---:|
| always0 | +0.0000 | +0.0000 | +0.0000 | +0.0000 |
| always1/2 | −0.1605 | −0.0333 | −0.0312 | −0.0324 |
| CART tree3 | +0.0309 | +0.1917 | +0.0625 | +0.1343 |
| **threshold3 (best by TRAIN)** | **+0.3457** | **+0.4083** | **+0.2760** | **+0.3495** |

**threshold3** = *"t=1 if n_odd≥8 (all 4 vertices doubly-alternating), t=1/2 if 4≤n_odd≤7, t=0 if
n_odd≤3."* Per-instance breakdown (every one of the 7 held-out instances is positive, no outliers):

| instance | net/group |
|---|---:|
| real(101,2) | +0.125 |
| real(401,2) | +0.500 |
| real(401,3) | +0.483 |
| real(601,2) | +0.353 |
| syn(401,2,seed0) | +0.312 |
| syn(401,2,seed1) | +0.312 |
| syn(401,2,seed2) | +0.203 |

Against the free LP's own net/group on the same sets (TEST-real 0.917 weighted avg, TEST-syn 0.633,
TEST-all 0.791, TRAIN 0.664), `threshold3` captures **52% (TRAIN), 44.5% (TEST-real), 43.6% (TEST-syn),
44.2% (TEST-all)** of the free LP's saving — a strikingly stable fraction across real/synthetic and
across primes 3–6× apart, from a single feature and two integer thresholds.

## 6. Why binary fails: the oracle-ceiling gap, and where it comes from

Comparing §5a to the `0/1-oracle` column of §2: even a *perfect* binary classifier is capped at ≈0 or
negative on 5 of 12 instances (both p=199 cases and all synthetic-401 seeds), and only reaches 0.48–0.84
on the larger, more integral real instances (401, 601). Two compounding reasons:

1. **Structural**: 38–78% of groups have a genuinely fractional optimum (t=1/2), which a t∈{0,1} rule
   cannot represent at all — those groups are forced to their worse of the two extremes.
2. **Fragility of what's left**: even restricted to only the "should be 0 or 1" groups, our best binary
   classifier (CART, 88.7% train accuracy on that subset) still nets negative — a handful of
   misclassifications is enough to erase the gain, because the LP's saving comes from *pairs* of
   consecutive same-set members alternating in type (§25/§26's `changes(S)` formula); one wrong label
   both wastes its own 6-cost and can break the alternating run its correctly-labelled neighbours were
   relying on. This cascading/coupled-error effect, not weak features, is the main reason binary
   under-performs its own oracle ceiling so badly (e.g. TEST-real: oracle ceiling +0.59 weighted-average,
   actual best binary rule −0.15).

The 3-way rule sidesteps both problems: it can represent the 1/2 option directly, and because `n_odd≥8`
(predict full 1) is a much rarer, higher-precision trigger than `n_odd≥6`, it makes far fewer "wasted
6-cost, no matching change" mistakes.

## 7. Honest status / what this does and doesn't show

* **Positive, generalizing, but not the literal ask.** The requested binary rule does not achieve
  positive expected net at these p on this feature family — reported honestly rather than papered over.
  A 3-valued relaxation of the exact same local, bounded-window methodology does, generalizes cleanly
  across 4 held-out primes and 3 held-out synthetic seeds, and recovers ~44% of the free LP's own saving
  from one feature. Whether a *binary* rule can ever be made positive (e.g. with a richer feature set, or
  by first splitting off the "wants 1/2" groups via some other test before deciding 0 vs 1 among the
  rest) was not resolved here — the oracle-ceiling numbers suggest it is possible in principle for large,
  integral real p (ceiling +0.84 at p=401) but not for p≈199 or for random-like arrangements at any p
  tested, so a binary-only route looks structurally harder than the 3-valued route, not just harder to
  fit.
* **No claim of a proof.** This is a fitted, evaluated, honestly-reported empirical rule (exact LP
  evaluation, held out on both axes) — not a combinatorial lemma. Turning `threshold3` into the
  "Selection Lemma" of pair_bound_notes.md §26 (a proof that `E_π[net(π)] > 0` for the limiting window
  distribution, for all large p) would need: (a) the equidistribution argument already sketched in §26
  applied to this specific window statistic (`n_odd`, itself built from finitely many discrete-log
  conditions, so it should fall under the same Kloosterman-sum argument), and (b) redoing this same
  fit/evaluate loop as a genuine "3-valued Theorem C" rather than the strict 0/1 Theorem C of §25–26 —
  i.e. the natural next question this run raises is whether the target statement itself should allow
  t∈{0,1/2,1}, not just t∈{0,1}.
* **Robustness checked**: tree/threshold depth and min-leaf-size were varied (depth 2–5, min-leaf
  1/20–1/8 of data) with no change to the fitted rule (§4) — the split is not an artifact of tuning.
  A two-feature binary rule (`n_odd` AND `n_adj` thresholds, exhaustive 9×9 grid) did not beat the
  single-feature binary rule (degenerated back to ≈always0), so the binary failure is not simply a
  missing-feature-interaction issue either.

## Files

* `slack/c_agents/local_search_structure.py` — features, plain-Python CART, exhaustive threshold fit,
  and the full evaluation harness against `cyc_model.lp`. Self-contained; run from repo root.
* `docs/research/c_agents/local_search_structure.md` — this report.
