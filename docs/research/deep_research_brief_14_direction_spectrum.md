# Deep-research brief 14 — спектр направлений и κ (бывший «бриф 12»: номер 12 занят SAT-оптимизацией A280537 от 21.08)

(Русское резюме внизу.  Это брифинг про ПРАЙОР-АРТ для одного конкретного измерения.  Нужны точные ссылки с цитатами, а не обзор
задачи no-three-in-line — задачу мы знаем.  Ответ «не нашёл» по каждому вопросу ценен ровно так же, как ответ «нашёл», если он
подкреплён тем, ГДЕ искали.)

## 0. What we measured (so the answer can be calibrated)

Data: Achim Flammenkamp's no-three-in-line database (https://wwwhomes.uni-bielefeld.de/achim/no3in/, file `all_known_solutions`,
state of 2026-08-31).  Complete enumeration of all 2n-point solutions for n ≤ 20 (118 057 D4-orbits at n = 20); for n = 21…76 only
solutions with non-trivial symmetry (mostly rot2 up to n ≈ 31, rot4/rct4 above).

**Measurement 1 (a constant).**  Let κ(n) = (number of diagonals x − y = const carrying exactly two points) / n, averaged over all
solutions.  Result: κ = 0.731 ± 0.002, flat from n = 12 to n = 57 (complete data to n = 20; the symmetric-only samples above agree
within 0.001; a weighted fit K + c/n gives K = 0.732).  A maximum-entropy null model — 2n random points in the n×n grid subject only
to "≤ 2 points per diagonal", with the true diagonal lengths n − |j| — gives 0.639 at n = 20 and 0.6486 in the limit n → ∞.
Real solutions sit 13 % above the null: forbidding collinear triples in *all other* directions pushes pairs *onto* the diagonals.

**Measurement 2 (a law).**  Every pair of points determines a primitive direction (a, b).  For each solution we histogram the
C(2n, 2) = n(2n − 1) pairs by direction ("direction spectrum"; the total is an identity and served as a control).  At n = 20,
480 distinct directions are realised — essentially every primitive vector available in the 20×20 difference set.  Divided by the
expectation for a *uniformly random* 2n-subset of the grid (which is Σ_s (n − s|a|)⁺(n − s|b|)⁺ · 2n(2n−1)/(n²(n²−1))), the ratio
is monotone in m = max(|a|, |b|):

| direction | (1,0) | (1,±1) | (1,±2) | (1,±3) | (2,±3) | m=4 | m=5–7 | m=12 |
|---|---|---|---|---|---|---|---|---|
| measured / random | 0.54 | 0.61 | 0.78 | 0.94 | 0.99 | 1.08 | 1.16–1.18 | 1.09 |

((1,0) is forced: exactly n row-pairs.)  Short directions are depleted, long directions enriched, crossover at m ≈ 3–4.

**Mechanism we suspect.**  A pair in direction (a, b) shades (forbids) the ≈ n/max(|a|,|b|) − 2 remaining cells of its line; a
configuration that must reach 2n points cannot afford many expensive pairs, so short directions are depleted, and since the total
pair count is fixed the surplus lands on long directions.  (In a DFS this is the classical least-constraining-value heuristic;
our own solver already has it as an option.)

**Why it matters to us.**  The Guy–Kelly heuristic is itself a sum over directions: T(n) = Σ_{gcd(a,b)=1} Σ_{s≥2} (s−1)(n−s|a|)⁺(n−s|b|)⁺,
and the corrected constant c = π/√3 gets its π from 6/π², the density of primitive directions.  We measured the heuristic's error
in aggregate (Zenodo 10.5281/zenodo.22063191); the spectrum above is that error *decomposed by direction*.  Before we write it up we
must know whether anyone has measured or derived it.

**What we already know and do NOT need repeated.**  Guy & Kelly 1968; Hall–Jackson–Sudbery–Wild 1975; Flammenkamp 1992/1998;
Guy's 2004 correction with Ellmann (OEIS A000769); Voutier arXiv:2603.00215; Prellberg's threshold n ≥ 493; the 2026 paper
arXiv:2607.05255 (Ghosal, Goenka, Grebennikov, Keevash, Kwan, Pham, "No-(k+1)-in-line problem for k ≥ 3") whose Remark 1.7 says
there are "important statistical differences between the case k = 2 and the case k ≥ 3 (related to the relative significance of lines
in different directions)" — this is the closest thing we know to our object, but it is theoretical, large-n, about random
constructions, and (as far as we can see) contains no measurement on actual extremal configurations.

## 1. Questions, by priority

**Q1. Has the direction spectrum of actual maximal configurations been published anywhere?**  Any table, plot, or sentence giving
the number of point pairs per slope, the occupancy of diagonals (or of lines of any fixed direction), "slope distribution",
"direction statistics" of no-three-in-line solutions — at any n, on any dataset.  Look at: Flammenkamp's own pages (readme,
symmetry_remarks, the 1992 and 1998 papers, the "near miss" material); Guy–Kelly 1968 and Guy's later notes (UPINC problem F4) —
did they discuss *which* directions dominate the triple count?; Anderson 1979; Pegg (MathWorld); Knuth TAOCP 4B exercises
(no-three-in-line appears in the exact-cover exercises); recreational literature (Dudeney, Gardner columns); computational papers
using SAT/CP on the problem (any author, 2000–2026), including Marijn Heule's 2026 results for n = 65…76 (talks, slides, GitHub,
blog posts — what does he say about structure of solutions?); Jacob Davies' 2026 AI-constructed solutions (any writeup?).

