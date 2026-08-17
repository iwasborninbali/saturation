"""hjsw_boxes_check.py — checks for Theorem 2 of paper/hjsw_window.tex (third solver):
for EVERY 2p×2p box W = [x0,x0+2p)×[y0,y0+2p) every lawful subset of H(c,p)∩W has ≤ 3(p−1) points.

Checked here (nothing of the proof is trusted; everything is recomputed from point sets or from the residues):
  1. sanity: the closed formula  Z + 2|L| = 2(p−1) + 2s + 2·Σ_O (e_O+f_O)  agrees with brute-force line enumeration
     (rich lines found over all pairs of points) on random boxes;
  2. scan: for all primes p ≤ P1, all c, all boxes (x0,y0 mod p): Z + 2|L| ≤ 3(p−1)  (this is the theorem's inequality),
     with equality for some boxes;
  3. orbit lemma: for all p ≤ P2, all c, all boxes: every generic V4-orbit has (e_O,f_O) ∈ {(0,0),(0,2),(1,1),(2,0)};
  4. proof identities (θ = c_a+c_b−k, η = c_b−c_a, split conditions, parity, "F1 ⇒ not(E1 and E2)") on random instances up to p=199.
usage: python3 slack/hjsw_boxes_check.py [P1=31] [P2=23]"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hjsw_window_check import lines_ge3


def pts(p, c, x0, y0):
    return [(x, y) for x in range(x0, x0 + 2 * p) for y in range(y0, y0 + 2 * p) if x % p and y % p and (x * y - c) % p == 0]


def brute_bound(p, c, x0, y0):
    P = pts(p, c, x0, y0); L = lines_ge3(P)
    for (dx, dy, _) in L: assert (dx, dy) in ((1, 1), (1, -1)), "rich line of slope other than ±1"
    on = set(q for m in L.values() for q in m)
    return len(P) - len(on) + 2 * len(L)


def orbits(p, c, x0, y0):
    """for each generic orbit {a,-a,b,-b} (ab=c): (e,f) = numbers of split sigma-/tau-pairs; also s and the exceptional split count"""
    rx = lambda t: x0 + ((t - x0) % p); ry = lambda u: y0 + ((u - y0) % p)
    inv = lambda a: pow(a, -1, p)
    seen = set(); out = []; s = 0
    for a in range(1, p):
        b = c * inv(a) % p
        if a == b or a == (-b) % p: s += 1
        if a in seen: continue
        orb = {a, (-a) % p, b, (-b) % p}; seen |= orb
        if len(orb) < 4: continue
        # sigma-pairs {a,-b},{-a,b}: split iff d differs; d(class (u,w)) = rx(u)-ry(w)
        d = lambda u, w: rx(u) - ry(w); e = lambda u, w: rx(u) + ry(w)
        e1 = d(a, b) != d((-b) % p, (-a) % p); e2 = d((-a) % p, (-b) % p) != d(b, a)
        f1 = e(a, b) != e(b, a); f2 = e((-b) % p, (-a) % p) != e((-a) % p, (-b) % p)
        out.append((e1 + e2, f1 + f2))
    return out, s // 2


def formula_bound(p, c, x0, y0):
    ob, s = orbits(p, c, x0, y0)
    return 2 * (p - 1) + 2 * s + 2 * sum(e + f for e, f in ob)


def proof_identities(p, c, x0, y0):
    rx = lambda t: x0 + ((t - x0) % p); ry = lambda u: y0 + ((u - y0) % p); inv = lambda a: pow(a, -1, p)
    mx = ((2 * x0) // p + 1) * p; my = ((2 * y0) // p + 1) * p; mux = mx - 2 * x0; muy = my - 2 * y0
    assert 1 <= mux <= p and 1 <= muy <= p
    v = (x0 - y0) % p; seen = set()
    for a in range(1, p):
        b = c * inv(a) % p
        if a in seen or a == b or a == (-b) % p: continue
        seen |= {a, (-a) % p, b, (-b) % p}
        Xa, Xb, Xa_, Xb_ = rx(a), rx(b), rx(-a), rx(-b); Ya, Yb, Ya_, Yb_ = ry(a), ry(b), ry(-a), ry(-b)
        dP, dQ, dR, dT = Xa - Yb, Xb_ - Ya_, Xb - Ya, Xa_ - Yb_; eP, eQ, eR, eT = Xa + Yb, Xb_ + Ya_, Xb + Ya, Xa_ + Yb_
        for u, w in [(dP, dQ), (dT, dR), (eP, eR), (eQ, eT)]: assert (u - w) % p == 0 and abs(u - w) <= p
        E1, E2, F1, F2 = (dP != dQ), (dT != dR), (eP != eR), (eQ != eT)
        exa = (Xa + Xa_ - mx) // p; exb = (Xb + Xb_ - mx) // p; eya = (Ya + Ya_ - my) // p; eyb = (Yb + Yb_ - my) // p
        assert Xa + Xa_ == mx + exa * p and Xb + Xb_ == mx + exb * p and Ya + Ya_ == my + eya * p and Yb + Yb_ == my + eyb * p
        assert {exa, exb, eya, eyb} <= {0, 1}
        s_, t_ = Xa - x0, Xb - x0; assert exa == (s_ > mux) and exb == (t_ > mux)
        yta, ytb = Ya - y0, Yb - y0; assert eya == (yta > muy) and eyb == (ytb > muy)
        ca = int(s_ + v >= p); cb = int(t_ + v >= p); assert yta == s_ + v - p * ca and ytb == t_ + v - p * cb
        k = (mux - muy + 2 * v) // p; assert mux - muy == -2 * v + p * k and k in (0, 1, 2)
        theta = (dP + dR - (mx - my)) // p; assert dP + dR - (mx - my) == theta * p and theta == ca + cb - k
        eta = (eR - eP) // p; assert eR - eP == eta * p and eta == cb - ca
        A = exb - eya; B = exa - eyb; G = eya - eyb; D = exa - exb
        assert E1 == (theta != A) and E2 == (theta != B) and F1 == (eta != 0) and F2 == (eta != G - D)
        assert (E1 + E2 + F1 + F2) % 2 == 0
        if F1: assert not (E1 and E2)
        assert E1 + E2 + F1 + F2 <= 2


if __name__ == "__main__":
    P1 = int(sys.argv[1]) if len(sys.argv) > 1 else 31
    P2 = int(sys.argv[2]) if len(sys.argv) > 2 else 23
    primes = lambda P: [p for p in range(3, P + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]
    random.seed(1)
    for _ in range(60):
        p = random.choice(primes(19)); c = random.randrange(1, p); x0 = random.randrange(-p, p); y0 = random.randrange(-p, p)
        assert brute_bound(p, c, x0, y0) == formula_bound(p, c, x0, y0), (p, c, x0, y0)
    print("1. formula Z+2|L| = 2(p-1)+2s+2*sum(e+f) agrees with brute force on 60 random boxes (p<=19)")
    for p in primes(P1):
        mx = 0; eq = 0
        for c in range(1, p):
            for x0 in range(p):
                for y0 in range(p):
                    b = formula_bound(p, c, x0 - (p - 1) // 2, y0)
                    assert b <= 3 * (p - 1), (p, c, x0, y0, b)
                    if b == 3 * (p - 1): eq += 1
        print(f"2. p={p}: Z+2|L| <= 3(p-1) for all c and all {p*p} boxes; equality for {eq} (c,box) pairs", flush=True)
    for p in primes(P2):
        seen = set()
        for c in range(1, p):
            for x0 in range(p):
                for y0 in range(p):
                    ob, s = orbits(p, c, x0, y0)
                    for ef in ob:
                        seen.add(ef); assert ef in ((0, 0), (0, 2), (1, 1), (2, 0)), (p, c, x0, y0, ef)
        print(f"3. p={p}: orbit lemma — (e,f) values over all c, boxes, generic orbits: {sorted(seen)}", flush=True)
    n = 0
    for _ in range(300):
        p = random.choice(primes(199)[3:]); c = random.randrange(1, p); x0 = random.randrange(-3 * p, 3 * p); y0 = random.randrange(-3 * p, 3 * p)
        proof_identities(p, c, x0, y0); n += 1
    print(f"4. proof identities verified on {n} random (p,c,x0,y0) instances (all generic orbits each), p<=199")
    print("all checks passed")
