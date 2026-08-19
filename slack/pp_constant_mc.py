"""pp_constant_mc.py — Monte-Carlo version of pp_constant.py, with the k = d linear relation (Σ of all d roots ≡ −κ mod 1 when f has no x^{d−1} term).
Samples residues x from the local law: k_σ ~ size-biased P_k^σ; positions of the k−1 partners uniform (for k = d: k−2 uniform and the last determined by
u_x + Σ partners ≡ −κ); thresholds θ₊ = 1−g, θ₋ = g + 2u_x (mod 1); classes; U(x) and the rich-line count from the residue's pattern (attributed 1/k to x).
usage: pp_constant_mc.py "P0,..,Pd" [kappa] [samples] [relation:0/1]"""
import sys, random
P = [float(t) for t in sys.argv[1].split(',')]; d = len(P) - 1
kappa = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
S = int(sys.argv[3]) if len(sys.argv) > 3 else 400000
rel = int(sys.argv[4]) if len(sys.argv) > 4 else 1
rng = random.Random(11)
law = [(k, k * pk) for k, pk in enumerate(P) if k >= 1 and pk > 0]; tot = sum(w for _, w in law)
cum = []; acc = 0
for k, w in law: acc += w / tot; cum.append((acc, k))
def draw_k():
    r = rng.random()
    for c, k in cum:
        if r <= c: return k
    return cum[-1][1]
def partners(u, k):
    if k == 1: return []
    if rel and k == d:
        others = [rng.random() for _ in range(k - 2)]
        last = (-kappa - u - sum(others)) % 1.0
        return others + [last]
    return [rng.random() for _ in range(k - 1)]
U = 0.0; L = 0.0
for _ in range(S):
    u = rng.random(); g = rng.random(); thp = 1 - g; thm = (g + 2 * u) % 1.0
    kp = draw_k(); km = draw_k()
    pp = partners(u, kp); pm = partners(u, km)
    # slope +: class 0 iff pos >= thp ; n+ = # roots (incl x) in x's class
    cx = (u >= thp); npl = 1 + sum((v >= thp) == cx for v in pp)
    n0 = sum(v >= thp for v in pp) + cx; n1 = kp - n0
    L += ((n0 >= 4) + (kp + n0 >= 4) + (kp + n1 >= 4) + (n1 >= 4)) / kp    # residue's rich lines shared among its k members
    cxm = (u <= thm); nmi = 1 + sum((v <= thm) == cxm for v in pm)
    m0 = sum(v <= thm for v in pm) + cxm; m1 = km - m0
    L += ((m0 >= 4) + (km + m0 >= 4) + (km + m1 >= 4) + (m1 >= 4)) / km
    U += (kp + npl <= 3) * ((nmi <= 3) + (2 * km - nmi <= 3)) + (km + nmi <= 3) * ((npl <= 3) + (2 * kp - npl <= 3))
U /= S; L /= S
print(f"d={d} kappa={kappa} rel={rel}: L/p={L:.4f} U/p={U:.4f} cost/p={2*L+U:.4f} = {(2*L+U)/2:.4f} N")
