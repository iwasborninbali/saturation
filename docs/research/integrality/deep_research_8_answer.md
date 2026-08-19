# Deep research 8 — answer

Answer to `docs/research/integrality/deep_research_brief_8_integrality.md`, written after a verification
pass over the Q1–Q7 corpus (every source re-fetched, every computation re-run), three adversarial reviews
(arithmetic / integrality-gap / structural), two opposing theses, and three sets of counter-proposals.

**Calibration convention used throughout.** Unless stated otherwise, a transfer probability is
`P(the mechanism, executed perfectly, yields a PROVED bound strictly below the current state of the art
3.44817(p−1))`. That is a different and much harder question than "is the source real" or "would the
mechanism close its hole", and several probabilities in the raw corpus silently answered one of the
easier questions. Where the corpus's number answered a different question, both are given.

**Re-judged against the state after 48 commits** (H3 closed positively, H4 closed negatively on three
routes, H1 partially computed, proved constant 3.44817(p−1)). Cards that were ranked highly *because a
hole was open* are marked and re-ranked.

---

## 0. Verdict in ten lines

1. **No literature mechanism transfers.** After hostile verification, the highest transfer probability
   in the entire corpus is 0.08, and after re-judging against the new state the highest is **0.05**.
   Every celebrated "SDP beats LP for packing" story is arity-2 constraints made computable by a large
   symmetry group; ours is order 2–4.
2. **The corpus's fabrication record is unusually clean** — no invented paper, no invented author, one
   transplanted theorem-number pointer, one misattributed arXiv id, four wrong constants (§12).
3. **The single most important finding is structural and negative, and it is new since the brief:** a
   stability theorem for one hyperbola now *exists* (Prop. `prop:stability`, sharp) and *still does not
   help*, because the literature's stability+exchange machinery operates near a single structure's
   extremum and our extremum sits **between two** (a ≈ b ≈ 1.5(p−1), where both halves are far from
   maximal on their own hyperbola). H4(ii) is the sentence to remember from this whole exercise.
4. **Second most important, and it prunes four questions at once:** every cover / packing / near-partition /
   fractional-cover / "counting through a point" / exchange-charging bound is a nonnegative combination of
   the per-line constraints, hence ≥ LP(all) ≈ 3.40(p−1). This is the brief's "defect δ ⇒ O(δ)" question:
   there is no named theorem because the statement is ordinary fractional relaxation.
5. **Third: H3 is LP-invisible.** Adding the sharpest linear content of Lemma `orbopt` (per-orbit caps 12/6,
   both hyperbolae, plus orbit-union caps) to LP(all) changes the value by *exactly zero* at every prime
   11 ≤ p ≤ 61, with no cut even active. Any mechanism consuming H3 through a per-orbit, per-hyperbola or
   distance-to-a-maximum count is dead before it starts.
6. **The brief's own calibration is wrong in three places** and every ranked list inherits the error:
   3.45 is LP(1), not LP(all) (floor ≈ 3.32–3.40); H4 ⇔ H7 ⇔ the target with no loss in the constant, so a
   Q2/Q5 "transfer" *is* a complete solution; and the k = −1 gains are 2, 4, 6, 5 (monotone through p = 17,
   spread 4), not the all-k sequence 5, 5, 6, 5 the published conjecture is about.
7. **Two of the project's own analytic blockers are not real** (the most valuable positive output here, and
   both are reverse findings): Conjecture A needs `E/(p−1)` above an *absolute constant* (≈ 9, or ≈ 5.8 on
   §23's own numbers), not `→ ∞` — a constant threshold is carried by bounded-σ families whose Kloosterman
   counts are rigorous, making it a **finite check plus 51 classical counts, no Burgess**; and §26a's window
   law for w ≥ 2 is provable in four lines by the Kummer/branch-locus argument already in `lemma_run.tex`.
8. **But even a fully proved model theorem cannot beat 3.4482**: `pair_bound_notes` line 585 gives its own
   ceiling as `4(p−1) − c·p/log p`. So the entire H5/spectral vector — the analytically hardest thing in the
   brief — is aimed at a target already dominated by a proved result. This dominates Q3 and Q1-MC3.
9. **H8 asks for something proved not to exist** (orbit unions attain exactly 16/32 = the trivial bound, and
   packing bounds are LP duals); H2 is dead in both limit categories by measurement; H6 is difficulty-conserved;
   H1 has exactly one uncomputed item left and two repo documents disagree about whether it was computed.
10. **Keep pushing? Not on any H-route as stated.** Three cheap computations decide whether the target itself
    is right (§11), one new exact lemma closes the whole covering/block family with a proof rather than
    numerics (§10.1), and the honest retarget is the union case of Conjecture G at o(p) (§13).

---

## 1. Q1 [H1, H2] — SDP / SoS / flag algebras against LP for packings with many small constraints

### (i) Sources

All CONFIRMED verbatim against primary text unless marked.

| Source | Statement used | Status |
|---|---|---|
| Gijswijt, PhD thesis, arXiv:1007.0906, Ch. 7 §7.1, **Prop. 45** | "The maximum in (7.2) equals 1 + (3ⁿ − 1)/2", with the explicit assignment 1 / ½ / 0 / ¼ and constraint (iv) `x^{i,0}_{i,i}=0`; and the author's own "This is an appealing idea. Unfortunately, it turned out to be false in general." / "This bound is very poor." | **CONFIRMED** (PDF extracted; every word verbatim) — but **OVER-INTERPRETED** by the card, see below |
| de Laat–Vallentin, Math. Program. Ser. B **151** (2015) 529–553, arXiv:1311.3789 §1.2 | definition of `las_t(G)` with the "and 0 otherwise" clause; θ′(G) = las₁(G) ≥ … ≥ las_{α(G)}(G) = α(G); "the t-th step in Lasserre's hierarchy is a 2t-point bound"; Laurent's precedence | **CONFIRMED** verbatim. Caveat the card omits: stated for **graphs** (arity 2); the 3-uniform extension is routine but not literally in the source |
| Laurent, Math. Program. **109** (2007) 239–261 | Delsarte = first bound in the hierarchy; **Schrijver's bound lies strictly between the first and second**; the second needs O(n⁷) variables and "seems out of reach"; Schrijver's is O(n³) | **CONFIRMED** (upgraded from "verified-secondary": entry appears verbatim as de Laat–Vallentin ref [26]) |
| Kunisky–Bandeira, Math. Program. **190** (2021) 721–759, arXiv:1907.11686 | degree-4 SoS does not certify a value asymptotically smaller than λ_max(W) ≈ 2 for GOE | **CONFIRMED** verbatim |
| Jones–Potechin–Rajendran–Tulsiani–Xu, FOCS 2021, 406–416, arXiv:2111.09250 | SoS lower bound for sparse independent set, d > log²n, k = Ω(n/(√d·log n·D_SoS^{c₀})) | **CONFIRMED** verbatim |
| Kothari–Potechin–Xu, STOC 2024, arXiv:2406.18429 | degree-2D SoS fails to certify max independent set is o(n/(√d·D⁴)) in ultra-sparse G(n,d/n) | **CONFIRMED** |
| Elek, RSA, arXiv:0711.2800 | "graph parameters such as the independence ratio … are not testable in bounded degree graphs" | **CONFIRMED** verbatim |
| Hatami–Lovász–Szegedy, GAFA **24** (2014) 269–296, arXiv:1205.4356 | limit of a locally-globally convergent bounded-degree sequence is representable by a graphing | **PARTIALLY CORRECT** attribution: the colored-neighbourhood metric is **Bollobás–Riordan's**, refining Benjamini–Schramm; HLS proved graphing representability |
| Bachoc–Vallentin, JAMS **21** (2008) 909–924; Musin, Annals **168** (2008) 1–32 | semidefinite three-point bounds; τ₄ = 24 by a modified LP; Odlyzko–Sloane LP gives only τ₃ ≤ 13, τ₄ ≤ 25 | **CONFIRMED** |
| **Rupert Li**, Adv. Math. **460** (2024) art. 110043, arXiv:2206.09876 | Cohn–Elkies LP provably **not** sharp in dimensions 3, 4, 5 | **CONFIRMED** — the card credited this to "Cohn–Triantafillou". **MISATTRIBUTION**, see §12 |
| de Courcy-Ireland–Dostert–Viazovska, Math. Comp. **93** (2024) 1993–2029, arXiv:2211.09044 | Cohn–Elkies not sharp in dimension 6 | **CONFIRMED** |
| Cohn–Kumar–Miller–Radchenko–Viazovska, Annals **185** (2017) 1017–1033 | "an optimal auxiliary function for the linear programming bounds" in dim 24 | **CONFIRMED** |
| Baber, arXiv:1201.3587; Razborov, SIAM J. Discrete Math. **24**(3) (2010) 946–963 | π(K₄³) ≤ 0.5615 by flag algebras; the tight 4/9(1−o(1)) statement | **CONFIRMED** |
| Tulsiani, "CSP gaps and reductions in the Lasserre hierarchy", full version 5 Nov 2009 | 2^k/2k − ε gaps; Independent Set / Chromatic Number gaps after 2^{Ω(√(log n log log n))} rounds; 1.36 for Vertex Cover over Ω(n^δ) rounds | **CONFIRMED** verbatim; the k-uniform **Hypergraph Vertex Cover** gap of k−1−ε is **verifiably ABSENT** from this version (zero grep hits) |
| Chlamtač–Singh, APPROX 2008 | Θ(1/γ²) levels find an independent set of size **n^{Ω(γ²)}** in a 3-graph with one of size γn; 1/γ levels give nothing | **CONFIRMED**; the card's open exponent question is resolved as stated |
| Schrijver, IEEE-IT **51** (2005) 2859–2866; Gijswijt–Mittelmann–Schrijver, IEEE-IT **58** (2012) 2697–2705; Ellenberg–Gijswijt, Annals **185** (2017) 339–343; Balogh–Lidický–Salazar, SIAM JDM **33**(3) (2019) 1261–1276 | Terwilliger-algebra block diagonalisation; quadruple distances; cap-set 2.756ⁿ; flag algebras for crossing numbers | **CONFIRMED** |

**The Gijswijt correction, because it is load-bearing.** Program (7.2) is Schrijver's *symmetrized triple*
SDP with the forbidden-triple variables zeroed. Its PSD matrix has entries `M'_{u,v} = y_{{0,u,v}}`, a
degree-3 moment — a principal-submatrix projection of the level-2 moment matrix. By Laurent's own
accounting (cited two sources later in the same corpus) Schrijver-type triple bounds sit **strictly between
Lasserre level 1 and level 2**, so `las₂ ≤ value(7.2)`: Prop. 45 kills the symmetrized triple SDP and
leaves level 2 untouched. Calling it "our x = 2/3 blindness reproduced one level up" overstates it. One
point *in the card's favour* that it missed: over F₃ the affine-cap condition `u+v+w = 0` is genuinely
Hamming-scheme invariant, so nothing is lost to over-symmetrization — the collapse is real, just not at
the level claimed.

### (ii) Mechanism cards

**MC1 — line-clique Schur cut `1_ℓᵀ Y 1_ℓ ≤ 2 + s_ℓ`, the corpus's headline deliverable. KILLED.**
Inputs: the ({∅} ∪ pairs-in-ℓ) submatrix `[[1,uᵀ],[u,Diag(u)]]`. Step: Schur complement `Diag(u) − uuᵀ ⪰ 0`
iff `Σu ≤ 1`. Output: the stated cut. The derivation is *correct* and the K_n^{(3)} proof of concept
(s² ≤ s+2 ⇒ s ≤ 2 against LP 2n/3) is *correct*. Three independent kills:
(a) its stated premise — "no cvxpy/Mosek/SDPA installed, so the actual value was NOT computed" — is **false**:
`slack/t221/sdp_level1.py` ran a level-1 lift with localizing constraints on exactly this instance;
(b) the cut is **provably dominated** by that computation: `sdp_level1.py` imposes `Σ_{i∈ℓ} Y_ij ≤ 2y_j` for
every `j ∈ ℓ`, which summed over `j ∈ ℓ` gives `1_ℓᵀ Y 1_ℓ ≤ 2 s_ℓ`, strictly stronger than `2 + s_ℓ`
whenever `s_ℓ < 2`; hence value(MC1) ≥ 43.9974 / 59.7414 / 62.9187 at p = 13/17/19, i.e. ≥ 3.667 / 3.734 /
3.496 times (p−1);
(c) its Step-5 "evidence" is a degrees-of-freedom artefact: residual 0 exactly when κ(κ+1)/2 ≥ n and > 0
exactly when κ(κ+1)/2 < n, in 8 of 9 primes.
*Worth salvaging as a diagnostic, not a relaxation:* Step 4's observation that on a tight line the vectors
`u_x` must sum to exactly zero, and that slack is bought only by pulling `s_ℓ` below 2, is a correct and
useful way to see why the LP optimum is rigid; the `ker(M_T)` rank test is a cheap screen.

**MC2 — full `las₂` on the 8(p−1) candidates. Survives as a correctly costed impossibility record.**
Moment-matrix side `1 + n + C(n,2)` = 3241 / 4657 / 8257 / 15577 at p = 11 / 13 / 17 / 23, with 1.7·10⁶ to
4.3·10⁸ free moments. Its strongest argument is the one the card buries: **the primes where any level-2
object is computable are exactly the primes where LP(all) − α is O(1)** — LP(all) = α = 32 at p = 11 — and
the gap only becomes Ω(p) where the matrix is unusable. The obstruction is purely computational; Gijswijt
does not rule `las₂` out mathematically.

**MC3 — degree-4 SoS for the vertical-pair model `min T(ε) = E + εᵀCε`. Survives, but its target is dominated.**
Inputs verified exact against the repo: λ_min = −3.21, −2.37, −2.44, −4.03, −3.53, −4.50, …; E/(p−1) = 5.4,
4.3, 4.5, 6.6, 6.4, 9.1, …; spectral column 21.4, 23.1, 32.5, 45.5, 63.9, 129, 138; exact minima 24, 28, 42,
48, 80, 136. Two corrections: the "within 5% from p = 23 on" is a misquote (the 5% is at p = 29: 129.1 vs 136;
at p = 23 it is 63.9 vs 80, a 20% gap); and C_p has **no bounded moments** (m₂ ≍ log p, |λ_min| ≍ √(log p)),
so it is Wigner-*shaped* but not fixed-variance Wigner and the Kunisky–Bandeira transfer is heuristic.
**The dominating objection (new):** `pair_bound_notes` line 585 states the model's own ceiling —
"at least (E + (p−1)λ_min)/Δ deletions … ⇒ a bound for the MODEL of the form 4(p−1) − c·p/log p or better;
not T1". Since p/log p = o(p), *no* proof of the model theorem can produce a constant improvement on 4(p−1),
hence cannot reach 3.594, 3.4482, or the LP floor. MC3 is a diagnostic.

**MC4 — flag algebras / SDP over local densities. Survives as a correct, well-sourced negative,
now closed in both limit categories by measurement.** Dense limit is null: triple density
8.57·10⁻³ (p=11) → 7.30·10⁻⁴ (p=41) → 1.29·10⁻⁵ (p=401), i.e. Θ(log p / p²). Bounded-degree local–global
limit does not contain the sequence: mean triple-degree 26.4, 30.1, 37.0, 51.4, 62.4, 66.2 at
p = 11, 19, 41, 101, 199, 401 (≍ 11 log p, **unbounded**), and min/max degree ratio 13/46 … 32/119, i.e.
3.5–4.8 and **not shrinking**, so the Frankl–Rödl / Pippenger near-regularity hypothesis fails by a factor
≈ 4 uniformly. Max codegree is **exactly 6** at every prime from 11 to 401 — the hypergraph is locally
simple (a partial linear space), which is exactly what makes the analogy tempting and exactly the part that
does not carry the argument.

**MC5 — symmetry-reduced 3- or 4-point bound. Survives as the single cleanest structural reason the
coding-theory successes do not transfer, and is now a measurement rather than an inference.**
Two independent searches, and they **disagree on the order**, which I report rather than average: one found
exactly **2** maps at p = 11, 13, 17 (identity and `x ↦ p−x`) among all `(x,y) ↦ (e₁x+a, e₂y+b)` and swap-composites
preserving P₋₁ and the box; the other found a free **Klein four-group** {id, `(x,y)↦(x,2p−y)`, `(x,y)↦(p−x,y)`,
composite} at p = 13…41 with all point-orbits of size 4. The discrepancy is almost certainly boundary handling
of `y = 0 ↦ 2p`. Both agree the order is O(1), which is the load-bearing fact. Confirmed in the repo: the
Klein four-group acts on the **p−1 classes** (`hjsw_window.tex` line 214), and "F_p-affine equivalence is not
a symmetry of the window" (line 648; `pair_bound_notes` line 270). With |Aut| = O(1) there is no
block diagonalisation, hence no route from a numerical value at p ≤ 19 to a statement about all p.

### (iii) Transfer against I1–I6, and the new H1 state

`I5` (spectral representation) is what MC3 plugs into and is dominated by the model's own 4(p−1) ceiling.
`I6` (exact solvers to p ≈ 23–61) is what MC2 needs and cannot get. `I1`+`I2` are what MC4 would need and
they deliver a *sparse, unbounded-degree, non-near-regular* object that no limit theory covers. `I4` is
what MC5 needs and it supplies a group of order 2–4.

**The H1 state must be stated precisely, because the repo contradicts itself.** What was computed
(`slack/t221/sdp_level1.py`, `docs/research/integrality/sdp_level1_report.md`) is the **level-1** lift: a
moment matrix `[[1,yᵀ],[y,Y]]` indexed by ∅ and singletons with pair entries, plus McCormick/RLT and
localizing constraints `Σ_{i∈ℓ} Y_ij ≤ 2y_j`, `Σ_{i∈ℓ}(y_i − Y_ij) ≤ 2(1−y_j)`. Results, two independent
runs, same conclusion, slightly different numbers — cite both:

| p | LP(all) | SDP local(all), `sdp_level1.py` | SDP, `slack/sdp_lawful.py` (`certificate_hierarchy.md`) | α | % of LP−α closed |
|---|---|---|---|---|---|
| 11 | 32.0000 | 32.0000 | 32.00 | 32 | LP already tight |
| 13 | 44.8000 | 43.9974 | 43.96 | 40 | 16.7% |
| 17 | 60.1538 | 59.7414 | 59.64 | 54 | 6.7% |
| 19 | 63.6364 | 62.9187 | 62.83 | 59 | 15.5% |

Proved facts from that run, and they are the most useful things in it: **SDP θ(all) = LP(all) exactly**
(rank-1 `Y = yyᵀ` is feasible, since `y_i y_j ≥ y_i + y_j − 1` always), and **SDP local(strong) = LP(strong)
exactly**. So all of the SDP's power comes from localizing the **weak** lines — and it is 7–17%,
non-monotone. `certificate_hierarchy.md`, `REPORT §17` and `hjsw_window.tex` all call this object "level 2";
`sdp_level1_report.md` correctly calls it level 1 and says level 2 has not been run. **A genuine level-2
relaxation over triples — the first level that can carry a three-point line as a single moment entry — has
never been computed.** Every document should be corrected to say which lift was run.

| Card | corpus P | **re-judged P** | why |
|---|---|---|---|
| MC1 line-clique Schur cut | 0.35 → 0.02 | **killed** | dominated by a computation already in the repo |
| MC2 full `las₂` | 0.03 → 0.02 | **0.02** | cost is real; primes with a gap are the primes it cannot reach |
| MC3 degree-4 SoS on the model | 0.10 → 0.07 | **0.02** | even a perfect answer gives 4(p−1) − c·p/log p (§20), below the proved 3.4482 |
| MC4 flag algebras | 0.02 | **0.01** | both limit categories now closed by measurement |
| MC5 symmetry reduction | 0.02 | **0.01** | \|Aut\| = 2–4, measured |
| *genuine level-2 over triples* (uncomputed) | — | **0.05** to beat 3.4482; **0.15** to close ≥ 40% of the LP−α gap | the one live item in H1 |

### (iv) Negative findings

- **The imported SoS pessimism is vacuous, and this cuts the project's way.** Jones et al. and
  Kothari–Potechin–Xu lower-bound SoS by Ω(n/(√d·polylog)) ≈ n/8 = 1.0(p−1) — far *below* the 3(p−1)
  target. Our independence ratio is α/n = 3/8 = 0.375, **constant**, whereas a random 3-graph of the same
  degree has √(log d/d) = 0.352, 0.336, 0.312, 0.277, 0.257, 0.252 at p = 11 … 401, **decaying**. So no
  published SoS lower bound rules out level 2 here, which makes level 2 *more* worth trying, not less.
  Adopt the one-line check: any card citing a random-instance SoS lower bound must state the value it
  lower-bounds SoS by, in units of (p−1); below 3, the citation is decorative.
- **Barak–Chan–Kothari (STOC 2015, arXiv:1501.00734) is irrelevant here** and must be demoted to a
  footnote. The source is CONFIRMED verbatim, and the predicate claim is correct (|P⁻¹(1)| = 7 and
  {000,011,101,110} is pairwise independent). But BCK bounds SoS's ability to *refute* a MaxP instance
  near |P⁻¹(1)|/2^k, and our packing is always satisfiable (all-zero), so it says nothing about
  `max Σx` subject to all constraints. The corpus's claim that it "kills any hope of a general theorem
  that level 2 sees triples" is **WRONG**.
- **Every LP-sharpness success in the literature is a two-dimensional miracle**: Delsarte's LP is sharp for
  kissing numbers in exactly dimensions 8 and 24 (Levenshtein; Odlyzko–Sloane, both 1979, independently)
  and Cohn–Elkies is now *provably* not sharp in dimensions 3, 4, 5 (Li) and 6 (de Courcy-Ireland–Dostert–
  Viazovska). Flag algebras plateau at 0.561666 on Turán (3,4) above the conjectured 5/9 — structurally the
  same shape as our 3.44 plateau.
- **The combinatorial anatomy is honest and reproducible** (recomputed from scratch, exact match including
  a counter-intuitive non-monotone dip at p = 37): lines with ≥ 3 points 208, 230, 422, 496, 668, 1028,
  1248, 1118, 1808; 3-point lines 112, 100, 284, 292, 436, 660, 836, 620, 1244; collinear triples 704, 684,
  988, 1444, 1744, 2888, 2992, 3368, 3948; LP(all) 32.0000, 44.8000, 60.1538, 63.6364, 78.1250, 92.1126,
  104.7619, 122.3109, 142.2976 at p = 11 … 41. Note LP(all)/(p−1) oscillates in 3.20–3.76 with no p in
  11…41 sitting at 3.45.
- **"Mean degree 25 at p ≈ 2000"** is unlabelled and does not match the collinear-triple degree (measured
  37.0 / 51.4 / 62.4 / 66.2 at p = 41 / 101 / 199 / 401, growing); it matches only the 3-point-line degree.

---

## 2. Q2 [H3, H4] — stability of algebraic extremals + exchange arguments giving "construction + O(1)"

**This section's content changed completely while the research was running.** H3 is closed positively; H4 is
closed negatively on three routes. Read (iv) first.

### (i) Sources

| Source | Statement used | Status |
|---|---|---|
| Ball–Lavrauw, "Planar arcs", JCTA **160** (2018) 261–287, arXiv:1705.10940v4 | **Lemma 10**: `f_x(y) = (−1)^{t+1} f_y(x)` for all x, y ∈ S, with `f_a` the product of the t linear forms whose kernels are the t tangents at a | **CONFIRMED** verbatim. Needs the normalisation `f_a(e) = (−1)^{t+1} f_e(a)` at a fixed e ∈ S, which the card drops |
| — same | **Theorem 1** (arc of size q+2−t not on a conic and not on a degree-t curve lies in the intersection of two curves of degree ≤ t + p^{⌊log_p t⌋}) | **PARTIALLY CORRECT**: has a **second branch** requiring the explicit technical condition (1) `p^{⌊log_p t⌋}(t + p^{⌊log_p t⌋}/2 + 3/2) ≤ (t+2)(t+1)/2`, which the abstract itself flags |
| — same | **Theorem 2** (q = p^{2h}, p ≠ 2: size ≥ q − √q + 3 + √q/p ⇒ conic); **Theorem 3** (q prime: size ≥ q − √q + 7/2 ⇒ conic) | **CONFIRMED** verbatim |
| — same, introduction | Segre (q even) ≤ q − √q + 1; Voloch (q prime) ≤ (44/45)q + **8/9**; Voloch (q odd non-square) ≤ q − ¼√(pq) + (29/16)p − 1; Hirschfeld–Korchmáros ≤ q − ½√q + 5 (char ≥ 5), improved to +3 for q ≥ 529, q ∉ {3⁶, 5⁵} | **CONFIRMED**; the 8/9 uncertainty is **RESOLVED** (Ball–Lavrauw line 166–169, ref [29] = J. Geom. **38** (1990) 198–200) |
| Hirschfeld–Thas, arXiv:2503.06243 (8 Mar 2025; Mathematics **13** (2025) 1489) | Thm 3.2, Thm 3.4 (Segre 1955: every oval in PG(2,q), q odd, is a non-singular conic), **Thm 3.6(ii)** (q odd, k > q − ¼√q + **25/16** ⇒ extends to an oval, due to Segre 1967 and Thas, J. Algebra **106** (1987) 451–464), Thm 4.4 (Kaneta–Maruta) | **CONFIRMED** exactly; the card gave no authors |
| Stępień–Szymaszkiewicz, "Arcs in Z²_{2p}", arXiv:1512.02175 | Lemma 2.1 τ(Z_p²) = p+1 (**p odd**); Lemma 2.2 τ(Z²_{mn}) ≤ min{m·τ(Z²_n), n·τ(Z²_m)}; Thm 3.1 τ(Z²_{2p}) ≤ 2p+2 with equality at p = 3, 5; Remark 3.2; Lemma 3.6; Thm 3.9; τ = 8, 12, 12, 18, 20 for n = 6, 10, 14, 22, 24 | **CONFIRMED** |
| Balogh–Füredi–Roy, Amer. Math. Monthly **130** (2023) 437–445, arXiv:2103.15850 | Sidon in {1..n}: ≤ √n + 0.998 n^{1/4} | **CONFIRMED**. Chain: Lindström 1 → BFR 0.998 → O'Bryant 0.99703 → Carter–Hunter–O'Bryant **0.98183** (Acta Math. Hungar. **175** (2025) 108–126, arXiv:2310.20032) |
| — | "the only improvement ever obtained on the second-order term of the Sidon problem in an interval" | **UNVERIFIABLE** (negative existential over 80 years) |
| Vosper, JLMS **31** (1956) 200–205 (+ Addendum 280–282) | critical pairs of subsets of Z_p | **CONFIRMED** |
| Freiman 3k−4, two-set form | the card writes `\|P\| = \|Q\| = k+r` | **PARTIALLY CORRECT**: the standard conclusion is `\|P\| ≤ \|A\|+r`, `\|Q\| ≤ \|B\|+r`; no source was given. Bollobás–Leader–Tiba arXiv:2204.09816 is a real strengthening but does not source the classical statement |
| Haviv–Levy, arXiv:1703.04118 Thm 1.1 | max sum-free in Z_p is ⌊(p+1)/3⌋, with the classification (p=3k+1: [k+1,2k], [k,2k−1], and for k ≥ 4 {k} ∪ [k+2,2k−1] ∪ {2k+1}; p=3k+2: [k+1,2k+1]), restating Diananda–Yap / Yap / Rhemtulla–Street | **CONFIRMED** two ways (source + independent exhaustive computation over Z_p, p ≤ 43, including the k ≥ 4 caveat) |
| Darmann–Pferschy–Schauer–Woeginger, DAM **159** (2011) 1726–1735 | max matching under disjunctive constraints is NP-hard even when every conflict component is a single edge; MST polynomial in that case | **CONFIRMED** |
| Kovács–Nagy–Szabó, Adv. Comb. **2026:7**, arXiv:2508.07632 | (1−2/k)kn ≤ f_k(n) ≤ kn for even k, **(1−3/k)kn** for odd k; f₃(n) ≥ 1.973n | **CONFIRMED**; the card said odd-k bounds are "tighter" — they are **weaker**. The repo's `[KNS25]` entry is correct in every field |
| Green, "100 open problems", **Problem 72** | the 2N question; "(3/2 + o(1))N such points" from HJSW [167]; 2N configurations for N up to around 50; and "It is possible that any no-three-in-a-line subset of [N]² is either small, or has a large subset which reduces (mod p) to a set of points on a curve in F_p²" | **CONFIRMED** verbatim (read directly). Update: n ≤ 64 (Prellberg, Feb 2026, per Voutier) |
| Voutier, arXiv:2603.00215v2 | Guy–Kelly's `f_n ~ (2π²/3)^{1/3}n`, Guy's 22 Oct 2004 note recording Ellmann's correction to `3c² = π²`, i.e. c = π/√3 ≈ 1.813799 | **CONFIRMED** verbatim |
| Stępień–Misiak–Szymaszkiewicz–Szymaszkiewicz–Zwierzchowski, arXiv:1406.6713 | at most **2 gcd(m,n)** points on an m×n discrete torus | **CONFIRMED**; a WebFetch summary claiming "2p for Z_p × Z_p" was correctly caught as a mis-summary (the truth p+1 is stronger) |

### (ii) Mechanism cards

**Card 1 — orbit-gadget decomposition ⇒ sharp stability for one hyperbola. SUPERSEDED IN-REPO.** The card
is mathematically correct (`|S ∩ P_O| ≤ 12 − j` from `eq:count` restricted to O gives `|S\M| ≤ d_O` and
`|M\S| = d_O + j ≤ 2d_O`; cross-orbit collinear triples = 0 at p = 11…23, reproduced), but it is not a
transfer and it is not new: the project proved it at note version **v1.12** (`prop:stability`) and has since
sharpened it. Its sharp constants are HJSW-box-only (in a general box the (0,0) and (1,1) orbits have 1296
and 144 maxima, so the per-orbit maximum is not unique). **P = 0** as a transfer.

**Card 2 — Segre's lemma of tangents → dual envelope → point count. Survives as a negative.** Verdict does
not depend on the fabricated 7/4 constant. Two obstructions, the second fatal on its own:
(a) an arc of size q+2−t has *exactly* t tangents through each of its points — a finiteness with no analogue
in the box, where a point of P lies on Θ(p) lines meeting P again, so `f_a` would have degree Θ(p) and every
point count is vacuous;
(b) Segre-type stability *concludes* "the near-maximal arc lies on a conic"; for us that is the **hypothesis**.
**P = 0.01.**

**Card 3 — Bose/Qvist counting through a point with a parity invariant. Near-negative, 0.02.** Mechanism
described correctly; the classical facts (q+1 lines through a ∈ S partition S∖{a} so |S| ≤ q+2; #tangents
through an external point ≡ |S| mod 2; for q even all tangents concur at the nucleus and adding it gives a
hyperoval, i.e. "construction + 1") are right. Its dismissal of a parity phenomenon used the k = −1-only
gain sequence 2, 4, 6, 5; with the correct all-k sequence 5, 5, 6, 5 the conclusion is unchanged. The only
live residue is H8's sub-idea (a scale L at which the Gaussian-step family through a point almost-partitions
the candidates) — and §6 shows that is now proved impossible.

