"""U_model.py -- the per-residue uncovered probability U(pi, thp, thm, delta, eps, x0_over_p)
of section 2 of docs/research/cubic_matching_local_law.md, exact closed-form derivation
(no Monte Carlo, no discretisation error -- exact breakpoint/arc integration over tau, tau').

Derivation summary (see g39_U_validation.txt for the numerical cross-check against the dumps):

Independent data of residue x at position pi (all mod-1 reals):
  slope +: coin E+ (P=1/2) -> k+ = 3 if E+ else 1; if k+=3, one free partner position tau
           (uniform on [0,1)), the other partner position is forced to
              tau3 = frac(-pi - tau - 3*x0p)                      [tau2+tau3 = -x, spec sec.2]
           class+(t) = 1 iff pos(t) < thp;  a := class+(x) = 1 iff pi < thp.
           n+ = 1 + #{partners in class a}  (n+=1 when k+=1).
  slope -: symmetric, coin E- (P=1/2), tau' uniform, tau3' = frac(-pi - tau' - 3*x0p) (SAME
           formula / same additive constant K0 = frac(-pi-3*x0p), since both cubics x^3-x=c
           and x^3+x=c have zero coefficient of x^2, i.e. root sum 0 mod p, independent of sign).
           class-(t) = 0 iff pos(t) <= thm;  b := class-(x) = 0 iff pi <= thm.
           n- = 1 + #{partners in class b}.

Line sizes through lift (delta,eps) [spec sec.2, verified against cube_matching_fast.py
covered_table() line by line -- code and spec agree exactly]:
  slope +: delta=eps:        k+ + n+
           (0,1): a=0 -> 2k+-n+, a=1 -> n+
           (1,0): a=0 -> n+,     a=1 -> 2k+-n+
  slope -: (0,0): b=0 -> n-,     b=1 -> 2k--n-
           (1,1): b=0 -> 2k--n-, b=1 -> n-
           (0,1),(1,0):        k- + n-
Uncovered iff BOTH the slope-+ size and the slope-- size are <= 3 (<4).

KEY FACT used below: the slope-+ data (E+,tau) and slope-- data (E-,tau') are independent of
each other, and the size-on-slope-+ depends only on (E+,tau) [given delta,eps,a fixed], the
size-on-slope-- only on (E-,tau') [given delta,eps,b fixed].  Hence

    U = P+(delta,eps,a,thp,pi,x0p) * P-(delta,eps,b,thm,pi,x0p)          (exact factorisation)

and each factor reduces (case analysis on k=1 vs k=3, done exactly below, not by simulation) to

    delta=eps            (slope+):  P+ = 1/2                         (k+=3 branch always size>=4)
    (delta,eps)=(0,1),(1,0) (slope-): P- = 1/2                       (symmetric reason)
    (delta,eps)=(0,1), a=1 (slope+): P+ = 1                          (n+<=3 always)
    (delta,eps)=(1,0), a=0 (slope+): P+ = 1
    (delta,eps)=(0,1), a=0 (slope+): P+ = 1/2 + 1/2 * Q(target=0)    [k+=3, need BOTH partners class 0]
    (delta,eps)=(1,0), a=1 (slope+): P+ = 1/2 + 1/2 * Q(target=1)
    (delta,eps)=(0,0), b=0 (slope-): P- = 1
    (delta,eps)=(1,1), b=1 (slope-): P- = 1
    (delta,eps)=(0,0), b=1 (slope-): P- = 1/2 + 1/2 * Q'(target=1)
    (delta,eps)=(1,1), b=0 (slope-): P- = 1/2 + 1/2 * Q'(target=0)

where Q(target) = P_tau( class(tau)==target AND class(tau3)==target ), computed EXACTLY (not by
grid) as the length of the intersection, on the circle [0,1), of the two arcs
   {tau : class(tau)=target}  (an interval bounded by the threshold thp or thm)
   {tau3=frac(K0-tau) : class(tau3)=target}  (a rotated copy of the same interval, since
        tau3 is an orientation-reversing rotation of tau by K0).
Both arcs have length thp (resp. 1-thp) for the +threshold case (analogous for -/thm); their
intersection is computed by exact interval arithmetic (arc_overlap below), never a numerical grid.
"""
import numpy as np


def _arc_overlap_with_box(s, L, a, b):
    """Exact measure of the circular arc [s, s+L) mod 1 intersected with the straight
    interval [a, b) subset of [0,1].  s,L,a,b are numpy arrays (or scalars) broadcastable
    together, 0<=s<1, 0<=L<=1, 0<=a<=b<=1."""
    s = np.asarray(s, dtype=np.float64)
    L = np.asarray(L, dtype=np.float64)
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    e = s + L
    # piece 1: [s, min(e,1)) intersect [a,b)
    e1 = np.minimum(e, 1.0)
    ov1 = np.clip(np.minimum(e1, b) - np.maximum(s, a), 0.0, None)
    # piece 2 (only if e>1): [0, e-1) intersect [a,b)
    e2 = e - 1.0
    ov2 = np.where(e > 1.0, np.clip(np.minimum(e2, b) - np.maximum(0.0, a), 0.0, None), 0.0)
    return ov1 + ov2


