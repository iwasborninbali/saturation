> External LLM-assisted audit ("Gate B: FAIL"), relayed by the owner on 2026-08-19 from ChatGPT agents working on `docs/research/task_for_agents_barrier.md`
> and `deep_research_brief_5_barrier.md`.  Not a human referee.  Our response: `docs/research/pair_bound_notes.md` §13.

Verdict: the current computational program is useful reconnaissance but cannot support the proposed barrier theorem, T1, or an
unspecified O(1)-gain conjecture (failure of identification/certification, not a disproof).

Decisive findings (their wording, abbreviated):
1. Finite-field symmetry is not a symmetry after lifting: p=7, G=[-3,10]x[0,13]: alpha(H: xy=1) = 18 = 3(p-1); the F_7-shear image
   C: (x-y)y = 1 has alpha(C ∩ G) = 16 (certificate: rich lines x=-1,1,6,8, x+y=10,11 with 4 points each, 4 uncovered points ⇒ ≤ 16;
   witness of size 16 given).  So quotienting conics by AGL_2/PGL_3 is invalid; only integral affine box-preserving bijections.
   p=5: alpha(P_2)=15 ≠ alpha(P_3)=16 although 3 = 2^{-1} mod 5.
2. "Conics, c=2, exactly 3(p-1)" is too broad — equality is proved for xy=c in the HJSW placement only (upper bound not disproved).
3. Blocker heuristic not invariant under the choice of the one-hyperbola optimum (over the 9^s cores: unblocked 0–2 at p=13,k=2;
   0–4 at p=5,k=2); raw blocker counts do not lower-bound deletion cost — the object is a hitting/transversal problem / exchange frontier.
4. Finite data (gains 5,5,6,5) cannot distinguish constant, a log p, a sqrt p, delta p; the 3p x 3p values do not distinguish a limit
   below 3/2 from convergence to 3/2; v0.5 typo 1.44 (fixed in v0.6).
5. Certification: witnesses certify lower bounds only; SAT/MIP/CP-SAT share the point/line generator; needed: independently regenerated
   rich-line sets, UNSAT proofs (DRAT/LRAT) or exact branch certificates; the p=23 74/75 inconsistency between briefs and v0.5 must be
   pinned to a tag.
6. Definitions for a general statement: box conventions, box origin, k ∈ F_p^* \ {1}, fixed vs adversarial k(p), reduced curves without
   line components, reducible/singular curves separately, common coordinates for the two-prime experiment.
Corrected experiment design: pin tag + manifest with hashes; two independent line generators; no symmetry quotient without box
automorphism; certified intervals L ≤ alpha ≤ U for all p, k with strata over k; the exchange frontier (deletions r from a one-hyperbola
core vs additions from H(k), over all cores); test the actual curve class (all conics by coefficient tuples mod box symmetries; generic
pairs of conics; reducible/singular); predeclared competing rates; falsification criteria per claim.
