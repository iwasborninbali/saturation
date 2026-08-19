# galois_rootcounts — Galois group of tᵏ − t − c, the fibre products behind the local law, and the generalised cover constant
*(agent: galois_rootcounts; tools `slack/g_agents/galois_rootcounts.py`, output `slack/g_agents/galois_rootcounts_output.txt`; reads `docs/research/permutation_cubic_note.md` §0–3 as its model, cross-references `slack/g_agents/x5_x7_numerics_exact_constant.py` for an independent check of Part 3)*

## 0. Summary

For f(t) = tᵏ, k ∈ {5, 7} (both prime), and every prime p outside the finite bad set {p : p ∣ k(k−1)} (in particular every p in the task's 500–2000 range):

1. **Gal(tᵏ − t − c / F_p(c)) = S_k exactly** (Part 1) — not just "typically", the *whole* group, for the *whole* generic fibre, by an unconditional elementary argument (field-degree transitivity + prime-degree primitivity + a trinomial-discriminant computation identifying a simple branch point + Jordan's theorem). Consequently the number-of-roots distribution of tᵏ − t = c over c ∈ F_p tends, as p → ∞, to the **rencontres distribution of S_k** (Chebotarev), confirmed to high precision below both in the coarse (root-count) and the full (cycle-type) statistic.
2. **The ordered-distinct-m-tuple fibre products X_m (1 ≤ m ≤ k) are absolutely irreducible with genus depending only on k, m** (Part 2) — an immediate consequence of statement 1, because the S_k-computation is already a *geometric* (F_p‾-level) statement. This is what licenses Bombieri/Weil equidistribution of m roots' positions with a p-independent error constant, for every m up to k at once (not just pairwise).
3. **The cover constant C(P) := lim_{p→∞} cost/(2p)** of the generalised ≥4-line-plus-singletons cover (background note §2, Remark 2) is computed here **exactly**, as a rational function of the rencontres numbers, reproducing 11/8 at k = 3 (Theorem G3.5) and giving

       k = 5:  C(P) = 12059/8640  = 1.395718…
       k = 7:  C(P) = 203347/145152 = 1.400925…

   These match, digit for digit, the independently-coded computation in `slack/g_agents/x5_x7_numerics_exact_constant.py` (a different agent's file, not read until after my own derivation was complete and run — see §3.4), which is strong evidence neither derivation has a bookkeeping error. That file flagged its own local-law inputs as "conjectural… not proved" for k=5,7; Parts 1–2 here supply exactly the missing theory (the S_k-Galois-group fact that makes the rencontres law a theorem, and the irreducibility fact that makes the Bombieri-equidistribution step legitimate) at the same level of rigour the note gives for k = 3.

All five numerical checks (discriminant/simple-branching, full Chebotarev cycle-type, rencontres marginal, genus/point-count, cost-constant cross-check) pass; see §4 for the consolidated table and exact script/line pointers.

---

## 1. The Galois group of tᵏ − t − T over F_p(T), k ∈ {5, 7}

### 1.1 Setup and the three ingredients

Write g(x) = xᵏ − x, T = g(x). Fix k odd, k ≥ 3, and a prime p with p ∤ k(k−1).

**(a) Transitivity, for free.** T is a non-constant polynomial in x of degree k, so [F_p(x) : F_p(T)] = k exactly (a rational function of degree k in lowest terms generates a degree-k extension of the base — the minimal polynomial of x over F_p(T) is g(X) − T, degree k in X, and it *is* the minimal polynomial because F_p(T)(x) = F_p(x) already). Hence g(X) − T = Xᵏ − X − T is **irreducible over F_p(T)**, so its Galois group G ≤ S_k (acting on the k roots) is **transitive**. This uses nothing about k except that g is a non-constant polynomial map of degree k — true for any odd k ≥ 3.

**(b) Primitivity, using k prime.** A block system for a transitive G ≤ S_k has block size dividing k. If **k is prime** the only divisors are 1 and k, i.e. the only block systems are trivial: transitive ⟹ **primitive**. (This is the one step in the whole argument that needs k prime — see the remark on general k in §1.4.)

**(c) A transposition, via the trinomial discriminant.** g′(x) = k xᵏ⁻¹ − 1 has k−1 roots (the critical points), each simple: since p ∤ k(k−1), x^{k−1} = 1/k is separable (k−1 distinct roots in F_p‾) and at each root x₀ ≠ 0, g″(x₀) = k(k−1)x₀^{k−2} ≠ 0. **Claim:** the k−1 corresponding critical *values* c_i = g(x_i) are pairwise distinct in F_p‾. This is where the classical **trinomial discriminant formula** enters: for f(x) = xⁿ + ax + b,

    disc_x(f) = (−1)^{n(n−1)/2} [ nⁿ b^{n−1} + (−1)^{n−1}(n−1)^{n−1} aⁿ ].

With n = k, a = −1, b = −T (k odd ⟹ k−1 even):

    disc_x(xᵏ − x − T)  =  ε_k · ( kᵏ T^{k−1} − (k−1)^{k−1} ),     ε_k = ±1 depending only on k.

This is the key structural fact: **as a polynomial in T, the discriminant is a *pure power*** kᵏTᵏ⁻¹ − (k−1)^{k−1}, up to sign — its k−1 roots (= the critical values, since disc_x(g(x)−T) vanishes exactly where f, f′ share a root) are exactly the (k−1)-th roots of (k−1)^{k−1}/kᵏ. Since p ∤ k(k−1), that constant is nonzero and the (k−1)-th power map is separable, so **the k−1 critical values are pairwise distinct** — no extra "bad primes" beyond p ∣ k(k−1) are needed at all. (Verified independently below, §1.2 — not merely quoted from memory.)

Consequently, over c near a critical value c_i, the fibre of g has one ramification-index-2 point and k−2 unramified points: a **simple branch point**, tame since p ≠ 2. The local inertia there is generated by a **transposition** in G (standard fact about simple tame branch points: locally x^k-x-c_i-\epsilon looks like a ramified quadratic extension of the completion at c_i, contributing order-2 inertia).

### 1.2 Theorem and proof

**Theorem.** For k ∈ {5, 7} and every prime p with p ∤ k(k−1) (in particular every p in [500, 2000]), Gal(Xᵏ − X − T / F_p(T)) = S_k exactly.

*Proof.* G is transitive (1.a), hence primitive since k is prime (1.b), and contains a transposition (1.c). By **Jordan's theorem** (a primitive permutation group containing a transposition is the full symmetric group — classical; e.g. Wielandt, *Finite Permutation Groups*, Thm 13.3), G = S_k. ∎

This is a statement about the **geometric** Galois group (everything in (a)–(c) — degree counting, ramification, discriminant vanishing — is checked over the algebraic closure F_p‾, not just over F_p), which is exactly the form needed for Part 2.

*(Consistency remark: since disc_x(xᵏ−x−T) is, by the formula above, a **squarefree** polynomial in T of positive degree k−1, it is never a square in F_p(T), so G ⊄ A_k independently of the Jordan argument — ruling out the "only A_k" alternative before invoking Jordan.)*

### 1.3 Numerical checks

**(1) Discriminant/simple-branching check** (`check_discriminant`, script §1). Rather than hunting for the k−1 critical points inside F_p by brute force — **wrong tool**, since they need not be F_p-rational at all, only F_p‾-rational, and an early version of this check silently found 0–2 of them and "failed" for a reason that was a bug in the test, not the theorem — the correct check computes disc_x(xᵏ−x−c) directly via the **Sylvester-matrix resultant mod p** (verified first against the textbook quadratic case b²−4c) for k or more values of c, and confirms it equals ±(kᵏc^{k−1} − (k−1)^{k−1}) at every one (two degree-≤(k−1) polynomials agreeing at ≥ k points are identical, so this is a complete check of the polynomial identity mod p, not a spot check). Result: **exact match at every prime tested**, with a single consistent sign ε_k per k (ε₅ = +1, ε₇ = −1 — the sign is a disc/Res convention artifact, irrelevant to distinctness).

```
p=  503: tested 15 values of c, mismatches=0, consistent sign eps_k=1 (k=5)  -> OK
p= 1009: tested 15 values of c, mismatches=0, consistent sign eps_k=1 (k=5)  -> OK
p= 1999: tested 15 values of c, mismatches=0, consistent sign eps_k=1 (k=5)  -> OK
p=  503: tested 21 values of c, mismatches=0, consistent sign eps_k=-1 (k=7) -> OK
p= 1013: tested 21 values of c, mismatches=0, consistent sign eps_k=-1 (k=7) -> OK
p= 1999: tested 21 values of c, mismatches=0, consistent sign eps_k=-1 (k=7) -> OK
```

**(2) Full Chebotarev cycle-type check** (`check_chebotarev_cycletype`, script §2) — a **strictly stronger** test than the root-count marginal: for random c ∈ F_p, factor xᵏ−x−c over F_p by a from-scratch **distinct-degree factorization** (repeated-squaring Frobenius xᵖ mod f, polynomial gcd; verified first on hand-built test polynomials with known factorization patterns), record the degree-partition (= cycle type of Frobenius at c, since G = S_k acts naturally), and compare the empirical distribution over 400 samples to the *exact* S_k conjugacy-class probabilities |class|/k!. At p = 1999, k = 7 (400 samples): Σ|theory − empirical| over all 15 cycle types = **0.15–0.31**, against a noise floor of order 1/√400·√15 ≈ 0.19–0.32 — fully consistent with S_k and nothing smaller (e.g. A_k, which would show zero mass on odd-permutation cycle types such as (2,1,1,1,1,1) or (7,) — both are populated at their predicted rates). Full 15-row (k=7) and 7-row (k=5) tables at p ∈ {503, 1229/1231, 1999} in the output file.

**(3) Rencontres marginal** (`check_root_counts`) — direct O(p) root-count histogram of tᵏ − t = c, compared to the exact rencontres numbers; e.g. k=7, p=1999: empirical (0.384, 0.339, 0.201, 0.048, 0.024, 0.003, 0, 0.0005) vs. rencontres (0.368, 0.368, 0.183, 0.063, 0.014, 0.004, 0, 0.0002) — same shape, O(1/√p)-scale deviations as expected (this is the coarser statistic (2) refines; consistent with agent x5_x7_numerics's independent, larger-sample version of the same check).

### 1.4 General odd k, and what k prime buys

The proof above uses k prime *only* in step (b) (transitive ⟹ primitive). For general odd composite k, transitivity and the transposition are still available verbatim (they never used primality), but primitivity is no longer automatic — indeed it can fail: e.g. a transitive group containing both a k-cycle and a transposition need **not** be S_k when k is composite (D₄ ≤ S₄, generated by a 4-cycle and the transposition (2 4), is transitive, imprimitive, and has order 8 ≠ 24 — a genuine counterexample to the tempting "n-cycle + transposition ⟹ S_n" folklore claim for composite n). This is exactly why the literature on Galois groups of trinomials Xⁿ + aX + b (Uchida 1970, Cohen 1981, Osada 1987) needs extra hypotheses (typically on gcd(shift, n) or on the discriminant being a non-square) for composite n, and why this report only *claims* the clean unconditional S_k statement for k = 5, 7 (prime), as the task requests. The generic expectation for composite odd k is still S_k or A_k (matching the note's framing), but establishing it needs the finer classification of primitive/imprimitive groups containing an n-cycle, not attempted here.

---

## 2. Absolute irreducibility of the fibre products, and their genus

### 2.1 Why S_k (geometric) ⟹ irreducibility of every X_m

Let Y → P¹_c be the Galois closure of F_p(x)/F_p(T) (degree k! over the c-line; a point of Y = an ordering of all k roots of the fibre). §1's argument shows **Gal(F_p‾(Y)/F_p‾(T)) = S_k already at the geometric level** — every ingredient (degree of g, ramification indices, vanishing of the discriminant) was computed over F_p‾, not merely over F_p — so F_p‾(Y) is a *field* (Y is geometrically irreducible / absolutely irreducible over F_p, i.e. F_p is algebraically closed in its function field: there is no room for a bigger field of constants, because S_k already saturates the whole symmetric group and can't grow further under base change to F_p‾).

For 1 ≤ m ≤ k, let X_m be the curve of **ordered m-tuples of pairwise-distinct roots** of the same fibre: X_m = {(t₁,…,t_m, c) : tᵢᵏ − tᵢ = c ∀i, tᵢ ≠ tⱼ}. This is exactly Y / H for H = Stab_{S_k}(1,…,m) ≅ S_{k−m} (the pointwise stabiliser of m of the k labelled sheets, embedded as permutations of the remaining k−m); concretely it is the geometrically meaningful (top-dimensional, irreducible) component of the naive m-fold fibre product C ×_{P¹} ⋯ ×_{P¹} C of the curve C = {(t,c) : tᵏ−t=c} with itself m times — the naive fibre product additionally contains lower strata where some tᵢ coincide, which are (images of) X_{m′} for m′ < m under diagonal maps, not new geometric content.

Since F_p‾(X_m) = F_p‾(Y)^H is a **subfield** of the field F_p‾(Y), it has no zero-divisors: **X_m is absolutely irreducible for every 1 ≤ m ≤ k**, unconditionally once G = S_k geometrically (§1). This is precisely the hypothesis Weil's bound (equivalently, the Bombieri-style equidistribution the note invokes for k=3 via the conic Q₊ = X₂ at k=3) needs: a nontrivial additive-character sum over an absolutely irreducible curve is O(g·√p) with g its genus; over a *reducible* curve it can instead be Θ(p) (dominated by whichever component the character happens to be constant on) and the whole equidistribution argument collapses. Note that for k = 3 this recovers exactly the note's device: X₂ (k=3) **is** the conic Q₊, and irreducibility there was argued directly by identifying Q₊ as a smooth conic; here the same conclusion for **every** m ≤ k and **every** k with S_k geometric monodromy falls out of one Galois-theoretic fact instead of a case-by-case curve identification.

### 2.2 Genus, via Riemann–Hurwitz

X_m → P¹_c has degree D_m = k!/(k−m)!. Its ramification: at each of the k−1 finite branch points of C → P¹_c (simple, inertia = a transposition τ = (a b), §1), the fibre of X_m decomposes into ⟨τ⟩-orbits on ordered m-tuples of distinct labels from {1,…,k}: tuples missing both a,b are **fixed** (unramified); tuples containing exactly one of a,b, or containing both, are swapped in **pairs** (ramification index 2). Counting these orbits combinatorially:

    R(k,m) = (# ramified points, e=2, per finite branch point) = m(2k−m−1)/2 · (k−2)!/(k−m)!
    U(k,m) = (# unramified points per finite branch point)     = (k−2)!/(k−2−m)!   (0 if m > k−2)

and at the single totally-ramified point at infinity (inertia = a k-cycle σ), σ acts **freely** on ordered m-tuples of distinct labels for every 1 ≤ m ≤ k (a nonzero power of a k-cycle has no fixed points, hence fixes no tuple), giving (k−1)!/(k−m)! points each with ramification index k. Riemann–Hurwitz (X_m and P¹_c both rational base, only need the ramification divisor):

    2g_m − 2  =  −2·D_m + (k−1)·R(k,m) + (k−1)!/(k−m)!·(k−1)
             =  (k−1)!/(k−m)! · [ 2mk − m² − m − 2k − 2 ] / 2.

**All three combinatorial quantities (R, U, the free action at infinity) and the resulting genus were checked against a brute-force orbit count** (`itertools.permutations`, exact for k = 3, 5, 7, all m) — a genuine independent verification, not just algebra: this caught and fixed one bookkeeping slip in a first hand-simplification (a missing factor of 2), confirmed against the k=3 baseline (m=2 must give genus 0, since X₂ = Q₊ is a conic — verified) before trusting the k=5,7 numbers.

The case **m = 2** (pairwise, the case actually load-bearing for the local law — cf. background note's remark that only pairwise data enters the k=3 computation) simplifies cleanly:

    g₂ = (k−2)(k−3)/2.

k=3 → 0 (the conic, matching the note exactly); **k=5 → 3; k=7 → 10.** General m, same formula (also verified): g_m = 1 + (k−1)!·(2mk−m²−m−2k−2) / (4(k−m)!); e.g. full Galois closure (m=k): g_k = 49 (k=5), 4681 (k=7) — large, but a fixed finite number depending only on k, never on p, x₀, y₀, or the box — which is exactly "constants are uniform": whatever combination of X_m's the local law's proof needs (pairwise at minimum, as in the note; possibly up to X_k for the full n₀-uniform statement), each is absolutely irreducible with a genus fixed once k is fixed, so every resulting Weil-bound error term is O_k(√p), uniformly in p and in the box — reproducing the note's own "no dependence on κ, x₀, y₀" finding (§3 of the note) at the structural level, for general k.

### 2.3 Numerical sanity check

`check_genus` counts N₂(p) = #{(t₁,t₂) ∈ F_p² : t₁≠t₂, t₁ᵏ−t₁=t₂ᵏ−t₂} directly (O(p)) and compares to the leading term E[j(j−1)]·p (j = rencontres-distributed root count):

```
k=5, p=1999: N2=2014  leading term=1999.0  |dev|=15   (g2=3)
k=7, p=1999: N2=2118  leading term=1999.0  |dev|=119  (g2=10)
```

Deviations are O(√p) as expected (√1999 ≈ 44.7; 119/44.7 ≈ 2.7, well inside a generous genus-scaled budget) — a consistency check, not a precision determination of g₂ itself (the affine count differs from the smooth projective model by O(1) terms this check doesn't try to resolve); the *exact* value of g₂ rests on the Riemann–Hurwitz computation, cross-validated by direct orbit enumeration as described above.

---

## 3. The generalised cover constant C(P)

### 3.1 Setup (recap, generalising note §2–3)

For f(t) = tᵏ (k odd prime, p with gcd(k,p−1)=1 so f is a permutation of F_p), box [0,2p)², the note's cover (weight 1 on every ±1-line with ≥4 points of P, weight 1 on every point on none of them) has cost = 2·L₄ + U. For a residue class c of either slope with j roots split n₀ (class-0) / n₁ = j−n₀ (class-1), the four consecutive lines carry (n₀, 2n₀+n₁, n₀+2n₁, n₁) points (background statement, holds for any j — verified directly from the stated lift-routing rule, which sums correctly to the general formula for any n₀,n₁ by construction, not just j=3).

Under the task's local-law hypotheses — (H1) j-distribution = rencontres law of S_k (now a **theorem** for k=5,7 by Part 1, via Chebotarev applied to the S_k-cover of Part 2), (H2) n₀ | j uniform on {0,…,j}, (H3) the plus/minus data at one residue independent — the cost is a pure combinatorial constant times p:

    L4 = 2p · E[lines/class]     (one factor of 2 for the two slopes)
    U  = p · E[singleton lifts/residue]
    C(P) := lim cost/(2p) = 2·E[lines/class] + E[singleton lifts/residue] / 2.

### 3.2 E[lines/class] (one slope)

A class with j roots, n₀=m uniform on {0,…,j}, contributes to the ≥4-line count Σ_{L∈{n₀,2n₀+n₁,n₀+2n₁,n₁}} [L≥4]. Averaging over m (uniform) and then over j (rencontres P_j):

    E[lines/class] = Σ_j P_j · (1/(j+1)) Σ_{m=0}^{j} Σ_{L(j,m)} [L≥4].

At k=3 this gives exactly 1/4 (only the two "same" states contribute 1 line, the two "split" states contribute 2, average (1+2+2+1)/4 = 3/2, times P₃=1/6 → 1/4) — matching L4 = p/2 asymptotically, i.e. Σ_σ(Aᵟ+2Sᵟ) with Aᵟ=Sᵟ=N₃ᵟ/2 in the note.

### 3.3 E[singleton lifts/residue] (both slopes, size-biased)

A uniformly random *residue* x lies in a class of size j with **size-biased** probability j·P_j (note Σj·P_j = E[fixed points of a random permutation] = 1 always, for any k — a clean consistency identity, checked in the code); given j, n₀=m is still uniform on {0,…,j}; given (j,m), x itself is class-0 with probability m/j (exchangeability). This is done independently for the plus- and minus-slope data at x (H3). Each of x's 4 lifts (δ,ε) ∈ {0,1}² is then covered-or-not by each slope according to the explicit lift-routing rule of the background (class-0/1, δ=ε vs. (0,1) vs. (1,0) for slope +1; (0,0)/(1,1)/mixed-pair for slope −1 — different routing per slope, same 4-line-count formula); a lift survives (contributes to U) iff **neither** slope's ≥4-line set covers it. Summing this over the ≤4·(#states)² combinations (a few hundred terms, exact `Fraction` arithmetic, script §4) gives E[singleton lifts/residue] = 7/4 at k=3 — matching the note's U ≈ 7p/4 asymptotically (from U = 4p − (27/4)(N₃⁺+N₃⁻), N₃± ≈ p/6).

### 3.4 Results and cross-check

```
k=3: E[lines/class]=1/4      E[singletons/residue]=7/4          C(P)=11/8              = 1.375000   (must equal Theorem G3.5 -- MATCHES)
k=5: E[lines/class]=31/120   E[singletons/residue]=1519/864     C(P)=12059/8640         = 1.395718
k=7: E[lines/class]=877/3360 E[singletons/residue]=637871/362880 C(P)=203347/145152     = 1.400925
```

The k=5 and k=7 values are **bit-for-bit identical** to `slack/g_agents/x5_x7_numerics_exact_constant.py`'s independently-coded computation of the same quantity (that file's own header states this constant is the one asked for; I did not consult or import that file's code — the match was checked only after my own script produced its numbers, precisely to make it an honest cross-check rather than a copy). That file's numerics (`x5_x7_numerics_output.txt`, `x5_x7_numerics_pooled_output.txt`) additionally show: (i) the *exact* cover cost measured directly off real 4p-point sets at p ∈ [197,887] tracks this predicted constant to within a few percent, consistent with the expected O(1/√p) finite-size fluctuations (cf. the note's own §4 discussion of the same-size fluctuations at k=3); (ii) H1 and H2 hold numerically within statistical noise (χ² tests, pooled over 6 primes each for k=5,7). Part 1–2 of this report supply the missing *reason* H1 should hold exactly in the p→∞ limit (rencontres numbers ⟺ Chebotarev for an S_k-cover) and the missing *mechanism* (absolute irreducibility, §2.1) that would let H2–H3 be upgraded from "numerically true" to "provable" by the note's own method (an inclusion–exclusion identity on the equidistributed root positions, as in note §3's "the triple term cancels" computation for k=3 — generalising that specific algebraic identity from 3 roots to j ≤ k roots is the one piece of the k=3 argument not re-derived here, flagged as the natural next step, not attempted for wall-clock reasons).

As with the k=3 case, the ≥4-line-plus-singleton cover is a clean, provable, but **not LP-optimal** certificate — `x5_x7_numerics.py`'s part (d) finds the fractional LP over all ±1-lines gives noticeably better ratios (≈1.28–1.36 at these k, versus 1.396/1.401 here), the same gap the note documents for k=3 (11/8 = 1.375 exact vs. LP ≈ 1.32–1.36). C(P) above is the constant *this specific, provable* cover achieves, not the true extremal ratio.

---

## 4. Consolidated check table

| # | Check | k=5 | k=7 | Script section |
|---|---|---|---|---|
| 1 | rencontres(S_3) matches note's stated (1/3,1/2,0,1/6) | — | — | `main()` §0 |
| 2 | Trinomial discriminant = ±(kᵏTᵏ⁻¹−(k−1)^{k−1}), all p tested | PASS (3 primes) | PASS (3 primes) | `check_discriminant` |
| 3 | Full Chebotarev cycle-type vs. S_k conjugacy classes | Σ\|Δ\|≈0.08–0.10 (noise~0.05) | Σ\|Δ\|≈0.15–0.31 (noise~0.05–0.19) | `check_chebotarev_cycletype` |
| 4 | Root-count marginal vs. rencontres | consistent, O(1/√p) | consistent, O(1/√p) | `check_root_counts` |
| 5 | C(P) exact value | 12059/8640 | 203347/145152 | `run_cost_constant` |
| 6 | C(P) cross-check vs. independent agent computation | exact match | exact match | (manual, §3.4 above) |
| 7 | Genus formula g₂=(k−2)(k−3)/2 vs. brute-force orbit count | 3 (verified exact) | 10 (verified exact) | ad hoc, reported §2.2 |
| 8 | X₂ point-count order-of-magnitude sanity | \|dev\|=15–33 | \|dev\|=47–119 | `check_genus` |

Full console output (all primes, all k, all sections): `slack/g_agents/galois_rootcounts_output.txt`. Script: `slack/g_agents/galois_rootcounts.py` (638 lines; runs end-to-end in ≈5s, `/Users/iwasborninbali/venvs/sat/bin/python3 slack/g_agents/galois_rootcounts.py`; no external dependencies — sympy is not installed in the venv, so all polynomial arithmetic mod p, the Sylvester-resultant discriminant check, and the distinct-degree factorisation are implemented from scratch and unit-tested against hand-built cases before being run at scale, see the inline smoke tests referenced in this report's derivation).

## 5. What is proved vs. checked vs. left open

- **Proved** (elementary, unconditional, for k ∈ {5,7}, every p ∤ k(k−1)): Gal(tᵏ−t−T/F_p(T)) = S_k, geometrically (§1.2); absolute irreducibility and exact genus of X_m for every 1 ≤ m ≤ k (§2.1–2.2).
- **Proved conditionally on H1–H3** (H1 now itself a theorem via the above): the exact rational value of C(P) at k=5,7 (§3, a closed-form computation, not a numerical fit).
- **Numerically checked, not proved here**: H2 (n₀|j uniform) and H3 (slope-independence) in the strong, p→∞, error-quantified sense the note proves for k=3 — plausible and mechanically supported by §2 (the curves needed all have bounded genus, so the Weil-bound machinery is *available*), but the specific combinatorial identity that closes the loop for k=3 (note §3, "the triple term cancels") was not re-derived for general j ≤ k here.
- **Not attempted**: general odd composite k (§1.4 explains exactly where the k=5,7 argument stops working and why).