def _Q(K0, th, target):
    """P_tau( class(tau)==target AND class(tau3)==target ), tau3=frac(K0-tau), for a
    threshold-type class with class=1 iff x<th on [0,1) (arc [0,th)), class=0 -> arc [th,1).
    tau3's class-1 arc is the rotated arc {tau3<th} <=> tau in arc(start=frac(K0-th), len=th).
    """
    K0 = np.asarray(K0, dtype=np.float64)
    th = np.asarray(th, dtype=np.float64)
    if target == 1:
        # tau-arc: [0, th);  tau3-arc (class3=1): start=frac(K0-th), length=th
        s3 = np.mod(K0 - th, 1.0)
        return _arc_overlap_with_box(s3, th, 0.0, th)
    else:
        # tau-arc: [th, 1);  tau3-arc (class3=0): complement, start=K0, length=1-th
        s3 = np.mod(K0, 1.0)
        return _arc_overlap_with_box(s3, 1.0 - th, th, 1.0)


def _P_plus(pi, thp, x0p, d, e):
    """P(size on slope + through lift (d,e) is <=3), d,e python ints 0/1."""
    pi = np.asarray(pi, dtype=np.float64)
    thp = np.asarray(thp, dtype=np.float64)
    x0p = np.asarray(x0p, dtype=np.float64)
    a = (pi < thp).astype(np.int64)
    if d == e:
        return np.full(np.broadcast(pi, thp, x0p).shape, 0.5, dtype=np.float64)
    K0 = np.mod(-pi - 3.0 * x0p, 1.0)
    if (d, e) == (0, 1):
        Q0 = _Q(K0, thp, 0)
        return np.where(a == 1, 1.0, 0.5 + 0.5 * Q0)
    elif (d, e) == (1, 0):
        Q1 = _Q(K0, thp, 1)
        return np.where(a == 0, 1.0, 0.5 + 0.5 * Q1)
    else:
        raise ValueError((d, e))


def _P_minus(pi, thm, x0p, d, e):
    """P(size on slope - through lift (d,e) is <=3)."""
    pi = np.asarray(pi, dtype=np.float64)
    thm = np.asarray(thm, dtype=np.float64)
    x0p = np.asarray(x0p, dtype=np.float64)
    b = (pi > thm).astype(np.int64)
    if (d, e) in ((0, 1), (1, 0)):
        return np.full(np.broadcast(pi, thm, x0p).shape, 0.5, dtype=np.float64)
    K0 = np.mod(-pi - 3.0 * x0p, 1.0)
    # NOTE: class-(t) = 1 iff t>thm (arc (thm,1]), the MIRROR of class+'s [0,th) convention
    # that _Q is written for, so the target passed to _Q must be flipped (1<->0) here.
    if (d, e) == (0, 0):
        Q1 = _Q(K0, thm, 0)
        return np.where(b == 0, 1.0, 0.5 + 0.5 * Q1)
    elif (d, e) == (1, 1):
        Q0 = _Q(K0, thm, 1)
        return np.where(b == 1, 1.0, 0.5 + 0.5 * Q0)
    else:
        raise ValueError((d, e))


def U(pi, thp, thm, d, e, x0p):
    """U(pi, thp, thm, delta, eps, x0_over_p): probability the lift (d,e) of a residue at
    position pi with slope+/- thresholds thp,thm is uncovered.  pi,thp,thm,x0p vectorised
    (numpy arrays or scalars, mutually broadcastable); d,e are python ints in {0,1} (a single
    lift per call -- loop over the 4 lifts to cover all of them, as the validation script does).
    Exact (no Monte Carlo, no grid): closed-form arc-intersection integration over tau,tau'.
    """
    d = int(d); e = int(e)
    Pp = _P_plus(pi, thp, x0p, d, e)
    Pm = _P_minus(pi, thm, x0p, d, e)
    return Pp * Pm


if __name__ == "__main__":
    # quick self-test: compare exact arc formula against brute-force fine-grid / Monte-Carlo
    rng = np.random.default_rng(0)
    n = 20000
    pi = rng.random(n); thp = rng.random(n); thm = rng.random(n); x0p = rng.random(n)
    for d, e in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        exact = U(pi, thp, thm, d, e, x0p)
        # Monte Carlo cross-check
        M = 4000
        Ep = rng.random((M, n)) < 0.5
        tau = rng.random((M, n))
        Em = rng.random((M, n)) < 0.5
        taup = rng.random((M, n))
        K0 = np.mod(-pi - 3 * x0p, 1.0)
        a = (pi < thp).astype(np.int64)
        b = (pi > thm).astype(np.int64)
        kp = np.where(Ep, 3, 1)
        km = np.where(Em, 3, 1)
        tau3 = np.mod(K0 - tau, 1.0)
        c2p = (tau < thp).astype(np.int64); c3p = (tau3 < thp).astype(np.int64)
        npl = np.where(Ep, 1 + (c2p == a) + (c3p == a), 1)
        tau3p = np.mod(K0 - taup, 1.0)
        c2m = (taup > thm).astype(np.int64); c3m = (tau3p > thm).astype(np.int64)
        nmi = np.where(Em, 1 + (c2m == b) + (c3m == b), 1)
        if d == e:
            sizep = kp + npl
        elif (d, e) == (0, 1):
            sizep = np.where(a == 0, 2 * kp - npl, npl)
        else:
            sizep = np.where(a == 0, npl, 2 * kp - npl)
        if (d, e) in ((0, 1), (1, 0)):
            sizem = km + nmi
        elif (d, e) == (0, 0):
            sizem = np.where(b == 0, nmi, 2 * km - nmi)
        else:
            sizem = np.where(b == 0, 2 * km - nmi, nmi)
        unc = (sizep <= 3) & (sizem <= 3)
        mc = unc.mean(axis=0)
        print(f"(d,e)={(d,e)}: max|exact-MC|={np.max(np.abs(exact-mc)):.4f} mean|.|={np.mean(np.abs(exact-mc)):.5f}  (MC noise ~ 1/sqrt(M)={1/np.sqrt(M):.4f})")
