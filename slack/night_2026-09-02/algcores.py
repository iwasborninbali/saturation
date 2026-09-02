#!/usr/bin/env python3
"""Алгебраические ядра: содержат ли известные 2n-решения no-3-in-line большие куски модулярных коник?

Для каждого решения S (2n точек в n x n) и простого p ищем максимум |S ∩ C| по семействам
  (a) гиперболы  (x+a)(y+b) ≡ k (mod p),           параметры a,b ∈ Z_p, k любое  -> p^2 сдвигов
  (b) коники     (x+a)^2 + c(y+b)^2 ≡ k (mod p),   c ∈ Z_p\{0}                   -> p^3 комбинаций
Максимум по k берётся бесплатно: это наибольшая кратность значения формы на точках S.
Нуль-модель: случайные расстановки «2 в строке, 2 в столбце» без запрета троек — та же статистика.
Вывод: по n — процентили максимального перекрытия (решения против нуля), верхние хиты с параметрами.
"""
import sys, os, json, time, argparse, collections
import numpy as np
from multiprocessing import Pool

ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
IDX = {c: i for i, c in enumerate(ALPHA)}

def primes_between(lo, hi):
    out = []
    for q in range(max(2, lo), hi + 1):
        if all(q % d for d in range(2, int(q ** 0.5) + 1)): out.append(q)
    return out

