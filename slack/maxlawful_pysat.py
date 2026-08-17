"""maxlawful_pysat.py — independent check of the maximum lawful subset of a candidate set (integer collinearity),
different encoding (per-line at-most-2 via totalizer) and different solver (CaDiCaL via python-sat).
usage: maxlawful_pysat.py U p q N [s_lo s_hi]   (mode U of slack/liftmax.c: hyperbolas xy=1 mod p and mod q, x shifted by -(p-1)/2)
       maxlawful_pysat.py file cands.txt [s_lo s_hi]   (x y per line)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import saturation as S
from math import gcd
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

def cands_U(p, q, N):
    out = []
    for x in range(N):
        for y in range(N):
            xp = (x - (p - 1) // 2) % p; xq = (x - (q - 1) // 2) % q
            ok = (xp != 0 and y % p != 0 and (xp * y) % p == 1) or (xq != 0 and y % q != 0 and (xq * y) % q == 1)
            if ok: out.append((x, y))
    return out

def lines(cands):
    """all maximal collinear subsets (>=3) of the candidates, as index tuples"""
    idx = {c: i for i, c in enumerate(cands)}
    seen = set(); out = []
    n = len(cands)
    for i in range(n):
        for j in range(i + 1, n):
            (x1, y1), (x2, y2) = cands[i], cands[j]
            dx, dy = x2 - x1, y2 - y1; g = gcd(abs(dx), abs(dy)); dx //= g; dy //= g
            if dx < 0 or (dx == 0 and dy < 0): dx, dy = -dx, -dy
            c0 = dx * y1 - dy * x1
            key = (dx, dy, c0)
            if key in seen: continue
            seen.add(key)
            mem = [k for k, (x, y) in enumerate(cands) if dx * y - dy * x == c0]
            if len(mem) >= 3: out.append(tuple(mem))
    return out

def solve(cands, s, secs=None):
    L = lines(cands); n = len(cands)
    pool = IDPool(start_from=n + 1)
    with Cadical153() as sol:
        for mem in L:
            enc = CardEnc.atmost(lits=[k + 1 for k in mem], bound=2, vpool=pool, encoding=EncType.seqcounter)
            for cl in enc.clauses: sol.add_clause(cl)
        enc = CardEnc.atleast(lits=list(range(1, n + 1)), bound=s, vpool=pool, encoding=EncType.totalizer)
        for cl in enc.clauses: sol.add_clause(cl)
        ok = sol.solve()
        if ok:
            model = set(v for v in sol.get_model() if 0 < v <= n)
            pts = [cands[v - 1] for v in model]
            return True, pts
        return False, None

if __name__ == "__main__":
    if sys.argv[1] == "U":
        p, q, N = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); cands = cands_U(p, q, N)
        lo = int(sys.argv[5]) if len(sys.argv) > 5 else 1; hi = int(sys.argv[6]) if len(sys.argv) > 6 else len(cands)
        tag = f"U p={p} q={q} N={N}"
    else:
        cands = [tuple(map(int, l.split()[:2])) for l in open(sys.argv[2]) if l.strip()]
        N = max(max(x, y) for x, y in cands) + 1
        lo = int(sys.argv[3]) if len(sys.argv) > 3 else 1; hi = int(sys.argv[4]) if len(sys.argv) > 4 else len(cands)
        tag = f"file {sys.argv[2]} N={N}"
    print(f"{tag}: candidates={len(cands)} lines(>=3)={len(lines(cands))}", flush=True)
    best = None
    for s in range(lo, hi + 1):
        ok, pts = solve(cands, s)
        if ok:
            S.the_law(frozenset(x * N + y for (x, y) in pts), N)          # verified by the law
            best = (s, sorted(pts)); print(f"  s={s}: SAT (ratio {s/N:.3f})", flush=True)
        else:
            print(f"  s={s}: UNSAT  => max = {s-1}", flush=True); break
    if best: print("  witness:", best[1])
