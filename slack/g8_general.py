"""g8_general.py — C4: for general k, the residue-group classification of ±1 lines of P_k = H(1) ∪ H(k) in the HJSW box, by the same
mechanism as §24 (k=-1): on x-y ≡ d the H(1) classes are the pair {a, -1/a} (a - 1/a ≡ d) and the H(k) classes the pair {b, -k/b}
(b - k/b ≡ d); a pair 'shares' its centre iff sign X(a) ≠ sign X(1/a) (resp. sign X(b) ≠ sign X(k/b)); LEMMA (F2 for every k): both pairs
shared ⇒ the two centres coincide ⇒ an 8-point +1 line (proof: L' = X(a)-X(1/a)-X(b)+X(k/b) ≡ 0 mod p, |L'| ≤ 2p-2, and the four sign cases
force L' = 0, p, -p, 0 = the required value).  Slope -1 (x+y ≡ e): pairs {a, 1/a} (a + 1/a ≡ e) and {b, k/b} (b + k/b ≡ e), shared iff
sign X(a) = sign X(1/a) (resp. X(b) = X(k/b) sign).  Counts G8(k,p) = both-shared groups on both slopes = number of 8-point ±1 lines
(cross-checked against the point-level count of slack/blocks_general.py).  usage: g8_general.py pmax k1 k2 ...   (k = -1 allowed)"""
import sys
def primes(n): return [q for q in range(3, n + 1) if all(q % d for d in range(2, int(q ** 0.5) + 1))]
def g8(p, k):
    h = (p - 1) // 2; k %= p
    X = lambda u: (u % p) if (u % p) <= h else (u % p) - p
    inv = [0] * p
    for a in range(1, p): inv[a] = pow(a, -1, p)
    def count(slope):
        # slope +1: pairs by d = a - c/a with c = 1 (H1) or k (Hk); shared iff opposite signs of X(a), X(c/a)
        # slope -1: e = a + c/a; shared iff same signs
        H1 = {}; Hk = {}
        for a in range(1, p):
            for c, D in ((1, H1), (k, Hk)):
                ca = c * inv[a] % p
                key = (a - ca) % p if slope > 0 else (a + ca) % p
                D.setdefault(key, set()).add(frozenset({a, (-ca) % p if slope > 0 else ca}))   # the pair {a, -c/a} (slope +) or {a, c/a} (slope -)
        both = 0; total4 = 0
        for key in set(H1) & set(Hk):
            P1 = [pr for pr in H1[key] if len(pr) == 2]; Pk = [pr for pr in Hk[key] if len(pr) == 2]
            if len(H1[key]) != 1 or len(Hk[key]) != 1: continue        # exactly one pair each (generic case)
            pr1 = next(iter(H1[key])); prk = next(iter(Hk[key]))
            if len(pr1) != 2 or len(prk) != 2: continue                # degenerate (fixed) classes excluded
            total4 += 1
            a = min(pr1); b = min(prk)
            s1 = (X(a) > 0) != (X(inv[a]) > 0); sk = (X(b) > 0) != (X(k * inv[b] % p) > 0)
            if slope < 0: s1 = not s1; sk = not sk
            if s1 and sk: both += 1
        return both, total4
    bp, tp = count(+1); bm, tm = count(-1)
    return bp + bm, tp + tm
if __name__ == "__main__":
    pmax = int(sys.argv[1]); ks = [int(x) for x in sys.argv[2:]]
    import statistics
    for k in ks:
        vals = []
        for p in primes(pmax):
            if p < 11 or k % p in (0, 1): continue
            g, t = g8(p, k); vals.append((p, g, t))
        big = [(g / p) for p, g, t in vals if p >= 100]
        print(f"k={k}: G8/p over primes 100..{pmax}: mean {statistics.mean(big):.4f} min {min(big):.4f} max {max(big):.4f} (n={len(big)}); "
              f"4-class groups/p mean {statistics.mean(t/p for p,g,t in vals if p>=100):.3f}; both-shared fraction {sum(g for p,g,t in vals if p>=100)/sum(t for p,g,t in vals if p>=100):.3f}; "
              f"sample: {[(p,g) for p,g,t in vals if p in (101,199,401,499)]}", flush=True)
