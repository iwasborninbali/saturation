"""pp_constant.py — asymptotic cost/p of the cover 'weight 1 on every slope-±1 line with ≥4 lifted points + singletons' for the box lift of a
permutation polynomial f (fixed degree, p→∞), given the root-count laws P_k^± = density of residues c with k roots of f(t) ∓ t = c.
Local law assumed: root positions u_t and the threshold jointly uniform (θ₊ = 1−g, θ₋ = g + 2u_x mod 1 for the residue x; classes:
class₊(t)=0 iff u_t ≥ θ₊, class₋(t)=0 iff u_t ≤ θ₋); root counts of the two slopes independent of each other and of positions.
Line sizes: for a residue c with k roots and n₀ of class 0: n₀, k+n₀, k+n₁, n₁ (n₁=k−n₀); a root's 3 'central' lifts lie on lines of sizes k+n and
2k−n (n = #roots in its class), its outer lift on a line of size n.  A lift is uncovered iff both its ±1 lines have <4 points:
U(x) = [k₊+n⁺≤3]·([n⁻≤3]+[2k₋−n⁻≤3]) + [k₋+n⁻≤3]·([n⁺≤3]+[2k₊−n⁺≤3]);  L = Σ_σ Σ_c ([n₀≥4]+[k+n₀≥4]+[k+n₁≥4]+[n₁≥4]).
cost/p = 2·L/p + U/p.   usage: pp_constant.py "P0,P1,...,Pd" ["P0-,P1-,..."] [grid]"""
import sys, math
from functools import lru_cache
def binom(n, m): return math.comb(n, m)
def rich_lines_per_residue(P):
    # E over c: Σ_k P_k · E_{n0 uniform on 0..k}[#rich lines]  (n0|k uniform: Bin(k,U) is uniform)
    tot = 0.0
    for k, pk in enumerate(P):
        if k == 0 or pk == 0: continue
        e = 0.0
        for n0 in range(k + 1):
            n1 = k - n0
            e += (n0 >= 4) + (k + n0 >= 4) + (k + n1 >= 4) + (n1 >= 4)
        tot += pk * e / (k + 1)
    return tot
def U_per_residue(Pp, Pm, grid=400):
    # residue x: k₊ = k w.p. k·P_k (size-biased), partners' positions i.i.d. uniform; classes via θ₊ = 1−g, θ₋ = (g + 2u) mod 1
    kp_law = [(k, k * pk) for k, pk in enumerate(Pp) if k >= 1 and pk > 0]
    km_law = [(k, k * pk) for k, pk in enumerate(Pm) if k >= 1 and pk > 0]
    sp = sum(w for _, w in kp_law); sm = sum(w for _, w in km_law)
    kp_law = [(k, w / sp) for k, w in kp_law]; km_law = [(k, w / sm) for k, w in km_law]
    tot = 0.0
    for i in range(grid):
        u = (i + 0.5) / grid
        for j in range(grid):
            g = (j + 0.5) / grid
            thp = 1 - g; thm = (g + 2 * u) % 1.0
            # class of x on +: 0 iff u ≥ θ₊ ; partner in x's class w.p. qp
            qp = (1 - thp) if u >= thp else thp
            qm = thm if u <= thm else (1 - thm)
            # distributions of n⁺ = 1 + Bin(k₊−1, qp), n⁻ = 1 + Bin(k₋−1, qm)
            def dist(law, q):
                out = {}
                for k, w in law:
                    for m in range(1, k + 1):
                        pr = w * binom(k - 1, m - 1) * q ** (m - 1) * (1 - q) ** (k - m)
                        out[(k, m)] = out.get((k, m), 0.0) + pr
                return out
            Dp = dist(kp_law, qp); Dm = dist(km_law, qm)
            e = 0.0
            for (kp, npl), wp in Dp.items():
                for (km, nmi), wm in Dm.items():
                    ux = (kp + npl <= 3) * ((nmi <= 3) + (2 * km - nmi <= 3)) + (km + nmi <= 3) * ((npl <= 3) + (2 * kp - npl <= 3))
                    e += wp * wm * ux
            tot += e
    return tot / (grid * grid)
if __name__ == '__main__':
    Pp = [float(t) for t in sys.argv[1].split(',')]
    Pm = [float(t) for t in sys.argv[2].split(',')] if len(sys.argv) > 2 and ',' in sys.argv[2] else Pp
    grid = int(sys.argv[-1]) if len(sys.argv) > 2 and ',' not in sys.argv[-1] else 300
    L = rich_lines_per_residue(Pp) + rich_lines_per_residue(Pm)
    U = U_per_residue(Pp, Pm, grid)
    print(f"L/p={L:.4f}  U/p={U:.4f}  cost/p = 2L/p + U/p = {2*L+U:.4f}  = {(2*L+U)/2:.4f} N")
