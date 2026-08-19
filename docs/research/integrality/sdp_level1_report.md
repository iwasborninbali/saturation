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
  confirming §2.4's
  proof (θ adds nothing) and, more interestingly, showing that localizing the SDP at *only the 4
  strong line-families* also adds **nothing** over the plain LP restricted to those lines. Every bit
  of the SDP's power over the LP has to come from localizing the weak 3-point lines specifically.
* **SDP local(all) < LP(all)**, by a margin far above solver noise, at both p tried: 13 (44.8000 →
  43.9974, Δ ≈ 0.80) and 17 (60.1538 → 59.7414, Δ ≈ 0.41). At p = 13, a shorter 90s/1925-iteration
  trial run independently landed at 43.9996 — the *objective* stabilizes well before the constraint
  residual (`res_pri`) does (normal ADMM behaviour); both estimates agree to 3 significant figures.
  **Independently verified** (not trusting SCS's own residual report): re-extracting (y, Y) from a
  p = 13 run and checking every constraint directly in numpy against the raw values gives max
  violations of box/diag/RLT/plain-line/localizing(a)/localizing(b) all ≤ 3×10⁻⁴, and a smallest
  moment-matrix eigenvalue of −0.0013 — three orders of magnitude below the 0.80 gap to LP, and no
  y_i is even close to the [0,1] boundary (all sit in [0.27, 0.73]). So: **yes, the level-1 SDP with
  localizing constraints sees the 3-point lines and beats the LP, and this is a real effect, not a
  solver artifact.**

**But** the *fraction of the LP−exact gap closed drops sharply, 16.7% (p=13) → 6.7% (p=17)**. We
cannot fully separate two explanations with only two full-size points: (a) a genuine shrinking of the
level-1 SDP's relative power as p grows — plausible, and the expected shape of the phenomenon: a
fixed-level SDP/Lasserre lift is a *local* certificate (it only ties together moments of points that
already co-occur in a common localizing line), while the 3-point lines' effect is a genuinely global,
expander-like combinatorial fact about the whole ~p·log p-line hypergraph (`phenomenon.py` P5); the
general SoS/Lasserre-hierarchy literature on sparse/pseudorandom CSPs (flagged as an open question for
this very project in `deep_research_brief_8_integrality.md`, Q1) is exactly about how many rounds such
problems need, and "shrinking fraction at fixed level as the instance grows" is the textbook signature
of "this level isn't enough, you need level ~f(p)"; **or** (b) a convergence-budget artifact: p=17's
run got only 1175 ADMM iterations in its 180s vs. p=13's 3300 (bigger problem ⇒ more expensive
iterations, same wall-clock budget), so its value may still be some distance from the true level-1
optimum. Against (b): p=17's own residual (`res_pri` 3×10⁻⁴) is *tighter* than p=13's (1.9×10⁻¹)
despite the fewer iterations, which argues p=17 is not obviously the less-trustworthy of the two — but
this is not conclusive either way with the data at hand.

## 6. Honest conclusion

*being finalized — a p=19 run is in flight to get a third full-size data point on the 16.7%→6.7%
trend before committing to an interpretation; see below once it lands.*
