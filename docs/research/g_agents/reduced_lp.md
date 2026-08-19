# reduced_lp: the reduced ±1-line LP for the permutation cubic, and a type-based explicit rule

Task `reduced_lp` (background: G3′ in `docs/research/curves_conjecture.md` §8–9, and
`docs/research/permutation_cubic_note.md` — Theorem G3.5). Code: `slack/g_agents/reduced_lp.py`
(run with `/Users/iwasborninbali/venvs/sat/bin/python3 slack/g_agents/reduced_lp.py` from the repo
root; **all 5 test primes together run in ≈1.6s wall-clock**; verbatim output also saved to
`slack/g_agents/reduced_lp_output.txt`). Test primes throughout: p ∈ {101, 197, 401, 599, 797}
(all prime, all ≡ 2 mod 3).

## 0. Setup recap

Residue points (x, y = x³ mod p), x = 0..p−1 (a bijection). Box lift: 4p points, one **rectangle**
per residue x: P1=(x,y), P2=(x+p,y), P3=(x+p,y+p), P4=(x,y+p). (P1,P3) share a slope‑(+1) ("diagonal",
X−Y=const) line; (P2,P4) share a slope‑(−1) ("antidiagonal", X+Y=const) line. Rows/columns each carry
exactly 2 points (one rectangle's own), so they never help beyond what the rectangle itself needs.

**Rectangle reduction (THREAD[127]).** With w ≥ 0 the ±1-line weights and t_P the total ±1-line weight
at point P, the *exact* optimal rows+columns cost of one rectangle is

```
2 · max( (1−t_P1)₊ + (1−t_P3)₊ ,  (1−t_P2)₊ + (1−t_P4)₊ )        (x₊ := max(0,x))
```

(proved here by LP duality on the small 4‑variable/4‑constraint row/col sub‑LP of one rectangle: its
constraint graph is a 4‑cycle a–c–b–e with edges (a,c)→P1, (a,e)→P2, (b,e)→P3, (b,c)→P4, whose dual is
the fractional matching polytope of C₄ — **integral**, since C₄ is bipartite — with the two perfect
matchings {(a,c),(b,e)} and {(a,e),(b,c)} as the only useful vertices, giving exactly the two sums
above.) Rows/columns are never shared between two different rectangles (row Y and column X both belong
to exactly one residue), so the rows/columns optimum decomposes rectangle‑by‑rectangle for *any* fixed
w, and

```
reduced-LP cost = min_{w≥0}  2 Σ_l w_l + Σ_r 2·max(...)
```

is a genuine LP once the two maxes and the two hinges (·)₊ are linearised with one aux var m_r ≥ 0 per
rectangle and 4 aux vars u_{r,0..3} ≥ 0 (standard epigraph trick: `reduced_lp()` in the code).

## (a) Verification against the full explicit LP

`full_lp()` builds rows, columns, every diagonal line and every antidiagonal line as **independent**
0/1‑incidence LP variables (cost 2 per unit weight, **no** extra per‑point slack z_P — literally "rows,
columns and ±1 lines as separate variables"), and solves the ordinary covering LP directly. `reduced_lp()`
implements the closed form above. They must agree — and they do, to solver precision:

| p | full_lp | reduced_lp | \|diff\| |
|---|---|---|---|
| 101 | 267.3333 | 267.3333 | 5.7e‑14 |
| 197 | 541.6667 | 541.6667 | 4.6e‑13 |
| 401 | 1091.0000 | 1091.0000 | 1.4e‑12 |
| 599 | 1644.1667 | 1644.1667 | 1.1e‑12 |
| 797 | 2209.0000 | 2209.0000 | 3.2e‑12 |

Exact agreement at every tested p, at pure floating‑point‑noise level — confirming the rectangle
reduction is exact, not just an upper bound, for this specific "rows+columns+±1‑lines‑only, no z_P"
LP.

**Honest side‑finding (not part of task (a), but worth flagging since the task background quotes
numbers from it).** `slack/lp_curve.py`'s published `pm1` values — 266.00 (1.3168N) at p=101, 534.00
(1.3553N) at p=197, cited in the task background as "the LP with rows, columns and the lines of slope
±1" — are **slightly smaller** than the numbers above (267.33 / 541.67). The reason: `lp_curve.py`
drops rows/columns entirely (they never reach its `len(s)≥3` line filter) and replaces them with a
**generic per‑point slack z_P** (cost 1 per point, unconstrained per point) rather than genuine shared
row/column *line* variables. For a 2‑point line this is not neutral: using the shared line variable at
weight t contributes t to *both* of the line's 2 points at cost 2t, exactly matching two independent
z_P's set equal — but z_P can set them *unequal* at the same marginal cost, which is strictly better
whenever demand is asymmetric between the two points of a row/column. We verified this directly: adding
z_P on top of rows+columns+diag+antidiag in `full_lp` recovers 266.00 / 534.00 exactly. So there are
genuinely **two different LPs** in play here: the literal "rows, columns, ±1‑lines as separate
variables" LP that (a) asks about (1.32–1.39N below), and the slightly more permissive
lines‑plus‑generic‑point‑slack LP of `lp_curve.py` (1.317–1.355N for p=101,197, presumably similarly
≈0.3–1.4% below ours at larger p). **All "LP optimum" numbers in parts (b)–(d) below refer to our own
`reduced_lp`/`full_lp` value** (rows+columns+±1‑lines only, no z_P) — the one the task's rectangle‑
reduction formula is proved exact for.

## (b) reduced_lp optimum / N

| p | N=2p | reduced_lp | /N | /p |
|---|---|---|---|---|
| 101 | 202 | 267.33 | 1.3234 | 2.6469 |
| 197 | 394 | 541.67 | 1.3748 | 2.7496 |
| 401 | 802 | 1091.00 | 1.3603 | 2.7207 |
| 599 | 1198 | 1644.17 | 1.3724 | 2.7449 |
| 797 | 1594 | 2209.00 | 1.3858 | 2.7716 |

Consistent with the task background's "1.32–1.36N" ballpark (the small excess over the 101/197 figures
quoted there is exactly the z_P gap above), slowly increasing with p, comfortably inside (1.5−c)N.

## (c) Anatomy: weight by group pattern and slope

**Group patterns (independently re‑derived from the raw point set, not assumed):** a residue class with
1 root always gives a 3‑line group of sizes **(1,2,1)** ("single"); a class with 3 roots x₁,x₂,x₃ gives
either a 3‑line group of sizes **(3,6,3)** ("balanced", all 3 roots on the "same side") or a 4‑line
group of sizes **(1,4,5,2)**/**(2,5,4,1)** ("split", 2‑vs‑1 — the two orientations are mirror images and
are pooled below by the line's own point‑count, which is unambiguous except that own‑size 2 needs the
shape to disambiguate "single's middle line" from "split's outer tip"). A handful of p ≡ 11 mod 12
(here: p=599, diagonal slope only) also have rare double‑root classes giving small 2‑member groups —
negligible in count (2 of 599 groups) and folded into the nearest bucket by own‑size in the rule.

**Two clean, exact (std = 0 across every group, every p, every slope) facts**, confirmed numerically at
every one of the 10 (p, slope) combinations tested:
- every **own‑size‑1** line (the outer tip of a single or the far tip of a split): optimal weight **= 0** exactly;
- every **own‑size‑6** line (the middle of a balanced group): optimal weight **= 1** exactly.

Both make sense from the rectangle formula: a size‑1 line is a strictly worse (2× the marginal cost)
substitute for what rows/cols already give that one point for free at the margin; a size‑6 line, once
at weight 1, fully saturates (t=1) the *diagonal pair* (P1,P3) of all 3 of its member rectangles
simultaneously — no other single line can do that for 3 rectangles at once as cheaply.

**Every other position is genuinely fractional, with real (non‑degenerate) instance‑to‑instance
variance** — e.g. at p=797:

| slope | shape | own\_size | groups(shapes) | weight mean | [min,max] | std |
|---|---|---|---|---|---|---|
| diag | balanced | 3 (tip, ×2/grp) | 61 | 0.5301 | [0, 1] | 0.479 |
| diag | single | 2 (mid) | 398 | 0.6474 | [0, 1] | 0.458 |
| diag | split | 5 (inner) | 72 | 0.9051 | [0.5, 1] | 0.188 |
| diag | split | 4 (inner) | 72 | 0.5660 | [0, 1] | 0.334 |
| diag | split | 2 (tip) | 72 | 0.2917 | [0, 1] | 0.406 |
| anti | balanced | 3 (tip) | 62 | 0.3978 | [0, 1] | 0.456 |
| anti | single | 2 (mid) | 398 | 0.6149 | [0, 1] | 0.465 |
| anti | split | 5 | 71 | 0.8920 | [0, 1] | 0.285 |
| anti | split | 4 | 71 | 0.6174 | [0, 1] | 0.327 |
| anti | split | 2 | 71 | 0.4155 | [0, 1] | 0.444 |

(full tables for all 5 p are in `slack/g_agents/reduced_lp_output.txt`, part (c)). The means drift
noticeably with p (e.g. diag balanced‑tip: 0.51 → 0.32 → 0.37 → 0.36 → 0.53 across the 5 p — not
monotone) and the **std is close to the Bernoulli‑at‑the‑mean maximum** at every position except the
two split "inner" lines (size 4, size 5) — i.e. these weights are close to a genuine 0/1 (bimodal)
decision at the instance level, not a smoothly‑varying fraction, matching the max(·,·) structure of the
rectangle formula (see §(d.3) below: it is a *sharing* mechanism, not an averaging one). Diagonal and
antidiagonal show visibly **different** shape‑count mixes at small p (e.g. p=101: diagonal is 100%
balanced, 0% split — a real, if finite‑size, asymmetry between x³−x and x³+x, also seen independently in
`slack/g_agents/group_types_output.txt`) but converge toward comparable mixes by p≈599–797.

## (d) A type‑based rule

**(d.1) Flat rule — weight depends only on (slope, shape, own‑size).** We do *not* hand‑pick constants:
we solve the LP obtained by forcing all lines of the same (slope, position) type to share **one**
variable, jointly across all 5 p (so it is the exact optimum of this restricted family, not a guess) —
`fit_flat_rule()`. It converges to clean thirds, identical on both slopes:

| type (own‑size) | diag | anti |
|---|---|---|
| size 1 (tip) | 0 | 0 |
| single‑mid (2) | **1/3** | **1/3** |
| split‑tip (2) | 0 | 0 |
| balanced‑tip (3) | **2/3** | **2/3** |
| split‑inner (4) | **2/3** | **2/3** |
| split‑inner (5) | **2/3** | **2/3** |
| balanced‑mid (6) | 1 | 1 |

Cost/N, evaluated *independently* of the fit (pure O(p) arithmetic on the resulting fixed weights —
`evaluate_labelled()`, a completely separate code path from the fitting LP, so this is a genuine,
checkable upper bound regardless of whether the fit is truly optimal):

| p | rule/N | LP/N | gap | 1.5N − rule |
|---|---|---|---|---|
| 101 | 1.4158 | 1.3234 | +0.092N | +0.084N |
| 197 | 1.4399 | 1.3748 | +0.065N | +0.060N |
| 401 | 1.4522 | 1.3603 | +0.092N | +0.048N |
| 599 | 1.4669 | 1.3724 | +0.095N | +0.033N |
| 797 | 1.4642 | 1.3858 | +0.078N | +0.036N |

Already **c ≥ 0.033** at every tested p with a rule stateable in one line: *0 on size‑1 lines and
split‑tips, ⅓ on single‑classes' own line, ⅔ on every other non‑maximal line, 1 on the balanced‑class's
6‑line.*

**(d.2) Interaction rule — adds the cross‑slope term.** The task explicitly allows conditioning on "the
interaction with the other slope's group of the same residues"; §(c)'s high per‑position variance is the
signal that this matters. For a line ℓ define

```
nsmall(ℓ) = #{ member rectangles x of ℓ : x's OWN class on the OTHER slope has shape 'single' }
```

(a *big* other‑slope class — balanced or split — means that rectangle's other‑pair corners are already
well served from that side; a *small*/single other‑slope class means they are not). This is a strong,
essentially structural signal — a direct diagnostic on p=401 (`slack/g_agents/reduced_lp_output.txt`
does not contain this raw breakdown, reproduced here for the record) shows the diagonal balanced‑tip
weight going 0.07 → 0.00 → 0.64 → **1.00 (exactly, std=0)** as nsmall runs 0→1→2→3 out of 3 members —
a near‑bimodal jump exactly where all 3 members of the tip's group are themselves "unsupported" on the
other slope.