**Card 4 — CRT / projection product bound (torus). Survives as a negative, with the corpus's cleanest
computation.** Sources exact; the narration of Steps 1–2 is muddled (the projection to Z₂² has 4 fibres, not
2; the right move is Lemma 2.2 with m = 2, n = p, giving τ ≤ 2(p+1)). The decisive datum, reproduced exactly:
torus-Z²_{2p} collinearity on the same 4(p−1) lifts gives **1080, 1584, 2880, 3672** triples and maximum
**12, 14, 18, 20 = p+1**, while box collinearity gives **26, 28, 40, 50** triples and maximum
**30, 36, 48, 54 = 3(p−1)**, at p = 11, 13, 17, 19. The torus constraint system is ≈ 40× denser and answers
the wrong question. Anything that only sees mod-2p collinearity proves the wrong theorem. **P = 0.01**, and
worth one line in the note about H6.

**Card 5 — exchange by blocking pairs / Hall transversal. Negative, and now superseded by the repo's own
H4(i).** All numbers reproduced to optimality: level 0 `max(|S₂| − |R|)` = 24, 25, 34, 38, 44, 53, 56 at
p = 11…31 with |R| = 16, 23, 30, 34, 44, 59, 64 and |S₂| = 4(p−1) always (53–71% of M₁ deleted); level 1
(adding rows and columns) = **exactly p−1** at p = 11…23, i.e. exactly the trivial 4(p−1), attained by
deleting all of M₁ and taking all of P₂; level 2 (the complete constraint system for S₁ ⊆ M₁) = 2, 3, 5 at
p = 11, 13, 17. **The framing must be corrected:** levels 0 and 1 are strict relaxations that drop every
triple with two points in S₂, so their weakness kills a *proof route*, not the statement. The corpus's
summary claim "H4's inequality is FALSE by Ω(p)" is a **category error** and must be withdrawn — the level-2
values 2, 3, 5 are exactly what H4 predicts. Also withdraw "B.13 suspected the slope-4-to-5 was an artefact
of moment counting; it is not": the exact optima give `|S₂|/|R|` = 2.5, 2.09, 2.13, 2.12, 2.0, 1.90, 1.875 at
p = 11…31, so the moment bound **was** lossy by ≈ 2×, exactly as B.13 suspected. **P = 0** (closed).

**Card 6 — redirected exchange: charge to triples with TWO points on H(−1). The corpus's only
forward-looking Q2 card. RE-RANKED DOWN, 0.12 → 0.08 → 0.03.** Its premise is verified (all of H4's content
sits in the 2-in-S₂ triples) and its diagnosis of why the literature's exchange devices fail is correct: the
**Dyson e-transform** `(A,B) ↦ (A ∪ (B+e), B ∩ (A−e))` needs a ground set closed under translation by e, and
the box is not — that is the precise failing step, and it is worth keeping verbatim. Four discounts:
(a) H4 is now closed negatively on three routes;
(b) the charging is a per-point argument, hence a nonnegative combination of local constraints, hence
bounded below by LP(all) ≈ 3.40(p−1) — the same ceiling as everything else in §8 group B;
(c) the O(1) evidence at level 2 is three primes, and level 2 *is* the original problem restricted to
S₁ ⊆ M₁ — the same wall, not a new one;
(d) the localisation to the (p−1)/4 half-row/half-column candidates Q₀ is a conjecture and its own decisive
experiment has never been run.

### (iii) Transfer against I1–I6

`I4` is what all of Cards 2–5 want and what the project already has in full (`prop:lines`, `lem:gadget`,
`lem:orbdec`). `I6` supplied every number. **Nothing in Q2 plugs into an interface the project does not
already saturate.** The honest statement is that the Q2 literature was searched thoroughly, the mechanisms
were read correctly, and none of them survives the box.

### (iv) The negative findings, which for Q2 are the whole content

**H4 is closed negatively on three routes, with numbers.**
- **(i) Blocking pairs give slope 1/2, not 1.** No q has F(q) = ∅ (mean 3.2–3.8 pairs per q), but the minimum
  vertex cover breaking all q at once is τ = 18, 22, 30, 34 at p = 11, 13, 17, 19 = **0.45–0.47 |H(−1)|**;
  one deletion unblocks two points on average, so the mechanism yields only `b ≤ ~2|D|` and hence no bound at
  all. Independently reproduced with an exact MILP: τ = 17, 23, 30, 34, 44, 59, 64 at p = 11…31, i.e.
  τ/|H(−1)| = 0.425 → 0.533, and `|H(−1)|/τ` = 2.35 → 1.88.
- **(ii) The reduction to a union of two rigid maxima FAILS, and the reason is the important one.** The exact
  maximum inside `M ∪ R(M)` is 30, 38, 52, 54 = 3(p−1) + O(1) at p = 11, 13, 17, 19, while α(P₋₁) = 32, 40,
  54, 59. H3 only bites near a ≈ 3(p−1); **the extremum of the pair sits in the MIDDLE**, a ≈ b ≈ 1.5(p−1),
  where both halves are far from maximal on their own hyperbola; there `t₁ + t₂ = 6(p−1) − |S|` is huge and
  the bound degenerates to 4.5(p−1). This is a **structural identity, not a numerical accident**: feeding
  `|E_i| ≤ t_i` into `|S| ≤ K + t₁ + t₂` with `t₁+t₂ = 6(p−1) − |S|` gives `|S| ≤ (K + 6(p−1))/2`, so
  `|S| ≤ 3(p−1)+C` requires `K ≤ 6C = O(1)` while `K ≥ |M| = 3(p−1)` trivially. The sharp form
  `|E_i| ≤ min(t_i, p−1−2s)` is *worse*: it gives `|S| ≤ K + 2(p−1−2s) ≈ 5(p−1)`, above trivial.
  **THIS IS THE CENTRAL FINDING FOR Q2:** the literature's stability+exchange mechanisms operate near a
  single structure's extremum, and this extremum is between two structures.
- **(iii) There is no local route at all.** Inside an orbit union `O ∪ R(O)` (32 points) the exact maximum is
  **16** — precisely the trivial "2 per row" bound — so summing over orbits returns exactly 4(p−1) and there
  is *no local competition between the hyperbolae whatsoever*. All the competition producing 3(p−1) instead
  of 4(p−1) is **global**, between different orbits through mixed three-point lines.

**H3 is LP-invisible, which retires the whole stability family as an input to a certificate.** Adding the
sharpest linear content of Lemma `orbopt` — per-orbit caps `Σ_{v∈O} x_v ≤ 12` (generic) and `≤ 6`
(exceptional) on **both** hyperbolae, plus the orbit-union caps ≤ 16 / ≤ 8 from H4(iii) — to LP(all) changes
the value by **exactly zero** at every prime 11 ≤ p ≤ 61, and **not one of the 6–32 cuts is even active**
(mean slack 3.4–5.1 out of a cap of 12; the fractional optimum puts only ≈ 7–8.5 points into a 16-point
orbit). The aggregate form is worse: the LP optimum splits 1.61–1.86 / 1.65–1.99 (p−1) between the two
hyperbolae at every prime up to 163, so `Σ_{H(±1)} x ≤ 3(p−1)` is slack by ≥ 1.196(p−1) — 53.2 at p = 43,
208.3 at p = 163, growing linearly. The derivation explains why: `prop:stability` is one rank-1 LP cut
(`Σ_q(1[m=0] + m(q))x_q ≤ Z + 2|L| = 3(p−1)`) whose every ingredient is already a constraint of the pair's
own LP. Worse for the programme's framing: **the one-hyperbola problem has integrality gap exactly zero**
(LP over all rich lines of H₁ = 3(p−1) = α at p = 11…31, residual 0.00e+00), so H3 is a theorem about the
part of the system where the phenomenon is provably absent.

**The Klein-reflection compression is dead, with numbers.** `R(x,y) = (p−x, y)` is an affine involution of
the box mapping H(1)-lifts bijectively onto H(−1)-lifts, and `α = |Ψ(S)| + ω(S)` with
`Ψ(S) = (S∩H₁) ∪ R(S∩H₂)`, `ω(S) = |S₁ ∩ R(S₂)|`. Measured: `max|Ψ(S)|` = 32, 40, 52, 57 at p = 11…19
(excess over 3(p−1): 2, 4, 4, 3 — **bounded**), but `max ω(S)` = 16, 19, 26, 29, 33 at p = 11…23 =
**1.50–1.63 (p−1) = Θ(p)**. So the fold loses a linear number of points and the decomposition yields no
bound. This is the natural reading of H4's "shifting/compression" pointer and of the Klein symmetry. Related:
no maximum is R-symmetric for p ≥ 13 (`max{2|A| : A ∪ R(A) lawful}` = 32, 38, 52, 58, 66 at p = 11…23
against α = 32, 40, 54, 59, ≥ 70), so no averaging or fixed-point argument over R is available. At p = 11 it
*does* reach α, and the reason is visible: the pair has exactly **39** maxima there (odd), forcing an
R-fixed one.

**The multiplicity objection is WRONG in both directions and must be withdrawn.** The old adversarial claim
"unlike Segre's unique conic, we have exponentially many extremals" is refuted by Lemma `orbopt` (generic
orbits are rigid with a unique maximum; 9^s counts only the exceptional ones). The *replacement* objection at
the working density also fails, and was tested: H₁'s lawful-set lattice is a direct product of (p−1−2s)/2
copies of an 8-point gadget with generating polynomial [1,8,28,50,43,14,1,0,0], 2s three-point lines
[1,3,3,0] and 2s free points [1,1], so the number of lawful S₁ of size 1.5(p−1) is 2^33, 2^40, 2^54, 2^61,
2^75, 2^97, 2^104 at p = 11…31 (≈ 3.5 bits per class) — yet the radius **forced by counting** is only
d = 1, 1, 1, 3, 3, 3, 5 while the *true* sharp radius is `min(t, p−1−2s)` = 8, 8, 12, 16, 20, 24, 28.
Counting forces nothing; the existing lemma is far stronger than any multiplicity obstruction and is still
useless. **Any card resting on "uniqueness of extremals" as the discriminator must be re-scored on something
else** (§7 says what).

**B.12(iv) / the "spanned directions" identity is provably vacuous, not merely unavailable.** Lawfulness
gives `C(|S|,2) = Σ_ℓ C(|S∩ℓ|,2) ≤ #{lines with ≥2 points of P₋₁} = C(8(p−1),2) − Σ_{n_ℓ≥3}(C(n_ℓ,2)−1)`, and
the subtracted term is O(p log p) (measured total collinear triples 704, 3948, 13708, 32936 at
p = 11, 41, 101, 199, i.e. ≈ 29 p log p) against `C(8(p−1),2) ≈ 32p²`. The bound is `|S| ≤ 8(p−1) − O(log p)`.
Nothing can be repaired here.

**Two structural facts worth keeping.** The exact defect identity on the pair:
`|S| = 6(p−1) − Δ(S₁) − Δ(S₂)` with `Δ` the `eq:count` defect (verified: 23+5 = 28 = 60−32 at p = 11;
30+2 = 32 = 72−40 at p = 13), with the line-deficiency term carrying 22/23 and 22/30 of the defect. And the
occupancy profile at an exact optimum: `{5:2, 6:1, 8:2}` at p = 11 and `{6:4, 8:2}` at p = 13 — almost all
16-point quads sit at exactly the target 6 and the entire gain is carried by 2 saturated quads. Saturating
many quads is possible but never profitable (`max #saturated` = 3/5, 4/6, 6/8 at p = 11, 13, 17 with |S| =
24, 36, 49 = 3(p−1) − 6, 3(p−1), 3(p−1) + 1 against α = 32, 40, 54).

---

## 3. Q3 [H5] — character / mixed sums over 2-D sets below the Burgess range

### (i) Sources

Every source verified; **no fabrications in this question at all** — the cleanest bibliographic record in the
corpus.

| Source | Statement | Status |
|---|---|---|
| Chang, "Burgess inequality in F_{p²}", GAFA **19** (2009) 1001–1016, **Theorem 11** | for χ nontrivial mod p, `x²+axy+by²` not a perfect square mod p, and intervals I, J with \|I\|,\|J\| > p^{1/4+ε}: `\|Σ_{x∈I,y∈J} χ(x²+axy+by²)\| < p^{−δ}\|I\|\|J\|` with δ = δ(ε) > 0 **independent of the form** | **CONFIRMED** verbatim (appears twice in the PDF). Attributions in her intro also confirmed: p^{1/3+ε} Burgess [B3] = JLMS **43** (1968) 271–274; ρ_n = n/(2(n+1)) Davenport–Lewis (1963); p^{2/5+ε} Chang |
| — applied to x²+y² | disc = −4 is never a perfect square mod an odd p, so the hypothesis holds for **every odd p**; Chang's proof splits into Case 1 (irreducible, p ≡ 3 mod 4) and Case 2 (reducible, distinct roots, p ≡ 1 mod 4), so **both residue classes are covered by one theorem** | **CONFIRMED** |
| Chu, arXiv:2501.12325 = J. Lond. Math. Soc. (2) **112** (2025) e70351 | Thm 1.5 (1 ≤ k < 2n, F split into linear forms, full-rank coefficient matrix, `H_min ≤ p^{1/2}`, bound `‖H‖H_min^{−(2n−k′)/r} p^{k(r+2n−k′)/(4r²)+ε}`); Cor 1.6 (n ≤ k); Cor 1.7 (k ≤ n: p^{1/4+κ}); Thm 1.3 (energy ≪ H^{2n}p^ε); saving δ ≈ 4κ²/(1+√(1+2κ))² "independent of n" | **CONFIRMED**, every exponent |
| Konyagin, Mat. Zametki **88**(4) (2010) 529–542 / Math. Notes **88** (2010) 503–515 | Burgess threshold p^{1/4+ε} for boxes in F_{p^n} for **all n**, uniformly in the basis, with an **n-independent** saving p^{−ε²/2} | **CONFIRMED** at near-primary level: Gabdullin, arXiv:1806.04783, states it as "Theorem C ([Kon])" with the saving exponent ε²/2 |
| Pierce–Xu, Algebra & Number Theory **14** (2020) 1911–1951, arXiv:1907.03108 | Condition 1.1 ((Δ,q)-admissible); Thm 1.1 with Θ = ⌊(r−1)/(n−1)⌋; Cor 1.2; Cor 1.3 with `β_n = 1/2 − 1/(2(n+1))`, saving δ_n ≈ (n+1)²κ²/(4(n−1)), nonempty as soon as r ≥ 2n−1; global form `‖H‖H_min ≫ q^{n/2+κ}` | **CONFIRMED** verbatim; the global form's extra hypothesis `H_min ≥ ‖H‖^{c₀/n}` was omitted by the card |
| Alsetri–Shao, arXiv:2509.07765 = Bull. LMS **58** (2026), doi 10.1112/blms.70293, **Thm 1.1** | for a proper **rank-2 GAP** A ⊂ F_p with \|A\| ≥ p^{1/4+ε}: `\|Σ_{n∈A} χ(n)\| ≪_ε p^{−δ}\|A\|` — the exponent is on the **cardinality** \|A\| = H₁H₂ | **CONFIRMED**; issue number "no. 4" is **UNVERIFIED** (two searches say issue 2; Wiley 403s). Co-author Xuancheng Shao was missing from `holes.py` |
| Bourgain–Chang, C. R. Math. Acad. Sci. Paris **348** (2010) 115–120 | nontrivial estimate for `Σ_{x∈∏[a_i,a_i+H]} χ(∏_j L_j(x))` for **n forms in n variables, linearly independent over F_p**, all side lengths H > p^{1/4+ε} | **CONFIRMED** (upgraded to primary via Numdam) |
| Heath-Brown–Pierce, arXiv:1404.1677 = JLMS, doi 10.1112/jlms/jdv009, **Thm 1.2** | D := d(d+1)/2; for H < q^{1/2+1/(4r)}: `Σ e(f(n))χ(n) ≪_{r,d} H^{1−1/r}q^{(r+1+D)/(4r²)}(log q)²`; δ ≈ κ²/(D+1) at H = q^{1/4+κ}; and Chang's earlier δ = κ²/(4((d+1)²+2)(1+2κ)) | **CONFIRMED** verbatim |
| Shparlinski, "Modular hyperbolas", Japan. J. Math. **7** (2012) 235–294, arXiv:1103.2879, §4.4 / Thm 13 | asymptotic only for Z ≥ p^{3/4+ε}; nontrivial upper bound for Z ≥ p^{1/2+ε}; "These results seem to be the limit of what can be achieved within the standard exponential sum techniques and currently available estimates on incomplete Kloosterman sums" | **CONFIRMED** in substance; the card quotes the sentence with two word substitutions ("appear"/"seem", "within standard"/"within the standard") — quote exactly or drop the quotation marks |
| Bourgain–Garaev, Izv. Math. **78**:4 (2014) 656–707, arXiv:1211.4184; Bourgain, GAFA **18** (2009) 1477–1502 | multilinear Kloosterman under an entropy condition | **UNVERIFIABLE**: bibliographic data correct, **theorem statements never obtained**; the abstract is uninformative about hypotheses |

### (ii) Mechanism cards

**MC1 — Chang Thm 11 as the QR-density input for Conjecture A. A citation, not a transfer.**
As a *citation* it is essentially certain (P ≈ 0.90): the theorem is verbatim, the hypothesis holds for
every odd p in both residue classes. Two caveats to record: the annulus decomposition {σ ≍ S} and the
coprimality restriction each cost an extra p^ε (Möbius tail `Σ_{d>D} S²/d²` with `D = S/p^{1/4+ε}`), so the
usable threshold is **p^{1/4+2ε}**, not p^{1/4+ε}; and no published version of the disc/weighted form exists
(routine but unpublished). As a *transfer that advances the certificate*: **P = 0.02** (down from the
corpus's 0.05, because the model's ceiling is 4(p−1), §1 MC3).

**MC2 — conic reparametrisation "the circulant symbol IS a Burgess-shaped sum". KILLED as a mechanism;
the algebra survives as a fact.** With `t = (r−s₁)/s₂` on `r² = s₁²+s₂²`:
`μ_F = −(σ+r)²/(2s₁s₂) = −(σ+r)/(σ−r) = (t+1)/(t(t−1))` and `μ′_F = (s₂−s₁+r)²/(2s₁s₂) = −t(t+1)/(t−1)`.
This is **verified symbolically and exhaustively** (p ∈ {11..1009}, 1 ≤ s₁,s₂ < 40, both roots — 16728 cases,
0 failures), and should be preserved in the notes. But the card's identification of "exactly which literature
mechanism would close it" rests on **two misread sources**:
(a) Bourgain–Chang needs n forms in n **variables**, linearly independent over F_p; three affine forms
`t+1, t, t−1` in *one* variable is a degenerate system whose n = 1 case is plain Burgess. Chu's Thm 1.5
likewise needs 1 ≤ k < 2n, so n = 1 admits only k = 1.
(b) Alsetri–Shao bound `Σ_{n∈A} χ(n)` — the character of the **identity** on a GAP, unweighted. It does not
bound `Σ_{t∈A} w_t ψ(f(t))` for a rational f. So even in the counterfactual world where the half-angle set
were a proper rank-2 GAP, their theorem would not apply.
The one-variable statement actually needed — Burgess for `χ(f(t))` with f a ratio of products of distinct
linear factors, over an interval — is plausible but **could not be located in any of the eight sources**.
Mark it unverified. One labelling error to fix before any re-computation: the card calls μ′ "the mixed
multiplier", but §23 assigns **both** μ and μ′ to the same-type slots. **P = 0.03.**

**MC3 — Pierce–Xu for the 4-D product form. KILLED as a mechanism, kept as the answer to a brief bullet.**
The admissibility check was re-done independently and is correct: `F = N(z₁)N(z₂)N(z₁+z₂)` has six linear
factors with coefficient vectors (1,±i,0,0), (0,0,1,±i), (1,±i,1,±i), pairwise non-proportional for odd p,
so F is squarefree, g = 1, h = F is Δ-th-power-free for all Δ ≥ 2, and the first four rows already span
F̄_p⁴ — so no A ∈ GL₄ makes h independent of a variable. Pierce–Xu Cor 1.2 with n = 4 gives **p^{2/5+κ}**,
two full regimes above p^{1/4}. Chu's Cor 1.6 is **vacuous** here (k = 6 > n = 4 forces exponent
6/8 = 3/4 > 1/2, contradicting `H_min ≤ p^{1/2}`). One arithmetic slip to fix: Chu's improvement range is
`n ≤ k < 4n²/(3n+1)` = 64/13 ≈ 4.92 at n = 4, so Chu improves on Pierce–Xu at **k = 4 only**, not k ≤ 5
(the card conflated it with the neighbouring range 4n/3). **So the brief's "4-D product form — anything at
all?" has a definite answer: nothing below p^{2/5}.** **P = 0.05** → as a transfer, 0.02.

**MC4 — aggregate the per-family Kloosterman count into a ternary congruence; multilinear Kloosterman.
Survives ONLY as the cheap numerical experiment; its literature half is entirely unverified.**
Its Step-3 arithmetic is correct and was re-checked: naive completion with Deligne's Kl₃ needs
`L²|M| ≫ p² log³p`, i.e. σ ≪ 4/log³p, which fails for every σ ≥ 1; and the intermediate route (incomplete
Kloosterman per family, then sum over the ≍σ families) reproduces the identical σ ≪ p^{1/4}/log p wall. So
any gain must come from genuine cancellation in the third variable — precisely the unverified part.
**The adversarial kill (FATAL):** the family presence bit is not removable by any re-parametrisation.
Presence is `[s₁²+s₂² ≡ □] = χ(N(s₁+is₂))`; for p ≡ 3 mod 4 that is literally "z is a square in F_{p²}"
(N(z) = z^{p+1}), and for p ≡ 1 mod 4 it splits as `χ(s₁+is₂)χ(s₁−is₂)`. Hence (a) you cannot let the
multiplier run over an interval, because dropping presence gives an *upper* bound on a superset while the
model theorem needs a *lower* bound on E; (b) expanding presence as (1+χ)/2 leaves the weighted family
character sum, which is B.18 Addendum 2's barrier verbatim; (c) as a 5-variable point count the completion
error is √(p³) = p^{1.5} per character against a main term ≍ 16p per dyadic scale — worse by p^{1/2}.
Measured: `W(S) = Σ_{s₁,s₂≤S} χ(s₁²+s₂²)/(s₁+s₂)²` has `|W|/‖w‖₁` = 0.39, 0.041, 0.242, 0.200 at
S = p^{1/4} for p = 1009, 10007, 100003, 10⁶, and `|W|/‖w‖₂` = 1.4–2.1 at every p and scale — exactly the
random level and no lower, reproducing B.18 Add. 2's `max_ψ|S|/Σw` = 0.65, 0.49, 0.48, 0.52, 0.54. Since
`‖w‖₂/‖w‖₁ ≍ 1/log S`, even a perfect "random level" theorem buys only 1/log p — precisely the log p growth
of E and not one factor more. **P = 0.20 → 0.08 → 0.03.**

**MC5 — Burgess over structured sets (rank-2 GAPs, small doubling, Bohr sets): a verified NO.**
The verdict is right and is the most durable deliverable in Q3, but **the numbers must be replaced.** The
card's doubling measurements (12.4 / 31.5 / 16.5 at p = 10007 and 32.2 / 128.9 / 130.8 at p = 100003, against
"benchmarks" 24 / 70 / 16.5 and 64 / 296 / 143) **do not reproduce**: its script subsampled 700 elements when
|T| > 700 and benchmarked against a formula `min(p,n²)/n` rather than a simulation. Exact, unsampled
recomputation against a *matched simulated random subset*: p = 10007, S = p^{0.25}: |T| = 64, add 29.5 vs
random 29.6, mul 29.6 vs 29.7; S = p^{0.33}: |T| = 202, 43.2 vs 43.3; S = p^{0.45}: |T| = 1766, 5.7 vs 5.7
(both saturated at ≈ p/|T|); p = 100003, S = p^{0.25}: |T| = 136, **65.5 vs 65.4**; S = p^{0.33}: |T| = 976,
101.6 vs 101.7. So the half-angle set sits at **exactly** the random level, with no "factor of 2 from the ±
pairing" — that was a measurement artefact and the explanation should be deleted. **The conclusion is
strengthened, not weakened:** a proper rank-2 GAP of any size has doubling ≈ 4 independent of size, and we
measure 65.5 at |T| = 136 — identical to random to within 0.2%. **P = 0.02.**

