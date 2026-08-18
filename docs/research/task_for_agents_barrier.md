# Task for reasoning agents (work in parallel with the deep research; no repository access needed — the repo is public)

Repository: https://github.com/iwasborninbali/saturation (public; read-only is enough).  Start with
  paper/hjsw_window.pdf   — the theorem for one hyperbola (definitions, orbit lemma, LP certificate) — 13 pages, read §1–§5;
  docs/research/slack_experiments.md — our computational data on unions;
  slack/verification/pairs_p19.txt, slack/witnesses/pair_*.txt — exact maxima and witnesses for pairs of hyperbolae;
  slack/cpsat_max.py, slack/maxlawful_pysat.py, slack/crosslines.py — how the maxima/rich lines are computed (Python; the law
  is checked by saturation.py: three points are collinear iff the 3×3 determinant vanishes).
If they want to compute: python3 slack/cpsat_max.py M 13 26 1,2 8 600  (max lawful subset of H(1)∪H(2) mod 13 in the 26×26 HJSW box,
8 workers, 600 s; needs ortools).

## Notation
p odd prime, h = (p−1)/2, G(p) = [−h, 3h+1] × [0, 2p−1] (the HJSW box), H(k) = {(x,y) ∈ Z²: xy ≡ k (mod p)}, P_k = (H(1) ∪ H(k)) ∩ G(p),
|P_k| = 8(p−1).  Lawful = no three collinear.  α(P) = size of a largest lawful subset.  Known: α(H(1) ∩ G(p)) = 3(p−1) exactly
(theorem), and α(P_k) = 3(p−1) + {5,5,6,5} for p = 11,13,17,19 (best k), 70 ≤ α ≤ 74 at p = 23.

## The problem
PROVE OR DISPROVE:  α(P_k) = 3(p−1) + O(1) as p → ∞ (for each fixed k, or uniformly in k).
Weaker targets, in decreasing order of value:
  (T1) α(P_k) ≤ 3(p−1) + o(p);
  (T2) α(P_k) ≤ (3+ε)(p−1) for some explicit ε < 1 (e.g. ε = 1/2), i.e. the union of two hyperbolae cannot reach 4(p−1)... note the
       trivial bound is 4(p−1) + something? no: |P_k| = 8(p−1), the trivial bound is far; the LP relaxation gives ≈ 3.65(p−1) at p=13
       and is NOT tight (true value 41 = 3.42(p−1)); prove an LP/duality bound strictly below 4(p−1) for all p;
  (T3) the same for k = −1 only (P_{−1} is symmetric under (x,y) ↦ (x, −y) mod p; maybe easier);
  (T4) an explicit construction with α(P_k) ≥ 3(p−1) + ω(1) — this would be a surprise and very interesting.
Also of value: any structural statement about maximum lawful subsets of P_k (e.g. "they contain the HJSW set of one hyperbola
minus O(1) points"), proven or refuted with a certified counterexample.

## What breaks for two hyperbolae (from the note, §6)
For one hyperbola every rich line (≥ 3 points) has slope ±1 and lies inside a 16-point orbit; the LP dual (weight 1 per rich line)
is exact.  For P_k, a line meets each hyperbola in ≤ 2 classes, so points of FOUR classes can be collinear, rich lines of many slopes
appear (their number grows quickly with p), they cross orbits, and the LP is far from tight.  Heuristic: fix the HJSW set S₂ ⊂ H(1);
almost every point of H(k) ∩ G(p) lies on a line through two points of S₂ (log p blocking pairs per point on average; 0–2 unblocked
points for p ≤ 101): to add a point of the second hyperbola one must delete points of the first.

## Deliverable
A written argument (LaTeX or markdown) for whichever of T1–T4 you can establish, with every lemma stated; or a clear account of
where each attempted route fails, plus any certified numerical evidence (send back point lists; we verify with saturation.py).
Do not spend effort on re-proving the one-hyperbola theorem.  Do not trust LLM-generated "proofs" without a line-by-line check —
we will re-derive everything.

## Резюме по-русски
Задача агентам: доказать (или опровергнуть), что объединение двух модульных гипербол в боксе HJSW даёт максимум 3(p−1)+O(1) законных
точек — со списком ослабленных целей T1–T4; данные и код в публичном репозитории, доступ давать не нужно (read-only достаточно).
