"""m8_audit.py — audit of Proposition m8 / m8asym of the note (docs: paper/hjsw_window.tex).

Four independent computations of m_8(p), the number of slope-(+1) integer lines carrying eight
points of P_{-1} = (H(1,p) u H(-1,p)) ∩ G(p), plus the geometry of the cubic

    C_0 :  a b^2 + (a^2 - 1) b + a = 0   over F_p.

  [A] geometric   -- count 8-point slope-(+1) lines from the class data (as slack/km1_lines.py)
  [B] Prop. m8    -- pairs (a,b) on C_0 with the sign conditions and the exact L-equation, /4
  [C] polytope    -- (X(a), X(1/a), X(b)) in W_1 u W_2 u W_3 u W_4 (Step 2 of Prop. m8asym), /4
  [D] geometry    -- smoothness of the projective closure, points at infinity, the Jacobian

Findings (2026-08-18, fourth solver):
  * [A] = [B] = [C] for every prime 11 <= p < 200 (exclusions a^2 = -1, b^2 = 1 respected);
  * C_0 is SMOOTH for every p >= 3 -- it is a genus-1 curve, not a possibly-singular one, so
    Aubry-Perret is not needed: Hasse's bound suffices and |C_0(F_p)| is exactly p - 2 - a_p;
  * C_0 is F_p-isomorphic to y^2 = x^3 - x (j = 1728, CM by Z[i]) for every p > 2, via
    y = 2ab + a^2 - 1  =>  y^2 = a^4 - 6a^2 + 1, then the standard quartic -> Weierstrass map;
  * the boundary hyperplanes x_i = 0 and T in {0, +-p/2, +-p} carry NO point of C_0 with a,b != 0.

usage:  python3 slack/m8_audit.py [pmax]        (default 200)
"""
import sys
from collections import Counter
from fractions import Fraction


def primes(n):
    return [q for q in range(3, n + 1) if all(q % d for d in range(2, int(q ** 0.5) + 1))]


def on_C0(a, b, p):
    return (a * b * b + (a * a - 1) * b + a) % p == 0


# ---------------------------------------------------------------- [A] geometric ground truth
def m8_geometric(p):
    """number of slope-(+1) integer lines x - y = d carrying eight points of P_{-1}"""
    h = (p - 1) // 2
    X = lambda u: u if u <= h else u - p
    diag, anti = Counter(), Counter()
    for a in range(1, p):
        b = pow(a, -1, p)
        x, y = X(a), b                       # base copy of the class (a, 1/a)
        for r in (0, 1):
            for s in (0, 1):
                diag[x - y + (r - s) * p] += 1
                anti[x + y + (r + s) * p] += 1
    n = 0
    for d, n1 in diag.items():
        if n1 + anti.get(p - d, 0) == 8:
            n += 1
    for e, n2 in anti.items():               # lines meeting only the H(-1) copy
        if (p - e) not in diag and n2 == 8:
            n += 1
    return n


# ---------------------------------------------------------------- [B] Proposition m8
def m8_prop(p):
    h = (p - 1) // 2
    X = lambda u: u if u <= h else u - p
    c = 0
    for a in range(1, p):
        if (a * a) % p == p - 1:             # a^2 = -1 excluded (sigma-fixed class)
            continue
        ia = pow(a, -1, p)
        for b in range(1, p):
            if not on_C0(a, b, p) or (b * b) % p == 1:   # b^2 = 1 excluded (tau-fixed)
                continue
            ib = pow(b, -1, p)
            x1, x2, x3, x4 = X(a), X(ia), X(b), X(ib)
            if not (x1 * x2 < 0 and x3 * x4 > 0):
                continue
            if x1 - x2 + x3 + x4 == p * ((1 if x1 > 0 else 0) - (1 if x3 < 0 else 0)):
                c += 1
    return Fraction(c, 4)


# ---------------------------------------------------------------- [C] the four polytopes
def m8_polytope(p, respect_exclusions=True):
    """W_1..W_4 of Step 2; comparisons use 2T against p to stay in exact integer arithmetic"""
    h = (p - 1) // 2
    X = lambda u: u if u <= h else u - p
    c = 0
    for a in range(1, p):
        ia = pow(a, -1, p)
        for b in range(1, p):
            if not on_C0(a, b, p):
                continue
            if respect_exclusions and ((a * a) % p == p - 1 or (b * b) % p == 1):
                continue
            x1, x2, x3 = X(a), X(ia), X(b)
            T = x1 - x2 + x3
            if ((x1 > 0 > x2 and x3 > 0 and p < 2 * T < 2 * p) or
                (x1 > 0 > x2 and x3 < 0 and 0 < 2 * T < p) or
                (x1 < 0 < x2 and x3 > 0 and -p < 2 * T < 0) or
                (x1 < 0 < x2 and x3 < 0 and -2 * p < 2 * T < -p)):
                c += 1
    return Fraction(c, 4)