### (iii) Transfer against I1–I6, and the union-bound reframing

**The p^{1/4} threshold is primarily a UNION-BOUND threshold, and it is the same number as Burgess's floor
for an unrelated reason.** At scale S the system carries ≍ S² families; every Weil-level fact about one
object costs error √p·log^c p; the main term per dyadic scale is ≍ p. Error < main ⟺ S²√p ≪ p ⟺
**S ≪ p^{1/4}**. Burgess's own floor for prime moduli is also p^{1/4}, unimproved since 1962 and verified
across every setting checked here. So per-object rigour (`I1`, `I3`) and cross-object cancellation (H5) live
on **complementary, abutting, never-overlapping** ranges. Measured at p = 100003 (p^{1/4} = 17.8):
at σ = 17, L = 11765, the actual direction count is 33154 against the Kloosterman main term 33218.7 (ratio
0.998) — while (Weil error √p·log²p)/(per-family main 4L²/p) = **7.57**; at σ = 35 the ratio is 1.033 with
error/main 32.1; at σ = 142, ratio 1.074 with error/main **528.6**. The count is true and unprovable at
exactly the scale where half the mass sits: the fraction of the B.15(b) model mass at σ ≥ p^{1/4} is 0.43,
0.71, 0.37, 0.50, 0.61, 0.59 at p = 199, 997, 4001, 10007, 100003, 10⁶ (mean ≈ 0.53).

**N1 (the decisive negative) is confirmed and survives its most natural rescue.** Chang gives QR-density
½+o(1) only for σ ≥ p^{1/4+ε}; the per-family box count `N_box ≍ c₀p/σ²` is a Kloosterman count in a box of
side L = 2p/σ, rigorous only when L ≫ p^{3/4}log p, i.e. σ ≪ p^{1/4}/log p. The two windows abut at p^{1/4}
without meeting. Aggregating before completing does not help (main ≍ p, error ≍ σ²√p log²p — the identical
threshold, reached a second, independent way). The rescue that was tested and fails: Shparlinski §3.2
Theorem 16 (`Σ_{a=1}^m |#H_{a,m}(X,Y) − φ(m)XY/m²|² ≪ X(X+Y)m^{o(1)}`) plus Cauchy–Schwarz onto the ≍σ
present families gives `Σ_{a∈M}|error| ≪ L√(2σ)p^{o(1)}` against an aggregate main term σL²/p, ratio
`√2·√σ/2 > 1` for every σ ≳ 2.

