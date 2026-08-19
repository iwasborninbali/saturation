# Prop m7asym (k = −1): the number of seven-point ±1-lines is m₇(p) = m₈(p) + O(√p log⁴p) = p/12 + O(√p log⁴p)
*(first solver, 2026-08-19; for T2.21 — the same argument as Prop m8asym / §24 (T2.18), nothing new to compute)*

Setting (note, Section "Two hyperbolae"): k = −1, slope +1, residue d; the H(1)-pair {a, −1/a} (a − 1/a ≡ d) and the H(−1)-pair {b, 1/b} (b + 1/b ≡ d);
the pair shares its centre iff X(a)X(1/a) < 0 (resp. X(b)X(1/b) < 0); the group is (4,8,4) iff both pairs share, (3,7,5,1)/(1,5,7,3) iff exactly one shares,
(2,6,6,2) iff none (Section "Two hyperbolae", Lemma groups; §24). Let A = "the H(1)-pair shares", B = "the H(−1)-pair shares".
Prop m8asym computes, on the genus-1 curve C₀(−1) : ab² − (a²−1)b + a = 0 (b + 1/b = a − 1/a) with the four linear forms X(a), X(1/a), X(b), X(1/b) — the fourth
determined by X(b) − X(a) + X(1/a) — that #{d : A ∧ B} = (1/3)·(number of residues d with two two-element pairs) + O(√p log⁴p), i.e. m₈ = p/12 + O(√p log⁴p),
via the volume 1/3 of the region {A ∧ B} for the law (X(a), X(1/a), X(b)) uniform on (−p/2,p/2)³.
Claim: the regions {A ∧ ¬B} and {¬A ∧ B} have volume 1/6 each, {¬A ∧ ¬B} volume 1/3.  Proof: P(A) = P(X(a)X(1/a) < 0) = 1/2 (two independent uniform signs),
so P(A ∧ ¬B) = 1/2 − 1/3 = 1/6; the map (X(a), X(1/a), X(b)) ↦ (X(b), X(1/b), X(a)) with X(1/b) = X(b) − X(a) + X(1/a) is measure preserving on the torus
and exchanges the roles of the two pairs (it sends A to B and B to A: X(1/a) = X(1/b) − X(b) + X(a) is the inverse relation), whence P(¬A ∧ B) = 1/6, and
P(¬A ∧ ¬B) = 1 − 1/3 − 1/6 − 1/6 = 1/3.  (This is the (1/3, 1/3, 1/3) law of §24: "both shared / exactly one / none".)
The counting error is the same as in Prop m8asym (Selberg polynomials for the four interval conditions, Bombieri on C₀(−1)): O(√p log⁴p).  Hence
   m₇(p) := #{seven-point lines of slopes ±1} = #{(3,7,5,1)-groups, both slopes} = m₈(p) + O(√p log⁴p) = p/12 + O(√p log⁴p),
and likewise the number of (2,6,6,2)-groups is p/12 + O(√p log⁴p).  (Data, B.19: B₇/p = 0.088, 0.088, 0.050 at p = 113, 137, 199 — fluctuating around 1/12.)
Consequence for T2.21 (second solver's plan): with the orbit cover lemma (saving 1 per clean (3,7,5,1)-orbit) and the cleanliness lemma
(#clean ≥ 2m₇ − 2·#incidences), α(P₋₁) ≤ 4(p−1) − 4m₈ − #clean + O(1) = (11/3 − 1/6 + 2ι + o(1))(p−1), ι = lim #incidences/p, to be computed.