def boundary_points(p):
    """points of C_0 with a, b != 0 on the boundary hyperplanes x_i = 0, T in {0, +-p/2, +-p}"""
    h = (p - 1) // 2
    X = lambda u: u if u <= h else u - p
    n = 0
    for a in range(1, p):
        ia = pow(a, -1, p)
        for b in range(1, p):
            if not on_C0(a, b, p):
                continue
            x1, x2, x3 = X(a), X(ia), X(b)
            T = x1 - x2 + x3
            if 0 in (x1, x2, x3) or 2 * T in (0, p, -p, 2 * p, -2 * p):
                n += 1
    return n


# ---------------------------------------------------------------- [D] geometry of C_0
def Fh(a, b, z, p):   return (a * b * b + (a * a - z * z) * b + a * z * z) % p
def Fa(a, b, z, p):   return (b * b + 2 * a * b + z * z) % p
def Fb(a, b, z, p):   return (2 * a * b + a * a - z * z) % p
def Fz(a, b, z, p):   return (2 * z * (a - b)) % p


def geometry(p):
    """(#projective points, singular points, points at infinity)"""
    pts = ([(a, b, 1) for a in range(p) for b in range(p)] +
           [(a, 1, 0) for a in range(p)] + [(1, 0, 0)])
    pts = [P for P in pts if Fh(*P, p) == 0]
    sing = [P for P in pts if Fa(*P, p) == 0 and Fb(*P, p) == 0 and Fz(*P, p) == 0]
    return len(pts), sing, [P for P in pts if P[2] == 0]


def ap_congruent(p):
    """a_p of y^2 = x^3 - x: 0 if p = 3 mod 4, else 2A with p = A^2 + B^2, A odd, A + B = 1 mod 4"""
    if p % 4 == 3:
        return 0
    for A in range(1, int(p ** 0.5) + 1):
        B2 = p - A * A
        B = int(round(B2 ** 0.5))
        if B * B == B2 and A % 2 == 1:
            for sA in (A, -A):
                for sB in (B, -B):
                    if (sA + sB) % 4 == 1:
                        return sA * 2
    return None


def check_isomorphism(p):
    """y = 2ab + a^2 - 1 => y^2 = a^4 - 6a^2 + 1; then (X, Y) = (2(y + a^2) - 6, 2aX) lands on
       Y^2 = X^3 + 12X^2 + 32X, and (X + 4, Y)/(4, 8) lands on y^2 = x^3 - x.  Returns #failures."""
    inv4, inv8 = pow(4, -1, p), pow(8, -1, p)
    bad = 0
    for a in range(1, p):
        for b in range(p):
            if not on_C0(a, b, p):
                continue
            y = (2 * a * b + a * a - 1) % p
            if (y * y - (a ** 4 - 6 * a * a + 1)) % p:
                bad += 1; continue
            X_ = (2 * (y + a * a) - 6) % p
            Y_ = (2 * a * X_) % p
            if (Y_ * Y_ - (X_ ** 3 + 12 * X_ * X_ + 32 * X_)) % p:
                bad += 1; continue
            xx, yy = ((X_ + 4) * inv4) % p, (Y_ * inv8) % p
            if (yy * yy - (xx ** 3 - xx)) % p:
                bad += 1
    return bad


def main():
    pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    ps = [p for p in primes(pmax) if p >= 11]

    print("=== [A] geometric = [B] Prop. m8 = [C] polytope form ===")
    print(f"{'p':>5} {'[A] geom':>9} {'[B] Prop':>9} {'[C] poly':>9} {'bdry':>5} {'m8/p':>7}")
    bad = 0
    for p in ps:
        A, B, C = m8_geometric(p), m8_prop(p), m8_polytope(p)
        bd = boundary_points(p)
        ok = (A == B == C) and bd == 0
        bad += not ok
        print(f"{p:5d} {A:9d} {str(B):>9} {str(C):>9} {bd:5d} {A / p:7.4f}"
              + ("" if ok else "   <-- MISMATCH"))
    print(f"mismatches: {bad}\n")

    print("=== [D] geometry of C_0: smooth, genus 1, isomorphic to y^2 = x^3 - x ===")
    print(f"{'p':>5} {'#C_0 proj':>10} {'p+1-a_p':>8} {'#sing':>6} {'#inf':>5} {'iso fails':>10}")
    bad = 0
    for p in [q for q in primes(min(pmax, 80)) if q >= 5]:
        n, sing, inf = geometry(p)
        cm = p + 1 - ap_congruent(p)
        fails = check_isomorphism(p)
        ok = (not sing) and n == cm and len(inf) == 3 and fails == 0
        bad += not ok
        print(f"{p:5d} {n:10d} {cm:8d} {len(sing):6d} {len(inf):5d} {fails:10d}"
              + ("" if ok else "   <-- MISMATCH"))
    print(f"mismatches: {bad}")


if __name__ == "__main__":
    main()
