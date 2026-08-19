# Deep-research brief 8 — "integrality from many weak constraints": where else does this phenomenon live, and how were OUR holes filled there?

(Русское резюме и инструкция — внизу.  Приложения: `phenomenon.py` — спецификация явления; `holes.py` — восемь дыр H1–H8 с полями
"filled_elsewhere".  Задача ресёрча — найти для каждой дыры системы, где аналогичная дыра ЗАКРЫТА, описать механизм закрытия
и оценить переносимость.)

## 0. The phenomenon in one paragraph (see `phenomenon.py`)
A packing problem "at most cap = 2 points on every line" over a finite candidate set V (for us: the 8(p−1) lifts of the two hyperbolae
xy ≡ ±1 (mod p) into a 2p×2p box).  Constraints split into STRONG ones (lines with ≥ 5 candidates: rows, columns, slopes ±1) — visible to
linear programming, certified by covers — and WEAK ones (three-point lines of all other slopes, ~p·log p of them): individually almost
worthless (x ≡ 2/3 satisfies all of them), jointly they determine the truth.  Numbers: trivial 4(p−1); LP with all lines ≈ 3.45(p−1);
proved 11/3 → 115/32 ≈ 3.59 (covers by rows/columns/±1-blocks); truth by all exact data 3(p−1)+O(1) (gain ≤ +6 for p ≤ 19; conjecture:
≤ +6 for all p).  The parent problem (no-three-in-line in [N]²: 2N trivial, 1.5N constructions, nothing < 2N − o(N) proved — Green, Problem
72) is the same phenomenon in pure form.  Signatures: many constraints of size cap+1 with degrees ~log|V| and O(1) codegrees; LP(all) ≈
LP(strong); algebraic extremals; O(1) gain over the construction; local certificates plateau far above the truth.

## 1. Our holes (see `holes.py`; each has a "testable now" experiment we can run ourselves)
H1 higher-order relaxations never computed (SoS/Lasserre level 2, hypergraph θ, Delsarte-type LP over local densities);
H2 no "flag-algebra" formulation over the local limit (we do have the local law: equidistribution of positions on curves + Kummer
independence);
H3 no stability theorem for near-maximum lawful subsets of ONE hyperbola (we have the exact classification 9^s of the maxima);
H4 no exchange/matching lemma "each point of the second hyperbola costs one point of the first" (numerically the trade-off slope is
exactly 1 at every split);
H5 the analytic wall: 2-D short character/mixed sums below p^{1/4} (Burgess range) — needed by any spectral/Fourier argument with
positions; the trace method needs dimension ~log p where known multi-dimensional Burgess bounds (Chang 2009 for binary quadratic forms
at p^{1/4+ε}; Pierce–Xu 2020: p^{1/2−1/(2(n+1))}) degrade;
H6 no algebraic (polynomial-method) formulation of "three lifts are collinear in Z²" — the mod-p part is algebraic, the p-part of the
determinant depends on POSITIONS (inequalities);
H7 no supersaturation lemma T(S) ≥ c(|S| − 3(p−1) − C) for arbitrary S;
H8 no regular sub-structure where a Bose-type "count through a point" works.

## 2. Research questions — for each, we want: (a) the analogous system, (b) the mechanism that closes the analogous hole there,
## (c) the exact hypotheses the mechanism needs, (d) an honest assessment of transferability to our setting (lifted curves in a box)

Q1 [H1, H2]  Where have SDP/SoS or flag-algebra certificates beaten LP for packing problems with many small constraints?
  - coding theory: Delsarte LP → Schrijver's SDP (Terwilliger algebra), Cohn–Elkies for sphere packing, three-point bounds;
  - Turán-type problems: flag algebras (Razborov), incl. applications in discrete geometry (Balogh–Lidický et al.: empty polygons,
    crossing numbers) and to sparse/local-limit settings ("flag algebras for bounded degree graphs", Benjamini–Schramm limits,
    factor-of-iid, local algorithms for LP/SDP: Kuhn–Moscibroda–Wattenhofer);
  - independence numbers of hypergraphs: θ-like SDP bounds (Bachoc–Pêcher–Thiéry?), Lasserre hierarchy on 3-uniform hypergraphs;
  - what is known about how many levels are needed to see "3-term" constraints (SoS lower bounds for random 3-XOR / for spin-glass energy:
    Kunisky–Bandeira, Barak et al.).
  Deliverable: a recipe for the smallest relaxation likely to see our three-point lines, with the size of the computation at p ≈ 20–60.

Q2 [H3, H4]  Stability of algebraic extremals + exchange arguments giving "construction + O(1)":
  - arcs in PG(2,q): Segre's lemma of tangents, "incomplete arcs are contained in conics" (Segre, Thas, Voloch, Ball–Lavrauw...),
    complete arcs and secants ("every point outside a complete arc lies on a secant"); the MDS conjecture (Ball 2012) — the polynomial
    method for "no k in a hyperplane";
  - additive combinatorics: Vosper's theorem (structure of critical pairs), Kneser, Freiman; sum-free sets in Z_p exact ⌊(p+1)/3⌋;
    Sidon sets and the "√N + O(1)" problem — any partial results proving O(1) gains anywhere?
  - shifting/compression (Erdős–Ko–Rado, Kleitman): a general device turning extremal into structural — does it exist for point-line
    problems in boxes/tori?
  - no-three-in-line in the torus (Z/n)² and in F_p² (arcs = p+1): what exactly is known for boxes [N]² (Guy–Kelly, Flammenkamp,
    Green Problem 72), for "no-three-in-line on a curve mod p in a box" (Hall–Jackson–Sudbery–Wild 1975; Kovács–Nagy–Szabó 2026).
  Deliverable: candidate formulations of a stability theorem for one hyperbola and of an exchange lemma for two, with the analogous
  proofs in the literature summarised step by step.

