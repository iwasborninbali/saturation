"""pp_constant_exact.py — exact rational constant C_k of the tied-threshold local law (perm_poly_theorem_notes.md §2) for the rencontres laws S_k:
cost/p = 2·L/p + U/p with U/p = ∬ E[U | u,g] du dg, E[U|u,g] a polynomial in q₊(u,g), q₋(u,g) (partner-in-x's-class probabilities), piecewise on
(a) g+2u<1: q₊=1−g, q₋=g+2u; (b) 1≤g+2u<2, u+g<1: q₊=1−g, q₋=2−g−2u; (c) 1≤g+2u<2, u+g≥1: q₊=g, q₋=g+2u−1; (d) g+2u≥2: q₊=g, q₋=3−g−2u.
usage: pp_constant_exact.py k"""
import sys
import sympy as sp
from math import factorial, comb
k = int(sys.argv[1]); d = k
P = [sp.Rational(1, factorial(j)) * sum(sp.Rational((-1)**i, factorial(i)) for i in range(d - j + 1)) for j in range(d + 1)]
qp, qm, u, g = sp.symbols('qp qm u g')
law = [(j, j * P[j]) for j in range(1, d + 1) if P[j] != 0]     # size-biased weights (sum = 1)
assert sum(w for _, w in law) == 1
def dist(q):
    out = {}
    for kk, w in law:
        for m in range(1, kk + 1):
            out[(kk, m)] = w * comb(kk - 1, m - 1) * q**(m - 1) * (1 - q)**(kk - m)
    return out
Dp = dist(qp); Dm = dist(qm)
EU = 0
for (kp, npl), wp in Dp.items():
    for (km, nmi), wm in Dm.items():
        val = (1 if kp + npl <= 3 else 0) * ((1 if nmi <= 3 else 0) + (1 if 2 * km - nmi <= 3 else 0)) + (1 if km + nmi <= 3 else 0) * ((1 if npl <= 3 else 0) + (1 if 2 * kp - npl <= 3 else 0))
        if val: EU += val * wp * wm
EU = sp.expand(EU)
def integ(expr, region):
    # region: list of (u_lo, u_hi) with g-bounds function -> integrate g inside u
    total = 0
    for (glo, ghi, ulo, uhi) in region:
        inner = sp.integrate(expr, (g, glo, ghi))
        total += sp.integrate(inner, (u, ulo, uhi))
    return sp.nsimplify(total)
# region (a): g in [0, 1-2u) for u in [0, 1/2)
Ra = [(0, 1 - 2*u, 0, sp.Rational(1, 2))]
# region (b): 1 <= g+2u < 2 and u+g < 1: g >= 1-2u, g < 1-u  -> need 1-2u < 1-u i.e. u>0; also g<1: for u<1/2: g in [1-2u, 1-u); for u>=1/2: g in [0, 1-u)
Rb = [(1 - 2*u, 1 - u, 0, sp.Rational(1, 2)), (0, 1 - u, sp.Rational(1, 2), 1)]
# region (c): 1 <= g+2u < 2 and u+g >= 1: g >= max(1-2u, 1-u) = 1-u (u>=0), g < min(1, 2-2u): for u<1/2: g in [1-u, 1); for u>=1/2: g in [1-u, 2-2u)
Rc = [(1 - u, 1, 0, sp.Rational(1, 2)), (1 - u, 2 - 2*u, sp.Rational(1, 2), 1)]
# region (d): g >= 2-2u (u>1/2), g<1
Rd = [(2 - 2*u, 1, sp.Rational(1, 2), 1)]
subs = {'a': {qp: 1 - g, qm: g + 2*u}, 'b': {qp: 1 - g, qm: 2 - g - 2*u}, 'c': {qp: g, qm: g + 2*u - 1}, 'd': {qp: g, qm: 3 - g - 2*u}}
regions = {'a': Ra, 'b': Rb, 'c': Rc, 'd': Rd}
U = 0
for key in 'abcd':
    U += integ(sp.expand(EU.subs(subs[key])), regions[key])
U = sp.nsimplify(U)
# L/p: 2 slopes × Σ_k P_k E_{n0 uniform}[#rich]
Lp = 0
for j in range(1, d + 1):
    if P[j] == 0: continue
    e = sum(int(n0 >= 4) + int(j + n0 >= 4) + int(j + (j - n0) >= 4) + int(j - n0 >= 4) for n0 in range(j + 1))
    Lp += P[j] * sp.Rational(e, j + 1)
L = 2 * Lp
C = 2 * L + U
print(f"k={k}: L/p = {L} = {float(L):.6f};  U/p = {U} = {float(U):.6f};  C_k = cost/p = {C} = {float(C):.6f};  C_k/2 = {C/2} = {float(C/2):.6f} N")
