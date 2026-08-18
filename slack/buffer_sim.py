"""buffer_sim.py — the uniform-t certificate (§28/§29) on real cycles and in the k=2 limit model.

Real instance (p, k): along every cycle (coset a0<k>) the slots are κ_{a0 k^j} (even) and μ_{a0 k^{j+1}} (odd); s∈{0,1} = special.
Buffer of capacity m (units of t=1/m): at a special μ deposit 1 unit if level<m (else BLOCKED), at a special κ withdraw 1 unit if level>0.
D = t·(#unblocked μ-specials); rows/cols cost = 2L − 4D per cycle; net per group = 4D/G8 − 6t = t·(4·U/G8 − 6), U = #unblocked μ.
β = blocked/(#μ-specials): net>0 ⇔ β<1/4.  Window certificate: disjoint windows of W slots, g_w = unblocked μ's from the WORST start
(full buffer); Σ_w g_w ≤ U (monotone coupling) — E[g_W] and the remainder U − Σ g_w.
Limit model (k=2): u=a/p uniform → sign X(2^j a) = bit_j(u), coarse X(2^j a)/p = tail 0.u_j u_{j+1}…; ā=1/a: sign X(2^{-j}ā) = ε_{j-1},
coarse = 0.ε_{j-1}ε_{j-2}… (reverse binary digits, i.i.d. fair); partner existence = fair coins; partner sharing via fresh uniform B and
X(k/b) ≡ X(b) − X(x) + X(1/x) (slope +1) / X(x)+X(1/x)−X(b) (slope −1); μ-partner via a' with X(1/a') ≡ X(a') − X(y) + X(k/y) (+1) /
X(y)+X(k/y)−X(a') (−1).  usage: buffer_sim.py real p k [W]   |   buffer_sim.py model N [W] [seed]"""
import sys, math, random
sys.path.insert(0, 'slack')

def red(t):
    """reduce t (units of p) into (−1/2, 1/2)"""
    t = t - math.floor(t + 0.5)
    return t

def real_sequence(p, k):
    from cycle_stats import specials
    S = specials(p, k)
    L = 1
    while pow(k, L, p) != 1: L += 1
    r = (p - 1) // L
    # cosets: representatives via primitive root powers
    from cycle_stats import prim_root
    g = prim_root(p)
    seqs = []
    for i in range(r):
        a = pow(g, i, p); seq = []
        for j in range(L):
            seq.append(('K', a) in S); seq.append(('M', k * a % p) in S)
            a = k * a % p
        seqs.append(seq)
    G8 = sum(1 for t in S if t[0] == 'K') // 2
    return seqs, G8

def run_buffer(seq, m, start):
    """seq: list of bool over slots (even=κ, odd=μ); returns (unblocked μ count, blocked μ count, final level)"""
    lvl = start; U = 0; Bk = 0
    for i, s in enumerate(seq):
        if not s: continue
        if i % 2 == 1:
            if lvl < m: lvl += 1; U += 1
            else: Bk += 1
        else:
            if lvl > 0: lvl -= 1
    return U, Bk, lvl

def analyse(seqs, G8, ms=(3, 4, 5, 6, 7, 8, 10, 12), W=None, label=''):
    nK = sum(sum(seq[0::2]) for seq in seqs); nM = sum(sum(seq[1::2]) for seq in seqs)
    slots = sum(len(seq) for seq in seqs)
    print(f"{label} slots={slots} G8={G8} #κspec={nK} #μspec={nM} density={nK/(slots/2):.4f}")
    for m in ms:
        t = 1.0 / m
        best = None
        for start in range(m + 1):
            U = sum(run_buffer(seq, m, start)[0] for seq in seqs)
            if best is None or U > best[0]: best = (U, start)
        U, start = best
        beta = 1 - U / nM if nM else 0
        net = t * (4 * U / G8 - 6) if G8 else 0
        line = f"  m={m:2d} t=1/{m}: unblocked μ={U} β={beta:.4f} net/group={net:+.4f}"
        if W:
            # window certificate: disjoint windows of W slots, worst start (full)
            Sg = 0; nw = 0; groups_in = 0
            for seq in seqs:
                for s0 in range(0, len(seq) - W + 1, W):
                    Sg += run_buffer(seq[s0:s0 + W], m, m)[0]; nw += 1
            netW = t * (4 * Sg / G8 - 6) if G8 else 0
            line += f" | windows W={W}: Σg={Sg} (E[g_W]={Sg/max(nw,1):.3f}) remainder={U - Sg} certified net/group={netW:+.4f}"
        print(line, flush=True)