**Q2. Is κ — the fraction of doubly-occupied diagonals, or any equivalent invariant — known?**  Equivalents: number of occupied
diagonals (= 2n − κn), number of points on the two main diagonals, "diagonal defects", occupancy words over {0,1,2} for the diagonal
direction.  A value near 0.73, or the null value 0.6486, appearing anywhere would settle this.

**Q3. Per-direction decomposition of the Guy–Kelly count.**  In Guy–Kelly 1968, in Guy's 2004 correction, in Voutier 2026, in
Prellberg's work: is the triple count T(n) ever split by direction, and is there any statement of the form "directions with
max(|a|,|b|) ≤ m contribute a fraction f(m) of the triples / of the threshold"?  Quote it verbatim if so.  And in arXiv:2607.05255:
what exactly is said about k = 2 and the "relative significance of lines in different directions" — quote Remark 1.7 and any
surrounding discussion in full.

**Q4. Adjacent theory.**  (a) Slopes determined by point sets: Ungar's theorem (2⌊n/2⌋ slopes), Scott's problem, "few slopes"
results — is there anything on the *multiset* of slopes (multiplicities), not just the number of distinct slopes?  (b) Random sets
avoiding collinear triples ("no-three-in-line in random subsets", "collinear triples in random sets", deletion/alteration method):
does any paper give the direction distribution of the surviving pairs?  (c) Hard-core / max-entropy models on the collinearity
hypergraph of the grid ("≤ 2 points on every lattice line"): has anyone computed the slope spectrum or diagonal occupancy of such a
model by cluster expansion, Bethe/cavity approximation, or transfer matrix?  A computable prediction for κ is what we most need.

**Q5. Regularities of solutions used inside search.**  Has anyone used statistical properties of known solutions as
*streamlining constraints* (Gomes & Sellmann, CP 2004; LeBras–Gomes–Selman, AAAI 2012) or as branching/value heuristics for
no-three-in-line search?  Which properties, and did they report a measured speed-up?  For Heule's 2026 SAT campaign specifically:
encoding, symmetry class handling, any added constraints beyond the problem itself, any cube-and-conquer split, compute used.

**Q6. Three dimensions.**  For "no four coplanar in the n×n×n grid" (OEIS A280537) the equivalence
"no 4 coplanar ⟺ in every projection along a lattice direction no 4 projected points are collinear" is elementary; has it been
used in the literature or in the 2016 Al Zimmermann contest ("Point Packing"?) writeups, and is any direction/plane statistic of
the record configurations published?

## 2. What counts as an answer

*Prior art* = a published or web-posted measurement (table/plot/number) of pairs-per-direction or diagonal occupancy on actual
solutions, or a theoretical law for the slope multiset of extremal configurations, or a computed κ-like constant.
*Not prior art* = the heuristic itself, generic slope-counting theorems, or the k ≥ 3 paper's remark (we have those).

Per question: verbatim quotes with page/section, exact references (DOI / arXiv id / URL, retrieval date), and where you searched
when you found nothing.  End with a one-line verdict per item: "spectrum law: known / partially / not found", "κ: known / not found",
"per-direction Guy–Kelly split: known / not found", "streamlining for this problem: known / not found".

---
## Резюме по-русски

Мы измерили на полной базе Фламменкампа (все решения до n = 20, симметричные до n = 76) две вещи: (1) долю диагоналей x − y = const
ровно с двумя точками — константа κ = 0.731 ± 0.002, ровная от n = 12 до 57, на 13 % выше нуль-модели «случайные 2n точек, ≤ 2 на
диагональ» (0.6486 в пределе); (2) спектр направлений — число пар точек на каждое примитивное направление, делённое на ожидание для
случайного множества: монотонный закон, короткие направления обеднены (0.54, 0.61, 0.78, 0.94 для m = 1, 1, 2, 3), длинные обогащены
(1.08…1.18 при m = 4…7).  Это — ошибка эвристики Гая–Келли, разложенная по направлениям.  Нужно узнать ДО написания текста: публиковал
ли кто-нибудь такое измерение или закон (Q1, Q2), делил ли кто-нибудь счёт Гая–Келли по направлениям (Q3), есть ли вычислимая
модель, предсказывающая κ (Q4c), использовал ли кто-нибудь такие закономерности внутри поиска, в частности Хойле в 2026 (Q5),
и есть ли аналог для трёхмерной задачи A280537 (Q6).  Что мы уже знаем и что повторять не нужно — перечислено в разделе 0.
Форма ответа — раздел 2: цитаты, точные ссылки, где искали, и вердикт в одну строку по каждому пункту.