We again *solve* (not guess) the constrained LP with one shared variable per (slope, type, nsmall)
bucket, jointly across all 5 p — `fit_interaction_rule()`. Result (again identical on both slopes, again
all multiples of 1/3):

| type (nmem) | nsmall=0 | 1 | 2 | 3 |
|---|---|---|---|---|
| single‑mid (1) | 1/3 | 1 | – | – |
| balanced‑tip (3) | 1/3 | 2/3 | 2/3 | 2/3 |
| split‑tip‑2 (2) | 0 | 0 | 2/3 | – |
| split‑inner‑4 (3) | 1/3 | 2/3 | 2/3 | 2/3 |
| split‑inner‑5 (3) | 2/3 | 2/3 | 1 | 1 |

i.e. every "middle" nsmall value collapses to the *same* value the fit already found optimal — so this
is not an approximation of a smoother underlying curve, it is the exact optimum of this bucket family,
which happens to only need a 0/1 threshold on nsmall (nsmall=0 vs nsmall≥1, except split‑tip's
threshold is at nsmall=2 and split‑inner‑5's is at nsmall≥2). Independently evaluated cost/N:

| p | rule/N | LP/N | gap | 1.5N − rule |
|---|---|---|---|---|
| 101 | 1.3927 | 1.3234 | +0.069N | +0.107N |
| 197 | 1.4382 | 1.3748 | +0.064N | +0.062N |
| 401 | 1.4347 | 1.3603 | +0.074N | +0.065N |
| 599 | 1.4357 | 1.3724 | +0.063N | +0.064N |
| 797 | 1.4504 | 1.3858 | +0.065N | +0.050N |

Strictly better than the flat rule at **every** tested p (as it must be — d.2's family is a strict
superset of d.1's), never worse than the unrestricted `reduced_lp` (as it also must be — it is a
restriction of it): **LP ≤ interaction‑rule ≤ flat‑rule** holds at all 5 p, exactly as the nesting of
the three families requires — a useful internal consistency check that the two fits and `reduced_lp`
are all solving the *same* underlying cost functional. Worst case over the 5 p: **1.4504N at p=797,
i.e. c ≥ 0.0496**; the rule is within 0.06–0.07N of the true LP optimum throughout, versus the flat
rule's 0.07–0.09N gap.

**(d.3) Why a *constant* rule cannot fully close the gap to the LP, and a cautionary numerical note.**
Two things worth recording plainly (per the task's request to be honest about negative results):

1. We first tried transplanting Theorem G3.5's own explicit cover ("weight 1 on every ±1‑line with ≥4
   points, 0 below") through *this* framework (`evaluate_labelled` with weights {size1:0, single‑mid:0,
   balanced‑tip:0, split‑s2:0, split‑s4:1, split‑s5:1, balanced‑mid:1}). It performs **much worse**
   here — 1.74–1.81N, i.e. barely better than the trivial 2N and *worse* than both rules above —
   because Theorem G3.5's cover relies on generic per‑point slack z_P (cost 1/point) to mop up
   everything a ≥4‑line doesn't cover, and z_P is simply unavailable in the rows/cols‑only reduced LP:
   forcing 0/1 weights here creates asymmetric row/column demand that the (rows/cols‑only) mechanism
   handles far less efficiently than z_P would (see the (a) side‑finding above — this is the same
   mechanism, now costing much more because the 0/1 rule is a far cruder trigger for it than the true
   LP's fractional weights). This is a real, load‑bearing fact about *this specific* reduced LP, not a
   defect of Theorem G3.5 (which is correct and tight in its own, z_P‑using framework) — the two
   frameworks are provably different LPs (part (a)) and a cover good for one is not automatically good
   for the other.
2. Our first attempt at an interaction rule used the *raw fraction* nsmall/nmem as the weight directly
   (no optimisation) — a natural-looking idea given how well nsmall correlates with the LP's per‑
   instance choice. It gave **1.61–1.66N**, markedly *worse* than the flat constant rule (1.42–1.47N)
   despite "knowing more". The reason is again the max(·,·) structure: a shared line's cost‑efficiency
   comes from *simultaneously* saturating several rectangles at once, and setting its weight below what
   any of its needy members requires (e.g. 1/3 instead of 1 when only 1 of 3 members is needy) forfeits
   that sharing for the needy member without saving anything for the others (who didn't need the
   weight anyway) — so naive interpolation can be strictly dominated by a well‑chosen *constant*,
   confirming that the right way to use the nsmall signal is as a **bucket key for a properly
   re‑optimised LP** (d.2), not as a plug‑in formula. (A genuine bug — a sign error in the fixed‑
   contribution bookkeeping of the first constrained‑LP implementation — was also caught this way: it
   produced a bucketed‑rule cost *below* the unrestricted `reduced_lp` optimum, which is structurally
   impossible for a restriction of the same feasible region, and was fixed before any number in this
   report was accepted; the fix and the ordering check LP ≤ d.2 ≤ d.1 are now permanent internal
   consistency checks in `main()`.)
3. A quick (not included in the shipped rule, to keep it simple/explicit) experiment splitting "big"
   other‑slope classes into balanced‑vs‑split (a 74‑bucket fit instead of d.2's ~20) closes the gap
   further, to 1.386–1.434N (worst case c ≥ 0.066 instead of 0.050) — confirming more of the residual
   gap to the true LP is genuine further cross‑slope structure rather than LP degeneracy, at the cost of
   a much less memorable rule. We did not chase this further; d.2 already meets the task's target
   comfortably.

## Summary

| rule | worst‑case cost/N (p≤797) | margin c | gap to true LP |
|---|---|---|---|
| trivial (rows+cols only) | 2.000N | 0 (barely qualifies) | — |
| Theorem G3.5's cover, transplanted here (no z_P) | 1.812N | 0.19 (poor: much worse than d.1/d.2) | — |
| **(d.1) flat type rule** (0, ⅓, 0, ⅔, ⅔, ⅔, 1 by position) | **1.467N** | **0.033** | 0.07–0.09N |
| **(d.2) interaction rule** (+ nsmall cross‑slope term) | **1.450N** | **0.050** | 0.06–0.07N |
| reduced_lp / full_lp (true optimum, this framework) | 1.386N | 0.114 | 0 |

All numbers reproduced verbatim by `python3 slack/g_agents/reduced_lp.py` (≈1.6s). Both (d.1) and (d.2)
are explicit, closed‑form (multiples of 1/3), p‑independent rules meeting the task's goal — cost ≤
(1.5−c)N for every one of the 5 tested p, with (d.2) the closer of the two to the LP (≈1.32–1.39N in
this framework; the task background's slightly lower 1.32–1.36N figure uses the z_P‑augmented LP, see
the honest side‑finding in part (a)).
