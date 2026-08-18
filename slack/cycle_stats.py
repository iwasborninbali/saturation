"""cycle_stats.py — arithmetic input for theorem C: along the class-cycle κ_a → μ_{ka} → κ_{ka} → μ_{k²a} → … (one ⟨k⟩-coset), mark the
'special' classes (members of (4,8,4) groups on either slope, both bases) and report: #K (κ-specials), #M (μ-specials), the number of K→M
transitions in the cyclic sequence of specials, the walk range (running #K−#M), and local window statistics (frequency of the 4 patterns of two
consecutive classes (κ_a, μ_{ka}) being (special,special)/(s,n)/(n,s)/(n,n)) — all should be p·const + O(√p log^c p) by Kloosterman-level
equidistribution of the least residues of (k^j a, k^{-j}/a).  usage: cycle_stats.py pmax [k]  (k=0: smallest primitive root)"""
import sys, math
sys.path.insert(0, 'slack')
from g8_general import primes
def prim_root(p):
    fac = []; m = p - 1; d = 2
    while d * d <= m:
        if m % d == 0: fac.append(d)
        while m % d == 0: m //= d
        d += 1
    if m > 1: fac.append(m)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac): return g
def specials(p, k):
    """set of special classes: ('K', a) for κ_a=(a,1/a) in an 8-group; ('M', b) for μ_b=(b,k/b) in an 8-group; via the group classification (both slopes)"""
    h = (p - 1) // 2
    X = lambda u: (u % p) if (u % p) <= h else (u % p) - p
    inv = [0] * p
    for a in range(1, p): inv[a] = pow(a, -1, p)
    S = set()
    for slope in (+1, -1):
        H1 = {}; Hk = {}
        for a in range(1, p):
            for c, D in ((1, H1), (k, Hk)):
                ca = c * inv[a] % p
                key = (a - ca) % p if slope > 0 else (a + ca) % p
                D.setdefault(key, set()).add(frozenset({a, (-ca) % p if slope > 0 else ca}))
        for key in set(H1) & set(Hk):
            if len(H1[key]) != 1 or len(Hk[key]) != 1: continue
            pr1 = next(iter(H1[key])); prk = next(iter(Hk[key]))
            if len(pr1) != 2 or len(prk) != 2: continue
            a = min(pr1); b = min(prk)
            s1 = (X(a) > 0) != (X(inv[a]) > 0); sk = (X(b) > 0) != (X(k * inv[b] % p) > 0)
            if slope < 0: s1 = not s1; sk = not sk
            if s1 and sk:
                for x in pr1: S.add(('K', x))
                for y in prk: S.add(('M', y))
    return S
def analyse(p, k):
    S = specials(p, k)
    # cycle through the coset of 1: κ_{k^j} → μ_{k^{j+1}} → κ_{k^{j+1}} …  (for primitive k this is the whole class graph)
    L = 1
    while pow(k, L, p) != 1: L += 1
    seq = []; a = 1
    for j in range(L):
        seq.append(('K', a) in S); seq.append(('M', (k * a) % p) in S)
        a = (k * a) % p
    K = sum(seq[0::2]); M = sum(seq[1::2])
    # walk: running (#K specials - #M specials)
    w = 0; mn = 0; mx = 0
    for i, s in enumerate(seq):
        if s: w += 1 if i % 2 == 0 else -1
        mn = min(mn, w); mx = max(mx, w)
    # transitions K->M in the cyclic subsequence of specials
    sp = [(i % 2) for i, s in enumerate(seq) if s]   # 0 = K, 1 = M
    trans = sum(1 for i in range(len(sp)) if sp[i] == 0 and sp[(i + 1) % len(sp)] == 1) if sp else 0
    # window statistics: pattern of (κ_a, μ_{ka}) = (seq[2j], seq[2j+1])
    pat = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 0}
    for j in range(L): pat[(int(seq[2 * j]), int(seq[2 * j + 1]))] += 1
    return L, K, M, trans, mx - mn, pat
if __name__ == "__main__":
    pmax = int(sys.argv[1]); k0 = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    print("p k ord | K M | K->M transitions | walk range | range/sqrt(p) | (s,s) (s,n) (n,s) (n,n) per L")
    for p in primes(pmax):
        if p < 11: continue
        k = prim_root(p) if k0 == 0 else k0 % p
        if k in (0, 1): continue
        L, K, M, tr, rng, pat = analyse(p, k)
        print(f"{p} {k} {L} | {K} {M} | {tr} | {rng} | {rng/math.sqrt(p):.2f} | {pat[(1,1)]/L:.3f} {pat[(1,0)]/L:.3f} {pat[(0,1)]/L:.3f} {pat[(0,0)]/L:.3f}", flush=True)
