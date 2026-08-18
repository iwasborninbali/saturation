# Deep-research brief 6 — exact statements and references we need for one proof (short, precise)

(Русское резюме внизу.  Нужны ТОЧНЫЕ формулировки теорем с константами и ссылками на страницы; никакого обзора.)

## Context (one paragraph)
We prove: for the union of the two modular hyperbolae xy ≡ ±1 (mod p) in the 2p×2p HJSW box, every no-three-in-line subset has at
most 4(p−1) − 4·m₈(p) points, where m₈(p) = number of slope-(+1) integer lines carrying eight candidate points.  Then we show
m₈(p) = p/12 + o(p).  The counting reduces to: the number of F_p-points (a,b) of the affine cubic C₀: a b² + (a²−1) b + a = 0 (a ≠ 0)
whose least absolute residues (X(a), X(1/a), X(b)) ∈ [−(p−1)/2, (p−1)/2]³ lie in an explicit union of four convex polytopes (defined by
sign conditions and by the value of the linear form X(a) − X(1/a) + X(b) relative to p/2, p).  We want the count = (1/3)|C₀(F_p)| + error.
Our sketch: (i) C₀ absolutely irreducible (discriminant a⁴ − 6a² + 1 not a square); (ii) for (u,v,w) ≠ 0 the function ua + v/a + wb is
non-constant on C₀, so Bombieri's bound gives |Σ_{P∈C₀(F_p)} e_p(ua + v/a + wb)| ≤ C√p; (iii) Erdős–Turán–Koksma ⇒ box discrepancy of
{(a, 1/a, b) mod p} is O(p^{−1/2} log³ p); (iv) polytope with O(1) faces ⇒ count = vol·N + O(p^{5/6} log³ p) (covering by boxes), or better
via isotropic discrepancy.

## Questions (each: exact statement, constants, precise citation with page/theorem number)
1. **Bombieri's theorem** for exponential sums along a curve: E. Bombieri, "On exponential sums in finite fields", Amer. J. Math. 88 (1966)
   71–105 — the exact statement (Theorem 6? ) bounding |Σ_{P ∈ C(F_q)} ψ(f(P))| for an absolutely irreducible curve C of degree d and a
   rational function f (with poles), including the hypothesis (f not of the form g^p − g + const) and the constant (d² + 2d·deg f − 3)√q or
   whichever is correct.  Also the modern references: Kowalski's notes, Iwaniec–Kowalski "Analytic Number Theory" Ch. 11 (Theorem 11.23?),
   Perelmuter 1969, and the version for affine curves with poles at infinity of f (our f = ua + v/a + wb has poles where a = 0 and at
   infinity).  We need a statement we can quote verbatim with correct hypotheses.
2. **Absolute irreducibility criterion** we use: a polynomial F(a,b) = a b² + (a²−1) b + a, monic-ish quadratic in b over F_p(a) with
   non-square discriminant in F̄_p(a) ⇒ irreducible over F̄_p(a) ⇒ (being primitive in b) irreducible in F̄_p[a,b].  Confirm this reasoning
   (Gauss lemma) and give a textbook reference; also whether C₀ is smooth for all p ≥ 5 (compute the singular points; the genus) — we only
   need |C₀(F_p)| = p + O(√p) (Weil for possibly singular absolutely irreducible plane curves: Aubry–Perret bound |#C(F_q) − q − 1| ≤ 2g√q + δ).
3. **Erdős–Turán–Koksma inequality** in dimension s = 3: exact form D_N ≤ C_s (1/H + Σ_{0<‖h‖_∞≤H} |S_N(h)|/(N r(h))) with r(h) = Π max(1,|h_i|)
   and the constant C_s (e.g., 3^s / …); reference (Kuipers–Niederreiter, Uniform Distribution of Sequences, Theorem 2.? / Drmota–Tichy).
   Note our point set lives on the discrete torus (Z/p)³ — state the version for finite abelian groups or explain the reduction.
4. **From boxes to convex polytopes**: the cleanest reference for "the number of points of a sequence with box discrepancy D in a convex set
   K ⊂ [0,1)^s is N λ(K) + O(N D^{1/s})" (isotropic discrepancy J_N ≤ 4s D_N^{1/s}, Kuipers–Niederreiter Thm 1.6?), and the sharper bound for
   polytopes with a bounded number of faces (O(N D log?) or O(N·D)·(faces)) if one exists (e.g., via decomposition into O(1/ε) boxes; or
   Beck–Chen / Schmidt for polytopes).  We only need o(N); the best clean exponent is welcome.
5. **A shortcut**: is there a known result on the joint distribution of least residues of (a, 1/a) (the modular hyperbola in a box) that we
   could cite directly — Shparlinski's survey "Modular hyperbolas" (Jpn. J. Math. 7, 2012) §"distribution in boxes" and the papers of
   Kerr, Shparlinski, Garaev on points of the hyperbola in small boxes — and could a similar statement for our cubic be cited rather than
   re-derived?
6. **Sanity**: is our claimed relative volume 1/3 (four polytopes of measure 1/8·2/3 each in the cube of least residues; details in
   docs/research/pair_bound_notes.md §12 and the note §"Two hyperbolae") consistent with a direct computation you can do?

## Deliverable
Verbatim statements with references (author, title, journal, year, theorem number, page), one paragraph each; a recommended way to write
the proof of "m₈(p) = p/12 + O(p^{5/6} log³ p)" in ≤ 1 page citing them; and any pitfalls (e.g., the p | denominator issue for f = ua + v/a).

---
## Резюме по-русски
Для одного доказательства нужны точные формулировки: оценка Бомбьери для сумм экспонент вдоль абсолютно неприводимой кривой
(с гипотезами и константой), критерий абсолютной неприводимости нашей кубики и оценка числа её точек, неравенство Эрдёша–Турана–Коксмы в
размерности 3 (с константой) и переход от боксов к выпуклым многогранникам — всё со ссылками на страницы. Плюс: можно ли сослаться на
готовые результаты о распределении (a, 1/a) в боксах (Шпарлинский), и проверка нашего объёма 1/3.