def load(path):
    by_n = collections.defaultdict(list)
    for l in open(path):
        l = l.strip()
        if l: by_n[(len(l) - 1) // 2].append(l)
    return by_n

def points(line):
    body = line[1:]; n = len(body) // 2
    x = np.array([IDX[c] for c in body], dtype=np.int64)
    y = np.repeat(np.arange(n, dtype=np.int64), 2)
    return x, y

def random_arrangement(n, rng):
    while True:
        p1 = rng.permutation(n); p2 = rng.permutation(n)
        if (p1 != p2).all(): break
    x = np.empty(2 * n, dtype=np.int64); x[0::2] = p1; x[1::2] = p2
    return x, np.repeat(np.arange(n, dtype=np.int64), 2)

def best_overlap(x, y, p, c_values):
    """максимальное перекрытие с гиперболой (a) и с кониками (b) при данном p; возвращает
    (best_a, (a,b,k)), (best_b, (c,a,b,k))"""
    m = len(x); A = np.arange(p, dtype=np.int64)
    xa = (x[None, :] + A[:, None]) % p            # (p, m)
    yb = (y[None, :] + A[:, None]) % p            # (p, m)
    # (a) гиперболы: v[a,b,i] = xa[a,i]*yb[b,i] mod p
    v = (xa[:, None, :] * yb[None, :, :]) % p     # (p, p, m)
    flat = v.reshape(p * p, m) + (np.arange(p * p, dtype=np.int64) * p)[:, None]
    cnt = np.bincount(flat.ravel(), minlength=p * p * p).reshape(p * p, p)
    idx = int(cnt.argmax()); ba = int(cnt.max())
    a_, b_ = divmod(idx // p, p); k_ = idx % p
    res_a = (ba, (int(a_), int(b_), int(k_)))
    # (b) коники: v = xa^2 + c*yb^2
    xa2 = (xa * xa) % p; yb2 = (yb * yb) % p
    best_b = (0, None)
    for c in c_values:
        v = (xa2[:, None, :] + c * yb2[None, :, :]) % p
        flat = v.reshape(p * p, m) + (np.arange(p * p, dtype=np.int64) * p)[:, None]
        cnt = np.bincount(flat.ravel(), minlength=p * p * p).reshape(p * p, p)
        bb = int(cnt.max())
        if bb > best_b[0]:
            idx = int(cnt.argmax()); a_, b_ = divmod(idx // p, p)
            best_b = (bb, (int(c), int(a_), int(b_), int(idx % p)))
    return res_a, best_b

def window_size(n, p, fam, par):
    """сколько всего клеток сетки лежит на этой конике (для контекста хита)"""
    X, Y = np.meshgrid(np.arange(n), np.arange(n), indexing='ij')
    if fam == 'a':
        a, b, k = par; return int((((X + a) * (Y + b)) % p == k).sum())
    c, a, b, k = par; return int((((X + a) ** 2 + c * (Y + b) ** 2) % p == k).sum())

def work(args):
    n, lines, plist, c_mode, seed, is_null = args
    rng = np.random.default_rng(seed)
    out = []
    for item in lines:
        x, y = random_arrangement(n, rng) if is_null else points(item)
        best = (0, None, None, None)
        for p in plist:
            c_values = range(1, p) if c_mode == 'full' else sorted({1, 2, 3, p - 1, p - 2, p - 3} - {0})
            (ba, pa), (bb, pb) = best_overlap(x, y, p, c_values)
            if ba > best[0]: best = (ba, p, 'a', pa)
            if bb > best[0]: best = (bb, p, 'b', pb)
        out.append((best[0], best[1], best[2], best[3], None if is_null else item))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('db'); ap.add_argument('--out', default='algcores_results.json')
    ap.add_argument('--nmin', type=int, default=8); ap.add_argument('--nmax', type=int, default=40)
    ap.add_argument('--full-upto', type=int, default=20, help='до этого n берём все решения и полное семейство (b)')
    ap.add_argument('--sample', type=int, default=1000, help='решений на n выше full-upto')
    ap.add_argument('--null', type=int, default=1000, help='случайных расстановок на n')
    ap.add_argument('--procs', type=int, default=os.cpu_count())
    ap.add_argument('--quick', action='store_true')
    a = ap.parse_args()
    by_n = load(a.db)
    results = {}
    t0 = time.time()
    for n in range(a.nmin, a.nmax + 1):
        if n not in by_n: continue
        lines = by_n[n]
        full = n <= a.full_upto
        if not full:
            rng = np.random.default_rng(n); lines = [lines[i] for i in rng.permutation(len(lines))[:a.sample]]
        if a.quick: lines = lines[:200]
        plist = primes_between(max(5, n // 2), 2 * n + 1)
        c_mode = 'full' if full else 'few'
        chunks = [lines[i::a.procs] for i in range(a.procs)]
        nnull = min(a.null, 200 if a.quick else a.null)
        null_chunks = [list(range(nnull))[i::a.procs] for i in range(a.procs)]
        with Pool(a.procs) as pool:
            sol = sum(pool.map(work, [(n, ch, plist, c_mode, 1000 + i, False) for i, ch in enumerate(chunks) if ch]), [])
            nul = sum(pool.map(work, [(n, ch, plist, c_mode, 2000 + i, True) for i, ch in enumerate(null_chunks) if ch]), [])
        so = np.array([r[0] for r in sol]); nu = np.array([r[0] for r in nul])
        q = lambda v: [int(np.percentile(v, t)) for t in (50, 90, 99, 100)]
        top = sorted(sol, key=lambda r: -r[0])[:5]
        results[n] = dict(solutions=len(sol), null=len(nul), primes=plist, c_mode=c_mode,
                          sol_pct=q(so), null_pct=q(nu), sol_mean=float(so.mean()), null_mean=float(nu.mean()),
                          frac_sol_ge_n=float((so >= n).mean()), frac_null_ge_n=float((nu >= n).mean()),
                          top=[dict(overlap=int(r[0]), p=r[1], family=r[2], params=r[3],
                                    window=window_size(n, r[1], r[2], r[3]), line=r[4]) for r in top])
        print(f"n={n:2d} sols={len(sol):6d} null={len(nul):4d} primes={plist[0]}..{plist[-1]} | "
              f"max overlap: solutions p50/p90/p99/max = {q(so)}  null = {q(nu)} | "
              f"mean {so.mean():.2f} vs {nu.mean():.2f} | >=n: {(so>=n).mean():.4f} vs {(nu>=n).mean():.4f} | {time.time()-t0:.0f}s", flush=True)
        json.dump(results, open(a.out, 'w'), ensure_ascii=False, indent=1)
    print("готово", flush=True)

if __name__ == '__main__':
    main()
