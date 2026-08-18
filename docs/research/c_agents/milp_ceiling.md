# milp_ceiling — the ceiling of the selection approach (t_G ∈ {0, 1/2, 1})

Agent task: **milp_ceiling**. Code: `slack/c_agents/milp_ceiling.py`. Model/tools: `slack/cyc_model.py`
(background: `docs/research/pair_bound_notes.md` §25–26). Python: `/Users/iwasborninbali/venvs/sat/bin/python3` (numpy/scipy 1.18, `scipy.optimize.milp` = HiGHS).

## Method

The free LP (`cyc_model.lp`) lets each group's weight t_G range continuously over [0,1]. A **selection
rule** — the kind an explicit bounded-window local rule from §26 can realistically compute — only ever
outputs one of three choices per group: unused (t=0), matched/half (t=1/2), full block (t=1). This script
computes the **exact optimum of that restricted problem**: continuous edge weights w_e ≥ 0, t_G ∈ {0,½,1},
via a genuine MILP solved with `scipy.optimize.milp` (HiGHS branch & bound) — not a heuristic.

**Encoding.** t_G ∈ {0,½,1} is encoded as one bounded integer n_G ∈ {0,1,2} with t_G := n_G/2 (equivalent
to, but simpler than, the two-binary z1,z2 encoding suggested in the brief — HiGHS handles bounded general
integers natively). A class v ∈ G gets coefficient 0.5 on n_G in the covering constraint; n_G's objective
coefficient is 6·0.5 = 3, so n_G=2 (t_G=1) costs 6, matching `cyc_model` exactly. Function `milp_solve(M)`
returns `(saving, w, t, res)`, mirroring `cyc_model.lp`'s signature.

**Instances.** Real: `cyc_model.build(p,k)` for (p,k) = (101,2), (199,2), (199,3) as specified, plus
(401,2), (401,3), (601,2), (601,3) as a cheap extra confirmation (builds/solves in ≤30ms each). Synthetic:
`cyc_model.synthetic(M, seed)` on the same three bases, **8 seeds each** (seeds 0–7), i.e. ≥5 seeds and two
sizes (p=101, p=199) as requested. All MILP solves finished in single-digit milliseconds with HiGHS status
"Optimal" and (checked directly) zero MIP gap — these are proven global optima, not just "good" solutions.

## Result 1 — real instances: the {0,½,1} restriction costs *nothing*

