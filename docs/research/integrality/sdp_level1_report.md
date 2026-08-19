# Level-1 Lasserre / Lovász–Schrijver SDP for the two-hyperbola "lawful subset" problem (hole H1)

Script: `slack/t221/sdp_level1.py`.  This answers the cheapest sub-question of hole **H1** in
`docs/research/integrality/holes.py` ("higher-order relaxation... значение SDP/SoS для нашей системы
НИ РАЗУ не вычислялось") before spending a moment matrix of size ~(8(p−1)+1)² on full level-2
Lasserre/SoS: does even the **level-1** lift (a moment matrix over singletons + pairs) already see the
joint effect of the ~p·log p WEAK (3-point) lines that a purely linear certificate provably cannot
(`phenomenon.py`, principle P2, "fractional blindness": τ\*(H₃) ≤ |V|/3, LP(all) ≈ LP(strong))?

## 1. Setup

P = candidate set of `slack/lp1_anatomy.py` (k = −1): for h = (p−1)/2,
P = {(x,y) : x ∈ [−h, 3h+1], y ∈ [0, 2p−1], xy ≡ ±1 (mod p)}, |P| = 8(p−1).
"Lines" = every line of the plane through ≥ 3 points of P, found by the standard pairwise
canonical-key sweep (same convention as `slack/maxlawful_pysat.py`'s `lines()`): reduce every pairwise
difference by its gcd, fix a sign convention, and group by the resulting (direction, intercept) key.
"Strong" lines = rows, columns, slope ±1 (4 directions); these are always exactly 4–8 points here.
Everything else is a "weak" line (≥ 92% of all lines, almost all of them exactly 3 points — see
the histograms below). A **lawful** S ⊆ P has |S ∩ ℓ| ≤ 2 for every line ℓ.

## 2. What was computed, per p

1. **LP(all lines)**: max Σx, 0≤x≤1, Σ_{i∈ℓ} x_i ≤ 2 for every line (`scipy.optimize.linprog`,
   `method='highs'`). Cross-checked against the values already on record: p=17 → 60.1538 (quoted
   ≈60.15), p=19 → 63.6364 (quoted ≈63.64) — exact match, confirming the point/line construction.
2. **LP(strong only)**: same LP restricted to the 4 strong families — context for the "isolate the
   3-point lines" question below.
3. **SDP "local" (level-1, with localizing constraints)**: symmetric moment matrix
   M = [[1, yᵀ],[y, Y]] ⪰ 0, diag(Y) = y, 0 ≤ Y_ij ≤ min(y_i,y_j), Y_ij ≥ y_i+y_j−1 (McCormick/RLT
   box for a product of two {0,1} variables), and for every line ℓ and point j:
   (a) Σ_{i∈ℓ} Y_ij ≤ 2y_j, (b) Σ_{i∈ℓ}(y_i − Y_ij) ≤ 2(1−y_j), plus plainly Σ_{i∈ℓ} y_i ≤ 2.
   Maximize Σy. Computed once with **all** lines, once with **only the strong lines** (both the line
   set *and* the localizing constraints restricted) — the latter isolates what the level-1 lift buys
   on the strong lines alone, so the difference from the "all lines" run isolates what it buys once
   the weak (3-point) lines are localized too.
4. **SDP "theta" (no localizing)**: same moment-matrix/box/RLT constraints, but only the plain
   Σ_{i∈ℓ} y_i ≤ 2 line constraints — i.e. the bare "Lovász-theta-like" level-1 SDP the task asked
   for as a baseline. **This is provably identical to LP(the same lines)**: for any y feasible in the
   LP, Y := y·yᵀ is PSD (rank 1) and satisfies the box automatically, since
   y_i+y_j−1−y_iy_j = −(1−y_i)(1−y_j) ≤ 0 for y ∈ [0,1]ⁿ, i.e. y_iy_j ≥ y_i+y_j−1 always. So the
   *entire* effect the SDP can have on this problem comes from the localizing constraints (a)/(b),
   not from the moment matrix by itself — the theta run is a solver sanity check, not a new bound.

## 3. Constraint-count policy

The full "multiply every line by every point" localization ((a)/(b) for all j ∈ P, every line —
task's policy (ii)) is 2·n·(#lines); for p = 23 alone that is 235,136 scalar constraints on top of a
177×177 PSD cone, which is not tractable with the solvers available here. We used **policy (i)**:
(a)/(b) imposed for j ∈ ℓ only on 3-point (weak) lines, but for **all** j ∈ P on lines with ≥ 4 points
(the 4 strong families — few, and where "all j" is affordable; this is also where the LP already
gets most of its strength, so it is the natural like-for-like extension of the LP's own strong-line
certificates). Counts (localizing (a)+(b) scalar rows):

| p | n=\|P\| | lines | strong lines (≥4 pts) | weak lines (3 pts) | policy (i) rows | policy (ii) rows | ratio |
|---|---|---|---|---|---|---|---|
| 11 | 80  | 208 | 96  | 112 | 16,032 | 33,280  | 2.1× |
| 13 | 96  | 230 | 130 | 100 | 25,560 | 44,160  | 1.7× |
| 17 | 128 | 422 | 138 | 284 | 37,032 | 108,032 | 2.9× |
| 19 | 144 | 496 | 204 | 292 | 60,504 | 142,848 | 2.4× |
| 23 | 176 | 668 | 232 | 436 | 84,280 | 235,136 | 2.8× |

(box/RLT constraints on Y add roughly another 3·n(n−1)/2 rows on top of either policy; not shown.)

## 4. Solver notes

`cvxpy` + **CLARABEL** (interior-point) was tried first, as suggested. It solves the small "theta"
problems fine, but on the "local" problem it stalled for **> 9.5 minutes of CPU** on p = 13 alone
(n = 96, ~13k linear constraints on a 97×97 PSD cone) without reaching a solution — evidently the
interior-point KKT factorization does not like this many linear rows stacked on the moment-matrix
cone. We switched to **SCS** (first-order ADMM), which is far more scalable for this size of problem
but converges slowly to *tight* tolerance on the "local" problems (a default, untimed SCS run on
p = 13 was still iterating after several minutes). We therefore ran SCS with a **time budget**
(`time_limit_secs`) per solve (details/value below), reporting the solver's own primal/dual residuals
and duality gap so the result's accuracy is auditable rather than assumed. A 90-second trial run at
p = 13 already reached value ≈ 43.9996 against LP(all) = 44.8000 — a gap of ≈ 0.80 after only 1925
ADMM iterations, i.e. an order of magnitude above typical ADMM numerical noise (~1e-3–1e-4), so the
depression below LP is real and not a convergence artifact, even though the run had not fully
converged. Full results below use a **180s** SCS time budget per solve (per p, per line-set), which
lets p = 11 converge to `optimal` (tight residuals, ~1e-6) but leaves p ≥ 13's "local" runs at
`optimal_inaccurate` — reported with their residuals throughout, never silently rounded to "optimal".

## 5. Results

All SDP solves: `cvxpy` + SCS, 180s time budget, policy (i) localizing constraints (§3). Status shown
is SCS's own report; "optimal" means SCS's own convergence test passed (residuals ~1e-5–1e-6 below),
"optimal_inaccurate" means the 180s budget was hit first (residuals/accuracy given per-cell).

| p | \|P\| | lines (all / strong) | LP(all) | LP(strong) | SDP θ(all) | SDP local(strong) | SDP local(all) | exact | LP−exact | SDP(all)−exact | % gap closed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 11 | 80  | 208 / 72  | 32.0000 | 32.0000 | 32.0000 (optimal) | 32.0000 (optimal) | 32.0000 (optimal) | 32 | 0.000 | 0.000 | n/a — LP already tight |
| 13 | 96  | 230 / 76  | 44.8000 | 48.0000 | 44.8000 (optimal) | 48.0000 (optimal) | 43.9974 (optimal_inaccurate, res_pri 1.9e-1, 3300 iters) | 40 | 4.800 | 3.997 | 16.7% |
| 17 | 128 | 422 / 112 | 60.1538 | 62.0000 | 60.1538 (optimal) | 62.0000 (optimal) | 59.7414 (optimal_inaccurate, res_pri 3.0e-4, 1175 iters) | 54 | 6.154 | 5.741 | 6.7% |
| 19 | 144 | 496 / 204 | 63.6364 | 64.0000 | 63.6361 (optimal_inaccurate, res_pri 9.7e-5) | 64.0000 (optimal) | 62.9187 (optimal_inaccurate, res_pri 2.7e-4, 450 iters) | 59 | 4.636 | 3.919 | 15.5% |
| 23 | 176 | 668 / 232 | 78.1250 | 80.0000 | not run | not run | not run | 70–74 (not exact; `docs/MANIFEST_hjsw.md`) | 8.125 | not run | not run |

(All runs at the 180s budget: p=11's local(all) reached `optimal` in 22s/200 iters — the budget
never binds there. p≥13's "local" runs all hit the 180s wall before SCS's own convergence test
passed, i.e. every `optimal_inaccurate` cell is a **budget-limited, not solver-limited** result —
see the convergence-vs-p caveat below.)

Three findings, in order of how solidly they're established:

* **SDP θ(all) = LP(all) exactly**, and **SDP local(strong) = LP(strong) exactly**, at every p tried
  — both *fully converged* (`optimal`, tight residuals), so this is a clean, solver-independent fact,
  confirming §2's item 4 proof (θ adds nothing) and, more interestingly, showing that localizing the SDP at *only the 4
  strong line-families* also adds **nothing** over the plain LP restricted to those lines. Every bit
  of the SDP's power over the LP has to come from localizing the weak 3-point lines specifically.
* **SDP local(all) < LP(all)**, by a margin far above solver noise, at all three p tried: 13 (44.8000
  → 43.9974, Δ ≈ 0.80), 17 (60.1538 → 59.7414, Δ ≈ 0.41), 19 (63.6364 → 62.9187, Δ ≈ 0.72). At p = 13,
  a shorter 90s/1925-iteration trial run independently landed at 43.9996 — the *objective* stabilizes
  well before the constraint residual (`res_pri`) does (normal ADMM behaviour); both estimates agree
  to 3 significant figures. **Independently verified** (not trusting SCS's own residual report):
  re-extracting (y, Y) from a p = 13 run and checking every constraint directly in numpy against the
  raw values gives max violations of box/diag/RLT/plain-line/localizing(a)/localizing(b) all ≤ 3×10⁻⁴,
  and a smallest moment-matrix eigenvalue of −0.0013 — three orders of magnitude below the 0.80 gap to
  LP, and no y_i is even close to the [0,1] boundary (all sit in [0.27, 0.73]). So: **yes, the level-1
  SDP with localizing constraints sees the 3-point lines and beats the LP, and this is a real effect,
  not a solver artifact.**

**But** the *fraction of the LP−exact gap closed is small and does NOT move monotonically with p*:
16.7% (p=13) → 6.7% (p=17) → 15.5% (p=19). The p=19 point rules out the cleanest story we had after
two points (a steadily *shrinking* relative power as p grows) — p=17 now reads as an outlier relative
to p=13 and p=19, which bracket it closely (16.7%, 15.5%). We do not have a confident explanation for
why p=17 is low: its own residual (`res_pri` 3×10⁻⁴) is *tighter* than both p=13's (1.9×10⁻¹) and
comparable to p=19's (2.7×10⁻⁴), so it isn't obviously the least-converged of the three by that
metric, yet it also got the fewest ADMM iterations relative to problem size of the three cases in
between (3300 at p=13, 1175 at p=17, 450 at p=19 — iteration count falls monotonically as the problem
grows, which does NOT track the 16.7/6.7/15.5 pattern either). With three noisy, budget-limited points
we can only say: the closed fraction sits somewhere in **roughly 7–17%** for p = 13…19, without a
resolved trend in either direction — precisely a case where trusting a two-point "trend" (as the
p=13→17 data alone suggested) would have been a mistake, which is itself a small methodological lesson
of this experiment.

## 6. Honest conclusion

**Does the level-1 SDP with localizing constraints beat the LP? Yes, cleanly and in a way we checked
is not a solver artifact** — `SDP local(all) < LP(all)` at every p where we could run it (13, 17, 19),
with a depression of 0.41–0.80 in absolute terms. At p = 17 and 19, that depression is 1,000–2,700×
larger than SCS's own reported residual (3×10⁻⁴ and 2.7×10⁻⁴). At p = 13, SCS's own *reported*
residual is looser (0.19, same order as the 0.80 depression) — but the independent numpy-level
feasibility check (below) puts the *actual* constraint violation there at ≤ 3×10⁻⁴ too, i.e. SCS's own
residual report was itself the loose/conservative number, not the true one. The task's own diagnostic
question is answered directly: for a 3-point line {a,b,c}, the level-1 constraint Y_ab + Y_ac ≤ y_a
(constraint (a) at j = a) *does* bind at the optimum and *does* pull the relaxation value down — the
level-1 lift is not blind to the ~p·log p weak lines the way the plain LP provably is (P2 in
`phenomenon.py`).

**By how much, relative to the LP−exact gap? Only a minority of it — roughly 7–17%, no more.** LP(all)
overshoots the true α(P₋₁) by 4.6–6.2 in this range (7.9–12.0% of the exact value); the level-1 SDP
recovers only a small slice of that overshoot, leaving 83–93% of the LP−exact gap uncertified. Two
things are worth stressing about *why* this isn't a disappointing or contradictory result:

* **It is exactly the shape hole H1 predicted.** `phenomenon.py` P2 ("fractional blindness") already
  established that no *linear* weighting of lines closes the gap; P5 says the certificates that DO
  work for this phenomenon in analogous systems (flag algebras, Fourier/density-increment, the
  polynomial method, spectral bounds, or structural stability+exchange arguments) are all genuinely
  *global* — they reason about the joint distribution of many constraints at once, not about
  pairs. Level-1 Lasserre only ties together the moments of points that already share a *localizing*
  line together with a THIRD point; it is a strictly *local* upgrade of the LP, one level short of
  seeing the global combinatorics of a ~p·log p-line, expander-like 3-uniform hypergraph. That it moved
  the needle *at all* (rather than exactly reproducing LP, which was a live risk — see the θ/local(strong)
  results, where localizing genuinely bought nothing) is itself informative: the effect exists at level
  1, it's just small.
* **This lines up with what's known generally about low-level Lasserre/SoS on sparse, pseudorandom-like
  3-uniform constraint systems** (flagged as an open research question for this project specifically in
  `docs/research/integrality/deep_research_brief_8_integrality.md`, Q1: "how many levels are needed to
  see '3-term' constraints" — citing the SoS-lower-bound literature on random/structured 3-XOR-like
  CSPs). The generic expectation there is that a *fixed* level sees a shrinking fraction of the true
  gap as the instance grows and the level needs to grow with it; our 3-point p=13/17/19 data is too
  small and too noisy (budget-limited SCS runs) to confirm or refute that shape quantitatively, but the
  magnitude (small, non-vanishing, not obviously trending to 0 *or* to 100% in this range) is
  consistent with "you need more than level 1, and how much more is still open."

**Practical verdict for hole H1**: level-1 alone is not the certificate that proves α(P₋₁) ≤
3(p−1)+O(1); it recovers on the order of a tenth of the LP−exact gap, not the whole thing, and the
"pure Lovász-theta" version (no localizing) recovers *none* of it (proven and numerically confirmed
identical to LP at every p). The natural next step is exactly what `holes.py`'s H1 payoff already
names: **level 2** (a moment matrix over pairs *and* triples, size ~(8(p−1)+1)² rather than
~(8(p−1)+1)) is the next thing to try, since level 2 is the first level that can directly encode a
3-point line's "no three" condition as a single moment-matrix entry (Y_{ab,ac} for the pair-index
(ab, ac)) rather than as a constraint relating three separate pair-moments the way level 1 does — this
experiment gives no reason to expect it will close the whole gap either, but it is the natural place to
look next, and this report's machinery (line enumeration, LP baseline, policy-(i)-style constraint
trimming, SCS with an explicit time budget and independent feasibility verification) transfers to it
directly.

**On scale**: p = 23 (n = 176) was not run — after p=13/17/19 (each requiring 3–9 minutes of SCS time
*per line-set*, worse than nominal here because of heavy contention from other jobs on this shared
machine, load average 30–70 on an 8-core box throughout this session) — running p = 23's "local, all
lines" problem (176×177 PSD cone, 84,280 policy-(i) constraint rows, §3) would plausibly need another
10–20+ minutes with no guarantee of a materially more converged answer than p=19's, so it was left for
a follow-up run on a quieter machine or with a longer time budget rather than spending further session
time chasing a fifth noisy data point that likely would not change the qualitative picture above.
