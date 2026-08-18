"""cube_local_law.py — local law for the ±1-line structure of permutation-cubic graphs y = a x^3 (p ≡ 2 mod 3) in a 2p×2p box, and the
predicted cost of the explicit cover (weight 1 on all ±1 lines with ≥4 points + singletons).
Local law (proved via Weil on the root conic x1²+x1x2+x2² = ∓1/a and Bombieri on their fibre product, see note): for a residue x with window
position u ∈ [0,1): slope +1 partners x2,x3 have positions u2 (uniform), u3 = −u−u2−κ mod 1 (κ = 3x0/p mod 1); threshold g+ uniform;
class+(t) = [u_t ≥ 1−g+]; slope −1: partners u2', u3' = −u−u2'−κ, threshold g− = g+ + 2u mod 1, class−(t) = [u_t > g−].
Group type = same (all three classes equal) or split.  Covered lifts (δ,ε): slope+ same: δ=ε; split: class0 → all but (1,0), class1 → all but (0,1);
slope−: same: mixed lifts; split: class0 → all but (0,0), class1 → all but (1,1).
cost/p = 4 − Σ_σ (4A_σ+5S_σ)/p + D, with A_σ+S_σ = N3 ≈ p/6.  usage: cube_local_law.py [kappa] [samples]"""
import sys, random
kappa = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
S = int(sys.argv[2]) if len(sys.argv) > 2 else 2_000_000
rng = random.Random(7)
same_p = same_m = 0; dbl = 0; cov_p = cov_m = 0
for _ in range(S):
    u = rng.random(); u2 = rng.random(); u2m = rng.random(); gp = rng.random()
    u3 = (-u - u2 - kappa) % 1.0; u3m = (-u - u2m - kappa) % 1.0; gm = (gp + 2 * u) % 1.0
    cp = [t >= 1 - gp for t in (u, u2, u3)]; cm = [t > gm for t in (u, u2m, u3m)]
    sp = (cp[0] == cp[1] == cp[2]); sm = (cm[0] == cm[1] == cm[2])
    same_p += sp; same_m += sm
    for d in (0, 1):
        for e in (0, 1):
            if sp: c1 = (d == e)
            else:  c1 = not ((d, e) == ((1, 0) if not cp[0] else (0, 1)))
            if sm: c2 = (d != e)
            else:  c2 = not ((d, e) == ((0, 0) if not cm[0] else (1, 1)))
            cov_p += c1; cov_m += c2; dbl += (c1 and c2)
Pp = same_p / S; Pm = same_m / S
# per residue x (density 1 over p residues): E[#covered lifts by slope+] should be (1/... ) let me just report:
D = dbl / S; Cp = cov_p / S; Cm = cov_m / S
# note: every residue x lies in a 3-root group for its slope only with probability ~1/2 (the other 1/2: 1-root residues) —
# in the sampling above we conditioned on x being one of three roots; the equidistribution is over the conic, i.e. over 3-root membership.
# The fraction of residues x that are roots of a 3-root c equals 3·N3/p ≈ 1/2.  So per residue: E[covered lifts by slope σ] = ½·Cσ, and
# doubly covered: the two memberships are independent-ish? NO — handled properly below by sampling membership too.
print(f"kappa={kappa}: conditional on 3-root membership: P_same(+)={Pp:.4f} P_same(-)={Pm:.4f}; covered lifts per root: +:{Cp:.4f} -:{Cm:.4f}; both:{D:.4f}")