def model_sequence(N, rng):
    """k=2 limit model: N κ/μ pairs → 2N slots. Returns list of bool."""
    PREC = 40
    ubits = [rng.random() < 0.5 for _ in range(N + PREC + 2)]        # forward bits u_j
    ebits = [rng.random() < 0.5 for _ in range(N + PREC + 2)]        # backward bits ε_{j-1} stored at index j+PREC (ε_{-i} for i≤PREC as tail)
    def coarse_fwd(j):   # 0.u_j u_{j+1} ... as value in (0,1)
        v = 0.0; w = 0.5
        for i in range(PREC):
            if ubits[j + i]: v += w
            w *= 0.5
        return v
    def coarse_bwd(j):   # 0.ε_{j-1} ε_{j-2} ... ; ε index i stored at ebits[i+PREC]
        v = 0.0; w = 0.5
        for i in range(PREC):
            idx = j - 1 - i + PREC
            if idx < 0: break
            if ebits[idx]: v += w
            w *= 0.5
        return v
    def signed(c): return c if c < 0.5 else c - 1.0
    seq = []
    xs = [signed(coarse_fwd(j)) for j in range(N + 1)]      # X(x_j)/p
    ws = [signed(coarse_bwd(j)) for j in range(N + 1)]      # X(1/x_j)/p
    for j in range(N):
        x, w = xs[j], ws[j]
        # κ_j: own pair shared on slope +1 iff signs differ, on slope −1 iff equal
        slope = +1 if (x > 0) != (w > 0) else -1
        exists = rng.random() < 0.5
        sK = False
        if exists:
            B = rng.random() - 0.5
            if slope > 0: kb = red(B - x + w); sK = (B > 0) != (kb > 0)
            else:         kb = red(x + w - B); sK = (B > 0) == (kb > 0)
        seq.append(sK)
        # μ_{j+1}: y = x_{j+1}, k/y = 1/x_j
        y, ky = xs[j + 1], ws[j]
        slope = +1 if (y > 0) != (ky > 0) else -1
        exists = rng.random() < 0.5
        sM = False
        if exists:
            A = rng.random() - 0.5
            if slope > 0: ia = red(A - y + ky); sM = (A > 0) != (ia > 0)
            else:         ia = red(y + ky - A); sM = (A > 0) == (ia > 0)
        seq.append(sM)
    return seq

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'real':
        p = int(sys.argv[2]); k = int(sys.argv[3]); W = int(sys.argv[4]) if len(sys.argv) > 4 else None
        seqs, G8 = real_sequence(p, k)
        analyse(seqs, G8, W=W, label=f"REAL p={p} k={k}")
    else:
        N = int(sys.argv[2]); W = int(sys.argv[3]) if len(sys.argv) > 3 else None
        seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        seq = model_sequence(N, random.Random(seed))
        # in the model, G8 := (#κ specials)/2 (each group has 2 κ's), consistent with K = M
        nK = sum(seq[0::2]); nM = sum(seq[1::2])
        print(f"MODEL k=2 N={N}: #κspec={nK} #μspec={nM} (K=M only in expectation here)")
        analyse([seq], nK / 2, W=W, label=f"MODEL N={N}")