Q3 [H5]  Character/mixed sums over 2-D sets below the Burgess range:
  - Chang (Burgess in F_{p²}, GAFA 2009; boxes in F_{p^n}); Bourgain–Chang on sums over sets with small doubling / GAPs; Alsetri
    (BLMS 2026, GAPs of rank 2); Karatsuba's method for χ(f(n)); Bourgain's sum-product approach to exponential sums; Heath-Brown–Pierce
    mixed sums; Pierce–Xu forms; anything on "character sums over Gaussian-integer discs χ(N(z))" or over norm forms of quadratic fields;
  - what is the smallest scale L for which |Σ_{|z|≤L} χ(N(z)) w(z)| = o(L²) is known for smooth/positional weights w? For products
    χ(N(z₁)N(z₂)N(z₁+z₂)) over 4-D boxes?
  Deliverable: a table (statement / range / hypotheses) and a verdict on the "large-scale restriction" idea (use only pattern families at
  scales ≥ p^{1/4+ε}, where linear counts survive) — which cycle sums remain out of range.

Q4 [H6]  Polynomial method with inequalities:
  - Bombieri–Pila (integer points on curves in boxes: algebra + box), Heath-Brown's determinant method, "polynomial method over Z with
    reduction mod p", Combinatorial Nullstellensatz with size constraints; Guth–Katz partitioning in F_p²?; Dvir/Kakeya; Segre;
  - is there ANY instance where a "no three collinear"/"few collinear" statement about a lifted (integer) point set with mod-p structure
    was proved algebraically?
  Deliverable: the exact algebraic form of our lifted-collinearity condition (we will supply the equation) and which known method could
  in principle exploit it.

Q5 [H7]  Supersaturation for point-line problems:
  - Erdős–Simonovits, Varnavides-type counting, hypergraph removal; in geometry: Szemerédi–Trotter and Elekes–Szabó/Elekes–Rónyai
    ("few collinear triples on curves of degree ≥ 3", quantitative versions over F_p: Bourgain–Katz–Tao, Rudnev, Shkredov);
  - Roth-type problems with restricted differences (Sárközy–Furstenberg; 3-APs with QR common differences) — our triples ARE 3-AP-like
    patterns along the curve with steps z ∈ Z[i] having χ(N(z)) = 1, plus lift/orientation signs.
  Deliverable: which known counting theorem for "collinear triples in dense subsets of an algebraic curve mod p in a box" comes closest,
  and what it would give (linear supersaturation? for which density?).

Q6 [H8]  Regularity that makes "counting through a point" work: arcs/ovals/ovoids (Bose, Qvist), blocking sets (Blokhuis — polynomial
  method), designs (Fisher, Ray-Chaudhuri–Wilson LP): what minimal regularity suffices, and can it be manufactured by restricting to a
  sub-family of directions (Gaussian steps of one scale)?

Q7 [meta]  Problems of the type "algebraic construction is conjecturally optimal up to O(1)" that WERE solved: list them (arcs, ovoids,
  Singer difference sets, sum-free sets, ...) with the closing method; and the ones that remain open (no-three-in-line, Sidon √N + O(1),
  Turán (3,4)); extract the pattern "what distinguishes the solved ones" (regularity? group structure? polynomial identity?).

## 3. Format of the answer we need
For each Q: (i) 3–6 sources with exact statements (theorem numbers if possible); (ii) a "mechanism card": inputs → steps → output;
(iii) transfer assessment: which of our interfaces I1–I6 (in `holes.py`) it would plug into, what is missing, and a probability
estimate; (iv) at the end, a ranked list of the three most promising transfers with a first experiment for each (we can compute up to
p ≈ 10⁵ for local statistics and solve exactly to p ≈ 20–60).

Attachments: `phenomenon.py`, `holes.py` (this directory); context: the note `paper/hjsw_window.tex` (v1.9/1.10, sections 5–10),
`docs/research/pair_bound_notes.md` (§§17–29, B.12–B.19), `model_theorem_conditional.md`.

---
## Резюме по-русски
Явление: правду задачи (3(p−1)+O(1)) определяют не сильные ограничения (строки/столбцы/±1‑прямые, доступные LP), а совокупность
слабых — трёхточечных прямых всех наклонов; LP их не видит (x ≡ 2/3 всех удовлетворяет), поэтому все наши сертификаты выходят на плато
3.45–3.6.  `phenomenon.py` описывает явление вне нашей задачи (рамки, принципы P1–P5, бестиарий похожих систем, признаки S1–S6, суть);
`holes.py` — восемь дыр H1–H8 (релаксации высшего порядка, флаги/локальный предел, устойчивость одной гиперболы, лемма обмена,
короткие суммы, алгебраизация лифтов, насыщение, регулярность для счёта «через точку») — с полем «где закрыто в других системах».
Просим: для каждой дыры найти системы, где аналогичная дыра закрыта, описать механизм (входы → шаги → выход), гипотезы, и оценить
переносимость на нашу систему (кривые mod p, поднятые в коробку); в конце — три самых перспективных переноса с первым экспериментом.
