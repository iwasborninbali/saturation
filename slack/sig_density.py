"""sig_density.py — EXACT densities of the run signatures (k=-1, §30): the bits xi_i = [X(u_i+u_{i+1})X(u_{i+1}-u_i) < 0]
along a run of consecutive quadratic residues, in the local law "v_i = X(u_i)/p i.i.d. uniform on (-1/2,1/2)".
Transfer operator on piecewise-polynomial densities with exact rational arithmetic:
   g(w) = int_{v : xi(v,w) = b} f(v) dv,      xi(v,w) = [ sgn c(v+w) != sgn c(w-v) ],  c(x) = ((x+1/2) mod 1) - 1/2.
Breakpoints in v for fixed w: {-w, ±1/2-w, w, w±1/2}; all crossings are dyadic, so everything stays exact.
usage: sig_density.py [maxlen]"""
import sys
from fractions import Fraction as F
from itertools import product

HALF = F(1, 2)

def polyint(c, lo, hi):
    """definite integral of the polynomial with coeffs c over [lo,hi]"""
    def ev(x):
        s = F(0); xp = F(1)
        for j, cj in enumerate(c):
            xp = x ** (j + 1)
            s += F(cj) * xp / (j + 1)
        return s
    return ev(hi) - ev(lo)

def polyint_sym(c, lo_coeffs, hi_coeffs, deg_cap=40):
    """indefinite-integral difference where lo,hi are affine in w: returns coeffs of the polynomial in w.
    lo_coeffs, hi_coeffs = (a0, a1) meaning a0 + a1*w."""
    def antider_at(affine):
        a0, a1 = affine
        # P(x) = sum_j c_j x^{j+1}/(j+1) evaluated at x = a0 + a1 w -> polynomial in w
        out = [F(0)]
        for j, cj in enumerate(c):
            if cj == 0: continue
            n = j + 1
            # (a0 + a1 w)^n / n * c_j
            from math import comb
            term = [F(0)] * (n + 1)
            for i in range(n + 1):
                term[i] = F(comb(n, i)) * (F(a0) ** (n - i)) * (F(a1) ** i)
            term = [F(cj) * t / n for t in term]
            if len(term) > len(out): out = out + [F(0)] * (len(term) - len(out))
            for i, t in enumerate(term): out[i] += t
        return out
    hi_p = antider_at(hi_coeffs); lo_p = antider_at(lo_coeffs)
    n = max(len(hi_p), len(lo_p))
    hi_p += [F(0)] * (n - len(hi_p)); lo_p += [F(0)] * (n - len(lo_p))
    return [hi_p[i] - lo_p[i] for i in range(n)]

def c_sign(x):
    """sign of the centred representative of x mod 1, for x in (-1,1); x != 0, ±1/2"""
    if -1 < x < -HALF: return 1
    if -HALF < x < 0: return -1
    if 0 < x < HALF: return 1
    return -1

def transfer(pieces, bit):
    """pieces: list of (lo, hi, coeffs in v). Returns list of (lo, hi, coeffs in w) for g(w)."""
    # candidate w-breakpoints: where the v-breakpoints (affine in w) cross each other or the piece endpoints, and ±1/2, 0
    affines = [(F(0), F(-1)), (HALF, F(-1)), (-HALF, F(-1)), (F(0), F(1)), (-HALF, F(1)), (HALF, F(1))]  # -w, 1/2-w, -1/2-w, w, w-1/2, w+1/2
    consts = sorted({p[0] for p in pieces} | {p[1] for p in pieces} | {-HALF, F(0), HALF})
    cand = {-HALF, F(0), HALF}
    for (a0, a1) in affines:
        for cst in consts:
            if a1 != 0: cand.add((cst - a0) / a1)
        for (b0, b1) in affines:
            if a1 != b1: cand.add((b0 - a0) / (a1 - b1))
    ws = sorted(x for x in cand if -HALF <= x <= HALF)
    out = []
    for i in range(len(ws) - 1):
        wlo, whi = ws[i], ws[i + 1]
        if wlo == whi: continue
        wm = (wlo + whi) / 2
        # breakpoints in v at w = wm
        bps = sorted({-HALF, HALF} | {a0 + a1 * wm for (a0, a1) in affines} | {p[0] for p in pieces} | {p[1] for p in pieces})
        bps = [b for b in bps if -HALF <= b <= HALF]
        acc = [F(0)]
        for j in range(len(bps) - 1):
            vlo, vhi = bps[j], bps[j + 1]
            if vlo == vhi: continue
            vm = (vlo + vhi) / 2
            if c_sign(vm + wm) == c_sign(wm - vm):
                if bit == 1: continue
            else:
                if bit == 0: continue
            # which f-piece?
            coef = None
            for (a, b, cc) in pieces:
                if a <= vm <= b: coef = cc; break
            if coef is None: continue
            # affine expressions of vlo, vhi in w (identify which affine/const produced them)
            def as_affine(val):
                for (a0, a1) in affines:
                    if a0 + a1 * wm == val: return (a0, a1)
                return (val, F(0))
            lo_a = as_affine(vlo); hi_a = as_affine(vhi)
            contrib = polyint_sym(coef, lo_a, hi_a)
            n = max(len(acc), len(contrib))
            acc += [F(0)] * (n - len(acc)); contrib += [F(0)] * (n - len(contrib))
            acc = [acc[t] + contrib[t] for t in range(n)]
        out.append((wlo, whi, acc))
    return out

def total(pieces):
    return sum(polyint(c, lo, hi) for (lo, hi, c) in pieces)

def signature_densities(maxlen):
    """P(xi_1..xi_m) for m = 1..maxlen; returns dict pattern -> Fraction"""
    res = {}
    for m in range(1, maxlen + 1):
        for pat in product((0, 1), repeat=m):
            pieces = [(-HALF, F(0), [F(1)]), (F(0), HALF, [F(1)])]   # density of v_1 (uniform, total mass 1)
            for b in pat:
                pieces = transfer(pieces, b)
            res[pat] = total(pieces)
    return res

if __name__ == '__main__':
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    d = signature_densities(M)
    for m in range(1, M + 1):
        s = F(0)
        for pat in product((0, 1), repeat=m):
            v = d[pat]; s += v
            print(f"  P{pat} = {v} = {float(v):.6f}")
        print(f"  [sum over patterns of length {m}: {s}]")
