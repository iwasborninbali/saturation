"""lns.py — large-neighbourhood search from a known book at resolution n to n + 2s.

Shift the known book by (s, s) inside the larger space (all its aliasing
relations survive the shift), free a small set F of orbits, keep the rest fixed,
and let there.c search a lawful completion (|F| + s orbits) exactly.  Repeat with
other F.  Every found book re-enters saturation.certify.

    python3 lns.py SOURCEFILE N_TARGET [--secs 20] [--k 4] [--tries 200] [--seed 1] [--mode corners|random|edge]
"""
from __future__ import annotations
import os, random, subprocess, sys, time
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web'))
import saturation as S
from decode import decode

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, 'there')

def rot4_orbit(u, v, N):
    m = N - 1
    return sorted({(u, v), (v, m - u), (m - u, m - v), (m - v, u)})

def orbits_of(pts, N, sym):
    """group the shifted markers into orbits (as tuples of cells)"""
    m = N - 1
    seen, orbs = set(), []
    for (u, v) in sorted(pts):
        if (u, v) in seen: continue
        if sym == 8 and u == v:
            o = sorted({(u, u), (m - u, m - u)})
        else:
            o = rot4_orbit(u, v, N)
        for c in o:
            assert c in pts, f"not closed under symmetry: {c}"
            seen.add(c)
        orbs.append(tuple(o))
    return orbs

def load_source(path, idx=0):
    lines = [l for l in open(path) if l.strip()]
    cls, n, book = decode(lines[idx])
    pts = {divmod(t, n) for t in book}
    if cls == 'rct4':
        m = n - 1
        # move the diagonal pair onto the main diagonal (swap reflection) if needed
        if any(u + v == m for (u, v) in pts):
            pts = {(v, u) for (u, v) in pts}
    return cls, n, pts

def try_completion(N, sym, fixed_cells, seed, secs):
    path = os.path.join(HERE, f'lns_fix_{os.getpid()}.txt')
    with open(path, 'w') as f:
        f.write(' '.join(str(u * N + v) for (u, v) in sorted(fixed_cells)))
    env = dict(os.environ, FIX=path)
    out = subprocess.run([BIN, str(N), str(sym), str(seed), str(secs)], capture_output=True, text=True, env=env).stdout.strip()
    os.remove(path)
    if out.startswith('book'):
        toks = [int(x) for x in out.split(' :')[1].split()]
        return 'book', frozenset(toks), out.split(' :')[0]
    return ('none' if out.startswith('none') else 'timeout'), None, out

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    opt = {sys.argv[i][2:]: sys.argv[i + 1] for i in range(len(sys.argv) - 1) if sys.argv[i].startswith('--')}
    src, N = args[0], int(args[1])
    secs = float(opt.get('secs', 20)); k = int(opt.get('k', 4)); tries = int(opt.get('tries', 200))
    seed = int(opt.get('seed', 1)); mode = opt.get('mode', 'edge'); idx = int(opt.get('idx', 0))
    rng = random.Random(seed)
    cls, n, pts = load_source(src, idx)
    s = (N - n) // 2
    sym = 2 if N % 2 == 0 else 8
    assert (cls == 'rot4') == (N % 2 == 0), "class/parity mismatch"
    shifted = {(u + s, v + s) for (u, v) in pts}
    orbs = orbits_of(shifted, N, sym)
    m = N - 1
    def edge_dist(o):   # distance of the orbit to the boundary of the target space
        return min(min(u, v, m - u, m - v) for (u, v) in o)
    print(f"source {src}[{idx}] class={cls} n={n} -> N={N} shift={s} sym={sym} orbits={len(orbs)}")
    t0 = time.time(); attempts = 0
    while attempts < tries:
        attempts += 1
        if mode == 'random':
            F = rng.sample(orbs, k)
        elif mode == 'edge':          # bias towards orbits near the boundary
            w = [1.0 / (1 + edge_dist(o)) ** 2 for o in orbs]
            F = []
            pool = list(range(len(orbs)))
            while len(F) < k:
                i = rng.choices(pool, weights=[w[j] for j in pool])[0]
                F.append(orbs[i]); pool.remove(i)
        else:
            raise SystemExit("mode?")
        fixed = set(shifted)
        for o in F:
            for c in o: fixed.discard(c)
        status, book, info = try_completion(N, sym, fixed, seed * 1000 + attempts, secs)
        el = time.time() - t0
        print(f"[{el:7.1f}s] try {attempts}: freed {len(F)} orbits ({sum(len(o) for o in F)} cells) -> {status}  {info[:60] if status!='book' else ''}")
        if status == 'book':
            claim = S.certify(book, N)
            print("FOUND:", claim)
            print("book", N, sym, *sorted(book))
            with open(os.path.join(HERE, f'lns_found_n{N}.txt'), 'a') as f:
                f.write(f"{claim}\n{' '.join(map(str, sorted(book)))}\n")
            return 0
    print("no completion found in", attempts, "tries")
    return 1

if __name__ == '__main__':
    sys.exit(main())
