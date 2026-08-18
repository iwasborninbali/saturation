# A self-contained problem for a fresh mind (no history, no literature — just the objects)

## Objects
Let p be an odd prime, h = (p−1)/2.  Work in the integer box  B = {−h, …, 3h+1} × {0, …, 2p−1}  (side 2p in each coordinate).
Let  W = { (x,y) ∈ B : xy ≡ 1 or xy ≡ −1 (mod p) }.   Facts you can verify quickly: |W| = 8(p−1); every column x ≢ 0 and every row y ≢ 0 of
the box contains exactly 4 points of W; the maps  (x,y) ↦ (p−x, y)  and  (x,y) ↦ (x, 2p−y)  are bijections of W.
Call a subset S ⊆ W *good* if no three points of S are collinear (as points of the plane).  Let α(p) = max |S| over good S.
Trivially α(p) ≤ 4(p−1) (two points per column).  Known values (exhaustive computer search):
   p:      11   13   17   19    23        29
   α(p):   32   40   54   59   70…74     ≥ 84
i.e. α(p) = 3(p−1) + (2, 4, 6, 5, ≥4, ≥0).
Also known (elementary, provable in one page): α(p) ≤ 4(p−1) − 4·m(p), where m(p) is the number of lines x − y = const carrying exactly
eight points of W (m(p) ≈ p/12).

## The question
Q1. Prove that α(p) ≤ (3+ε)(p−1) for some fixed ε < 2/3 and all large p — or, ideally, α(p) ≤ 3(p−1) + C.
Q2 (a cleaner sub-question, in case Q1 resists).  For a ∈ {1,…,p−1} let X(a) ∈ [−h,h] be the least absolute residue of a, and let
Y(b) ∈ [1,p−1] be the least positive residue.  For each choice of bits r_a ∈ {0,1} (a = 1..p−1) form the set
   S(r) = ⋃_a { (X(a) + r_a p,  Y(1/a) + s p),  (X(a) + (1−r_a) p,  Y(−1/a) + s p) : s ∈ {0,1} }        (4(p−1) points, ⊆ W).
Let T(r) be the number of collinear triples inside S(r).  Facts: with ε_a = (−1)^{r_a}, T is a quadratic polynomial
T = E + εᵀCε (E ≈ 3.6 (p−1) log p, C an explicit symmetric matrix with entries in (1/8)Z);  min_r T(r) = 24, 28, 42, 48, 80, 136 for
p = 11, 13, 17, 19, 23, 29 (all 2^{p−1} choices checked).  Prove that min_r T(r) ≥ c·(p−1) for an absolute c > 0 and all large p
(numerically the spectral bound E + (p−1)λ_min(C) already gives ≥ 3.6(p−1) for 41 ≤ p ≤ 71 and λ_min(C) ≈ −2.4·√(tr C²/(p−1))).
Q3.  Every collinear triple of W with three points from distinct residue classes (a class = the four points with the same (x mod p, y mod p))
is a sub-triple of a symmetric quadruple q, q+s₁D, q+s₂D, q+(s₁+s₂)D with D a primitive integer direction, and such a quadruple pattern
occurs iff s₁²+s₂² is a square modulo p.  Use this to (a) prove that E(p)/(p−1) → ∞, and (b) find any structure of C that bounds its
smallest eigenvalue below by −K·√(tr C²/(p−1)).

## Rules
Anything you prove must come with every lemma stated; conjectures must be labelled; numerical evidence is welcome but is not proof.
Do not spend time explaining why the problem "should be hard" — just attack Q2/Q3, they are concrete.
Small computations: the set W and its lines are trivial to generate; a solver for α at p ≤ 19 needs seconds.