**`I2` is mis-advertised, and the mis-advertisement points at where the project is stuck.** Lemma FE's
averaging variable is u (the fibre coordinate); its "independent coins" are the Legendre symbols
`χ(Δ_{σ,m}(u))` of six quadratics **in u** with the family FIXED, and the proof works because those six are
pairwise coprime squarefree polynomials in u. The single most important quadratic condition in the project —
`[s₁²+s₂² ≡ □]`, which switches families on and off — is **constant in u**, so I2 is silent on it by
construction. Worse, the presence bits are provably *not* independent coins: `χ∘N` is completely
multiplicative on Z[i], so `χ(N(z₁z₂)) = χ(N(z₁))χ(N(z₂))` is an exact relation. That is not a defect to be
fixed; it is the only unconditional structure the project has (B.17's "NR·NR = QR"), and the gap between
log log p (what multiplicativity gives) and log p (what equidistribution would give) is exactly the gap
between having I2 and having sub-Burgess cancellation. **`holes.py` I2 must be reworded.**

### (iv) Negative findings, and two reverse findings that are the most valuable output of this question

**N3 — `holes.py` H5's stated reason is wrong.** "Known multi-dimensional Burgess bounds degrade with
dimension" is false for **boxes**: Konyagin's threshold is p^{1/4+ε} in every dimension with an
n-independent saving p^{−ε²/2} (only the implied constant depends on n). The `β_n = 1/2 − 1/(2(n+1))`
degradation belongs to characters **at general forms** (Davenport–Lewis, Gillett, Pierce–Xu), a different
object. **The wall is SCALE, not dimension.** As written, H5 commissions searches for higher-dimensional
Burgess bounds, which exist, are available, and do not help. Independently, the trace method's dimension is
not binding either: `model_theorem_conditional.md` step 5 grants `tr C^{2k}` control for k ≤ p^{δ/3−ε}, and
p^{δ/3} ≫ log p for every fixed δ > 0. **The assignment's own framing ("is the trace method's dimension
~log p fatal?") should be retired.**

**N5 — §21(2)'s "p^{1/8+ε}" is not attainable and has been sitting in the notes as an unfillable citation
request.** p^{1/4} is a hard floor for prime moduli. Every threshold checked in this pass lands on p^{1/4+ε}:
Burgess 1962 (intervals), Chang Thms 5 and 11, Konyagin (F_{p^n} boxes, all n), Bourgain–Chang (products of
independent linear forms), Chu Cor 1.7 (k ≤ n), Alsetri–Shao (rank-2 GAPs, on the cardinality),
Heath-Brown–Pierce (mixed sums). Measured: at S = p^{1/8} the sum has n = p^{1/4} terms and its size is
≍ √n = p^{1/8} (|T|/√n = 0.29–1.93 across p = 1009…10⁶ and S/p^{1/4} = 0.22…4 — square-root cancellation at
every scale, including well below p^{1/4}), while the best proven bound there is the trivial n. Replace the
sentence with "p^{1/4+ε}, and this is a hard floor".

**N6 — no scale works for arbitrary positional weights.** With `w = χ̄∘N` the summand is |χ(N(z))|² = 1
wherever p ∤ N(z), so `|Σ_{|z|≤L} χ(N(z))w(z)| ≍ L²` at every L. The brief's Q3 must be posed with a
**bounded-variation** constraint on w.

**Alignment task (three places in the notes disagree with each other).** B.15(d) says "nontrivial from side
p^{1/3+ε}" and separately worries about the split case; §21(2) says p^{1/8+ε}; §23 restricts to p ≡ 3 mod 4.
All three should read **p^{1/4+2ε}, uniformly in p mod 4**, citing Chang Thm 11. Three inconsistent numbers
in a document shipped to external researchers is exactly how a wrong search gets commissioned.

**REVERSE FINDING 1 — Conjecture A is not a Burgess statement. This is the highest-value item in the corpus
and it should change `model_theorem_conditional.md`.** §21 itself says the model theorem needs `E/(p−1)`
above an **absolute constant** (≈ 9; §23's own `λ_min/√m₂` = −1.94…−2.08 and `m₂/(E/(p−1))` = 1.24–1.35 give
≈ 5.84), **not** `E/(p−1) → ∞`. A constant threshold is carried entirely by families at **bounded σ**, and
those are (a) a fixed finite list whose presence bits are Legendre symbols of a fixed finite list of integers
N = s₁²+s₂², and (b) at scales σ ≪ p^{1/4}, so every one of their Kloosterman box counts is **rigorous**.
Since χ_p is multiplicative, the whole presence pattern is a point of F₂^m for the m primes dividing some N
to an odd power; every prime realises *some* pattern, so `min over p ≥ min over all 2^m patterns` — a finite,
exactly computable quantity, evaluated by Walsh–Hadamard (c₀ = 24.4 calibrated from the repo's own measured
`E/(p−1)` = 17.2, 17.2, 20.0, 26.6, 28.1 at p = 199…4001):

| σ₀ | families | generators m | min over 2^m patterns of c₀·mass |
|---|---|---|---|
| 16 | 40 | 18 | 8.74 |
| 18 | 51 | 22 | **9.37** |
| 20 | 64 | 26 | 10.11 |

monotone non-decreasing in σ₀ (a pattern restriction), with the empirical worst case over 1000+ primes in
[200, 8000] agreeing (10.88 at σ₀ = 20, attained at p = 1877; minimum presence fraction 0.25, never near
zero because multiplicativity forces it — the 51 families at σ₀ = 18 span an F₂-space of dimension only 22).
Only family (3,4) with N = 25 is unconditionally present (the Pythagorean c₁ ≈ 0.1 of §21's correction); the
other ≈ 9.3 comes from the multiplicative structure. **STATUS: one agent's unreplicated computation.** Two
constants must be pinned to convert it into a theorem: (1) the explicit c₀ in `N_box ≥ c₀p/σ²` from the
Kloosterman count with lift multiplicity (1–4) and sub-triple multiplicity (≤ 4) written out — B.15(b)/§21
assert the shape but never fix c₀; (2) the threshold K in `λ_min ≥ −K√m₂` and the ratio
`m₂/(E/(p−1)) ≤ 1.35` as proved inequalities rather than measurements (the latter is essentially proved in
§21(3) via codegree ≤ 384). **P(the finite check survives independent replication and both constants can be
pinned) ≈ 0.5. P(this yields an unconditional model theorem) ≈ 0.25. P(it beats 3.4482) = 0**, because the
model theorem's own payoff is 4(p−1) − c·p/log p. That last line is the honest and uncomfortable point: the
project's hardest analytic obstacle guards a target that a proved combinatorial result already dominates.

**REVERSE FINDING 2 — §26a's window law for w ≥ 2 is provable, by the argument the project already owns.**
The window curve is the fibre product over the x-line of w copies of `b² − (x − 1/x)b − k = 0` translated by
`x_j = k^j x`. Its j-th discriminant is `Δ_j(x) = (k^j x − k^{−j}/x)² + 4k`, and
`x²Δ_j = k^{−2j}Q(k^j x)` with `Q(y) = y⁴ + (4k−2)y² + 1`; §27 already proves Q has four distinct nonzero
roots {±α, ±1/α} for k ∉ {0,1}. So the branch locus of the j-th extension is `R_j = k^{−j}·{±α, ±1/α}`, and
`R_i ∩ R_j ≠ ∅ ⟺ k^{j−i} ∈ {±1, ±α^{±2}}`. Pairwise-disjoint branch loci ⇒ every non-empty subproduct
`∏_{j∈S}Δ_j` has a simple root ⇒ non-square in F̄_p(x) ⇒ Galois group (Z/2)^w ⇒ absolutely irreducible ⇒
Bombieri–Perel'muter with error `O_w(√p·log^w p)`. Exactly the structure of `lemma_run.tex`, with branch loci
`k^{−j}·{±α,±1/α}` in place of {0,−1,…,−(k−1)}. Measured smallest resonance m (largest automatically-safe
window length): for k a primitive root, m = 50, 75, 99, 125, 200, > 200, 61 at p = 101, 151, 199, 251, 401,
601, 997 and > 200 at p = 2003, 5003, 10007 — i.e. ord(k)/2 or larger, vastly beyond any fixed w. Explicit
exceptional k: k = −1 (the degenerate short-cycle case §26a already separates), k = −1/3, and the roots of
`5k² − 2k + 1`. **HONEST SCOPE: this closes only the arithmetic half of Theorem C.** §26's SELECTION LEMMA
(find S with `2·changes(S) − 6|S| ≥ c·G₈`) is combinatorial and untouched. The correction moves Theorem C
from "blocked on two things, one of them analytic" to "blocked on one, and it is not analytic" — a
reclassification worth making, because the project has been treating the analytic half as the harder one.
**P(the lemma goes through as sketched) ≈ 0.7.**

**One effectivity caveat on the block certificate, so nobody quotes it at computable p.** The error in
Lemma `run` is `O_k(√p·log^k p)` with the implied constant governed by the genus `1 + 2^{k−2}(k−3)`, i.e.
≍ 2^k·k·√p·log^k p, against a main term p/2^{k+2}. Rigour needs `4^k·k·log^k p ≪ √p`, i.e.
`k·(2 + log₂log p) ≲ ½log₂ p` — which already fails at k = 2 for p = 10⁶. Measured maximal run of
consecutive quadratic residues: 21, 14, 17, 19 at p = 1009, 10007, 100003, 10⁶ (≈ 1.4 log p), so real runs
comfortably exceed the quantitatively verifiable range and the certificate relies on the (legitimate) tail
bound there. `Corollary cor:rundensity` is asymptotic in p **for each fixed K**, and the K → ∞ limit 3.4413
requires K after p, not with it. This should be stated in the note.

---

## 4. Q4 [H6] — polynomial method with inequalities (algebra + box)

### (i) Sources

| Source | Statement | Status |
|---|---|---|
| Bombieri–Pila, Duke Math. J. **59** (1989) 337–357 | `c(d,ε)N^{1/d+ε}` lattice points on an arc of an irreducible degree-d curve in a square of side N; **Lemma 1** (rank criterion: `rank(P_i^j)_{j∈J_d} < D`, D = (d+1)(d+2)/2); the norm `‖f‖_{N,k}`; f(x) = x^d shows 1/d is best possible | **CONFIRMED** verbatim |
| Bloom–Lichtman, Essential Number Theory **4**(2) (2025) **327–348** | Theorem 1 (attributed to Bombieri–Pila and Pila); the paper's declared scope excluding "the p-adic determinant method of Heath-Brown [14] and a global version of Salberger [**24**]"; the slicing bound `X^A_{n,d}(N) ≪ N^{n−2+1/d+o(1)}` (which is **Pila's**, not theirs) | **PARTIALLY CORRECT**: page range and the bracket number were both wrong in the card |
| Heath-Brown, Annals **155** (2002) **553–598** (with an appendix by Colliot-Thélène) | **Theorem 14** verbatim, incl. `k ≪_ε (V^d/T)^{d^{−(n−1)/(n−2)}}V^ε(log‖F‖)^{2n−3}`, the two numbered properties, and "Theorem 14 is in fact the fundamental result in this paper"; **Lemma 5** verbatim; the grouping `S(t) = {x : x ≡ ρt (mod p)}`; column operations forcing p^f divisibility | **CONFIRMED** verbatim (ORA full text). Page range was **553–595** in the card — wrong |
| — critical caveat | the divisibility in Heath-Brown's method comes from the points being congruent **to each other** mod p; our candidates are pairwise incongruent | **CONFIRMED** as a correct reading, and it is what kills the pedigree of M1 |
| Cilleruelo–Garaev, GAFA **21** (2011) 892–904, arXiv:1007.1526 | **Thm 1** `I₂(M;K,L) < M^{4/3+o(1)}/p^{1/3} + M^{o(1)}` (K=L: `M^{3/2+o(1)}/p^{1/2} + M^{o(1)}`), so M < p^{1/4} gives M^{o(1)}; **Thm 2** M ≪ p^{1/8} ⇒ I₃ ≪ M^{o(1)}; **Lemma 1** (for m ≥ √n, [m, m+n^{1/6}] contains at most two divisors of n); the pigeonhole `(tx+u₀)(ty+v₀) = n_z` with `\|z\| < T²M²/p + 2M/T + 1/2`; "Using the idea of Heath-Brown from [6]"; **Problem 1** asks to improve 1/4 | **CONFIRMED** verbatim. Two nits: the proof's case split is M < p^{1/4}/4, and the standing hypothesis 1 ≤ M ≤ p means the full 2p-box application is formally out of range (split into four boxes of side p) |
| Shparlinski, "Modular hyperbolas" survey | **the strongest verified item in Q4**: a full-text search of the 3890 extracted lines gives **ZERO** hits for "collinear", "general position", "no three", "determinant method", "Hjelmslev"; the three "Heath-Brown" hits are unrelated bibliography entries | **CONFIRMED** |
| **MISSED SOURCE, now added**: Chang–Cilleruelo–Garaev–Hernández–Shparlinski–Zumalacárregui, "Points on curves in small boxes and applications", Michigan Math. J. **63** (2014) 503–534, arXiv:1111.1543 | the direct generalisation of Cilleruelo–Garaev from `xy ≡ λ` to `f(x) ≡ y` and `f(x) ≡ y²` in an arbitrary square; Thm 1 for deg f = 3: `I_f(M;R,S) < M^{1/3+o(1)} + M^{5/3+o(1)}/p^{1/6}` | **CONFIRMED**; full-text search of 2508 lines: **zero** hits for "collinear", "general position", "no three". This is the most on-point paper for "algebra + box mod p" and it **confirms** the negative |
| Blokhuis–Ball, "Polynomials in Finite Geometry" (Braunschweig, 23 May 1999) | **Thm 3.1** (directions: N = 1, or N ≥ (q+3)/2, or `2+(q−1)/(p^e+1) ≤ N ≤ (q−1)/(p^e−1)`), for a set R of **exactly q** points in AG(2,q); **Thm 5.5** (blocking set of size < 3(q+1)/2 meets every line in 1 mod p points); the Rédei polynomial `H_m(W) = ∏(am − b + W)` **equals** W^q − W when m is not determined | **CONFIRMED** verbatim (the card said "divides"; equality is what the notes state) |
| Ball–Lavrauw, arXiv:1705.10940v4 | Thm 1 with condition (1); Lemma 10; the tangent count at a point of a k-arc is **q+2−k** | **CONFIRMED**; the card's hypotheses field said q+1−\|A\|, contradicting its own body |
| Kiermaier–Koch–Kurz, Adv. Math. Commun. **5** (2011) 287–301, arXiv:1401.4340 | **Thm 1.1** "The maximum size of a 2-arc in PHG(2, Z_25) is 21. The (21,2)-arc is unique up to isomorphism."; the four-case state of the art for chain rings of length 2 (q odd Galois "currently is the least satisfactory one", `((q+1)/2)² ≤ m₂ ≤ q²`); the 775-point search-space quote; **zero occurrences of "length 3"** | **CONFIRMED** verbatim |
| Boev–Landjev (**not** Landjev–Boev), Discrete Math. **310** (2010) 2061–2068 | Rédei-type blocking sets in projective Hjelmslev planes: **constructions only**, at nilpotency index 2 | **CONFIRMED**; closes the card's open uncertainty **in its favour** |
| Ghosal–Goenka–Grebennikov–Keevash–Kwan–Pham, arXiv:2607.05255 (6 Jul 2026); Grebennikov–Kwan, arXiv:2510.17743 | max = exactly kn for k ≥ 3 and large n; heavy-line statistics + Ehard–Glock–Joos pseudorandom hypergraph matchings + deletion + randomised switching (Simkin, Luria); the earlier n ≥ k ≥ 10³⁷ result | **CONFIRMED at primary level** (the card labelled it verified-secondary). **No algebraic method anywhere** |
| Nagy–Nagy–Woodroofe, European J. Combin. **114** (2023) 103796, arXiv:2209.01447 | **Thm 1.3** `\|S ∩ [1,n]²\| = Θ(n / log^{1+ε} n)` for an extensible general-position set; Construction 2.4 uses translated modular parabolas `y = (x−a_n)² + b_n (mod p_n)` and **deletes** one point of each collinear triple; Lemma 3.6 | **CONFIRMED** verbatim |
| Alon, Combin. Probab. Comput. **8** (1999) 7–29; Ball–Serra, Combinatorica **29** (2009) 511–522 | Combinatorial Nullstellensatz coefficient form; punctured version | **CONFIRMED**; note the published **Erratum**, Combinatorica, doi 10.1007/s00493-011-2837-7 — anyone building on the punctured version must check it |

### (ii) Mechanism cards

**M1 — "determinant method at s = 3". Survives as MATHEMATICS with its pedigree struck.**
Inputs: the box of diameter 2p. Step: for three box points, `|Δ| ≤ 4p² < p³`, so `Δ ≡ 0 (mod p³) ⟺ Δ = 0`;
and a Z-line through box points is primitive hence unimodular mod p³, so Z-collinear ⟺ the three images lie
on a common line of AHG(2, Z/p³). Output: `α(P₋₁)` = the maximum 2-arc of AHG(2, Z/p³) inside the image of V.
**Verified**, including the necessity of the box hypothesis: in the *full* grid (Z/27)² the triple
(0,0), (9,0), (0,3) has Δ = 27 ≡ 0 but lies on **no** unimodular Hjelmslev line (0 such lines by brute force),
so the earlier repo warning in `deep_research_2_2026-08-18.md` is refined, not contradicted. **But nothing of
either cited method is used**: Heath-Brown's divisibility comes from points congruent to each other mod p
(ours are pairwise incongruent) and Bombieri–Pila's Lemma 1 is a rank criterion for a degree-d curve through
many points. What is actually used is "an integer of absolute value < p³ divisible by p³ is zero". **Relabel
as "Archimedean size argument: the box costs exactly one p-adic level"**, and record that mod p² is *not*
enough (`#{Δ ≡ 0 mod p²}` is ≈ 1.6× larger: 1264/704 at p = 11, 1932/988 at p = 17, 3080/1744 at p = 23,
4612/2888 at p = 29, 6276/3948 at p = 41, 7312/4560 at p = 47; the ratio is 1.55–1.65 only from p ≥ 29).
The difficulty is conserved; the deliverable is a tautological restatement. **P = 0.05 → 0.03 → 0.02.**
*Convention warning:* the identity `#{Δ = 0} = #{Δ ≡ 0 mod p³}` was verified with the repo's symmetric
x-window `X ∈ [−h,h]`; with the naive [0,2p)² window the counts differ (720, 744, 1008, …), so the
convention is load-bearing and must be stated.

**M2 — homogeneous (position-free) family restriction. Its load-bearing claim is KILLED.**
The empirical core is real and reproduces exactly: the position-free fraction (`‖z‖₁·‖D‖_∞ ≤ p`, which is
precisely "D in the box [−L,L]² of Lemma K(iii)" with `L = ⌊p/(s₁+s₂)⌋`) among **weak-line** collinear
triples is **0.356, 0.368, 0.303, 0.372, 0.344** at p = 31, 61, 101, 151, 199, and the total collinear-triple
counts 2992 / 7092 / 13708 / 23844 / 32936 reproduce exactly. **What must be deleted** is the claim that "a
computed certificate over this sub-system CONVERTS INTO A THEOREM for all p, because every ingredient is
algebraic plus a Kloosterman count." Lemma K(iii) (§22) gives only that the **existence** of a box lift is
decided by sign(u), sign(v); which lifts occur — hence the incidence structure any LP/SoS certificate
consumes — is determined by the least residues `X(λ_j u)`, i.e. by positions. Making that uniform in p is
`I1` applied to ≍ S² families at once, and Lemma FE is stated for ONE fixed family with constants
`O_{i,j}(√p log^{16} p)` and a fibre product whose genus grows with |S|; no version uniform over a growing
family set exists in the repo or the literature. Two further discounts: restricting a covering LP can only
weaken it, so the experiment cannot beat LP(all) ≈ 3.40; and the *currently countable* range (`‖z‖₁ ≤ p^{1/4}`)
is 0.070, **0.000**, 0.082, 0.123, 0.112 of weak triples by independent recomputation (the exact 0.000 at
p = 61 alone shows the certifiable sub-system is not p-uniform). **P = 0.18 → 0.07 → 0.05**, and it stays
the highest-value experiment in Q4 only because it is cheap and its answer is genuinely unknown.

**M3 — Cilleruelo–Garaev multiplier pigeonhole + divisor bound. Correct source, honestly-stated wrong
direction.** It produces **sparsity** where H6/H7 need **supersaturation**; on the full box it returns the
trivial count; its usable range M₀ < p^{1/4} is exactly where our set already has O(1) points, making the
proposed experiment near-tautological. And its output is `M^{o(1)}` — an ineffective bound — which cannot
improve the explicit `N₀ ≤ 64·6 = 384` already in `pair_bound_notes` line 786. **P = 0.08 → 0.04 → 0.02.**

**M4 — curve + sign-polytope counting generalised to weak-line families. The most honest card in Q4.**
It correctly identifies both walls: a polytope-volume law gives *frequencies* and can never decide the
vanishing of a single algebraic integer (the carry hitting a prescribed value is a measure-zero event), and
summing over families needs the QR density of Gaussian norms below p^{1/4}, which is **verbatim H5**. So M4
reduces H6 to H5 rather than closing it. **P = 0.04 → 0.02.**

**M5 — Boolean-cube algebraisation. Its verified content is a CORRECTION TO THE REPO, not a mechanism.**
Independently re-derived from the `L(r,s), Q(r,s)` formulas of `pair_bound_notes` §8: the base determinant is
at most (p−1)(p−2), so `|M| < p−2` rather than the repo's stated `|M| ≤ 8p`; measured maxima 6, 6, 11, 10, 16,
21, 16, 23, 31, 32, 36, 41, 46, **48** at p = 11…61 (ratios 0.70–0.79 of p, not "≈ 0.8p"); and the fraction
of mod-p collinear class triples carrying at least one Z-collinear lift is 1.00, 1.00, 0.94, 0.94, 0.85, 0.86,
0.88, 0.77, 0.79, 0.61, 0.68, 0.63, 0.60 at p = 11, 13, 17, 19, 23, 29, 31, 37, 41, 47, 53, 59, 61
(the published list silently skips p = 43, where the value is 0.74). **So §8's "for most class triples none …
in a range of length ≈ 16p" is only true from p ≈ 60 onward, and the carry bound is sharper than stated.**
This correction should be committed. The named mechanism contributes nothing (the Combinatorial
Nullstellensatz gives *existence* of a non-vanishing point — the opposite of what is needed), and its
concrete experiment is already H1's "testable now". **P = 0.15 → 0.10 → 0.05.**

**M6 — NEGATIVE: Rédei / Segre / slice rank do not survive lifting. Survives as a pruning card, with three
numerical corrections.** Structural conclusions are right: Rédei needs `X^q − X` to split over a *field*;
Segre needs a well-defined tangent multiset; slice rank needs fixed q with growing n and a group-determined
third point. Corrections: (a) the number of directions in AHG(2, Z/p³) is **p²(p+1)**, not p⁴(p+1) — verified
by enumeration (36 at p = 3, 150 at p = 5; equivalently `|P¹(Z/p³)| = p³+p²`); (b) the tangent count is
**q+2−|A|**, not q+1−|A|; (c) two points whose difference is p·(unit) lie on exactly **p** common lines and
p²·(unit) on **p²** — the card's "distance 1 ⇒ p²" is misindexed. Add the cleaner reason Thm 3.1 is unusable:
it requires |R| = **exactly q**, and our residue configuration has 2(p−1) points, so the hypothesis fails
before any "all directions are determined" observation is needed. Also: Bombieri–Pila applied to the ≈ **16p**
(not 8p) integer conics `xy = c` carrying V gives `p^{1/2+o(1)}` per conic, `p^{3/2+o(1)}` total — vacuous
against |V| = 8(p−1). **P = 0.02 → 0.01.**

### (iii) Transfer against I1–I6

M2 wants a p-uniform version of `I1`/Lemma FE over a growing family set: not available, and the union-bound
arithmetic of §3(iii) says why it cannot be. M4 wants `I1` and correctly concludes it reduces to `I3`+H5.
M5's real output plugs into `I4` as a correction. M3 and M1 plug into nothing. **The whole "algebra + box"
technology bounds cardinalities and never produces covering statements** — verified twice over, by two
independent 30-page papers on exactly our object with zero collinearity content.

### (iv) Negative findings

- **The nearest thing to a "Bombieri–Pila for congruences" covering lemma is implicit inside
  Cilleruelo–Garaev's own proof** (`(tx+u₀)(ty+v₀) = n_z` covers the box solutions by O(1) conics) and
  **nobody states it as a standalone lemma.** Searched; not found.
- **Numbers that do not reproduce, and must not be quoted:** the ALL-triples position-free fractions
  (claimed 0.402, 0.412, 0.354, 0.393, 0.372; independent reconstruction gives 0.285, 0.306, 0.267, 0.318,
  0.301) and the certifiable sub-fractions (claimed 0.095, 0.000, 0.149, 0.158, 0.150; reconstructed 0.070,
  0.000, 0.082, 0.123, 0.112). The gap is exactly the 836 / 1728 / 2848 / 4308 / 5652 triples using two lifts
  of the **same** class, for which the B.15 family parametrisation is undefined and the card does not say what
  rule it applied. **Use only the weak-line figures**, which reproduce exactly and are the ones the argument
  needs anyway. The honest statement: roughly a third of weak-line triples are position-free, of which under
  a sixth is currently countable.
- **The block-delocalisation measurement** (from the arithmetic review, and it is the quantitative content of
  H4(iii)): rich lines crossing a block boundary = **0** at every p from 11 to 199 — `thm:blocks` confirmed
  independently. Weak lines confined to a single block: 12/1044 (p=31), 24/2416 (61), 20/4948 (101),
  16/6400 (127), 16/9332 (151), 20/13468 (199) — fraction 0.0115 → 0.0015, i.e. Θ(1/p). Blocks touched by a
  weak line at p = 199: 2 (1124 lines), 3 (9464), 4 (2860). The separation is uniform: mean t-diameter/p =
  0.366, 0.369, 0.373, 0.374, 0.374 at p = 61…251, deciles at p = 199 [0.201, 0.312, 0.412, 0.462, 0.487] —
  the profile of three uniform points on Z/p. **Consequence:** a certificate coupling blocks at t-offset δ has,
  for each fixed δ, a Weil count `p·vol + O_k(√p)`; summed over the Θ(p) offsets the error is Θ(p^{3/2})
  against a main term Θ(p), so to stay inside Weil the δ-support must be o(√p) — and such a certificate
  retains a vanishing fraction of the weak lines. Cauchy–Schwarz over δ gives Σ_δ|·| ≤ p^{3/2}, no gain.
  **The entire "local certificate + equidistribution" technology, which produced every proved bound in this
  project, is capped at 3.4413 for an arithmetic reason.**

---

## 5. Q5 [H7] — supersaturation for point-line problems on curves

### (i) Sources

| Source | Statement | Status |
|---|---|---|
| Li, "Collinear triples in permutations", Innov. Incidence Geom. **8** (2008) 171–173, arXiv:0805.0410 | `Ψ(σ) ≥ (q−1)/2` for every permutation of F_q, q odd, confirming the Cooper–Solymosi conjecture; the chain (1.1) (q−1)/4, (1.3) (5q−1)/14, (1.4) `♯K_σ = q(q+1)/2 + ‖Γ_σ‖`, Faber's identity (2.1)–(2.3) with the two moments q(q+1) and 2q(q+1) and "two lines with different slopes intersect at one point", and `Ψ = Σ C(\|e\|,3) ≥ Σ C(\|e\|−1,2)` | **CONFIRMED** verbatim; **sharpness independently verified** by brute force: `σ(x) = 1/x` gives Ψ = 2, 3, 5, 6, 8, 9, 11, 14, 15, 18, 20, 21, 23 = exactly (q−1)/2 at q = 5…47 |
| Blokhuis–Mazzocca, "The finite field Kakeya problem", Bolyai Soc. Math. Stud. **19** (2008) 205–218, arXiv:0911.4370 | Prop. 3 (Faber's incidence formula, 2006); **Prop. 7** `\|K\| ≥ q(q+1)/2 + (q−1)/2` for q odd with equality iff type K(O,ℓ,ℓ_A); Prop. 8 dual form `k*(q) = (q+1)(q+2)/2 + (q−1)/2`; "The essential ingredients in the proof are the Segre's lemma of tangents and the Jamison-Brouwer-Schrijver bound on the size of blocking sets in desarguesian affine planes"; Prop. 1 = Bichara–Korchmáros (1982), Prop. 2 = Blokhuis–Bruen (1989), Prop. 6 = Cooper (2006) | **CONFIRMED** verbatim |
| Cooper–Hyatt, arXiv:2501.02331 (4 Jan 2025) | **Thm 2** (minimisers are ELFTPs); Lemma 1 (**q ≥ 5**) + Cor 1.1 (Γ′ a hyperbola plus an external point); **Thm 3** (lex-least is `g(x) = x/(x−1)`, g(1)=1, i.e. (x−1)(y−1)=1); **Thm 4** (every generalized permutation in an affine plane of odd order admits a collinear triple, by the C(q,2)-over-(q−1) pigeonhole giving ⌈q/2⌉ = (q+1)/2); q = 2^k minimum 0 via σ(x)=1/x; Cooper–Solymosi Cor. 2.3 applies to all finite affine planes | **CONFIRMED** verbatim. Note: "minimisers have no collinear quadruples" is a stated consequence for AG(q,2); their **Question 3** is its generalisation — the card conflated the two by one step |
| Li–Liu–Liu–Wang, arXiv:2606.26735 (25 Jun 2026) | **Thm 1.1**: for every r ≥ 2 and K > 1 there is a **stable** r-graph F with an n-vertex r-graph having ex(n,F)+q edges and at most `K⁻¹·q·c(n,F)` copies, for all 1 ≤ q ≤ δn — so Mubayi's conjectured lower bound fails already at q = 1, by an arbitrarily large constant factor, in every uniformity | **CONFIRMED** (the identifier was checked specifically because a post-cutoff June-2026 arXiv id is the classic fabrication site). One overstatement: "the failure is NOT caused by non-uniqueness or instability" is the card's inference, not a quotation |
| Ma–Yuan, arXiv:2310.08081, Combinatorica **45** art. 18 (2025) | (i) infinitely many F with `h_F(n,q) < q·t_F(n,1)` for n ≫ q ≥ 4; (ii) `h_F = t_F` for 1 ≤ q ≤ ε_F n for a family including colour-critical graphs, disjoint unions of K_r, and the Petersen graph; (iii) threshold `q = Θ(n^{1−1/s})` | **CONFIRMED** verbatim |
| Mubayi, Adv. Math. **225** (2010) 2731–2740, arXiv:0905.3146 | supersaturation for colour-critical graphs, 1 ≤ q < cn; the C₅ instance `n²/4 + q` edges ⇒ ≥ `q(n/2)(n/2−1)(n/2−2)` copies | **PARTIALLY CORRECT**: the C₅ statement carries "**n even**", dropped by the card; and the constant "q < n/2" attributed to Erdős / Lovász–Simonovits appears in **neither** Mubayi's nor Ma–Yuan's text — **UNVERIFIED** |
| Raz–Sharir–de Zeeuw, Duke Math. J. **165** no. 18 (2016) 3517–3566, arXiv:1504.05012 | F vanishes on at most `O(n^{11/6})` points of A×B×C unless F has a special group-related form; same over R | **CONFIRMED** |
| Fox–Pham, arXiv:1708.08486, Discrete Analysis **2019:16** | tower height of `n_p(α,β)` determined for p ≥ 19 up to a constant factor **and an additive term depending only on p**; at β = α³/2 the dimension is a tower of twos of height `Θ((log p)·log log(1/α))` | **CONFIRMED** |
| Erdős–Simonovits, Combinatorica **3** (1983) 181–192 | the supersaturation problem statement | **CONFIRMED** bibliographically; paywalled, quoted only in its standard textbook form (no theorem number at risk) |
| Pikhurko–Yilma, arXiv:1208.4319 | determines `h_F(n,q)` asymptotically for colour-critical F and `q = o(n²)` — it does **not** itself assert `h_F = t_F` on the linear range; that attribution comes from Ma–Yuan | **CONFIRMED**; the card's own caveat was exactly right |
| **MISSED SOURCE, now added**: Chen–Liu–Nie–Zeng, "Random Turán and counting results for general position sets over finite fields", arXiv:2309.07744, §3.1 | Lemma 3.2 `λ₂(I_{q,d}) = q^{(d−1)/2}`; Lemma 3.3 (bipartite expander mixing bounds the number of lines with atypically few/many points of P by `4q^{d+1}/\|P\|`); **Lemma 3.4** balanced supersaturation for collinear triples in F_q²: a family S with `\|S\| ≥ (q(q+1) − 8q³/\|P\|)·C(\|P\|/(2q), 3)`, every point in ≤ `(q+1)·C(⌊2\|P\|/q⌋,2)` triples, every pair in ≤ `2\|P\|/q` triples | **CONFIRMED**. This is the closest genuine H7-analogue in the literature and the sweep missed it entirely |

### (ii) Mechanism cards

**Card 1 — Kakeya duality (Cooper → Faber → Blokhuis–Mazzocca → Li). Survives as a fully-sourced,
correctly-reasoned negative, but it is mislabelled.** The chain is verified verbatim at both ends and the
sharpness is verified numerically. Its obstruction argument is correct and decisive: Faber's identity needs
"two lines of distinct slopes meet in exactly one point", the box has Θ(p²) primitive directions where the
pigeonhole needs O(p), and there is no dual plane so Segre's lemma of tangents has no analogue.
**It is NOT H7**: Li's theorem has no |S| parameter — it asserts `Ψ(σ) ≥ (q−1)/2` at the single size |S| = q
(full transversal). Its true analogue in the project is **B.12/§20's H4′** — min T over the vertical-pair
2-factor model, also a fixed-size minimum over doubly-transversal sets — which the project has already
measured exactly to p = 29 (24, 28, 42, 48, 80, 136) and certified spectrally to within 5% at p = 29. Extra
pessimism the card missed: even in AG(2,q), with maximum triple-degree Δ, `(q−1)/2` triples force only
`(q−1)/(2Δ)` deletions, so Li's theorem gives **no nontrivial bound on the largest arc inside a transversal** —
the same deletion loss B.12 records for the box. **P = 0.04 → 0.02 → 0.01.**

**Card 2 — Ball–Lavrauw + Bézout residue-level companion theorem. TRUE, and KILLED as a transfer.**
The theorem is true and independently verified twice: the maximum no-three-collinear subset of
`{xy≡1} ∪ {xy≡−1}` in AG(2,p) is **exactly p−1 (excess 0)** for every prime 11 ≤ p ≤ 71 (and at p = 5), with
the single exception **p = 7, where it is 8 = (p−1)+2**. The proof logic is sound: `p−1 ≥ p−√p+7/2 ⟺ √p ≥ 4.5
⟺ p ≥ 23`; the two conics share only [1:0:0], [0:1:0] ⊂ ℓ_∞ hence no affine point; Bézout gives ≤ 4+4 = 8 <
p−1 for p ≥ 11. **But its probability 0.85 answered "is this theorem true and provable?" while every other
card's answered "does this help bound α(P₋₁)?"** Scored on the common question it is **0.02–0.03**: the
residue-level excess is identically **0** while the box excess (2, 4, 6, 5 at k = −1) **is** the entire
phenomenon; the gain is created by the lift/position degrees of freedom the residue theorem forgets; and
`next_targets.md` §G records that the box-level results G3 and C are already done and integrated into the note
(v1.4/v1.5), so the claim that this "answers Green's Problem-72 comment" is wrong — Green's comment and §G
are both about **lifted** sets in the box. **Ranking it first among the transfers was the single most
consequential calibration error in the corpus.**

**Card 3 — Erdős–Rademacher template. Survives as a negative, and is now MEASURED dead.**
Three-failure diagnosis, all sound: Turán density is 0 so Erdős–Simonovits is inapplicable (not merely weak);
the extremal structure is arithmetic, not a blow-up; the multiplier is not free from stability (and the
Li–Liu–Liu–Wang 2026 and Ma–Yuan refutations are verified). **Its decisive experiment has already been run
in the repo** and confirms it: `slack/min_triples.py`, logs `slack/verification/min_triples_p{13,17,19}.txt`,
results in `docs/THREAD.md` [90] — p=13, t = 5…12 → 2, 3, 5, 8, 10, 14, 16, 20; p=17, t = 5,6 → 0 (α = 54 ✓),
t = 7…11 → 1, 3, 5, 8, 10; p=19, t = 5 → 0 (α = 59 ✓), t = 6…10 → 1, 7, 12, 6(!), 16. Slope ≈ **1.5–2 triples
per extra point, with no p-dependence** — exactly the O(1) multiplier the card says retires the Rademacher
literature. These are feasible solutions, i.e. **upper** bounds on the minimum (CP-SAT lower bounds ≈ 0),
which strengthens the conclusion. **The card should cite this rather than propose it. P = 0.02 → 0.01.**

**Card 4 — parallel-class pigeonhole (Cooper–Solymosi Cor. 2.3; Cooper–Hyatt Thm 4). Negative.**
Headline arithmetic correct and decisive: `|S| = 4(p−1)` gives `C(|S|,2) ≈ 8p²` pairs, per-direction capacity
`⌊|S|/2⌋ = 2(p−1)`, so the pigeonhole needs ≲ 4p usable directions while the box supplies Θ(p²).
**Discard the window sub-computation**: capacity per direction is `min(⌊|S|/2⌋, #lines of that direction with
≥ 2 candidates)`, and since `#lines ≈ 2p(|u|+|v|) ≥ 2p ≈ ⌊|S|/2⌋` already at |u|+|v| = 1, the total is
≈ 2pL², not 2pL³, crossing 8p² at L ≈ 2√p, not 2p^{1/3}. Conclusion unaffected — no window makes the count
bite either way. **P = 0.02 → 0.01.**

**Card 5 — internal-nucleus counting (Bichara–Korchmáros / Blokhuis–Bruen / Blokhuis–Mazzocca Prop. 8).
Weakest, negative.** It inherits Card 1's obstruction (it is the dual of the same count) and adds a strictly
stronger hypothesis — perfect regularity at a point — which the ±1 line classification of §24 (lines carrying
up to 8 candidates) rules out structurally, not just numerically. Its stated value, naming the exact
regularity the box lacks, is diagnostic, not transfer. **P = 0.05 → 0.02 → 0.01.**

**NEW card — balanced supersaturation via expander mixing (Chen–Liu–Nie–Zeng, Lemmas 3.2–3.4).**
Inputs: any P ⊂ F_q², λ₂ of the point-line incidence graph. Steps: expander mixing bounds the number of lines
with atypical |P∩ℓ|; convert into a family of collinear triples with per-point and per-pair degree control.
Output: **balanced** supersaturation — exactly the shape a container or deletion argument consumes. **Why it
dies here, and the failure is by a bounded factor, which makes it a sharp citable obstruction rather than a
vague one:** Lemma 3.4(i) is positive only for `|P| > 8q²/(q+1) ≈ 8q` (and needs `|P| ≥ 6q` for the
binomial); the residue shadow of P₋₁ has `|P| = 2(p−1) ≈ 2q` — a factor **≈ 4** below threshold, and the
deficit is p-independent, so no p is large enough. Not fixable by sharpening constants: `λ₂ = q^{1/2}`, the
mixing error on a set of density |P|/q² is `q^{1/2}|P|`, and it beats the main term `|P|²/q` only well above
curve density. And **in the box there is no ambient plane, so the incidence graph does not exist.**
**P = 0.02 → 0.01.** Its real value: one citable sentence — "the pseudorandomness route to supersaturation
for collinear triples turns on at density 8/q; a pair of conics sits at 2/q".

### (iii) Transfer against I1–I6

Card 1 wants `I4`; the project holds it in a stronger form. The NEW card wants an ambient plane, which the box
does not provide, and a density 4× ours. Card 3's target is measured by `I6` and the measurement kills it.
**H7 does not plug into an interface, because H7 is not a hole:** `pair_bound_notes` B.12 lines 431–432 read
verbatim "T(S) = 0 forces |S| ≤ 3(p−1)+C₀, i.e. H4 ⇒ T1 in the strong O(1) form; conversely T1(O(1)) ⇒ H4
with c = 1 (delete one point per triple). So H4 is not an intermediate hypothesis but the target itself in
'supersaturation' form", and the project's own executable audit carries the same as `GAP-H-01` /
`GAP-C-05` / `GAP-P-03` with the equivalence brute-forced over 400 random 3-uniform hypergraphs and a passing
contract test `test_H4_and_H7_are_both_the_target_by_the_projects_own_notes`. **Any answer to Q5 is a complete
solution of the open problem, and the brief's difficulty calibration for this question is wrong.** The only
genuinely weaker form is B.12's `H4(ε)`: `T(S) ≥ c|S| whenever |S| ≥ (3+ε)(p−1)`, which yields T2, not T1 —
and note that the ε-form written in the corpus ("T(S) ≥ 1 whenever |S| ≥ θ(p−1)") is literally T2 restated
and is weaker still.

### (iv) Negative findings, including two blanket negatives that had to be withdrawn

- **CONFIRMED: there is no supersaturation result in the literature for the parent problem.** Independently
  searched: nothing bounds collinear triples from below for 2N+t points in the integer grid.
- **WITHDRAWN: "all finite-field incidence bounds are structurally the wrong direction and cannot be fixed;
  no incidence theorem bounds directions from above."** Refuted by Chen–Liu–Nie–Zeng, who derive a *lower*
  bound on collinear triples from incidence pseudorandomness. Replace with the quantitative version (density
  8/q vs our 2/q). The same paragraph also contained a non-sequitur: a set with no three collinear does not
  span "the maximum possible" number of directions — it spans C(|S|,2) **lines** but at most
  `min(C(|S|,2), #directions)` directions, and in a box the direction count is the binding constraint.
- **WITHDRAWN: "the box destroys the affine-plane counting BY A FACTOR p, and I measured it two ways."**
  Neither measurement supports it. (a) "In AG(2,q) with a permutation the dangerous-pair fraction is 1" is
  false: it is exactly **3/q** for the minimiser `σ(x)=1/x` (0.2727, 0.1765, 0.0732, 0.0423, 0.0309 at
  q = 11, 17, 41, 71, 97) and ≈ **0.61–0.71** for a random permutation; it equals 1 only for the full q×q
  grid, i.e. for the candidate *set*. So the box's measured 0.060 at p = 97 is roughly **twice** the AG(2,q)
  extremal object's 0.031 — the datum points the opposite way from the conclusion drawn from it.
  (b) "the box realises only ≈ Θ(p log p) of the ≈ Θ(p²) affine-plane constraints" is contradicted by the
  card's own data: the number of mod-p collinear class triples is `(p−1)(p−3−2[2 QR]) = Θ(p²)` (8832 at p = 97)
  and the surviving fraction there is 0.353, i.e. ≈ 3100 surviving triples — **Θ(p²), not Θ(p log p)**
  (a log p/p factor would predict 0.047, eight times smaller). The honest statement: the box loses roughly
  half to two-thirds of the residue-level collinearity constraints by p ≈ 100, with the surviving count still
  Θ(p²). **The conclusion is nonetheless right for the reason stated elsewhere in the same document — the
  direction count, Θ(p²) available versus O(p) needed — and the finding should be rewritten around that.**
- **Elekes–Szabó / Raz–Sharir–de Zeeuw is doubly vacuous, but one of the two reasons is a non-sequitur.**
  Reason (i) — RSdZ is an *upper* bound on `|Z(F) ∩ (A×B×C)|` while H7 needs a lower bound — is correct and
  by itself decisive. Reason (ii) as argued ("homogeneous of degree 2 ⇒ invariant under the diagonal action ⇒
  exactly the special group-related form RSdZ excludes") is **wrong**: homogeneity gives invariance under a
  one-parameter scaling, whereas the RSdZ exception is that the variety is locally the graph of a group
  operation after a coordinate change. Also RSdZ is stated over C and R, not F_p. **The valid replacement is
  a counting argument:** `x₁² − x₁(x₂+x₃) − x₂x₃ = 0` solves uniquely for x₃ given (x₁,x₂), so with
  A = B = C = F_p^* it has ≈ n² solutions, exceeding O(n^{11/6}); hence if the theorem applied, the special
  case must hold.
- **Verified and worth keeping: the exact collinearity criterion at residue level.** Three points
  `(x_i, e_i/x_i)` of `{xy = ±1}` with the lone sign on x₁ are collinear iff
  `x₁² − x₁(x₂+x₃) − x₂x₃ ≡ 0 (mod p)`; there are **zero** same-sign collinear triples; equivalently
  `x₃/x₁ = (1 − x₂/x₁)/(1 + x₂/x₁)`, a **Möbius involution**; and the exact solution count is
  `(p−1)(p−3) − 2(p−1)·[2 is a QR mod p]`. Re-derived by hand and confirmed by enumeration (80, 120, 192,
  288, 396, 8832 triples at p = 11, 13, 17, 19, 23, 97).

---

## 6. Q6 [H8] — manufactured regularity for Bose-type "counting through a point"

### (i) Sources

| Source | Statement | Status |
|---|---|---|
| Blokhuis, "Combinatorial problems in finite geometry and lacunary polynomials", Proc. ICM Beijing 2002, vol. 3, **537–546**, arXiv:math/0304463 | Barlotti's counting bound verbatim ("if B is a (k,n)-arc, then k ≤ (n−1)(q+1)+1 = nq−q+n, and equality implies that n\|q and all lines intersect B in 0 or n points"); Bruen's `q+√q+1` with equality iff q square and B a Baer subplane; **Thm 2.3** [Blokhuis 1994, Combinatorica **14**, 111–114] `\|B\| ≥ (3/2)(p+1)` with each point on exactly (p−1)/2 tangents at equality; **Thm 3.1** [Rédei 1970]; **Thm 2.2** [BBBSS 1999]; **Thm 2.4** [Szőnyi 1997] | **CONFIRMED** verbatim (pages were given as 537–545) |
| — | the pointer "**p. 237, Satz 24**" | **MISPLACED**: in the survey that pointer belongs to **Theorem 2.1** (the directions theorem); Theorem 3.1 carries only "[Rédei, 1970]" with no page or Satz number. This is the one manufactured theorem-number-like object in the whole corpus, produced by transplant |
| Blokhuis–Ball–Brouwer–Storme–Szőnyi (**this author order**), "On the number of slopes of the graph of a function defined **on** a finite field", JCTA **86** (1999) 187–196, doi 10.1006/jcta.1998.2915 | the four-case directions theorem, with the moreover-clause | statement **CONFIRMED** verbatim; the derived reading for q = p prime (N = 1 or N ≥ (p+3)/2) is **correct** (case 2 needs p = 2; case 3 forces e = 1 and gives the empty range 2 ≤ N ≤ 1). Author order and title were wrong in the card |
| Ball–Lavrauw | §2 Bose quote ("In 1947, Bose [4] was the first to observe that the largest planar arc has size q+1 if q is odd and q+2 if q is even"), ref [4] = Sankhyā **8** (1947) 107–166; "Each point of S is incident with precisely t tangents"; Lemma 11; Thm 12 (degree mt, m ∈ {1,2}) | **CONFIRMED** verbatim; Thm 12's extra hypothesis `\|S\| ≥ mt+2` was dropped (immaterial) |
| Ball–Blokhuis–Mazzocca, Combinatorica **17** (1997) 31–41; Ball–Blokhuis, Proc. AMS **126** (1998) 3377–3380; Denniston, J. Combin. Theory **6** (1969) 317–319 | maximal arcs in Desarguesian planes of odd order do not exist; the easier proof; the q-even constructions | **CONFIRMED** |
| Frankl–Rödl, European J. Combin. **6** (1985) 317–326; Pippenger–Spencer, JCTA **51** (1989) 24–42 | the nibble; near-regularity is the load-bearing hypothesis | bibliographic data **CONFIRMED**; the label "**Lemma 5.1**" is **UNCONFIRMED** and must be deleted, and the `(1±τ)D` / `Δ₂ < τD` form is properly Pippenger / Alon–Spencer Ch. 4.7, not FR verbatim (FR is stated for D-regular hypergraphs with codegree ≤ D/(log N)⁴) |
| Ray-Chaudhuri–Wilson, "On t-designs", Osaka J. Math. **12** (1975) 737–744 | Theorem 1: `b ≥ C(v,s)` for a design with **t = 2s even** and v ≥ k+s | **PARTIALLY CORRECT**: the card wrote t ≥ 2s, a valid restatement but not what the primary says |
| Green, Problem 72; Hall–Jackson–Sudbery–Wild, JCTA **18** (1975) 336–341 | 2N trivial; (3/2 + o(1))N construction | **CONFIRMED**; the URL attached was **arXiv:2512.11469**, which is a real but unrelated paper (Ramanathan–Prellberg–Lewis–Joshi–Dandekar–Dandekar–Panat, "Three methods, one problem: Classical and AI approaches to no-three-in-line", cs.AI, Dec 2025) |

### (ii) Mechanism cards

**MC1 — Bose/Barlotti counting through a point, the richness criterion. Correct, and it fails decisively.**
Inputs: `excess(q) = (|V|−1) − λ(q)` where λ(q) counts the fibres of the pencil through q. Steps: Bose beats
a fibre-size-n parallel class iff `r̄(q) > n/2`; against n = 4 the criterion is `excess(q) > (|V|−1)/2`.
Output, measured and reproduced exactly: the Bose bound is **7.00, 7.08, 7.38, 7.33, 7.41, 7.46, 7.43** times
(p−1) at p = 11…31 — nearly **twice** the trivial 4(p−1). Excess split: rows+columns exactly 4.00 at all 22
primes; ±1 lines 2.17–4.98; general 7.85 (p=11) → 27.70 (p=101), and **not monotone** (18.62 at p=53 > 16.68
at p=47; 19.67 at p=97 < 28.30 at p=89), so "growing like a polylog" is an unsupported extrapolation.
Corrections: `min_q excess(q)` ∈ **[10,17]** (not 10–18); and the label "**PROVED** + measured" must become
"**monotonicity proved; the quantitative failure measured to p ≤ 101**" — only monotonicity is a theorem
(restricting the line family refines the fibres, so λ can only increase). **Do not write "excess(q) = O(log p)"
into the note**: the richness ceiling bounds `n_ℓ`, not the *number* of rich lines through q, and the only
unconditional bound on that number is the trivial `(|V|−1)/2`, giving `excess(q) ≤ |V|`. Bounding
`max_q excess(q)` is essentially the missing "few collinear triples through a point" statement (the repo has
only the *lower* bound `E(p) ≫ p log log p`). **P = 0.02 → 0.01.**

**MC2 — the RICHNESS CEILING LEMMA + packing budget. The lemma is the strongest deliverable in Q6; the
budget must be relabelled.**
*Lemma (proof checked line by line, correct and unconditional for `|D|_∞ ≥ 3`):* a line with primitive
direction D and `|D|_∞ = d` cuts an arithmetic progression of at most `2p/d + 1` lattice points from the
window; for d ≥ 3 that is `2p/3 + 1 < p`, so `t ↦ t·(u,v) mod p` is injective and the residues along the line
are distinct; a line of AG(2,p) meets each of `xy = ±1` in ≤ 2 points, giving **≤ 4 candidates**. For d = 2 the
count is ≤ p+1 with one repeat, giving **≤ 5**. Rows/columns: 2p x-values, each residue twice, 2 residues per
row ⇒ **4**. Slopes ±1: ≤ 2 lifts per residue × 4 residues ⇒ **≤ 8**. Verified for all 22 primes
11 ≤ p ≤ 101: the maximum over `|D|_∞ ≥ 2` is **exactly 4** at every p, and the only directions carrying a
≥ 5-point line are (1,1) and (1,−1). **Correction:** "the max size is 8 every time" is **FALSE at p = 13 and
p = 17**, where the maximum line size is 6 (m₈ = 0 there, as the repo also records); write "≤ 8, attained only
by slopes ±1 and only when m₈ > 0".
*Budget:* `Σ(n_i − 2) ≤ ½|V| + Σ_{n≥5}(n/2 − 2)`, giving per-prime values 3.200, 3.667, 3.375, 3.111, 3.182,
2.714, 3.133, 3.000, 3.400, 3.048, 3.087, 3.308, 3.034, 2.867, 3.030, 3.057, 3.000, 3.051, 3.024, 3.159,
3.229, 3.000 (range 2.714–3.667, mean **3.122**, not 3.09), with the asymptotic (3+o(1))(p−1) resting on §24's
per-slope saving 0.488p. **THIS MUST BE RELABELLED AS A BOUND ON THE SAVING, NOT ON α.** By MC3′ (proved
below) every packing bound is ≥ LP(all), whose measured mean is 3.3960(p−1) and minimum 3.3168(p−1); so the
budget's values below 3.32 are not achievable bounds. Concretely: at p = 29 the budget reads 2.714(p−1) = 76,
but LP(all)(29) = 92.11, so **no fractional packing certificate at p = 29 goes below 92.11**. Without this
relabelling the card reads as "the highest-ranked surviving mechanism nearly reaches the target"; with it, it
reads as "provably 0.32(p−1) away". **P(the lemma is correct) ≈ 0.9. P(it routes below 3.4482) = 0.02.**

**MC3 — "every Bose/partition/near-partition bound is a feasible LP dual". SPLIT: half proved, half FALSE.**
The **packing half is correct** and re-derived: given `x_ℓ ≥ 0` with `Σ_{ℓ∋v} x_ℓ ≤ 1`, the weights
`w_ℓ = x_ℓ`, `w_v = 1 − Σ_{ℓ∋v} x_ℓ` are dual-feasible for `{max Σx_v : Σ_{v∈ℓ} x_v ≤ 2, 0 ≤ x ≤ 1}` with
cost `|V| − Σ_ℓ(n_ℓ − 2)x_ℓ`. Confirmed numerically (fractional packing vs LP(all): 32.000/32.000,
44.800/44.800, 60.178/60.154, 64.000/63.636, 78.759/78.125, 92.967/92.113, 105.628/104.762).
The **Bose half is FALSE**: the pencil of lines through q is not a packing (all its lines share q), so the
dual construction does not apply — and the card's own MC1 supplies the counterexample: in PG(2,q) the
assignment `x ≡ 2/(q+1)` is LP-feasible with value ≈ 2q while Bose gives q+2 < 2q. So Bose-through-a-point
demonstrably **beats** the LP in the model case; in our box it lands above the LP only because `excess(q)`
happens to be tiny, not by any duality. **The H8 negative must rest on the measured smallness of excess(q),
not on duality.**

**MC3′ — packing / near-partition / fractional-cover bounds are LP duals, hence ≥ LP(all). Survives at 0.85
and IS the answer to the brief's question.** The brief asked for a documented "approximate partition with
defect δ ⇒ bound degraded by O(δ)" argument. There is **no named theorem** — searched independently (partial
parallel classes, near-resolvable designs, packing/covering duality, Füredi's "Matchings and Covers in
Hypergraphs" survey which Blokhuis cites as [18]) — because the statement **is ordinary fractional
relaxation**, with the LP value as its floor. Held below 0.9 only because it is a derivation, not a citation.

**MC4 — Gaussian-scale sub-family, tested directly. Survives with narrowed scope.** Every measured number
reproduces exactly: at p = 101 the seven dyadic `|D|_∞` buckets give (#lines, coverage, mean multiplicity,
bound/(p−1)) = (676, 1.00, 3.49, **3.55**), (810, 0.95, 3.77, 4.84), (1144, 0.99, 4.73, 4.93), (918, 0.99,
3.75, 5.12), (1056, 1.00, 4.37, 5.02), (768, 0.97, 3.12, 5.49), (252, **0.67**, 1.43, 6.58). Multiplicity → 1
and coverage → 1 are in direct tension, and every scale ≥ 2 is worse than trivial. Two internal fixes:
"coverage is 0.95–1.00 at every scale" is contradicted by its own top buckets (0.78 at p=61, 0.67 at p=101),
and "the max multiplicity is 7–10" should be 3–10. **Scope correction:** the buckets are dyadic in `|D|_∞`,
which is **not** the brief's proposal (one arithmetic Gaussian-step family (s₁,s₂), interface `I3`), and a
single family lives on one direction hyperbola `uv ≡ 2e/(s₁s₂)` spanning many dyadic buckets. That version is
untested — but MC2's ceiling independently forces `(2/4)|V| = 4(p−1)` for every non-±1 direction, so it is
over-determined. **P = 0.02 → 0.05 → 0.02.**

**MC5 — exactly 8 residue directions through every candidate for every present family. UPGRADED by
verification, then DOWNGRADED by the union-bound wall.** The constant is **verified, not provisional**: for
p = 97, 191, 193 and every present family with `s₁+s₂ ≤ 12`, for every residue candidate (x, ε), the number of
(e, root z, position t) triples yielding a valid direction `u ≡ x/(z+t)`, `v ≡ 2e/(s₁s₂ u)` is exactly **8**,
with no exceptions (p=97: 16 families × 192 candidates; p=191: 25 × 380; p=193: 12 × 384). Two edge cases the
card omits: the degenerate family with `s₁²+s₂² ≡ 0 (mod p)` has one root and gives **4**, and positions with
`z+t ≡ 0` must be excluded. **The kill:** its stated payoff (H7) requires the box-fitting volumes `Vol_F` to
be uniform over families up to scale p^{1/4} — the card lists this as what is missing — and that is the
union-bound wall in its purest form (per family a lattice-rule/Erdős–Turán–Koksma count with error
√p·log^c p, times ≍ S² families, against a main term ≍ p: rigorous iff S ≪ p^{1/4}). **B.17 already extracts
`E ≥ c(p−1)·log log p` from exactly this technology summed over coprime families with `s₁+s₂ ≤ p^{1/4−ε}`.**
So MC5 is not a new route to H7; it is B.17 with a cleaner constant (it changes c, not log log p → log p).
And the card itself concedes it can never be a packing bound: Θ(polylog p) against a required Θ(p).
**P = 0.30 → 0.38 → 0.05.**

**MC6 — Rédei polynomial as the literature's one closure of a linear-in-q counting gap. Correct H6 pointer,
negative.** The Rédei setup is verbatim right (`X^q − X` divides `R[X,y]`; `r_i ≡ 0` for i = d+1…q−2;
`f(X) = ∏(X − a_i) = X^q g(X) + h(X)`), and the arithmetic `|B| = p+1+d` with `d ≥ (p+1)/2` is right. But the
survey's **Theorem 3.1 is about `f = X^q + g`**, whereas the blocking-set application produces
`f = X^q g(X) + h(X)`, and the survey explicitly hands that case to **Theorem 3.2**
(Blokhuis–Storme–Szőnyi 1998). So step 3 is not a one-line application of Theorem 3.1 as written. Three
obstructions, each independently fatal: sparse triples are not a full pencil; positions/inequalities have no
slot in a Rédei polynomial; the constraint direction is reversed. **P = 0.03 → 0.02.**

### (iii) Transfer against I1–I6, and the gutting of H8

MC5 plugs into `I3` and lands back on B.17. MC2's lemma is pure `I4` and is the one genuinely new piece of
mathematics Q6 produced. MC1/MC4 plug into `I6` and are measurements.

**H8 is not merely unfilled; it asks for something now proved not to exist.** Two independent reasons:
(a) H4(iii) — inside an orbit union `O ∪ R(O)` (32 points) the exact maximum is 16, the trivial row bound, so
summing over orbits returns **exactly 4(p−1)**; verified at every orbit of p = 11, 13, 17, 19, 23 with the
sums 40, 48, 64, 72, 88;
(b) MC3′ — every packing / near-partition / fractional-cover bound is ≥ LP(all) ≈ 3.40(p−1).
Together: **no "manufactured local regularity" can produce a bound below 3.40, and orbit-local versions
produce exactly the trivial bound.** This is the single biggest re-ranking the update forces, and it should be
written into `holes.py` as a closure rather than a hole.

**One over-reach to correct in the project's own text.** `paper/section_blocks.tex` remark (d) last sentence
("No certificate that is local for the orbits or for the blocks can therefore reach 3(p−1)") is right for
orbits and **over-reaches for blocks** — contradicted by the project's own theorem in the same section, since
block-local certificates *do* beat trivial (3.44817 proved, 3.4413 in the limit). Only two points of the
locality/value curve have ever been computed (scale 32 → exactly 4.000; scale 32·(run length) → 3.4413), and
`Σ_blocks α(block) → α` trivially as the block size → |P|. Publishing an in-principle impossibility on that
evidence is exactly the fabrication risk the project has been burned by. **The defensible claim is a RATE
claim, and the rate has not been measured.** Data now in hand: the best certificate decomposing over ≤ k
orbit-unions, computed exactly (ILP per block, then both the best partition bound and the strictly more
general best fractional-cover bound over the same blocks), gives

| k | p=13 (α=40) | p=17 (α=54) | p=19 (α=59) | p=23 |
|---|---|---|---|---|
| 1 | 48 = 4.0000(p−1) | 64 = 4.0000 | 72 = 4.0000 | 88 = 4.0000 |
| 2 | 48 = 4.0000 | 63 = 3.9375 | 64 = 3.5556 | 80 = 3.6364 |
| 3 | 44 = 3.6667 | 60–61 = 3.7500 | 64 = 3.5556 | 80 = 3.6364 |

so coupling **three** of the five-or-six orbit unions — more than half the instance — still leaves
≥ 3.5556(p−1), worse than the 3.44817 already proved. The correct statement is: **the locality needed to
reach 3(p−1) exceeds half the instance already at p = 19.** Note also that k = 2 is not always worthless
(p = 19 and 23 both gain 8), so "local certificates give exactly 4(p−1)" is true only at k = 1.

### (iv) Negative findings

- The Bose bound is 7.0–7.5(p−1), nearly twice trivial, at every prime to 31. The mechanism transfers
  verbatim and fails by a factor of 2.
- The 3-uniform collinear-triple hypergraph is **nowhere near degree-regular**, so the Frankl–Rödl /
  Pippenger nibble hypothesis fails: min/max triple-degree 13/46, 15/54, 22/60, 21/99, 23/111, 32/119 at
  p = 11, 19, 41, 101, 199, 401 — ratio 3.5–4.8, not shrinking. (The corpus's phrasing "at p = 13 there is a
  vertex of degree 0" is **wrong**: the quantity measured is the number of exactly-3-point lines through a
  point; in the triple hypergraph every candidate has degree ≥ 6 from its own row and column.) And even a
  perfect matching would give only `(2/3)|V| = 5.33(p−1)`, worse than trivial.
- The defect from the trivial bound is `4(p−1) − α` = **8, 8, 10, 13** at p = 11, 13, 17, 19, i.e. Ω(p),
  against Ball–Blokhuis–Mazzocca's defect of exactly 1 for maximal arcs. (The corpus's formula "p−6" is right
  only at p = 19; the error is inherited from the brief's own inconsistent gain list.)
- **The m₈ bookkeeping is internally inconsistent in the repo and should be settled:** B.9(ii) says
  `m₈(p) = (1/6 + o(1))p` "both slopes" while §17 says `m₈ ~ p/12` conjectural, and §24's per-slope density
  is 0.0795; measured m₈ = 16 at p = 101 (both slopes) gives 0.158 ≈ 1/6, consistent with 1/12 per slope.

---

## 7. Q7 [meta] — problems of type "algebraic construction optimal up to O(1)" that WERE solved

### (i) Sources

Every cited work exists with correct authors, venues, years and pages; every quoted theorem number is real.
Verified: Green's list (Problems 72 and 68 verbatim, bibliography [165] Guy–Kelly Canad. Math. Bull. **11**
(1968) 527–531, [167] HJSW JCTA **18** (1975) 336–341, [301] Voloch J. Geom. **38** (1990) 198–200);
Green–Tao arXiv:1208.4714 (Thm 1.3 orchard `⌊n(n−3)/6⌋+1`; Thm 1.4 with `n ≥ exp exp(CK^C)` and all but
`O(K^{O(1)})` points on a cubic; Thm 1.5's three cases; Melchior's dual Euler argument and Chasles's
Cayley–Bacharach as Prop. 4.1) — **all CONFIRMED verbatim**; Ball, JEMS **14** (2012) 733–748 (MDS for prime
fields, ≤ q+1 if k ≤ p; the abstract also has ≤ q+k−p for q ≥ k ≥ p+1 ≥ 4, and classifies the k ≤ p extremals
"generalising Beniamino Segre's arc is a conic theorem" — the card quoted only the first clause);
Blokhuis–Mazzocca Kakeya as Theorem 1.2 of arXiv:2003.08480, verbatim, correctly attributed to reference [3]
with editors (**and the card correctly caught and rejected a bad automated read "q²−q+1"**);
Carter–Hunter–O'Bryant Acta Math. Hungar. **175** (2025) 108–126; Ball–Blokhuis–Mazzocca Combinatorica **17**
(1997) 31–41 and Denniston; kissing numbers 240 and 196560 by Delsarte's LP (Levenshtein; Odlyzko–Sloane,
1979, independently, **sharp only in dimensions 8 and 24**); Razborov's 0.561666 against the conjectured 5/9;
cap set 2.756ⁿ upper against 2.218021ⁿ lower (Elsholtz–Pach–Rackham–Tyrrell–Villanueva, arXiv:2209.10045).

**Errors in the SOLVED/OPEN table, all in attributions rather than in facts:**
- **S2** (ovoids in PG(3,q), q odd): the size bound `q²+1` is the elementary cap bound of **Bose/Qvist**
  (1952); Barlotti and Panella (both Boll. Un. Mat. Ital. (3) **10** (1955), 498–506 and 507–513) proved the
  **classification** as an elliptic quadric, whose proof is a Segre-style argument, not "the same double count
  with planes". The row welds the wrong mechanism to the wrong authors, and does not mention that the q-even
  ovoid classification remains open.
- **S3** (Kakeya): the q-even bound `q(q+1)/2` is described in the source as "easy to see", not a
  Blokhuis–Mazzocca result; the q-even **classification** is Blokhuis–De Boeck–Mazzocca–Storme, Des. Codes
  Cryptogr. **72**(1) (2014) 21–31. And the cell "(f) = unique" is **wrong** for q even: the same passage says
  of hyperovals "the classical example consists of a conic and its nucleus, but many examples are known".
  *This error cuts in the table's own favour* — a second solved row with many extremals.
- **S7** (Zarankiewicz at projective-plane parameters, Reiman 1958): sits in **both** columns, since the value
  is known only where a projective plane is known to exist; as evidence for the discriminator thesis it is
  much weaker than the row implies.
- **S9**: "(f) = unique (stars)" is right for EKR with n > 2k but not for Ahlswede–Khachatrian, whose extremal
  families are the Frankl families.
- The Kovács–Nagy–Szabó paper cited (arXiv:2502.00176) is the **less relevant** of the two; the one the
  project actually builds on is arXiv:2508.07632 (Adv. Comb. 2026:7). And its construction is described as
  "probabilistic/algebraic" where the abstract says **purely probabilistic** ("bi-uniform random bipartite
  graphs and concentration inequalities").
- **UNVERIFIABLE and flagged as such by the card itself**: a WebFetch summary of Ellis–Keller–Lifshitz
  (J. Eur. Math. Soc. **26** (2024) 1611–1654, doi 10.4171/JEMS/1441) asserted a discussion of
  `n = (k−t+1)(t+1)` as a boundary where "two extremal families coexist"; a grep of the full extracted PDF
  found **zero** occurrences. **Do not cite EKL for boundary non-uniqueness.** What *is* verbatim, in
  Filmus's "The weighted complete intersection theorem" Theorem 3.1, is that the bound is a **maximum over r**
  of `μ_p(F_{t,r})` with equality "only if F is equivalent to a Frankl family F_{t,r}"; that uniqueness fails
  where two r tie is an inference from the max-form, not a quotation.

**THE SERIOUS DEFECT IS STALENESS, on the single closest relative of the parent problem.** Green's own
"Update 2025" — ten lines past where the card stopped reading — points to Grebennikov–Kwan
(arXiv:2510.17743, n ≥ k ≥ 10³⁷); and the problem has since been resolved for **all k ≥ 3** by
Ghosal–Goenka–Grebennikov–Keevash–Kwan–Pham (arXiv:2607.05255, 6 Jul 2026: the maximum is exactly kn for
k ≥ 3 and large n), which the project's own paper already cites as `[GGGKKP26]`. So the catalogue's most
relevant SOLVED row is missing, and it was closed with **none** of the discriminators (a)–(f) — by random
constructions, Ehard–Glock–Joos pseudorandom hypergraph matchings, deletion and randomised switching.
**Verdict V6 ("no mechanism in the literature has ever closed a problem of this shape without (b) or a
substitute exact identity") is therefore too strong as written and must be restricted to problems where the
UPPER bound is the open direction.** The distinction is legitimate — for k ≥ 3 the hard direction is the
*construction*, since kn is the trivial upper bound, whereas for us the upper bound is the open direction —
and the card drew it elsewhere; but V6 as delivered overstates its own coverage.

### (ii) The discriminator verdicts

**(f) uniqueness vs multiplicity of extremals is a RED HERRING, and this is now settled in both directions.**
The project's own Lemma `orbopt` shows generic orbits are rigid with a unique maximum and 9^s counts only the
exceptional ones, so the old objection "unlike Segre's unique conic, we have exponentially many extremals" is
withdrawn. The replacement objection at the working density was tested and also fails (§2(iv)): counting
forces radius d = 1…5 against a true sharp radius of 8…28. And two *solved* rows (Kakeya q even, maximal arcs
q even) have many extremals. **Every card in the corpus that scored on uniqueness must be re-scored.** The two
discriminators that *do* separate our system cleanly are: **is the certificate inside the LP hull**, and **is
the extremum a fixed point of a symmetry the tool breaks**.

**(b) constraint completeness/regularity, in the sharp form "the constraint hypergraph is a near-partition",
is the operative discriminator, and it is confirmed by measurement.** One hyperbola: maximum rich-line degree
is **2** and the double count `Z + 2|L| = 3(p−1)` is exact (verbatim in `hjsw_window.tex` line 152; and
Z = 2, 4, 4, 2, 2, 4, 2 with |L| = 14, 16, 22, 26, 32, 40, 44 gives 30, 36, 48, 54, 66, 84, 90 = 3(p−1) at
p = 11…31, with `MID = {q : m(q) = 2}` of size 8, 8, 12, 16, 20, 24, 28 = p−1−2s exactly). The pair: mean
rich-line degree **9.20, 8.62, 11.12, 11.97, 12.91** with maximum 14, 12, 17, 19, 18 at p = 11…23, and
31.6% / 24.5% / 21.8% / 22.0% / 18.7% of pairs on some rich line. **Important refinement the framing missed:**
the pair's **max codegree is 1** at every p — every pair of points lies on at most one rich line — so the
pair's rich-line hypergraph *is* a partial linear space. The failure is in **degree**, not in regularity in
general, and the double count needs degree ≤ 2.

**(c) polynomial identity: the strongest technical content in Q7, and it is a structural negative.**
For three distinct points `(a, c/a), (b, c/b), (d, c/d)` of `xy = c`, the collinearity determinant is
`c(b−a)(d−a)(d−b)/(abd)` — re-derived independently and correct. Since c, a, b, d are nonzero mod p, it
vanishes only when two parameters coincide: **no three distinct classes of one modular hyperbola are ever
collinear mod p.** So all one-hyperbola collinearity is a **pure lift phenomenon**, the constraint is never a
group equation on V, and the negative is structural rather than an exhaustion of effort.

**(a) transitive group action: absent, and the one place it exists is dominated.** The affine symmetry group of
P₋₁ in the box has order 2–4 (§1 MC5), and the Klein four-group acts on classes without lifting. The only
genuine transitive action in the system is `(Z/2)^{p−1}` on orientations of the vertical-pair model — which
is exactly the model whose ceiling is 4(p−1) − c·p/log p.

**(d) duality / magic-function LP in a changed variable space: the only family in the table not provably
capped by LP over lines, and the reason it still fails is (a).** Delsarte works because the Fourier transform
diagonalises a group action; with |Aut| = 2–4 there is no transform to change variables by. Its proposed cheap
diagnostic (odd-cycle inequalities on the conflict graph) is a Chvátal–Gomory rank-1 cut on a system whose
rank-1 closure is already almost the LP (the project measured `IP(1) = LP(1) − O(1)` for p ≤ 59, and the
strongest integral cuts available from the now-proved orbit theorem move the LP by exactly 0).

**(e) exchange / compression: absent, and the reason is checkable rather than impressionistic.** Every
classical device is validated on a *bounded window* and needs a closure property this system lacks: Dyson's
e-transform needs translation-closure (Vosper/Kneser/Freiman live in Z_p; the box is not translation-closed);
Frankl (i,j)-shifting needs the forbidden configuration preserved by the shift, but moving a point inside its
row destroys and creates collinearities on Θ(p) lines of other slopes; Zykov symmetrization needs
non-adjacency to be transitive; Kruskal–Katona needs a colex order on a shadow. The devices whose validity
*is* global are the min–max ones (Hall/König/Gallai–Edmonds), and they convert the exchange into exactly the
transversal number τ that H4(i) measures at 0.45–0.53|H(−1)| — off by a factor ≈ 2. Separately, **every
stability theorem in the literature is a statement at deficiency o(max)**: Segre/Ball–Lavrauw need an arc of
size ≥ q−√q+7/2 (deficiency O(√q)); Voloch's threshold is (44/45)q+8/9 (2.2% of the maximum); the sharpest
Ahlswede–Khachatrian stability (Ellis–Keller–Lifshitz) is stated for `|F| ≥ f(n,k,t) − O(·)` and only "if k/n
is bounded away from 0 and 1/2". The single classical stability theorem tolerating a **linear** deficiency is
Freiman 3k−4, and it pays with a conclusion whose container grows with the deficiency (an AP of length k+r) —
exactly the useless shape our sharp lemma has at t = Θ(p). **The literature has no precedent for what H4
needs, and the pattern of why is uniform.** The structural reason no bounded-window certificate can be
validated: gluing the two hyperbolae takes a totally decomposable constraint system (max component size 8,
p-independent) to a **single connected one** (one component covering 100% of the 8(p−1) points at every p
from 11 to 61).

### (iii) The re-ranked table, and one card killed

| row | (a) group | (b) near-partition | (c) identity | (d) LP/magic | (e) exchange | (f) unique extremal | closed? |
|---|---|---|---|---|---|---|---|
| ovals in PG(2,q), q odd | yes | yes (q+1 lines through each point partition) | Segre's lemma of tangents | — | — | yes (conic) | **yes** |
| hyperovals, q even | yes | yes | Qvist nucleus | — | +1 exchange | **no** (many hyperovals) | **yes** |
| maximal arcs, q odd | yes | yes | BBM polynomial argument | — | — | n/a (none exist) | **yes** |
| Kakeya AG(2,q), q odd | yes | yes (Faber's identity) | Segre + Jamison–Brouwer–Schrijver | — | — | yes (dual oval + line) | **yes** |
| Kakeya AG(2,q), q even | yes | yes | — | — | — | **no** (dual hyperovals) | **yes** |
| collinear triples in permutations | yes | yes (saturated parallel classes) | Faber's identity | — | — | ELFTPs (a family) | **yes** |
| sum-free in Z_p | yes | — | Cauchy–Davenport | — | Vosper | **no** (2–3 families) | **yes** |
| MDS for prime fields | yes | yes | Segre's lemma of tangents | — | — | yes | **yes** |
| kissing numbers, dims 8/24 | yes | — | — | **yes** (Delsarte sharp) | — | yes | **yes** |
| no-(k+1)-in-line, k ≥ 3 | **no** | **no** | **no** | **no** | **no** | **no** | **yes** (random + nibble; upper bound was trivial) |
| Sidon √N + O(1) | yes | — | — | — | — | ? | **no** (constant only) |
| Turán (3,4) | — | — | — | flag SDP plateaus 0.5617 vs 5/9 | — | ? | **no** |
| cap sets | yes | — | slice rank | — | — | ? | **no** (2.756 vs 2.218) |
| no-three-in-line in [N]² | **no** | **no** | **no** | **no** | **no** | ? | **no** |
| **our pair, one hyperbola** | Klein on classes | **yes** (degree ≤ 2, `Z+2\|L\| = 3(p−1)`) | **no** (lift phenomenon) | LP tight, gap 0 | — | rigid generic + 9^s | **yes** (3(p−1)) |
| **our pair, both** | order 2–4 on the box | **no** (degree 9–19) | **no** | LP floor ≈ 3.40 | τ off by 2× | 39 maxima at p = 11 | **no** |

`P(the table as an instrument) = 0.85 → 0.65`: the two core verdicts survive, but four rows have attribution
defects and one highly relevant SOLVED row was missing.

**KILLED: the "Segre / Voloch / Ball–Lavrauw stability" card, on redundancy.** Its actual deliverable was
"H3 should be reclassified from hole to available", and the project proved it at note version v1.12
(`prop:stability`), with the orbit-wise verification the card proposed as future work already run over all
orbits of all p ≤ 31 (`slack/t221/orbit_decomp_one.py`, `slack/t221/orbit_stability.py`). The card also
concedes that the Segre mechanism itself does not transfer (it needs projective, not affine, geometry).
**P = 0.10 → 0.** Note also that the brief's own description of the paper as v1.9/1.10 is stale: it is at
v1.13.

### (iv) Negative findings

- **`holes.py` has no status field** (`GAP-F-07`), which is why a closed hole kept being shipped to external
  researchers as open. This is the single cheapest process fix in the whole exercise.
- **Nothing is known about the harder half of Green's programme** — "the reduction to a curve happens at
  all". Its residue-level shadow is Green's own **Problem 68** ("Suppose that A ⊂ F_p² is a set meeting every
  line in at most 2 points. Is it true that all except o(p) points of A lie on a cubic curve?"), open, with
  only Voloch's (44/45)p+8/9 and Ball–Lavrauw's q−√q+7/2 as unconditional structure results — both far above
  the density where it matters. And there is a **counter-signal**: the neighbouring case k ≥ 3 was resolved
  *without algebra*. So neither of the project's two candidate targets proves HJSW optimal, and the algebraic-
  rigidity intuition behind the structural half has one nearby disconfirmation.
- **The literature's pattern, stated honestly:** every solved row in the table above was closed either by a
  near-partition double count with an exact identity (rows 1–8), or by a two-dimensional LP miracle (row 9),
  or by randomness against a trivial upper bound (row 10). Our pair has none of the three, and the third is
  unavailable because our open direction is the upper bound.

---

## 8. Adversarial review — the FATAL and SERIOUS attacks, grouped

Three lenses were run independently (arithmetic/analytic; combinatorial/integrality-gap; structural/stability).
Their attacks fall into eight groups. For each: what it kills, and what would have to be true to survive it.

### A. FATAL — the union-bound / scale wall (arithmetic lens)

**Kills:** Q3-MC4; the operational half of Q3-MC1 and `holes.py` H5's own "testable now" ("measure λ_min of C
restricted to large scales"); Q6-MC5's H7 payoff; and the effective range of the block certificate.

**The attack.** The p^{1/4} threshold that killed the spectral route is not primarily a *Burgess* threshold —
it is a **union-bound** threshold, and it is the same number for an unrelated reason. At scale S the system
carries ≍ S² families; every Weil-level fact about one object costs error √p·log^c p; the main term per dyadic
scale is ≍ p; so error < main ⟺ **S ≪ p^{1/4}**. Burgess's own floor for prime moduli is also p^{1/4}
(unimproved since 1962, verified across seven independent settings in this pass). Per-object rigour and
cross-object cancellation therefore live on complementary, abutting, never-overlapping ranges, and **four
separate surviving cards die at exactly this crossing**. Measured at p = 100003, σ = 17 ≈ p^{1/4}: the
Kloosterman prediction is right to 0.2% (33154 actual against 33218.7) while the Weil error bound is already
**7.6×** the per-family main term; at σ = 142 it is 528.6×. The mass genuinely splits (0.37–0.71 above
p^{1/4}, mean ≈ 0.53), so neither half can be discarded. Independently, the second-order form: the weighted
family sum sits at exactly the random level (|W|/‖w‖₂ = 1.4–2.1 at every p and scale), and since
‖w‖₂/‖w‖₁ ≍ 1/log S, **even a perfect "random level" theorem buys only 1/log p** — precisely the log p growth
of E and not one factor more.

**To survive:** a nontrivial estimate for `Σ_{s₁,s₂≤S} χ(s₁²+s₂²)` at `S = p^{1/4−η}` for fixed η > 0 —
i.e. an improvement of Chang GAFA 2009 Theorem 11 below its own hypothesis; **or** a nontrivial bound for the
incomplete Kloosterman count `#{(u,v) ∈ [−L,L]² : uv ≡ c}` with error `o(L²/p)` at `L = p^{3/4−η}` for a
positive proportion of c. Nothing in the literature touches either, and the obvious rescue
(Shparlinski's average-over-a Theorem 16 + Cauchy–Schwarz) was tested and fails by the factor `√2·√σ/2`.

### B. FATAL — the LP-dual cone (combinatorial lens)

**Kills:** Q6-MC1, MC2's *budget*, MC4; Q5 Cards 1, 4, 5; Q7's near-partition double count; Q4-M2; Q2-Card 6's
charging; the project's own block-decomposition family as a route below its own floor.

**The attack.** Every one of these produces a number that is a nonnegative combination of the constraints
"at most 2 points per line", hence ≥ LP(all). The floor was **remeasured** rather than inherited: over 25
primes 43 ≤ p ≤ 163, LP(all)/(p−1) has mean **3.3960**, min **3.3168**, max 3.5277, with **no trend** toward 3
(p = 113: 3.3633; p = 151: 3.3728; p = 163: 3.3664), consistent with the repo's own recorded 3.348 (p = 71)
and 3.406 (p = 101); LP(1)/(p−1) has mean 3.4674. Two consequences the corpus does not state.
(i) **The brief's "3.45 plateau" is LP(1), not the floor.** The floor is ≈ 3.32–3.40, so the deficit that must
come from outside the LP cone is ≥ 0.32(p−1) = Ω(p) uniformly in p; and the project's *proved* 3.44817 sits
**above** the measured fractional value of a larger constraint system, leaving at most
3.4482 − 3.3168 = 0.13(p−1) of headroom in the whole covering family — a third of what is needed, and that
assumes a perfect proof of the LP value, which nobody has proposed.
(ii) **All three "beat the LP" moves land in the same narrow band:** adding all Θ(p log p) weak lines
*fractionally* buys LP(1) − LP(all) = **0.0714(p−1)** on average; using integrality inside QR-run blocks buys
**0.019–0.039(p−1)** (LP(1) 3.4674 → theorem 3.4482 → limit 3.4286); the level-1 SDP with localizing
constraints buys **0.03–0.07(p−1)**. Three structurally independent mechanisms, each worth 0.02–0.07(p−1),
against **0.40(p−1) needed**. This is the quantitative content of the project's own phenomenon, and it is a
better headline for the note than any individual negative. "Individually worthless but jointly carrying the
whole truth" is exactly right, and the quantitative form is: jointly and *linearly*, the weak lines carry 18%
of it.

**To survive:** a certificate that couples at least two weak lines — equivalently, that is consistent across
≥ 4 quads simultaneously (§10.1 makes this requirement exact). No proposal in the corpus does.

### C. FATAL — H3 is LP-invisible (structural lens)

**Kills:** the entire stability family as an input to a certificate — Q2 Cards 1, 5, 6; Q7's Segre card;
Q5 Card 1's stability analogue; and the update's own framing "a stability theorem now EXISTS".

**The attack.** Adding the sharpest linear content of Lemma `orbopt` to LP(all) changes the value by **exactly
zero** at every prime 11 ≤ p ≤ 61, with **no cut even active** (details in §2(iv)). And the reduction
`|S| ≤ K + t₁ + t₂` is self-defeating as an identity: `t₁ + t₂ = 6(p−1) − |S|` forces `K ≤ 6C = O(1)` while
`K ≥ 3(p−1)`, and the measured `K` = 30, 36, 52, 54 at p = 11…19 against a requirement of 12, 24, 36, 30 —
a Θ(p) gap. The sharp form of the lemma makes it *worse*, not better. Finally, at the densities where α is
attained the lemma degenerates into a statement true of **every** subset of H₁: since every component of H₁'s
rich-line hypergraph is an 8-point gadget whose 6-point maximum is unique with complement exactly its 2 MID
points, `S \ M ⊆ MID` for every S ⊆ H₁ whatsoever, so `min_M|S\M| ≤ |MID| = p−1−2s` is a fact about H₁, not
about S. The informative branch is active only when `|S₁| > 2(p−1)+2s`, and since `|S₁|+|S₂| = α ≈ 3(p−1)+C`
at most **one** half can ever be informative, with a doubly-blind window of width ≈ p−1 in which neither is —
and the exact involution R forces the maximal-gain plateau to be symmetric about the centre of that window.
The killer detail, at p = 11 with proven-optimal witnesses: α = 32 is attained at |S₁| = 16, 20, 22, 25, and
at |S₁| = 20 and 22 the witness has `|S₁ ∩ MID| = 0`, i.e. **S₁ is literally a subset of a rigid maximum M —
distance zero, the strongest conclusion any stability theorem could deliver — and the bound still fails**,
because `max lawful inside M ∪ R(M) = 30 < 32`. Independently: `max{|S| : S₁ ⊆ some maximum M}` = 32 (= α,
proven optimal) at p = 11, 39 (= α−1, proven optimal) at p = 13, ≥ 53 at p = 17, ≥ 56 at p = 19 — so assuming
the perfect stability conclusion costs 0, 1, ≤ 1, ≤ 3 and leaves a residual problem that is still 3(p−1)+Θ(1)
and still open.

**To survive:** exhibit any valid inequality derived from `prop:stability` that is **violated** by the LP(all)
optimum. The two natural families (per-orbit caps, per-hyperbola caps) are slack by 30–60%.

### D. FATAL — the locality budget, and one over-reach to withdraw

**Kills:** every fixed-locality mechanism (Q1-MC4's locality half, Q4-M5, Q1-MC2 at fixed level, Q6-MC4).
**Withdraws:** `section_blocks` remark (d)'s generalisation from orbits to blocks (§6(iii)).
**The attack and the data** are in §6(iii): k = 1 gives exactly 4.0000(p−1); k = 3 still gives ≥ 3.5556(p−1),
worse than the proved 3.44817 while coupling more than half the instance. **To survive:** exhibit a partition
into blocks of size ≤ B with `Σ_blocks α(block) < 3.4(p−1)` for some bounded B. **To make the negative
publishable:** compute `Σ_blocks α(block)` for partitions into 2, 3, 4 consecutive QR-runs (B ≈ 64–256) at
p = 101, 199, 401 and report it as a **rate** statement. The rate has never been measured, and asserting the
in-principle impossibility without it is the fabrication risk the project has been burned by.

### E. FATAL — flag algebras / local limits, dead in both categories

**Kills:** Q1-MC4, Q7's flag-algebra branch, H2. Dense limit is null; the bounded-degree local–global category
does not contain the sequence; degrees are not near-regular; and even in the bounded-degree world Elek's
theorem says the independence ratio is not testable, so a finite-radius statistic could not pin the value
anyway. Numbers in §1(ii) MC4. **To survive:** exhibit a rescaled limit object explicitly and verify one
averaging identity (e.g. `d(F) = Σ_G d(F,G)d(G)`) on it. With unbounded degrees and a direction spectrum
spread over Θ(p) scales there is no candidate object.

### F. SERIOUS — misimported pessimism, in the project's favour

Barak–Chan–Kothari is irrelevant (§1(iv)). The sparse/ultra-sparse SoS lower bounds are **vacuous** here: they
lower-bound SoS by ≈ n/8 = 1.0(p−1), far below the 3(p−1) target, and our independence ratio is 0.375 constant
against a random 3-graph's decaying √(log d/d) = 0.352 → 0.252. **So no published SoS lower bound rules out
level 2 or level 4 here.** The delicacy worth naming: the global divergence is slow — a factor 1.5 at p = 401,
growing like √(log p/log log p) — so at every computationally accessible prime the instance looks random-like
even globally, which is exactly why the analogy is seductive and why it must be stated with these numbers
rather than as a slogan. **To survive as pessimism:** state the value the cited theorem lower-bounds SoS by, in
units of (p−1); below 3, the citation is decorative.

### G. SERIOUS — pricing against the wrong target

Ordered by what a *perfect* execution would yield: Q1-MC3 + all of Q3 → 4(p−1) − c·p/log p (the model's own
ceiling, `pair_bound_notes` line 585); Q6-MC1 → 7.0–7.5(p−1); Q5 Cards 1/4/5 → no bound in the box at all;
Q2 Cards 2–5, Q4 M1/M3/M4/M6, Q6 MC4/MC6 → negatives. **Every one is at or above the already-proved 3.4482.**
The only cards whose perfect execution would land below the state of the art are the genuine level-2 lift
(value unknown, never run) and, at one remove, an extension of the block method that absorbs the mixed
3-point lines. **To survive:** add a required field to every mechanism card — *"value in units of (p−1) if the
card works perfectly"* — and stop probability-ranking anything ≥ 3.4482 against T1.

### H. SERIOUS — calibration errors inside the brief, inherited by every ranked list

(i) 3.45 is LP(1); the floor is 3.32–3.40, and the proved 3.44817 is above the measured LP(all).
(ii) H4 ⇔ H7 ⇔ T1 with no loss in the constant, so any Q2/Q5 "transfer" is a complete solution — the brief
ships both as fillable holes with "testable now" experiments, and Q2 and Q5 are generated from them.
(iii) The gain sequence: for k = −1 (the frame both modules declare) the gains are **2, 4, 6, 5** — monotone
through p = 17, spread 4, failing `phenomenon.py`'s own S4 criterion (spread ≤ 3); over all k they are
5, 5, 6, 5, which is what the published conjecture is about; the brief's one-paragraph summary conflated the
two columns of `sec:beyond`.
(iv) All eight holes are upper-side and nothing guards `gain = O(1)`.
(v) `phenomenon.py`'s diagnostic cannot detect its own subject: `Signature` has no field for the integer
optimum, so the integrality gap — the definition in §0 — is not representable; S2 measures LP(all)/LP(strong),
which is equally high when LP is blind and when there is nothing to be blind to; `Strength` has no third value
and `verdict()` no third outcome, so "the phenomenon is absent here" is unsayable. **The instrument must be
repaired before it is shipped to anyone else.**

### Withdrawals — claims killed by these reviews and NOT to be reused

1. "Exponentially many extremals is fatal, unlike Segre's unique conic" — **wrong in both directions**, §2(iv).
2. "The box destroys the affine-plane counting by a factor p, and I measured it two ways" — both measurements
   unsound, §5(iv). The conclusion survives via the direction count.
3. "All finite-field incidence bounds are the wrong direction and cannot be fixed" — refuted by
   Chen–Liu–Nie–Zeng, §5(i).
4. "H4's inequality is FALSE by Ω(p)" — category error; levels 0/1 are strict relaxations, §2(ii) Card 5.
5. "B.13's slope-4-to-5 was not an artefact of moment counting" — backwards; the true slope is 1.9–2.5.
6. "Barak–Chan–Kothari kills any hope of a general theorem that level 2 sees triples" — irrelevant objective.
7. `section_blocks` remark (d)'s block clause — over-reach, §6(iii).
8. Q3-MC2's counterfactual thresholds and its doubling numbers; Q4-M2's "converts into a theorem for all p";
   Q6-MC3's Bose half; Q5-Card-2's 0.85 and its Green-Problem-72 claim.

---

## 9. Opposing theses

Two theses were developed independently against the project's programme. They are stated fairly, each with a
falsifiable prediction. **They are not averaged: they disagree about what the truth is, and agree only about
which experiment to run first — which is precisely why that experiment is ranked #1 in §11.**

### Thesis A — the target is mis-specified downward: α = (c + o(1))(p−1) with c ≈ 3.3, and the integrality gap is o(p)

**Statement.** "α = 3(p−1) + O(1)" is not a datum but a conjecture fitted to four integers. The defining
quantity — the integrality gap LP(all) − α — has been measured at exactly four primes, is exactly **zero** at
the smallest, and has never been measured above p = 19. The simpler competing reading is that
α(P₋₁) = (c+o(1))(p−1) with c ≈ 3.3, the full-LP gap is o(p), the weak three-point lines are **not** jointly
producing a linear gap, and the "3.45 plateau" is not blindness but nearly the answer — under which the
already-proved 3.448(p−1) is within ≈ 5% of the truth, H4 and H7 are not holes but **false statements**, and
all eight holes are a wall around the wrong building.

**Evidence.** (1) `certificate_hierarchy.md` is the only table where α and LP(all) coexist: p = 11 → 32 vs
32.00 (gap **0.00**), 13 → 40 vs 44.80, 17 → 54 vs 60.15, 19 → 59 vs 63.64; in units of (p−1) the gaps are
0, 0.400, 0.384, 0.258 — **falling across the last three, zero at the first**. (2) Least squares on the frame's
own k = −1 gains (2, 4, 6, 5 at p−1 = 10, 12, 16, 18): constant SSE 8.750; c·log n 5.330; c·√n 4.636;
c·n/log n 4.058; **c·n 2.704 with c = 0.3083 ⇒ α ≈ 3.308(p−1)** — the project's conjectured model is the worst
of five, and 3.308 sits squarely inside the measured LP(all) band. (3) 3(p−1) has no structural presence in the
extremal sets: §2's optimal splits are 15+18, 23+18, 19+35, 30+29 — balanced, with no half near its own
hyperbola's optimum, and the notes say it outright ("maximum sets are not 'core minus O(1)'"). So the equality
"3(p−1) = one hyperbola's maximum" is arithmetic coincidence, which is exactly why H4(ii) found stability
useless. (4) Principle P4 is **false for the pair**: the union at p = 11 has **39** maxima (exhaustively
enumerated; 39 = 3·13, no algebraic form) and removing one point from a maximum already permits a lawful
31-point set at distance ≥ **13** out of 31 from *every* maximum — against D(t) = t exactly for one hyperbola.
(5) The apparent flatness past p = 19 is a **search artifact**: `slack/witnesses/` stops at p = 23; the best
known lower bounds at p = 29 and 31 are 84 = 3(p−1)+0 and 91 = 3(p−1)+1, both from a light pass capped at
t ≤ 10 and ≈ 12 s/t whose own report says the interesting regime is "t ≈ 20–40, which we did not reach".
(6) `pair_bound_notes` §6 still lists (T4) — "construction with gain ω(1)" — as **open**, and the project's own
audit records that all eight holes are upper-side.

**Honest concessions the thesis makes.** The max-over-k sequence 5, 5, 6, 5 **is** flat and the constant fits
it best (SSE 0.75 vs 4.67), and that is the sequence the published conjecture is about. The one-hyperbola
theorem is exact, so the thesis requires the second hyperbola to buy Θ(p) — a substantive claim. And the gaps
0.400 and 0.384 at p = 13, 17 are not small; if they persist, c ≈ 3.05 and the project is right. The thesis is
not "c = 3.3"; it is "the evidence supports c ∈ [3.0, 3.45] roughly uniformly, and the project has assigned
probability ≈ 1 to the endpoint."

**Falsifiable prediction.** A one-sided witness ladder at p = 29, 31, 37, 41 (≤ 320 binaries, ≈ 1000–1250 rich
lines — smaller than instances the repo already solves), asking pure **feasibility** for
`|S| = 3(p−1) + g`, g = 7, 9, 11, 13, seeded in the balanced regime t ≈ (p−1)/2 to 2(p−1)/3 that
`exchange_test_report` §3 explicitly never reached, using LNS/annealing rather than branch-and-bound.
*Project's thesis predicts:* UNSAT at g = 7 for every p. *Thesis A predicts:* SAT at g = 7 for every p ≥ 29,
with best-found gains ≈ 9, 9, 11, 12 at p = 29, 31, 37, 41. Cheapest single decisive call: **p = 41, target
|S| = 127 out of |V| = 320.** Secondary, cheaper: close the p = 23 bracket exactly — α(23) ∈ {73, 74} kills the
conjecture immediately.

### Thesis B — the target is right but the precision is unaskable: demote the pair to the union case of Conjecture G at o(p)

**Statement.** Nothing downstream needs the O(1). Green's Problem-72 comment asks for a precise conjecture that
curves reducing mod p cannot beat HJSW, i.e. α ≤ (3/2+o(1))N = 3p + o(p); the project's own Conjecture G is
stated with o_d(1). The pair, as a reducible quartic, **is** on the critical path of G — that is the one real
hole the eight-item list omits — but at o(p), not O(1). Between 3p+o(p) and 3(p−1)+O(1) there is a factor of p
of unclaimed slack the project is voluntarily forgoing. H1–H8 are holes in a wall around that mis-specified
target: two of them (H4, H7) are the target restated, two are now closed, and the four survivors carry
post-verification transfer probabilities ≤ 0.08.

**Evidence.** (1) The O(1) is **below the project's own resolution**: every route that converts structure into
a constant passes through a √p·polylog equidistribution step (m₈ asymptotics via Bombieri + Selberg,
O(√p log⁴p); the block-signature densities behind 3.4482; the family counts of I1/I3; the G3.3 Weil-in-boxes
lemma), and none of these can ever produce an O(1) statement — while the purely combinatorial routes that could
are now *proved* exhausted. So the O(1) target sits precisely in the gap between what the analytic tools can
resolve and what the combinatorial tools can reach. (2) The premise is undecided at the very next prime:
α(23) is bracketed 69–74 and the conjecture's bound is 3(p−1)+6 = 72, so 73 or 74 refutes it. (3) **Revealed
productivity:** in a single documented session the curve programme produced the all-k theorem (v1.4), the
projection bound `α ≤ 4·min(|π_x C|, |π_y C|)`, G3 (cubic-graph structure), and G3.5 — "no cubic graph beats
HJSW", `α ≤ (11/8 + o(1))N` for **every** cubic graph in **every** 2p×2p box, proved by a ±1-line cover with
exactly interfaces I1 and I4; over the same period the pair programme moved a constant
4 → 11/3 → 115/32 → 3.4616 → 3.4482 and produced a proof that its own mechanism class is closed. The project's
own pre-registered odds read "D (new idea for 3(p−1)+O(1)): <10% per week, cost open" against goal G, delivered
the same morning as C. (4) A general bounded-degree theorem is **not free but is a ladder with computable
rungs**: the projection bound plus Chebotarev/Lang–Weil gives `α ≤ 4(1−δ)p` with δ the derangement proportion
of the monodromy of a coordinate projection, and by Cameron–Cohen δ ≥ 1/d in any transitive group of degree d
with equality iff sharply 2-transitive; hence α ≤ 3p iff both projection degrees are ≤ 4. So I1+I4+Chebotarev
settle Conjecture G for every irreducible curve whose two projections have degree in [2,4]; the residue is
(a) graphs of permutation polynomials/rational functions of bounded degree — where G3.5's ±1-line cover method
already works — and (b) a thin, explicitly Galois-characterised family with both projections of degree ≥ 5 and
derangement proportion < 1/4.

**Honest concessions.** The o(p) relaxation does **not** by itself unlock a known mechanism: LP(all) is
*trending up* (3.348 at p = 71 → 3.406 at p = 101), so covers cap near 3.44 asymptotically and cannot reach
3+o(1) either. Both targets need the same missing global argument, which kills the cleanest version of the
thesis and reduces it to a comparative/opportunity-cost argument. And the harder half of Green's programme —
that the reduction to a curve happens at all — is untouched, is itself Green's open Problem 68, and has a
counter-signal: for k ≥ 3 the answer was obtained *without algebra*. So neither target proves HJSW optimal.

**Falsifiable prediction.** *Primary:* settle α(23). If α(23) ≥ 73 the "gain ≤ 6" conjecture is false, the
k = −1 gain sequence reads 2, 4, 6, 5, ≥ 7 with no bounded pattern, and every one of H1–H8 is a hole in a wall
around a premise the data reject — Thesis B wins outright and the correct target becomes (3+o(1))(p−1). If
α(23) ≤ 72 and p = 29 also gives gain ≤ 6, the O(1) premise survives its first real test and Thesis B is
reduced to the opportunity-cost argument alone. Calibrated bet: **P(α(23) ≥ 73) ≈ 0.4**; P(gain ≤ 6 at both 23
and 29) ≈ 0.45. *Secondary:* for absolutely irreducible plane curves C/F_p of degree 3–6 at p ≈ 10⁴–10⁵,
compute `δ(C) = 4·min(|π_x C(F_p)|, |π_y C(F_p)|)/p`, and in parallel LP(all)/(2p) at p ≤ 200 for
(i) H(1)∪H(−1) in the HJSW box, (ii) the same in randomly shifted boxes, (iii) H(1) ∪ a cubic graph,
(iv) unions of two permutation-polynomial graphs. Thesis B predicts δ(C) < 3 for every C except permutation
polynomials/rational functions and a thin degree-≥5 family — i.e. Cameron–Cohen is the true difficulty grading
and the general theorem is a finite, gradeable programme — and predicts the HJSW pair is an **isolated** hard
instance (LP(all)/(2p) ≈ 1.7 there, ≤ 1.4 for the generic unions). If instead a positive proportion of
degree-3–6 curves has δ ≥ 3, or every union of two bi-surjective curves sits at LP ≈ 1.7 with truth 1.5, then
the pair is the *generic* hard case of Conjecture G, closing it **is** the general mechanism, and Thesis B loses.

### Where they disagree, explicitly

| | Thesis A | Thesis B |
|---|---|---|
| the truth | α ≈ 3.3(p−1); gap is o(p) | α = 3(p−1)+O(1), as the project believes |
| what 3.44 means | nearly the answer | a real plateau far above the truth |
| H4/H7 | candidate **false statements** | true but equal to the target, hence not holes |
| what to do | test the premise, then re-aim at c ≈ 3.3 | keep the theorem, drop the precision, retarget to Conjecture G at o(p) |
| if α(23) ≤ 72 and gain(29) ≤ 6 | thesis is reduced to nothing | thesis survives on opportunity cost |
| if α(23) ≥ 73 | wins outright | wins outright |

They agree on nothing about the mathematics and everything about the next computation. That is the strongest
available argument for running it.

---

## 10. Counter-proposals — the ones that survived

Four sets of counter-proposals were produced (identity/exact-structure, computational/empirical,
reformulation). What follows is what survived the reviews, with the hardest step named. Killed and not
resurrected: the multiplier-coset block idea (P ≈ 0.04, and almost certainly false — small multiplier order and
small family size are two independent arithmetic coincidences); and everything in §8's FATAL groups.

### 10.1 Quad transversality and the block-collapse theorem — the strongest surviving item

**Statement.** For `a ∈ F_p^*/{±1}` put `Q_a := {κ_a, μ_a, κ_{−a}, μ_{−a}}`, where `κ_b = (b, 1/b) ∈ H(1)` and
`μ_b = (b, −1/b) ∈ H(−1)`; `|Q_a| = 16`.
**(a) IDENTITY.** The (p−1)/2 quads partition P₋₁; the 4 rows and 4 columns of the box meeting `Q_a` meet no
other point of P₋₁. Hence `|S ∩ Q_a| ≤ 8` for every lawful S, `Σ_a 8 = 4(p−1)`, `6·(p−1)/2 = 3(p−1)` exactly,
and **`α(P₋₁) = 3(p−1) + max_{S lawful} Σ_a (|S ∩ Q_a| − 6)`** — T1 is literally "the total quad excess is
O(1)", with the trivial bound being exactly 8 per quad.
**(b) TRANSVERSALITY.** If a line ℓ meets P₋₁ in ≥ 3 points lying in ≥ 3 distinct classes, then ℓ meets every
quad in at most one point, **unless** the symmetric quadruple `q + {0, s₁, s₂, s₁+s₂}D` of B.15 attached to ℓ
satisfies `s₁² + s₂² ≡ 0 (mod p)`; in that case p ≡ 1 (mod 4), exactly one pair of points of ℓ shares a quad,
and that pair lies on a single hyperbola in the ν-related classes `κ_a, κ_{−a}`. The number of such
exceptional lines is O(1) — measured **0 at every one of p = 11, 19, 23, 31, 43, 47, 71, 103** (all ≡ 3 mod 4)
and 14–64 at every one of p = 13, 17, 29, 37, 41, 53, 61, 73, 89, 97, 101, 109 (all ≡ 1 mod 4), with **100%**
of the exceptional same-quad pairs on one hyperbola in ν-related classes, exactly as the algebra predicts.
**(c) BLOCK COLLAPSE.** For any partition B of P₋₁ let V(B) be the value of the block-local-consistency lift
(a distribution over lawful subsets per block, plus for each line a joint distribution over the states of the
blocks it meets, consistent with the marginals and supported on `|·∩ℓ| ≤ 2`). For every line ℓ meeting each
block in at most one point, the lift's constraint at ℓ is **equivalent to the single linear inequality
`Σ_{q∈ℓ} x_q ≤ 2`**. Hence, for the quad partition, the 3-point weak lines contribute to any such lift exactly
their LP inequality and nothing more: **all the extra strength of any block certificate comes from rows,
columns and ±1 lines.** No certificate in this family — §30's component decomposition, §17's QR-run block
theorem (3.44817), or any Sherali–Adams/Lasserre lift indexed by unions of quads with per-line block
consistency — can exploit the integrality of the weak system; in particular §30's declared "main open
technical task" (the transfer-matrix DP along the neighbour chain) is **capped at the rich-line value ≈ 3.44
and is not a route to 3(p−1)**.

**Proof sketch.** (a) `κ_a` and `μ_a` share the column pair `{X(a), X(a)+p}`; `κ_a` and `μ_{−a}` share the row
pair; so the four classes close under both the row- and column-partner maps, and the class graph of §29 for
k = −1 (cycles of length 2·ord(−1) = 4) *is* the quad. Each of the 4 rows and 4 columns carries 4 points, all
inside `Q_a`; a row of 4 collinear points forces ≤ 2, and summing over the 4 columns gives ≤ 8.
(b) By B.15 the points of ℓ lie at `q + tD`, `t ∈ {0, s₁, s₂, s₁+s₂}`, with x-residues `u(z+t)` where z is a
root of `z² + (s₁+s₂)z + s₁s₂/2 = 0` (discriminant `s₁²+s₂²`). Two points share a quad iff their x-residues
sum to 0, i.e. `2z + t_i + t_j ≡ 0`. Substituting the six pairs into the quadratic gives `−s₁²/4`, `−s₂²/4`,
`−(s₁²+s₂²)/4`; the first four force `s₁ ≡ 0` or `s₂ ≡ 0 (mod p)`, i.e. two lifts of the *same* class, excluded
by hypothesis. Only `s₁²+s₂² ≡ 0` survives, which needs −1 to be a QR. In the surviving cases the shared pair
is `{0, s₁+s₂}` or `{s₁, s₂}`, and in the sign pattern (e, −e, −e, e) both members carry the same sign, so the
pair lies on one hyperbola in a ν-pair. O(1) count: `s₂ ≡ ±i s₁` defines a rank-2 lattice of determinant p, so
by Minkowski its shortest vector has `s₁+s₂ ≳ c√p`, and the quadruple fits the box only if
`(s₁+s₂)·|D|_∞ ≲ 2p`, leaving O(1) admissible directions per admissible pair.
(c) **Coupling lemma** (elementary, and absent from the notes): three events with prescribed marginals
`p₁, p₂, p₃` admit a coupling with empty triple intersection **iff `p₁+p₂+p₃ ≤ 2`**. Necessity is Bonferroni;
sufficiency places arcs of lengths `p₁, p₂, p₃` consecutively on a circle of circumference 1 starting at
0, p₁, p₁+p₂ — consecutive arcs are disjoint whenever the total length is ≤ 2. Lift the event coupling to block
states by sampling conditionally independently inside each of the eight event/complement cells.

**Why it was not already tried.** The project owns every ingredient but has never combined them. B.15
classifies the mixed patterns as symmetric quadruples and even flags the `s₁²+s₂² ≡ 0` families as special
(its p ≡ 1 mod 4 examples 21²+74² = 61·97 and 80²+111² = 97·193), but only to explain the fluctuations of E(p)
analytically; nobody asked whether a quadruple can meet a row/column block twice. §30 FACT 2 and REPORT §17
assert block closure only for the **rich** lines and are silent about weak lines. H4(iii) measured one instance
of the consequence (max 16 inside a 32-point orbit union, which is exactly `Q_a ∪ Q_{1/a}`) as an observation,
not a theorem, with no statement about which lifts it kills. And the coupling lemma is what turns the
observation into a proof — it also explains, post hoc, why the level-1 SDP with localization closes only 7–17%
and why the block constant converged to 3.4413 rather than descending.

**Hardest step.** Two narrow residual pieces. (1) Turning (c) into a *numerical* impossibility rather than a
structural one: the argument shows the lift cannot see weak-line integrality, but to assert `V(B) > 3(p−1)` one
must additionally exhibit a feasible lift point of value > 3(p−1) (e.g. block marginals supported on a mixture
of near-maximum block states whose point marginals satisfy every weak-line inequality) — a construction, not a
new idea, but not free. (2) For **coarser** blocks (unions of k quads) transversality can fail because two of a
weak line's three quads may sit in the same block; the collapse then applies only to the block-transversal weak
lines, and one must show the non-transversal fraction → 0 (heuristically ≈ 3(k/N)² with N = (p−1)/2, i.e. ≈ 2%
for §30's components at p = 101).

**P(the lemma and the collapse go through as stated) ≈ 0.8. P(it yields a bound below 3.4482) = 0** — it is a
proof of impossibility plus a sharpened statement of the target, which is exactly its value.

**Two exact negatives it produced en route, both worth committing.** (1) The ρ-involution fold is dead
(§2(iv)). (2) The spanned-directions identity of B.12(iv)/GAP-H-03 is provably vacuous (§2(iv)).

### 10.2 Certified lower bounds on gain(p) up to p ≈ 150

**Statement.** Either exhibit a certified lawful `S ⊆ P_k` with `|S| ≥ 3(p−1)+7` for some p ≤ 150, refuting the
note's own falsifiable conjecture; or establish `max_{p ≤ 150} gain(p) ≤ 6` with witnesses, together with the
first structural data on near-optimal sets in the middle regime a ≈ b ≈ 1.5(p−1).

**Why it was not already tried.** It was explicitly declined (THREAD [188]: "проверка гипотезы … но это ЦП без
нового знания"). That judgement is wrong on three counts: the premise is guarded by nothing; the *tool* was
wrong rather than the question (the note records "CP-SAT 12 h: 70 (bound 78); MIP 8 h: 70 (bound 74)" at p = 23
and "CP-SAT 8 h: 84 (bound 92)" at p = 29 — twenty CPU-hours of generic branch-and-bound that at p = 29 did not
even beat 3(p−1), whereas *finding* good feasible sets is vastly cheaper than proving optimality); and there is
not a single known near-optimal configuration for p > 23 to look at, so **the witnesses are the missing
structural data** that H4(ii)/[187] says is all that remains.

**Engines, both measured.** (1) *Single-involution symmetry reduction:* restricting to sets invariant under
**one** involution halves the variables to 4(p−1) and costs only 0–2 points (p = 11: 32 = α for all three;
p = 13: 38/38/**40** — the "xy" involution hits α exactly; p = 17: 52/52/52 vs 54; p = 19: 56/58/56 vs 59).
Do **not** use the full group: measured `α_V − 3(p−1)` = +2, 0, +4, −2, −2, −8, −10, −8, −12 at p = 11…41, i.e.
full invariance loses Θ(p). (2) *LNS in the full space:* free the points of 2–4 QR-run blocks (32–128 points)
or one slope-±1 residue group, re-optimise those exactly with CP-SAT keeping the rest fixed, restart. Each
repair is a 32–128-variable exact solve. Seed from (a) a rigid one-hyperbola maximum, (b) balanced random
starts with `|S∩H(1)| ≈ |S∩H(−1)| ≈ 1.5(p−1)`, (c) the involution-reduced optimum polished in the full space.

**Hardest step.** Making a *failure* mean anything. A witness is trivially certifiable (sweep all lines through
two points of S), so the risk is the opposite one: the pipeline must be calibrated by reproducing the known
α at p = 11…19 within the same per-prime budget, and only primes where it did so may count as evidence for
"gain ≤ 6".

**P(the experiment produces decision-relevant data) ≈ 0.9. P(a witness with gain ≥ 7 is found at p ≤ 41) ≈ 0.25.**

### 10.3 The genuine level-2 lift, priced before it is computed — and the two proposals disagree

**Proposal (compute it).** Lasserre/moment relaxation with index set `I = {∅} ∪ V ∪ {pairs on a common 3-point
line}`, moments `y_S` for |S| ≤ 4, `y_S = 0` whenever S contains a collinear triple, plus box/RLT and line
constraints localized at every pair in I. Sizes measured: `|I|` = 397 / 981 / 1021 / 1485 at p = 13 / 17 / 19 / 23
for the weak-pair index, and 1213 / 1897 / 2405 / 3057 for the full-pair index — one PSD block of side ≤ 2405,
first-order (SCS) territory, hours not days after the order-2 symmetry reduction. **Kill criterion, stated in
advance:** at p = 13, LP(all) = 44.8000, level-1-localized = 43.9974, α = 40; if the verified value stays above
**43.0** (≤ 37.5% of the gap, the same band as level 1's 16.7%), declare the SoS route closed with a number,
correct the level-1/level-2 labelling in three documents, and retire H1.

**Proposal (price it instead).** Reformulate at the right scale: by H4(iii) the problem is exactly a Max-CSP
with `n = (p−1)/4` variables `x_ρ` (one per Klein orbit-pair, alphabet = the lawful configurations of its 32
points), objective `Σ|x_ρ|`, unconstrained value 4(p−1), constraints = the mixed 3-point lines, each touching
2 or 3 orbits; the target is that these force total deficit ≥ (p−1) − O(1), i.e. **one point per orbit out of
16**. The clause density is `m/n = Θ(log n)` with `m = Θ(p log p)` — i.e. **n^{1/2−o(1)} below the ternary
refutation threshold `m/n ≈ n^{k/2−1} = n^{1/2}`** (Raghavendra–Rao–Schramm, arXiv:1605.00058, STOC 2017:
strong refutation of random k-XOR at `m/n ≥ Õ(n^{(k/2−1)(1−δ)})` in `Õ(n^δ)` SoS rounds, matching
Grigoriev/Schoenebeck; polynomial-time SoS fails on random 3-SAT at `m/n = o(√n)`). Prediction: for every fixed
D, degree-D SoS has value ≥ (3.3 − o(1))(p−1), and the genuine level-2 lift will close **under 25%** of the
gap, with the fraction decreasing in p. **First experiment, cheaper than the solve:** build a *parameter-matched
random* instance (same n, same 32-point alphabet, `Θ(p log p)` random ternary constraints, max codegree 6) and
run the existing `slack/t221/sdp_level1.py` on it. If it closes the same 7–17% there, the density explanation is
confirmed and level 2 can be retired **by argument**; if it closes > 40%, the real instance is *harder* than
random for a structural reason worth finding, and level 2 earns its moment variables.

**The disagreement is real and should be resolved in the cheap direction:** run the surrogate first. Note also
that the second proposal's own probability (0.7) was for "the density explanation is right", not for "a better
bound", and the two must not be conflated. **P(level 2 beats 3.4482) ≈ 0.05. P(the surrogate settles the
question without the solve) ≈ 0.6.**

**Hardest step (for the solve).** Bookkeeping plus conditioning: `y_S = 0` must be imposed on every 4-set
containing a collinear triple, and the localizing constraints index `J ∪ {i}` which may leave I — dropping
versus extending changes the relaxation, and an error here silently produces a number that is neither level 1
nor level 2. With 10⁵+ equalities on a ≤ 2405-side cone SCS will return `optimal_inaccurate`, so the reported
gap must exceed the independently verified violation by orders of magnitude (as the level-1 run did: violations
≤ 3·10⁻⁴ against a gap of 0.80).

### 10.4 The null ladder — the missing null hypothesis

**Statement.** Define `N0(p)` = a uniform random 8(p−1)-point subset of the 2p×2p box with exactly 4 points in
every row and column; `N1(p)` = the classes with the Klein pairing and 4-lift structure kept but the
least-residue map `a ↦ X_a` replaced by a uniform odd bijection with positions drawn from I1's polytope law
(the whole-instance extension of `slack/t221/standard_model.py`); `N2(p)` = N1 plus independent Kummer coins for
family presence; `N3` = the real instance. Let `a_k = lim E α(N_k)/(p−1)`. **Conjecture:** `a₀ ∈ [3.40, 3.60]`,
`a₀ > 3.44817 ≥ a₁ ≥ a₂ > a₃ = 3`; the deliverable is the smallest k with `a_k = 3 + O(1)`. **Corollary (trivial
logic, and the usable half):** any certificate valid for every member of `N_k` cannot prove better than `a_k`.

**Why it was not already tried.** The project has **no null model at all** — its own audit records this as a
structural gap (`GAP-F-05`: "there is nothing with which to say the phenomenon is ABSENT here"; `GAP-P-05/06`;
`GAP-T-03/T-04`). Every number in the repo is measured on the real instance, and the only prime-free object it
owns (`standard_model.py`, 24 hours old) was built to tabulate per-signature block savings, not to serve as a
null. Nobody has asked what a random instance with the same box and row/column profile gives — the one question
that separates "LP is blind" from "LP sees exactly the generic part".

**Preliminary measurement, and it is the most consequential number to replicate in this whole document.**
At p = 11, seven samples of `N0` give α = **34, 34, 35, 35, 35, 35, 36**, mean **3.486(p−1)**, range
[3.40, 3.60] — against the true 3.200(p−1) and trivial 4.000(p−1), with triple counts 706–808 matching the real
instance's 704 to within 15%. **The generic value sits essentially on top of the 3.44–3.45 plateau** (proved
3.44817; LP over all lines 3.35–3.41; level-1 SDP 3.49–3.73). One prime, seven samples — **preliminary** — but
if it survives p = 13, 17 it reframes everything: the plateau is not LP weakness, it is the value of the null
model, and no certificate whose validity is preserved by randomizing the instance can beat it. Incidental
confirmation that the null is the harder object: the null MILPs took 50–111 s at p = 11 against ≈ 1 s for the
real instance.

**Hardest step.** The joint law of the position signs across blocks in `N1`. Making positions independent is
tempting and wrong — I1 gives a polytope law with genuine constraints (the descent law of `lemma_run.tex` is
exactly such a law inside a run) — and getting it wrong makes `a₁` meaningless. Concretely, the surrogate must
replace "inversion" by a fixed-point-free involution preserving the Klein relations; choosing it wrongly either
destroys the ±1 rich lines (N1 too easy) or reintroduces arithmetic (N1 = N3).

**P(the ladder produces a decision-relevant `a₀`) ≈ 0.85. P(`a₀` lands in [3.40, 3.60], confirming the plateau
as the generic value) ≈ 0.5.**

### 10.5 Scale localization of the integrality gap — the (|D|_∞, σ) truncation curve

**Statement.** For `IP_L(p)` = the maximum with only lines of primitive direction `|D|_∞ ≤ L`, and `IP^σ_T(p)`
= the same with only triples whose B.15 family has `s₁+s₂ ≤ T`, the loss fraction obeys a scaling law
`g(L,p) → G(L/√p)`: the constraints creating the integrality gap live at the **self-dual scale
`|D|_∞ ≍ σ ≍ √(2p)`**. Either (A) some fixed L ≤ 8, or some σ-window inside the Kloosterman-rigorous range
σ ≤ p^{1/4−ε}, already forces IP < 3.44817(p−1) asymptotically; or (B) for every fixed L,
`liminf IP_L/(p−1) ≥ 3.4`, and the descent uses only directions of size p^θ, θ > 0.

**Measured so far.** p = 11: `IP_1 = 32 = α`, so L* = 1. p = 13 (α = 40, trivial 48): `IP_L` = 48, 44, 42, 42,
**40 = α** for L = 1…5. p = 17 (α = 54, trivial 64): 62, 60, 58, 58, 56, 56, 56, 56, 56 for
L = 1, 2, 3, 4, 5, 6, 7, 8, 10 — and the **last two points need `|D|_∞ ∈ [11,14] ≈ 0.7p`**. Meanwhile `LP_L`
saturates at LP(all) already by L = 7 (60.250 → 60.154 at p = 17): **the whole integrality gap is created layer
by layer in slope-scale while the fractional value does not move.** Dually in B.15's σ coordinate: at p = 13 the
truncation to σ ≤ 6 gives exactly 4(p−1) = 48, and the descent starts only at σ ∈ (6, 8]. So the constraints
carrying the gap sit at the scale that **neither** the rigorous Kloosterman range (σ ≤ p^{1/4}) **nor** the
complete-sum/Weil head (|D|_∞ = O(1)) can count — a measurable explanation of why H5 is the barrier.

**And a proof-technique obstruction, measured.** The graph "two points share a line with ≥ 3 candidates and
`|D|_∞ ≤ L`" has components **exactly equal to the QR-run blocks at L = 1** (sizes 32k — an independent
re-derivation of `thm:blocks`) but **one giant component at L = 2** for every p ∈ {13, 17, 19, 23, 29, 31, 41,
53, 71, 101}. So the finite-table/standard-model technique that produced 3.44817 provably **cannot be reused
above L = 1**.

**Hardest step.** Even in case (A) the local limit does not determine the answer (Elek), so (A)'s honest content
is "a certificate with a finite description exists", not "the limit determines the value". And computationally,
`IP_L` at p = 29, 31 with 1028/1248 lines needs CP-SAT.

**P(case (A), i.e. some L ≤ 8 beats 3.4482) ≈ 0.10.** The evidence so far leans to (B) — which is itself
valuable: it would give a *measured* statement that the answer lives at direction scale Θ(p), the sharpest
available formulation of "all the competition is global", directly citable against every finite-radius
mechanism (H2, H8, flag algebras, manufactured regularity).

### 10.6 Two exact-structure proposals kept at low probability

**Quad excess ledger (P ≈ 0.06).** Aim at a discharging identity `Σ_a (|S∩Q_a| − 6) ≤ C`: classify the
saturated states Σ₈ (2-factors of the fixed 4+4 bipartite graph respecting the internal ±1 lines) and Σ₇
exactly, then prove a saturation-cost lemma charging each unit of excess in a quad with ≥ 7 points to a unit of
deficit in a weak-line-joined quad, with bounded multiplicity. Data it must reproduce: the occupancy profiles
and the saturation ladder of §2(iv). **Hardest step, and it is the same wall:** by §10.1(c) any accounting that
is integral inside quads and linear across them collapses to the LP, so the charging must read at least two weak
lines at once, i.e. span ≥ 4 quads. The easiest version is already dead — the number of simultaneously saturable
quads is *not* O(1) (3/5, 4/6, 6/8 at p = 11, 13, 17, ratio rising).

**Two-copy reformulation on ONE hyperbola (P ≈ 0.06).** Using `ρ(x,y) = (p−x, y)`,
`α(P₋₁) = max{|A|+|B| : A, B ⊆ H, A ∪ ρ(B) lawful}`, and applying `eq:count` to each part gives the exact
identity `|S| = 6(p−1) − Δ(A) − Δ(B)`, so T1 becomes `Δ(A) + Δ(B) ≥ 3(p−1) − C` — a pure lower bound on a sum
of two nonnegative, explicitly orbit-decomposed local defects, with all mixed constraints becoming a single
3-uniform hypergraph on 4(p−1) points whose same-hyperbola part is completely classified. **Hardest step:** the
cross-type edges are orbit-transversal, so §10.1(c) applies and no orbit-local or linear-across-orbits
accounting can force the bound; and the involution shortcut is unavailable (no maximum is ρ-symmetric for
p ≥ 13). Practical dividend regardless: the folded model has half the variables, making near-exact computation
feasible well beyond p = 23 — the ρ-symmetric lower bounds already give gains 2, 2, 4, 4, 0 at p = 11…23 at a
quarter of the cost.

### 10.7 Rigorous Guy–Kelly: the annealed certificate in the block basis (P ≈ 0.07)

**Statement.** With `G_ε(x) = Σ_j g_ε(j)x^j` counting block-lawful subsets of size j of a block of signature ε,
put `Φ(c) = inf_x [−c log x + Σ_{k≥2} 2^{−(k+2)} Σ_ε (D_k(S_ε)/k!) log G_ε(x)]` per (p−1) and `J(c) = c/18`;
target `α ≤ c_ann(p−1) + o(p)` with `c_ann = min{c : Φ(c) < J(c)}`. **Sub-target, worth having on its own: the
CEILING theorem** — no bound of this family can reach any c with `Φ(c) ≥ J(c)`, so the entire
entropy/first-moment/container family is capped at `c_ann`.
**Rigorous chain, no independence assumed:** for any x ∈ (0,1],
`N(a) ≤ x^{−a}(∏_ρ G_{ε_ρ}(x))·P_{μ_x}[no weak collinear triple]` where μ_x is the product measure over blocks
weighting each block-lawful configuration by `x^{|σ|}` — legitimate **precisely because `thm:blocks` makes the
strong constraints block diagonal**. The product is exactly computable (signature multiset from
`prop:descent`, `g_ε(j)` by a row DP or prime-free from `standard_model.py`), and generalized Janson gives
`P ≤ exp(−μ²/(2Δ))` with μ and Δ Weil-type counts over the B.15 families — the same technology as m₈ and E(p),
transferable through I1/I3. **The bound is global (not a fractional cover, hence not subject to §8's group-B
ceiling) while its ingredients are local counts the project already knows how to prove.** The literature anchor
has never been made rigorous anywhere: Guy–Kelly's heuristic for [N]² *is* this annealed computation with an
independence assumption, giving π/√3 = 1.813799 N < 2N after Ellmann's correction.
**Hardest step, and it is decisive:** Janson's exponent is capped at c/18 no matter how many triples there are
(measured `μ²/(2Δ)` at density 3/8 = 0.129, 0.151, 0.147, 0.142, 0.144, 0.147, 0.150, 0.153, 0.153, 0.154 times
p for p = 11…101 — remarkably flat, and algebraically → nq/18), while `Φ(3)` is plausibly of order 1 per (p−1),
a factor 6–8 too large. `J(3) = 0.1667` and `J(3.44817) = 0.1916`; since `Φ(3.44817) ≈ 0` a crossing exists, and
the crude estimate puts `c_ann ≈ 3.42–3.43`. Pushing further needs a Janson/Suen variant indexed by the B.15
**quadruples** rather than by pairwise overlaps, since every weak triple is a sub-triple of a symmetric
quadruple on a fixed direction hyperbola. **First experiment, one day, no prime needed:** compute `Φ(c)` exactly
for `c ∈ [3.0, 3.44817]` from the k ≤ 7 signatures and overlay `J(c) = c/18`; if `Φ(3.44) > 0.20`, the crossing
lies **above** the current proved bound and the entropy family is capped there — record the ceiling and stop.
Either outcome is a result.

---

## 11. Ranked transfers: the three best, each with a first experiment

**A statement that has to be made before the ranking.** The brief asked for "the three most promising
transfers". After verification and re-judging, **no literature transfer survives above P = 0.05**, and the
three best items in this document are therefore **not transfers**. They are the three computations that decide
whether the project's target is right, and they come from the adversarial and counter-proposal phases, not from
the literature. Ranking a Q2 or Q5 "transfer" highly would be ranking on the brief's own miscalibration
(H4 ⇔ H7 ⇔ T1), and none of the items below is a card that §8 killed. For completeness, the best genuine
literature transfers, with their re-judged numbers, are: Chang GAFA 2009 Thm 11 as a citation (P ≈ 0.90 as a
citation, 0.02 as a transfer); MC5's "exactly 8" (0.05, and it restates B.17); Q4-M2's homogeneous sub-system
(0.05); the genuine level-2 lift (0.05). That is the whole of it.

### #1 — Settle α(23) exactly, then a certified-witness ladder to p ≈ 150

**What.** Close the p = 23 bracket (`pair_bound_notes` §2 lists it as a DATA need: 69 ≤ α ≤ 74 against the
published conjecture's bound 3(p−1)+6 = **72**), then run the gain ladder of §10.2 at p = 29, 31, 37, 41 and a
thinned sequence to 150. Report gain(p) together with the anatomy of every witness: the (a,b) split, the
per-QR-run-block profile, the per-orbit occupancy `|S ∩ (O ∪ R(O))|`, and the number of points on lines of each
`|D|_∞`; then regress gain(p) on the arithmetic invariants the project already computes (s, p mod 8, m₈(p), the
QR-run signature) — a gain correlating with a growing invariant (m₈ ≈ p/12) is a growing gain.

**Size and tool.** p = 23: 176 binaries, 668 line constraints. p = 41: 320 binaries, ≈ 1250 lines. Tool:
`slack/cpsat_max.py` (CP-SAT) for the exact solve at p = 23, plus the single-involution reduction of §10.2
(88 orbit variables at p = 23; measured cost 0–2 points, ≈ 30 s per involution) and LNS repair over QR-run
blocks for the ladder. Feasibility only for the ladder — no optimality proof required. Cost: **hours**, and
p = 23 alone is ≈ 2 core-hours.

**Falsification criterion.** *Refutes the project's target:* a single **certified** lawful set with
gain ≥ 7 at any p ≤ 150 — and at p = 23, α ≥ 73 does it immediately. That would falsify the note's published
conjecture (`α(P_k) ≤ 3(p−1)+6`), make the k = −1 gain sequence 2, 4, 6, 5, ≥ 7 with no bounded pattern, convert
H4 and H7 from holes into **candidate false statements**, and re-price the proved 3.44817(p−1) from "a plateau
far above the truth" to "within ≈ 5% of the truth". *Supports it:* a properly calibrated search — one that
reproduces the known α = 54 at p = 17 and α = 59 at p = 19 within the same per-prime budget — topping out at
gain ≤ 6 at p = 23, 29, 37 and 41. **The pipeline is void if it fails that calibration**, and no conclusion may
be drawn from any larger p in that case.

**Why #1.** It is the only experiment both opposing theses nominate as primary, they make *opposite*
predictions about it, and it is the cheapest thing in this document. It also converts the project's only fifth
data point from a range into a measurement, and produces the first library of near-optimal configurations at
p > 23 — the only conceivable input to the structural theorem [187] says is all that remains. Calibrated:
**P(gain ≥ 7 found at some p ≤ 41) ≈ 0.25**; P(the experiment is decision-relevant either way) ≈ 0.9.

### #2 — Quad transversality census, then the block-collapse lemma

**What.** (a) Census: extend the transversality count of §10.1(b) to all primes 11 ≤ p ≤ 1009 by pair-hashing of
lines; assert **0** same-quad weak lines for every p ≡ 3 (mod 4), and record the count for p ≡ 1 (mod 4)
together with the minimal `s₁+s₂` of the responsible degenerate family. (b) Coarse-block audit: for the §30
component partition (`slack/t221/decomposition_check.py`) and the §17 QR-run partition, measure at
p = 101, 199, 401, 1009 the fraction of weak lines having ≥ 2 points inside a single block. (c) If both pass,
write the lemma and the corollary.

**Size and tool.** Existing line sweep plus the two existing block partitions; O(p²) per prime, minutes total
for the census and seconds for the audit. No solver needed.

**Falsification criterion.** A single same-quad weak line at any p ≡ 3 (mod 4) refutes part (b) of the lemma;
an exception count growing like a positive power of p for p ≡ 1 (mod 4) refutes its O(1) clause. For the
collapse: if the non-transversal fraction for the coarse blocks stays **above 5%** as p grows, coarse blocks do
see the weak system integrally, the strong form of (c) is false — and, notably, the right move would then be to
make blocks as **large** as possible, the opposite of the current programme.

**Why #2.** It converts H4(iii)'s observation into a **theorem** covering the §30 component decomposition, the
§17 block theorem, and every quad-indexed Sherali–Adams/Lasserre lift — including §30's declared "main open
technical task" (the transfer-matrix DP), which it caps at ≈ 3.44. It restates the target in its sharpest exact
form (`α = 3(p−1) + max Σ_a (|S∩Q_a| − 6)`, trivial bound exactly 8 per quad). And it tells every future
certificate designer the exact requirement: **couple at least two weak lines, i.e. be consistent across ≥ 4
quads simultaneously.** Calibrated: **P(the lemma goes through) ≈ 0.8**; P(it yields a better bound) = 0 — its
value is a proof of impossibility, which after §8 is what the project most needs.

### #3 — The null ladder N0, bundled with the matched random SDP surrogate

**What.** (a) 20 samples of `N0(p)` (random 8(p−1)-point sets in the same box with exactly 4 points per row and
per column) at p = 11 and 13, and 5 at p = 17; report mean and range of `α(N0)/(p−1)` against the true 3.200,
3.333, 3.375 and against trivial 4.000. (b) Bundled and cheaper: build a parameter-matched random instance for
the CSP reformulation of §10.3 ((p−1)/4 orbit variables, 32-point alphabet, Θ(p log p) random ternary
constraints, max codegree 6) and run the existing `slack/t221/sdp_level1.py` on it.

**Size and tool.** (a) MILP on the exact collinear-line system; measured 50–111 s per sample at p = 11, so
≈ 1 h at p = 13 and one overnight run at p = 17. (b) No new code beyond a generator.

**Falsification criterion.** (a) If `a₀ ≥ 3.9`, the null is uninformative and the ladder collapses — which
itself would mean the arithmetic carries *all* of the loss below trivial. If `a₀ ≈ 3.2`, i.e. the null already
reproduces the truth, then 3(p−1) is **entropic** and the entire arithmetic programme (m₈, blocks, H5, the
spectral route) is aimed at the wrong object — report this immediately. If `a₀ ∈ [3.40, 3.60]`, confirming the
preliminary 3.486 at p = 11, then the 3.44–3.45 plateau **is the generic value**, principle P2 becomes a sharp
testable statement instead of an unfalsifiable slogan, and H1/H2/H8 are priced at zero above `a₁`.
(b) If the surrogate's SDP closes the same 7–17% as the real instance, the clause-density explanation is
confirmed and **level 2 can be retired by argument rather than by an overnight solve**; if it closes > 40%, the
real instance is harder than random for a structural reason worth finding, and the level-2 lift earns its
moment variables.

**Why #3.** It supplies the null hypothesis the project's own executable audit says is currently *unsayable*
(`GAP-F-05`, `GAP-P-05/06`), which is the difference between "LP is blind" and "LP sees exactly the generic
part". Calibrated: **P(decision-relevant `a₀`) ≈ 0.85**; P(`a₀` confirms the plateau as the generic value)
≈ 0.5; P(the surrogate settles level 2 without the solve) ≈ 0.6.

### Immediately below the top three, in order

**#4 — the genuine level-2 lift** (§10.3), to be run only if #3(b) says the real instance is harder than random.
**#5 — the scale-localization curve `IP_L`** (§10.5), which either finds an L ≤ 8 beating 3.4482 (P ≈ 0.10) or
delivers the measured statement "the answer lives at direction scale Θ(p)".
**#6 — the annealed `Φ(c)` versus `J(c) = c/18` computation** (§10.7): one day, no prime, and either the first
non-cover certificate the project has ever had (`c_ann ≈ 3.42–3.43`) or an explicit ceiling theorem for the
entropy family.
**#7 — three free editorial corrections** that cost a paragraph each and are all decision-relevant:
Conjecture A is not a Burgess statement (§3(iv) reverse finding 1, pending independent replication);
§26a's window law for w ≥ 2 is provable (reverse finding 2), which moves Theorem C's blocker from analytic to
combinatorial; and the p^{1/4} alignment across B.15(d), §21(2), §23 and `holes.py` H5.

---

## 12. What was NOT found

### (a) Fabrications and misattributions found by verification — do not reuse

1. **"Segre: m′(2,q) ≤ q − ¼√q + 7/4 (q odd); Thas: ≤ q − ¼√q + 25/16", attributed to the introduction of
   arXiv:1705.10940.** Neither constant is in that paper: grepping the **full text of both v2 and v4** gives
   **zero** hits for "Thas", **zero** for "25/16", **zero** for "7/4". BL's intro lists only Segre's q-even
   `q−√q+1`, the two Voloch bounds and the two Hirschfeld–Korchmáros bounds. **25/16 is real but lives in the
   card's own second source** (Hirschfeld–Thas, arXiv:2503.06243, Thm 3.6(ii)) and is attributed there jointly
   to **Segre (1967) and Thas (J. Algebra 106 (1987) 451–464)** — so the card's split of credit is contradicted
   by its own other source, an internal contradiction inside one deliverable. **The constant 7/4 could not be
   located anywhere**; it may be contamination from BL's own `q − √q + 7/2`. **DO NOT put 7/4 in the note.**
2. **Rédei "p. 237, Satz 24" attached to Blokhuis's survey Theorem 3.1.** In the survey that pointer belongs to
   **Theorem 2.1** (the directions theorem); Theorem 3.1 carries only "[Rédei, 1970]" with no page and no Satz
   number, and the survey never asserts that Theorem 3.1 is Satz 24. **This is the one manufactured
   theorem-number-like object in the entire corpus, produced by transplant.**
3. **arXiv:2206.09876 credited to "Cohn–Triantafillou".** It is **Rupert Li**, single author,
   Adv. Math. **460** (2024) art. 110043. (Cohn–Triantafillou is a different paper, "via modular forms".)
   The mathematical claim attached — Cohn–Elkies not sharp in dims 3, 4, 5 — is correct and is Li's.
4. **"The direction of a pair of points of AHG(2, Z/p³) lives in a set of size p⁴(p+1)."** False by enumeration:
   it is **p²(p+1)** (36 distinct unimodular lines through the origin at p = 3, 150 at p = 5; equivalently
   `|P¹(Z/p³)| = p³+p²`). p⁴(p+1) would be 324 and 3750.
5. **"Segre needs a well-defined tangent count q+1−|A| per arc point."** It is **q+2−|A|**, per Ball–Lavrauw
   and per the same card's own step 2 — an internal contradiction.
6. **Frankl–Rödl "Lemma 5.1".** No such numbering could be confirmed. Delete the label; and the `(1±τ)D` /
   `Δ₂ < τD` form is properly Pippenger / Alon–Spencer Ch. 4.7 (FR 1985 is stated for D-regular hypergraphs
   with codegree ≤ D/(log N)⁴).
7. **Heath-Brown, Annals 155 (2002), pages "553–595"** → **553–598**.
8. **BBBSS**: author order is **Blokhuis**, Ball, Brouwer, Storme, Szőnyi, and the title ends "defined **on** a
   finite field" (JCTA 86 (1999) 187–196; the survey's theorem *label* reverses the first two names, which is
   probably how the error entered).
9. **Blokhuis ICM, pages "537–545"** → **537–546**.
10. **Bloom–Lichtman**: "a global version of Salberger **[23]**" → **[24]**; page range 327–**348**; and the
    slicing bound `N^{n−2+1/d+o(1)}` is **Pila's**, not theirs.
11. **"Landjev–Boev"** → **Boev–Landjev**, Discrete Math. **310** (2010) 2061–2068 (and the paper is
    constructions at nilpotency index 2 only, which closes the associated uncertainty in the card's favour).
12. **The URL attached to Green/HJSW, arXiv:2512.11469**, is a real but **unrelated** paper (Ramanathan,
    Prellberg, Lewis, Joshi, Dandekar, Dandekar, Panat, "Three methods, one problem: Classical and AI approaches
    to no-three-in-line", cs.AI, Dec 2025).
13. **KNS's odd-k bound described as "tighter"** — it is `(1−3/k)kn`, **weaker** than the even-k `(1−2/k)kn`.
14. **Q7's S2**: the ovoid size bound q²+1 is **Bose/Qvist**, not Barlotti–Panella (who proved the
    classification as an elliptic quadric); the row welds the wrong mechanism to the wrong authors.
    **Q7's S3**: the q-even Kakeya bound q(q+1)/2 is described in the source as "easy to see", the q-even
    classification is **Blokhuis–De Boeck–Mazzocca–Storme**, Des. Codes Cryptogr. 72(1) (2014) 21–31, and
    marking its extremal "unique" is wrong (many inequivalent hyperovals).
15. **Hatami–Lovász–Szegedy credited with introducing local–global convergence** — their own abstract
    attributes the metric to **Bollobás–Riordan**, refining Benjamini–Schramm.
16. **Ray-Chaudhuri–Wilson "t ≥ 2s"** — the primary says **t = 2s** (even).
17. **Mubayi's C₅ instance** is stated for **n even** (dropped); and "for q < n/2" attributed to
    Erdős / Lovász–Simonovits appears in **neither** Mubayi's nor Ma–Yuan's text — **UNVERIFIED**.
18. **Alsetri–Shao issue number "no. 4"** — two independent searches say **issue 2**; the Wiley page returns
    403. **UNVERIFIED either way**; cite as "Bull. London Math. Soc. 58 (2026), doi 10.1112/blms.70293".
19. **Shparlinski quoted inside quotation marks with two word substitutions** ("appear"/"seem",
    "within standard"/"within the standard"). Quote exactly or drop the marks.
20. **A WebFetch summary of Ellis–Keller–Lifshitz** asserted a discussion of `n = (k−t+1)(t+1)` as a boundary
    where "two extremal families coexist"; a grep of the full extracted PDF found **zero** occurrences.
    **Do not cite EKL for boundary non-uniqueness.**

**What must be said in the project's favour, because it is unusual:** across seven questions and roughly sixty
sources, **no paper, author, year, venue or page range was invented**; every theorem number quoted exists and
carries the content attributed to it, with the exceptions above; and the long verbatim quotations are
character-accurate, including the fiddly exponents (Chu's `H_min^{−(2n−k′)/r} p^{k(r+2n−k′)/(4r²)+ε}`,
Pierce–Xu's `‖H‖^{1−1/(2r)}H_min^{−1/(2r)}q^{(nΘ+1)/(4rΘ)}(log q)^{n+1}`, Heath-Brown–Pierce's
`q^{(r+1+D)/(4r²)}`). One agent even caught and correctly rejected a bad automated PDF read ("q²−q+1" for the
Kakeya bound). One post-cutoff June-2026 arXiv identifier (2606.26735) — the classic fabrication site — was
checked specifically and is **real**.

### (b) False statements about the project's own state

1. **"No cvxpy/Mosek/SDPA installed, so the SDP value was NOT computed."** False: `slack/t221/sdp_level1.py`
   used cvxpy + CLARABEL + SCS on exactly this instance, and the results are in
   `docs/research/integrality/sdp_level1_report.md`. The research agent did not read the directory it was
   writing into.
2. **"Could NOT verify the repo's journal reference Advances in Combinatorics 2026:7, doi 10.19086/aic.2026.7."**
   It is printed on **page 1** of the arXiv v2 PDF. The repo's `[KNS25]` entry is correct in every field.
3. **"arXiv:2502.00176 is NOT cited in the repo."** It is, in `docs/research/deep_research_2026-08-18.md`;
   it is only absent from the note's bibliography.
4. **"The H7 measurement appears not to have been run."** It has: `slack/min_triples.py`, logs
   `slack/verification/min_triples_p{13,17,19}.txt`, results in `docs/THREAD.md` [90] — and the measured slope
   (≈ 1.5–2 triples per extra point, p-independent) **confirms the card's own verdict**.
5. **"H3 is a theorem in a day and holes.py should be edited."** H3 was already `prop:stability` at note
   version **v1.12**, with the orbit-wise verification the card proposed as future work already run over all
   orbits of all p ≤ 31. The brief's own description of the paper as v1.9/1.10 is stale: it is at **v1.13**.
6. **One counter-proposal listed the pair's extremal count at p = 11 as open.** The repo has it:
   `stability_h3_report` §8 gives **39** maxima, exhaustively enumerated, with D(1) ≥ 13 out of 31 points.
   (Consistency check worth recording: 39 is odd, which forces an R-fixed maximum — matching the independent
   measurement `max{2|A| : A ∪ R(A) lawful} = 32 = α` at p = 11.)

### (c) Numbers that did not reproduce

1. **Q3's doubling measurements.** Claimed 12.4 / 31.5 / 16.5 at p = 10007 and 32.2 / 128.9 / 130.8 at
   p = 100003, against "benchmarks" 24 / 70 / 16.5 and 64 / 296 / 143. Exact unsampled recomputation against a
   *matched simulated* random set gives the half-angle set at **exactly** the random level (65.5 vs 65.4 at
   p = 100003, |T| = 136 — 0.2%). The card's script subsampled 700 elements and used a formula benchmark; the
   "factor of 2 from the ± pairing" was an artefact. **Conclusion strengthened, not weakened.**
2. **Q4's ALL-triples position-free fractions** (0.402 / 0.412 / 0.354 / 0.393 / 0.372 → reconstructed
   0.285 / 0.306 / 0.267 / 0.318 / 0.301) and certifiable sub-fractions (0.095 / 0.149 / 0.158 / 0.150 →
   0.070 / 0.082 / 0.123 / 0.112). Only the **weak-line** figures reproduce exactly.
3. **Q6:** `min_q excess(q)` 10–18 → **10–17**; "the max line size is 8 every time" — **false at p = 13 and 17**
   (it is 6); budget mean 3.09 → **3.122**; LP(all) range 3.29–3.55 → **3.20–3.76** for p ≤ 31; per-scale
   coverage 0.95–1.00 → **0.67–1.00**; max multiplicity 7–10 → **3–10**; N7's defect formula "p−6" → the true
   defects are **8, 8, 10, 13**.
4. **Q1's "measured mean degree 25 at p ≈ 2000"** — unlabelled, and it does not match the collinear-triple
   degree (37.0 / 51.4 / 62.4 / 66.2 at p = 41 / 101 / 199 / 401, growing); it matches only the 3-point-line
   degree.
5. **Q5's "in AG(2,q) with a permutation the dangerous-pair fraction is 1"** — it is **3/q** for the minimiser
   and ≈ 0.63 for a random permutation; it is 1 only for the full q×q grid.
6. **Two independent SDP runs give slightly different values** (43.96 / 59.64 / 62.83 in
   `certificate_hierarchy.md` versus 43.9974 / 59.7414 / 62.9187 in `sdp_level1_report.md`) — two different
   scripts, same conclusion. Both should be cited; neither is wrong.

### (d) Questions the literature does not answer (searched, not found)

1. **No supersaturation result for collinear triples in [N]²** — nothing bounds collinear triples from below
   for 2N+t points in the integer grid. Independently searched.
2. **No compression/shifting device for point-line problems on geometric ground sets.** **UNVERIFIABLE**:
   absence of evidence after an unrecorded search. The supporting *reason* is correct on its own terms (Frankl
   (i,j)-shifts do not preserve "no three collinear", because moving a point within its row destroys and creates
   collinearities on Θ(p) lines of other slopes).
3. **No named theorem of the form "approximate partition with defect δ ⇒ bound degraded by O(δ)" for point-line
   packing.** Searched independently (partial parallel classes, near-resolvable designs, packing/covering
   duality, Füredi's "Matchings and Covers in Hypergraphs" survey). The reason there is none: the statement **is**
   ordinary fractional relaxation, with LP(all) as its floor (§6, MC3′).
4. **No one-variable Burgess bound for `χ(f(t))` with f a ratio of products of distinct linear factors, over an
   interval.** Plausible (the Burgess shift `t ↦ mt+h` does factor such an f, which is why the
   "product of linear factors" case is the classical one), but **not located in any of the eight Q3 sources**.
   **UNVERIFIED.**
5. **No inhomogeneous version of Pierce–Xu Theorem 1.1** — it is stated for homogeneous forms, and
   homogenising costs a variable of length 1, killing `H_min`. This blocks the Cauchy–Schwarz reduction to n = 2
   that would have given p^{1/3+κ}.
6. **Bourgain–Garaev's entropy condition** and the shape of its admissible sources — **never obtained**. The
   abstract is uninformative about hypotheses. MC4's literature half is entirely unverified, and its probability
   should never have been priced as if it were.
7. **Nothing bounds from above the number of directions/lines spanned by a dense subset of the lifted pair**
   (B.12(iv), `GAP-H-03`) — and it is now **provably vacuous as an identity**: lawfulness gives
   `|S| ≤ 8(p−1) − O(log p)`.
8. **Nothing bounds `max_q excess(q)` unconditionally** — the "few collinear triples through a point"
   statement. The repo has only the *lower* bound `E(p) ≫ p log log p`.
9. **No upper bound below 2N − o(N) for no-three-in-line in [N]²** (Green Problem 72). Only the construction
   side has moved: (3/2+o(1))N for arbitrary N, 2N verified for n ≤ 64 (Prellberg, Feb 2026), and the
   Guy–Kelly heuristic constant is π/√3 ≈ 1.813799 after Ellmann's 2004 correction.
10. **The k-uniform Hypergraph Vertex Cover Lasserre gap of k−1−ε is verifiably ABSENT** from Tulsiani's
    5 Nov 2009 full version (zero grep hits over the extracted text) — not merely unverified.
11. **"The only improvement ever obtained on the second-order term of the Sidon problem in an interval"** —
    **UNVERIFIABLE**: a negative existential over 80 years of literature. (The chain 1 → 0.998 → 0.99703 →
    0.98183 is itself verified.)
12. **Nothing at composition length 3 in the Hjelmslev-plane arc literature.** Kiermaier–Koch–Kurz: zero
    occurrences of "length 3", every reference is to length 2; Boev–Landjev: nilpotency index 2 only,
    constructions only. And the state of the art for q odd over Galois rings is
    `((q+1)/2)² ≤ m₂ ≤ q²` — the source's own "least satisfactory" case.
13. **No statement anywhere connecting the modular-hyperbola literature to collinearity.** Two independent
    30-page papers on exactly our object — Shparlinski's survey (3890 lines) and
    Chang–Cilleruelo–Garaev–Hernández–Shparlinski–Zumalacárregui (2508 lines) — give **zero** hits for
    "collinear", "general position", "no three", and (in the survey) "determinant method".
14. **The nearest thing to a "Bombieri–Pila for congruences" covering lemma** is implicit inside
    Cilleruelo–Garaev's own proof (`(tx+u₀)(ty+v₀) = n_z` covers the box solutions by O(1) conics) and **nobody
    states it as a standalone lemma.**

### (e) Dead ends, recorded so nobody repeats them

Covers / LP / IP on rows, columns, ±1, ±2 lines (exhausted, and now with a measured floor); local inequalities
of any rank on those lines; the unbalanced exchange regime; the spectral route (conditional on sub-Burgess
cancellation, **and dominated by its own 4(p−1) ceiling**); the ρ-involution compression (ω = Θ(p));
the spanned-directions identity (vacuous); the blocking-pair charging (slope 1/2, τ ≈ 0.5|H(−1)|);
the reduction to `M ∪ R(M)` (extremum is in the middle); orbit-local and ≤ 3-orbit-local certificates
(≥ 3.5556(p−1)); flag algebras and every local-limit formulation (no limit object exists);
dyadic Gaussian-scale sub-families (every scale ≥ 2 worse than trivial); Rédei / Segre / slice rank after
lifting; the torus reduction (sees p+1, not 3(p−1)); the finite-table technique above `|D|_∞ = 1`
(one giant component at L = 2); Bose-through-a-point (7.0–7.5(p−1)); the multiplier-coset blocks
(two independent arithmetic coincidences required).

### (f) Internal inconsistencies in the project's own documents that must be fixed

1. **Level 1 versus level 2.** `sdp_level1_report.md` correctly calls the computed object the level-1 lift and
   says level 2 over triples has **not** been run; `certificate_hierarchy.md`, `REPORT` §17 and
   `hjsw_window.tex` all call the same object "level 2" and conclude the route does not go through level 2.
   Correct all three, and stop repeating the claim that level 2 has been tried.
2. **The p^{1/4} numbers disagree in three places:** B.15(d) says p^{1/3+ε}, §21(2) says p^{1/8+ε}, §23
   restricts to p ≡ 3 mod 4. All should read **p^{1/4+2ε}, uniformly in p mod 4**, citing Chang Thm 11.
3. **`certificate_hierarchy.md` still carries the superseded constant 3.4616** and its "предел 3.441"; the
   current values are **3.44817 proved, certificate range [3.4286, 3.4482], numerically 3.4413**.
4. **The m₈ asymptotic:** B.9(ii) "(1/6 + o(1))p — both slopes" versus §17 "m₈ ~ p/12 conjectural" versus
   §24's per-slope 0.0795. Settle the bookkeeping.
5. **`holes.py` has no status field** (`GAP-F-07`), which is why closed holes kept being shipped as open; and
   `holes.py` H5's `where_it_breaks` and I2's description are both factually wrong (§3).
6. **`section_blocks` remark (d)** over-reaches from orbits to blocks (§6(iii)).
7. **`phenomenon.py`'s diagnostic cannot represent the integrality gap, cannot say "absent", and its S4 fails
   on the frame's own numbers** (§8, group H(v)).
8. **`Corollary cor:rundensity` should be stated as asymptotic in p for each fixed K**, with the implied
   constant ≍ 2^K·K and effective range `K ≲ log p/(2 log log p)` (§3, effectivity caveat).
9. **`pair_bound_notes` §8's `|M| ≤ 8p`** should be `|M| < p−2`, with the measured maxima and the corrected
   statement that "most class triples give nothing" only from p ≈ 60 (§4, M5).

---

## 13. Recommendation

**Do not push any H-route as a literature transfer; the literature has been searched properly and it has
nothing.** Instead: (1) run the three computations of §11 — α(23) and the gain ladder, the quad-transversality
census, and the null ladder with its SDP surrogate — which together cost a day or two and decide whether the
target itself is right, whether the covering/block family can be closed with a proof instead of numerics, and
whether the 3.44 plateau is LP weakness or simply the generic value; (2) commit the quad-transversality /
block-collapse lemma (§10.1) as the impossibility theorem that retires the whole cover/packing/block/lift
family including §30's declared main open task, and record with it the exact requirement any future certificate
must meet — **consistency across ≥ 4 quads, i.e. coupling at least two weak lines**; (3) apply the free
corrections, of which three are decision-relevant: Conjecture A is a **finite check plus 51 classical
Kloosterman counts, not a Burgess statement** (pending independent replication of the 2^22-pattern computation
and the pinning of c₀ and K), §26a's window law for w ≥ 2 is provable by the argument already in
`lemma_run.tex` (moving Theorem C's blocker from analytic to combinatorial), and the p^{1/4} thresholds must be
aligned; (4) **delete H4 and H7 from the hole list** — the project's own B.12 says they are the target, and
keeping them makes every ranked list wrong — mark H3 closed-but-inapplicable, mark H8 closed as proved
impossible, close H2 and H6 with the measurements in hand, and reduce H1 to the single surrogate run; and
(5) **retarget what remains from `3(p−1)+O(1)` to the union case of Conjecture G at `(3+o(1))p`**, which is what
Green's Problem-72 comment actually asks for, is the only genuinely load-bearing use of the pair anywhere in
the project, and is stated in the same units (√p·polylog) as every tool the project owns — while accepting the
honest caveat that the relaxation does not by itself unlock a mechanism, since LP(all) trends to ≈ 3.44 either
way. The uncomfortable summary, and the reason this recommendation is not "keep pushing": the analytically
hardest thing in the brief (H5) guards a model whose own ceiling is `4(p−1) − c·p/log p`, and the
combinatorially cleanest things (H1, H2, H6, H8) are capped by an LP floor of ≈ 3.40 — so on the current target
every surviving route is dominated by a result already proved, and the only questions whose answers are not yet
determined are the three in §11.

---

## Резюме по-русски

1. **Переносов из литературы нет.** После враждебной проверки максимальная вероятность переноса во всём корпусе
   — 0.08, а после пересчёта под новое состояние проекта — **0.05**. Все известные «SDP бьёт LP для упаковок» —
   это ограничения арности 2, вычислимые благодаря большой группе симметрий; у нас порядок 2–4 (измерено).
2. **Библиографическая дисциплина корпуса неожиданно хорошая:** ни одной выдуманной статьи, автора, года или
   тома; одна пересаженная ссылка «Satz 24», одна путаница авторства arXiv:2206.09876 (Rupert Li, не
   Cohn–Triantafillou), четыре неверные константы (§12).
3. **Главная находка — структурная и отрицательная:** теорема устойчивости для одной гиперболы теперь ЕСТЬ
   (Prop. `prop:stability`, точная) и всё равно не помогает — механизмы «устойчивость + обмен» из литературы
   работают у экстремума ОДНОЙ структуры, а наш экстремум сидит МЕЖДУ двумя (a ≈ b ≈ 1.5(p−1)).
4. **Вторая находка сразу режет четыре вопроса:** любая оценка вида покрытие / упаковка / почти-разбиение /
   «счёт через точку» / зарядка обмена — это неотрицательная комбинация ограничений по прямым, значит
   ≥ LP(все) ≈ 3.40(p−1). Это и есть ответ на вопрос брифа про «дефект δ ⇒ O(δ)»: названной теоремы нет, потому
   что это обычная дробная релаксация.
5. **Третья: H3 невидим для LP.** Добавление сильнейшего линейного содержания леммы `orbopt` к LP(все) меняет
   значение РОВНО НА НОЛЬ при всех 11 ≤ p ≤ 61, ни одно из отсечений даже не активно.
6. **Калибровка брифа неверна в трёх местах:** 3.45 — это LP(1), а не пол (пол ≈ 3.32–3.40); H4 ⇔ H7 ⇔ цель без
   потери в константе, поэтому «перенос» в Q2/Q5 — это полное решение открытой задачи; прибавки при k = −1 равны
   2, 4, 6, 5 (монотонно до p = 17, разброс 4), а не 5, 5, 6, 5.
7. **Два собственных аналитических блокера проекта — не настоящие** (самая ценная положительная находка, обе
   обратные): Конъектура A требует `E/(p−1)` выше АБСОЛЮТНОЙ КОНСТАНТЫ (≈ 9, или ≈ 5.8 по числам §23), а не
   `→ ∞`; такой порог несут семейства с ограниченным σ, чьи клоостермановы подсчёты строгие, — это КОНЕЧНАЯ
   проверка (минимум по 2²² знаковым образцам даёт 9.37), а не сумма характеров. И закон окна §26a при w ≥ 2
   доказывается в четыре строки тем же куммеровским аргументом, что уже есть в `lemma_run.tex`.
8. **Но даже полностью доказанная теорема о модели не бьёт 3.4482:** `pair_bound_notes`, строка 585, даёт её
   собственный потолок `4(p−1) − c·p/log p`. Значит вся линия H5 нацелена на цель, уже перекрытую доказанным
   результатом.
9. **H8 просит то, чего доказано не существует** (объединения орбит дают ровно 16/32 = тривиальную границу, а
   упаковочные оценки — двойственные к LP); H2 мёртв в обеих категориях пределов; H6 сохраняет трудность; у H1
   остался ровно один невычисленный пункт, и два документа репозитория расходятся, вычислялся ли он.
10. **Три эксперимента (главный итог, все дешёвые).** (1) **α(23) точно, затем лестница сертифицированных
    свидетелей до p ≈ 150** — 176 бинарных при p = 23, CP-SAT плюс редукция по одной инволюции (стоит 0–2 точки
    при половине переменных) и LNS; фальсификация: любое сертифицированное множество с прибавкой ≥ 7 опровергает
    опубликованную гипотезу и превращает H4/H7 из дыр в ложные утверждения (α(23) ≥ 73 решает вопрос сразу);
    обратно — только откалиброванный поиск, воспроизводящий α = 54, 59 при p = 17, 19, даёт право на вывод
    «прибавка ≤ 6». Оба противоположных тезиса называют этот эксперимент главным и делают ПРОТИВОПОЛОЖНЫЕ
    предсказания.
11. (2) **Перепись трансверсальности квадов и лемма о блочном коллапсе** — минуты счёта до p ≤ 1009, без
    решателя. Квады `Q_a = {κ_a, μ_a, κ_{−a}, μ_{−a}}` разбивают P₋₁, дают тождество
    `α = 3(p−1) + max Σ_a(|S∩Q_a| − 6)` с тривиальной границей ровно 8 на квад, и всякая слабая прямая с тремя
    разными классами задевает три РАЗНЫХ квада, кроме O(1) исключений при `s₁²+s₂² ≡ 0` (измерено: 0 исключений
    при всех p ≡ 3 mod 4, 14–64 при p ≡ 1 mod 4). Отсюда элементарная лемма о склейке: слабые прямые дают любому
    блочному подъёму РОВНО своё LP-неравенство и ничего больше — то есть §30, блочная теорема §17 и любой
    Sherali–Adams/Lasserre по объединениям квадов заперты на ≈ 3.44. Фальсификация: одна одноквадовая слабая
    прямая при p ≡ 3 mod 4, или рост числа исключений как степень p.
12. (3) **Нулевая лестница** — случайное 8(p−1)-точечное множество в той же коробке с ровно 4 точками в строке и
    столбце. Предварительно при p = 11 (7 образцов): α = 34…36, среднее **3.486(p−1)** против истины 3.200 и
    тривиальной 4.000, — то есть ГЕНЕРИЧЕСКОЕ значение практически лежит на плато 3.44–3.45. Один простой, семь
    образцов, требует воспроизведения при p = 13, 17; но если подтвердится, плато — это не слепота LP, а
    значение нулевой модели, и никакой сертификат, устойчивый к рандомизации задачи, его не пробьёт. В том же
    заходе: прогнать существующий `sdp_level1.py` на случайном инстансе с теми же параметрами — если он закроет
    те же 7–17 %, уровень 2 закрывается АРГУМЕНТОМ, без ночного счёта.
13. **Что делать (§13).** Провести три эксперимента; закоммитить лемму о трансверсальности квадов как теорему
    невозможности для всего семейства покрытий/блоков (с точным требованием к будущим сертификатам: связность по
    ≥ 4 квадам, то есть склейка минимум двух слабых прямых); внести три бесплатные аналитические поправки;
    **удалить H4 и H7 из списка дыр** (это сама цель, B.12 говорит это дословно), закрыть H2, H6, H8, свести H1 к
    одному прогону; и **перенаправить остаток с `3(p−1)+O(1)` на объединённый случай Конъектуры G при
    `(3+o(1))p`** — именно это нужно программе Грина и именно это выражается в тех же единицах (√p·polylog), что
    и все инструменты проекта.
14. **Неудобное резюме:** самое трудное аналитически (H5) охраняет модель с собственным потолком
    `4(p−1) − c·p/log p`, а самое чистое комбинаторно (H1, H2, H6, H8) заперто полом LP ≈ 3.40. При текущей цели
    каждый выживший маршрут перекрыт уже доказанным результатом, и единственные вопросы с неопределённым ответом
    — три из §11.