| p | k | G8 (#groups) | LP saving/grp | MILP saving/grp | LP − MILP | LP already half-integral? |
|---|---|---|---|---|---|---|
| 101 | 2 | 16 | 0.7500 | 0.7500 | 0.000000 | **yes**, exactly |
| 199 | 2 | 32 | 0.8125 | 0.8125 | 0.000000 | **yes**, exactly |
| 199 | 3 | 34 | 0.8824 | 0.8824 | 0.000000 | **yes**, exactly |
| 401 | 2 | 64 | 0.9375 | 0.9375 | 0.000000 | **yes**, exactly |
| 401 | 3 | 58 | 0.8621 | 0.8621 | 0.000000 | **yes**, exactly |
| 601 | 2 | 102 | 0.9608 | 0.9608 | 0.000000 | **yes**, exactly |
| 601 | 3 | 94 | 1.0638 | 1.0638 | 0.000000 | **yes**, exactly |

For every one of these 7 real instances, `cyc_model.lp`'s continuous optimum lands on a vertex with every
t_G ∈ {0, ½, 1} already (checked to 1e-6; the raw solver output is literally `0.0`/`-0.0`/`0.5`/`1.0`, no
other value ever appears) — confirmed independently by running the actual MILP (not just the "a half-integral
LP-feasible point certifies MILP=LP" argument, though that argument is also valid and airtight here since
MILP's feasible region ⊆ LP's). **So on the real arrangement, restricting an explicit rule's menu to
{0,½,1} loses nothing relative to a fully free continuous rule** — the §26 "free LP" numbers (0.75, 0.81,
0.88, 0.94, 0.86, 0.96, 1.06/group, reproduced exactly here) already *are* the selection ceiling. This
looks structural (a half-integrality theorem for this cycle/hyperedge-cover polytope, in the spirit of the
classical half-integrality of fractional b-matching/edge-cover LPs), reinforced by the real arrangement's
reflection symmetry (§25); it is not merely a lucky coincidence of one instance, since it held at all 7.

## Result 2 — synthetic (random) instances: a genuine, small rounding gap

| base (p,k) | LP/grp mean [range], 8 seeds | MILP/grp mean [range] | mean rounding loss (LP−MILP)/grp | typical LP half-int-gap |
|---|---|---|---|---|
| (101,2) | 0.6944 [0.406, 1.050] | 0.6641 [0.375, 1.000] | **0.0303** | 0–0.24 (2/8 seeds exactly half-integral) |
| (199,2) | 0.5832 [0.477, 0.764] | 0.5469 [0.469, 0.719] | **0.0363** | 0.20–0.25 |
| (199,3) | 0.5707 [0.466, 0.699] | 0.5404 [0.441, 0.677] | **0.0303** | 0.21–0.25 |
| **overall (24 synthetic instances)** | mean 0.616 | **mean 0.584** | **0.032** (≈5–6% relative) | — |

Here the free LP is genuinely fractional in 22/24 synthetic draws (t-values land at generic fractions like
0.055, 0.15, 0.71, 0.98, not just multiples of ½) — the real arrangement's half-integrality is *not* a
generic property of this LP, it is special to the real, structured group placement. Restricting to
{0,½,1} on synthetic instances loses a real, consistent ~0.03/group (~5–6% relative) versus the free LP,
on top of the synthetic ceiling already being well below the real one (≈0.58–0.66/grp vs 0.75–1.06/grp) —
i.e. the real arrangement is a *better* substrate for a selection rule on both counts, not just one.

## Result 3 — window statistics: what the MILP selects vs skips

For every group G and each of its 4 vertices, `group_window_features` finds the nearest **other**
candidate-special vertex (candidate pool = the vertex set of *every* group in the model, i.e. "specials"
in the §25/26 sense) in the + and − cyclic directions, and records the gap length and whether it is odd
(⇒ opposite K/M type, since a ⟨k⟩-cycle strictly alternates K,M,K,M,... by construction — a "changing" gap
in the §26 sense) or even (same type). Sanity check: pooling this over all groups reproduces `cyc_model
.changes(M, M['groups'])/(#specials)` exactly (0.3750/0.5000/0.5294 for the three required real instances)
— matching the already-published §26 table bit for bit, so the feature extraction is verified correct.

Selected = groups with t_G > 0 in the MILP optimum; Unused = t_G = 0. (full = t_G=1, half = t_G=½ shown
separately below the merged row.)

**Real instances** (merged selected vs unused; distances in cycle steps):

| p,k | group | n vertices | avg nearest-gap | frac. gap alternates | frac. ≥1 side alternates |
|---|---|---|---|---|---|
| 101,2 | **selected** | 32 | 1.50 | **0.625** | **0.875** |
| 101,2 | unused | 32 | 2.75 | 0.125 | 0.250 |
| 199,2 | **selected** | 76 | 1.71 | **0.605** | **0.947** |
| 199,2 | unused | 52 | 1.96 | 0.346 | 0.538 |
| 199,3 | **selected** | 72 | 1.33 | **0.694** | **1.000** |
| 199,3 | unused | 64 | 1.88 | 0.344 | 0.562 |

Three-way split (real instances) shows a clean **monotone** ordering full(t=1) > half(t=½) > unused(t=0)
in "fraction of neighbour gaps that alternate type", at all three required real instances:
101,2: 0.875 > 0.375 > 0.125; 199,2: 0.750 > 0.521 > 0.346; 199,3: 0.708 > 0.667 > 0.344. Full-block groups
also sit closest to their nearest other special (avg nearest-gap 1.00 / 1.14 / 1.42 vs 2.75 / 1.96 / 1.88
for unused).

**Synthetic instances** (seed 0 of each base; same merged view): selected groups again beat unused ones on
every statistic, but the margin is smaller and the full-vs-half ordering is noisier (real's reflection
symmetry, §25, evidently sharpens the local signal that random placement blurs):

| p,k | group | n vertices | avg nearest-gap | frac. gap alternates | frac. ≥1 side alternates |
|---|---|---|---|---|---|
| 101,2 | selected | 36 | 1.92 | 0.694 | 0.917 |
| 101,2 | unused | 28 | 2.00 | 0.464 | 0.714 |
| 199,2 | selected | 44 | 1.59 | 0.670 | 0.886 |
| 199,2 | unused | 84 | 1.92 | 0.506 | 0.714 |
| 199,3 | selected | 44 | 1.55 | 0.659 | 0.864 |
| 199,3 | unused | 92 | 1.82 | 0.533 | 0.750 |

**Reading:** the MILP is, in every single case tested (6/6), preferentially activating groups whose 4
vertices sit *closer* to *other* candidate-special vertices *and* more often at odd (alternating-type)
distance from them — exactly the local feature the §26 "K→M transition" mechanics predicts should be
profitable. This is direct numerical evidence for what an explicit bounded-window local rule should key
on: **a group is a good pick if ≥1 of its 4 vertices has a same-side-nearby, opposite-type candidate
special within a short window** (empirically the "≥1 side alternates" gap between selected/unused is the
single sharpest of the three statistics: 0.875 vs 0.250, 0.947 vs 0.538, 1.000 vs 0.562 on the real
instances — selected groups get to 1.000/0.947/0.875 while unused sit at 0.25–0.56).

## The ceiling — headline numbers

- **Real instances** (this is the actual object of interest for theorem C): the {0,½,1}-selection ceiling
  is **exactly equal to the free continuous LP**, 0.75/grp (p=101,k=2) rising to 1.06/grp (p=601,k=3), with
  **zero loss** from discretizing t — verified on 7 real instances (both by an LP-half-integrality argument
  and by an independent exact MILP solve). So any theorem-C programme that only needs an explicit rule
  outputting t ∈ {0,½,1} is not leaving anything on the table relative to a continuous rule, *for the value
  achievable by the best possible (non-local, global) selection* — the open problem (§26's Selection
  Lemma) is entirely about finding a **local, window-bounded** rule that approaches this global ceiling,
  not about the {0,½,1} restriction itself.
- **Synthetic (random) instances**: ceiling is markedly lower, ≈0.58/grp on average (range across bases
  0.54–0.66/grp), i.e. noticeably below the real ceiling — confirming (independently of §25–26's own data)
  that the real arrangement's structure (not just its density) is doing real work, and that a rule tuned
  only to generic/i.i.d. placement will underperform on the real instances it actually needs to handle (or
  vice versa: a rule validated only on real instances may be over-optimistic about generic/equidistributed
  windows — worth keeping in mind for the §26 equidistribution step, where the *window-local* statistics,
  not the *global* MILP-selection statistics reported here, are what ultimately needs to equidistribute).

## Honest caveats

- This is a **global, non-local** ceiling: `milp_solve` sees the whole cycle before deciding any t_G, so it
  is *not* itself an explicit bounded-window local rule (that is the separate, harder combinatorial problem
  of §26's Selection Lemma) — it is an upper bound for what any local rule using only the {0,½,1} menu could
  hope to achieve, and evidence (Result 3) for what such a rule should locally test for.
- All numbers are exact optima on small instances (p ≤ 601); nothing here says anything about the p→∞
  asymptotics or equidistribution needed for theorem C itself — that is explicitly out of scope for this
  task (see §26 for the Kloosterman-sum argument that would be needed on top of a local rule).
- The half-integrality of the real-instance LP is an empirical (if 7-for-7, exact-to-the-bit) observation
  here, not a proof; a combinatorial reason (total half-integrality of this class of cover LP, akin to
  b-matching/edge-cover polytopes) is plausible but was not derived rigorously within the time budget.
- Window statistics use the *global* candidate pool (all G8 groups), matching how "specials" is used
  throughout §25–26 (e.g. the K→M transition density with S = all groups) — an actual bounded-window local
  rule would only see a window of fixed radius w around each group, not the whole cycle; Result 3's "avg
  nearest-gap" values (mostly 1–3 steps) suggest w = 3–6 already captures most of the relevant neighbours,
  consistent with the first solver's guess in §26 ("w = 2…4 will already give net > 0").

## Reproduce

```
/Users/iwasborninbali/venvs/sat/bin/python3 slack/c_agents/milp_ceiling.py         # full run (~1s)
/Users/iwasborninbali/venvs/sat/bin/python3 slack/c_agents/milp_ceiling.py quick   # 3 seeds, faster smoke test
```
`milp_solve(M, groups_subset=None, time_limit=120, mip_gap=1e-9)` — exact MILP, same signature shape as
`cyc_model.lp`. `group_window_features(M, groups)` / `window_report(M, groups, t, label)` — the window
statistics of Result 3, reusable on any model/solution pair.
