# Task 2 for external reasoning agents (ChatGPT or others) — the two-hyperbola theorem: verify, strengthen, generalise

Repository (public): https://github.com/iwasborninbali/saturation — read `paper/hjsw_window.pdf` (tag hjsw-note-v1.7; Sections 6–9: two hyperbolae, every second hyperbola, cubic graphs, permutation monomials; Section 10 for the data), Section
"Two hyperbolae: a first bound for H(1) ∪ H(−1)", and `docs/research/pair_bound_notes.md` §§11–17, §§23–24, B.9, B.19.  Verifiers:
`slack/km1_theorem_check.py`, `slack/block_cover_km1.py`, `slack/km1_lines.py`, `slack/lp1_dual.py`.

## What is proved (please attack it)
Setting: p odd prime, h=(p−1)/2, box G(p) = [−h, 3h+1] × [0, 2p−1], P₋₁ = {(x,y) ∈ G(p): xy ≡ ±1 (mod p)}, |P₋₁| = 8(p−1).
Theorem: every subset of P₋₁ with no three collinear points has ≤ 4(p−1) − 4·m₈(p) points, m₈(p) = number of lines x−y = const
carrying exactly 8 points of P₋₁.  Proof: line cover — the three lines c−p, c, c+p of every "good residue group" (a residue d mod p for
which the classes on x−y ≡ d form a shared σ-pair and the classes on x+y ≡ −d form a shared τ-pair with coinciding centres; 16 points on
those three lines, sizes 4,8,4), both slopes, plus every row disjoint from all groups; the reflections R:(x,y)↦(p−x,y), R′:(x,y)↦(x,2p−y)
swap the two hyperbolae and the two slopes, so the good groups are pairwise disjoint and R,R′-closed, and rows/columns are entirely inside
or outside; cost = 2·(6m₈ + 2(p−1) − 8m₈) = 4(p−1) − 4m₈.
Proposition: m₈(p) = p/12 + O(√p log⁴p) (Bombieri exponential sums along the cubic a b² + (a²−1) b + a ≡ 0; the four conditions are interval
conditions on four linear forms of (a, 1/a, b) mod p — Selberg polynomials).
Corollary: α(P₋₁) ≤ (11/3 + o(1))(p−1).

## Tasks, in order of value
A. **Adversarial verification** of the theorem: try to break Lemma "residue groups" (≤ 2 centres per residue; sizes (4,8,4)), Lemma
   "closure" (no class in two good groups; rows/columns entirely inside/outside), and the cost count.  A single counterexample p (compute!)
   would kill it; our verifiers pass for 11 ≤ p < 320.
B. **Strengthen the constant.**  Known (data p ≤ 199, `slack/block_cover2.py`, `slack/verification/lp1_types_p113_137_199.txt`): the LP with rows,
   columns and slope-±1 lines gives ≈ 3.45 (p−1); its optimum uses the (4,8,4) groups (= the theorem, saving 2 per group), the lines (7,5,3)
   of the (3,7,5,1) groups (saving 1 per group and slope, locally certifiable), and fractional weights on (2,6,6,2) groups (no local certificate).
   Densities of the three group types per slope → 1/12, 1/12, 1/6 (`slack/km1_lines_5678.py`; both/one/neither of the σ-, τ-pairs share centres).
   Concrete target: a BLOCK LEMMA for the (3,7,5,1) groups (take the lines 7,5,3; the leftover point of each group and of its R-, R′-images
   pair up in rows/columns) giving α(P₋₁) ≤ 4(p−1) − 4m₈ − B₇ + O(1) with B₇ = number of one-shared groups disjoint from the 8-groups, and the
   density of B₇ (a polytope count on the cubic, as for m₈) — this would give ≈ 3.6 (p−1).  Beyond that: prove or disprove that no cover by
   rows, columns and ±1 lines can beat 3.4 (p−1) asymptotically.
C. **General k.**  For H(1) ∪ H(k), k ≠ ±1, the reflections do not swap the hyperbolae; rows pair (1/y, y) ∈ H(1) with (k/y, y) ∈ H(k).
   Eight-point ±1 lines still exist with positive density (data: `slack/lp1_dual.py p k`; LP(1)/(p−1) ≈ 3.6–3.9 for k=2,3, p ≤ 199).
   Is there any provable bound α(P_k) ≤ (4−c)(p−1) for all k (or for infinitely many p and a fixed k ≠ −1)?  What structure replaces the
   mirror closure?
D. **The gap between the theorem (≈3.67) and the truth (3(p−1)+O(1) empirically)**: any idea that uses integrality (rank ≥ 2 inequalities,
   e.g. odd-cycle/clique cuts on the collinearity hypergraph restricted to a residue group and its row/column neighbours) to push the bound
   below 3.5?

## Deliverable
For A: a verdict with the failing p and the failing statement, or "no gap found" with what you checked.  For B–D: a proof (every lemma
stated) or a clear account of the obstruction, plus any certified computations (point/line lists we can re-verify with `saturation.py`).
Do not trust generated proofs without line-by-line checking; we re-derive everything.

## Резюме по-русски
Задание внешним агентам: (A) попытаться сломать нашу теорему о паре гипербол k=−1 (контрпример по p или дыра в леммах); (B) усилить
константу 11/3 до 3.5 через 5–7‑точечные диагонали явным дробным покрытием; (C) общие k — есть ли хоть какая‑то доказуемая оценка ниже
4(p−1); (D) идеи для использования целочисленности. Репозиторий публичный, доступ не нужен.


## Update 19.08 (v1.7) — new sections and the corresponding open questions
* Section 7 (every second hyperbola): Theorem α(P_k) ≤ 4(p−1) − (2G₈ − 2Σ|A_c−B_c|)/R (potential cover along the cycles of the row/column class graph),
  Corollary α ≤ 4(p−1) − c√p/log⁵p for ord(k) ≥ C√p log⁵p.  OPEN E: the LINEAR form: the same cover with uniform line weight t = 1/m (m = 4…6) saves ≈ 0.2 per
  eight-group numerically for every (p,k) and on random arrangements (docs/research/pair_bound_notes.md §28–29): prove α ≤ (4 − c₀)(p−1) — needs the local law
  of the special-class sequence along the cycles (fixed-window equidistribution at the level of fibred products of C₀(k)); the explicit local law for k = 2 is in
  the first solver's L1 (THREAD[122]); the obstacle: window length ≈ 60 ⇒ absurd constants.  A short-support argument (β = O(1/m) from two-point correlations +
  diffusivity) would do.
* Section 8 (cubic graphs ≤ (11/8+o(1))N) and Section 9 (permutation monomials, all odd k, ≤ (1.474+o(1))N; generic permutation polynomials corollary).
  OPEN F: the STRONG form: LP over all lines ≈ 1.1 N for cubics (three-point-line families of docs/research/curves_conjecture.md §7): prove α ≤ (4/3+o(1))N or
  ≈ 1.1 N — degrees in the 3-line hypergraph do not concentrate (CV ≈ 0.4), so a cover organised by families/positions is needed.
  OPEN G: the UNIVERSAL statement: every permutation polynomial of degree ≥ 3 has α ≤ (3/2 − c)N (Wan's value-set bound + Niederreiter–Robinson give a linear
  saving on at least one slope; the constant and the exceptional cases (dependent slopes, as for the hyperbola x ↦ 1/x) are the work).
