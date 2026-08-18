"""km1_lines_5678.py — k=-1: exact anatomy of the slope-(+1) integer lines of P_{-1} = (H(1) ∪ H(-1)) ∩ G(p) by residue group.
For residue d: H(1) classes κ=(a,1/a) with a-1/a ≡ d (0, 1 or 2 classes: a and -1/a; one class if a² ≡ -1), H(-1) classes R(λ), λ=(b,1/b)
with b+1/b ≡ -d (b and 1/b; one class if b² ≡ 1).  Centres (integer line offsets x-y): d_κ = X(a)-Y(1/a) for κ (copies (0,0),(1,1) on the
centre line, (1,0) on centre+p, (0,1) on centre-p); for R(λ): -e_λ = -(X(b)+Y(1/b)).  X = least absolute residue in [-h,h], Y = least
positive residue in [1,p-1].  Each class contributes (1,2,1) to (centre-p, centre, centre+p); the group's line sizes follow from how the
centres coincide: 4 classes with m centres at the smaller value c and 4-m at c+p give sizes (m, m+4, 8-m, 4-m).
Exact coincidence conditions (all centres are ≡ d mod p, in [-h-p+1, h-1], so at most two values c, c+p):
  d_κ  = X(a)-X(1/a) - p·[X(1/a)<0],   d_σκ = X(a)-X(1/a) - p·[X(a)>0]      ⇒ σ-pair shares its centre iff sign X(a) ≠ sign X(1/a);
  -e_λ = -X(b)-X(1/b) - p·[X(1/b)<0],  -e_τλ = -X(b)-X(1/b) - p·[X(b)<0]     ⇒ τ-pair shares its centre iff sign X(b) = sign X(1/b);
  cross: d_κ = -e_λ iff L := X(a)-X(1/a)+X(b)+X(1/b) = p·([X(1/a)<0] - [X(1/b)<0])  (L ≡ 0 mod p, |L| ≤ 2p-2, so L ∈ {-p,0,p}), similarly
  for the other three cross pairs with the corresponding sign brackets.
Output per p: counts of +1 lines of size 5,6,7,8 (m5..m8), the group patterns that produce them, densities, and the savings constant
s(p) = (2 m8 + 1.5 m7 + m6 + 0.5 m5)/(p-1) (per slope; the −1 slope is the R-mirror image).   usage: km1_lines_5678.py pmax [verbose]"""
import sys
from collections import Counter, defaultdict
def primes(n): return [q for q in range(3, n + 1) if all(q % d for d in range(2, int(q ** 0.5) + 1))]
def analyse(p):
    h = (p - 1) // 2
    X = lambda u: (u % p) if (u % p) <= h else (u % p) - p
    Y = lambda u: (u % p) if (u % p) else p
    lines = defaultdict(int)                       # integer offset -> number of points of P_{-1} on the +1 line x-y=offset
    patterns = Counter()                           # (n_classes, m) -> count of groups
    reasons = Counter()
    for d in range(p):
        # H(1) classes: a - 1/a ≡ d  <=>  a^2 - d a - 1 ≡ 0
        As = [a for a in range(1, p) if (a * a - d * a - 1) % p == 0]
        # H(-1) classes: b + 1/b ≡ -d <=> b^2 + d b + 1 ≡ 0
        Bs = [b for b in range(1, p) if (b * b + d * b + 1) % p == 0]
        centres = []
        seen = set()
        for a in As:
            cls = frozenset({a, (-pow(a, -1, p)) % p})       # κ and σκ share the class set {a, -1/a}? no: κ=(a,1/a) is one class; σκ=(-1/a,-a) is the class with x=-1/a
            ia = pow(a, -1, p)
            key = ('H1', a)
            if key in seen: continue
            seen.add(key)
            centres.append(X(a) - Y(ia))
        for b in Bs:
            ib = pow(b, -1, p)
            key = ('Hm1', b)
            if key in seen: continue
            seen.add(key)
            centres.append(-(X(b) + Y(ib)))
        if not centres: continue
        cmin = min(centres)
        m = sum(1 for c in centres if c == cmin)
        assert all(c in (cmin, cmin + p) for c in centres), (p, d, centres)
        patterns[(len(centres), m)] += 1
        for c in centres:
            lines[c - p] += 1; lines[c] += 2; lines[c + p] += 1
        if len(As) == 2 and len(Bs) == 2:
            a = As[0]; b = Bs[0]; ia = pow(a, -1, p); ib = pow(b, -1, p)
            sig = (X(a) > 0, X(ia) > 0, X(b) > 0, X(ib) > 0)
            sh_sigma = (X(a) > 0) != (X(ia) > 0); sh_tau = (X(b) > 0) == (X(ib) > 0)
            reasons[(m, sh_sigma, sh_tau)] += 1
    sizes = Counter(lines.values())
    return sizes, patterns, reasons
pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 500
verbose = len(sys.argv) > 2
tot = Counter(); totp = 0
print("p: m5 m6 m7 m8 | m8/p m7/p m6/p m5/p | savings/(p-1) | 4-class groups by m (m=#centres at the smaller value): 4:(4,8,4) 3:(3,7,5,1) 2:(2,6,6,2) 1:(1,5,7,3) 0")
for p in primes(pmax):
    if p < 11: continue
    sizes, patterns, reasons = analyse(p)
    m5, m6, m7, m8 = sizes.get(5, 0), sizes.get(6, 0), sizes.get(7, 0), sizes.get(8, 0)
    sav = (2 * m8 + 1.5 * m7 + m6 + 0.5 * m5) / (p - 1)
    g4 = {m: patterns.get((4, m), 0) for m in (4, 3, 2, 1, 0)}
    N4 = sum(g4.values()); N2 = sum(v for (n, m), v in patterns.items() if n == 2); N3 = sum(v for (n, m), v in patterns.items() if n == 3)
    print(f"{p:4d}: {m5:3d} {m6:3d} {m7:3d} {m8:3d} | {m8/p:.3f} {m7/p:.3f} {m6/p:.3f} {m5/p:.3f} | {sav:.3f} | 4:{g4[4]:3d} 3:{g4[3]:3d} 2:{g4[2]:3d} 1:{g4[1]:3d} 0:{g4[0]:3d} | N4={N4} N3={N3} N2={N2} N4/p={N4/p:.3f}" + (f"  reasons {dict(reasons)}" if verbose else ""), flush=True)
    tot['N4'] += N4
    if p >= 200:
        tot['m5'] += m5; tot['m6'] += m6; tot['m7'] += m7; tot['m8'] += m8; tot['sav'] += sav; totp += p; tot['n'] += 1
if tot['n']:
    print(f"# averages over primes 200..{pmax}: m8/p={tot['m8']/totp:.4f} m7/p={tot['m7']/totp:.4f} m6/p={tot['m6']/totp:.4f} m5/p={tot['m5']/totp:.4f} savings/(p-1)={tot['sav']/tot['n']:.4f}")
