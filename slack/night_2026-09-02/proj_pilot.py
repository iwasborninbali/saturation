"""Пилот: проекция 2n-точечных решений на диагональ. Данные: web/all_known_solutions."""
import numpy as np, collections, math, sys

ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
IDX = {c: i for i, c in enumerate(ALPHA)}

by_n = collections.defaultdict(list)
for line in open('/Users/iwasborninbali/saturation/web/all_known_solutions'):
    line = line.strip()
    if not line: continue
    body = line[1:]
    by_n[len(body)//2].append(body)

print("n : #решений в базе (полное перечисление до n=20)")
for n in sorted(by_n): 
    if n <= 21: print(f"  {n:2d} : {len(by_n[n])}")

def cols_of(n):
    a = np.frombuffer(''.join(by_n[n]).encode(), dtype=np.uint8).reshape(len(by_n[n]), 2*n)
    lut = np.zeros(256, dtype=np.int16); 
    for c,i in IDX.items(): lut[ord(c)] = i
    return lut[a].astype(np.int32)

def fiber_stats(n, dirvec):
    """занятость слоёв проекции вдоль направления dirvec=(a,b): слой = b*x - a*y"""
    a, b = dirvec
    cols = cols_of(n)                     # x
    S = cols.shape[0]
    rows = np.tile(np.repeat(np.arange(n, dtype=np.int32), 2), (S,1))   # y
    f = b*cols - a*rows
    lo = f.min(); L = int(f.max() - lo + 1)
    idx = (np.arange(S, dtype=np.int64)[:,None]*L + (f - lo)).ravel()
    occ = np.bincount(idx, minlength=S*L).reshape(S, L)
    return occ

out = {}
for n in range(6, 21):
    occ = fiber_stats(n, (1,1))          # слои x-y = const, проекция на антидиагональ
    assert occ.max() <= 2, "нашлись 3 на линии — данные битые"
    k2 = (occ == 2).sum(1)               # число дважды занятых диагоналей
    occupied = (occ > 0).sum(1)
    L = occ.shape[1]
    # длины пропусков между занятыми слоями
    pos = np.argwhere(occ > 0)
    same = pos[1:,0] == pos[:-1,0]
    gaps = (pos[1:,1] - pos[:-1,1])[same]
    span = np.zeros(occ.shape[0])
    first = np.argmax(occ > 0, axis=1)
    last  = L - 1 - np.argmax((occ > 0)[:, ::-1], axis=1)
    span = last - first
    out[n] = dict(S=occ.shape[0], k2=k2.mean(), k2n=k2.mean()/n, occ=occupied.mean(),
                  meangap=(span/(occupied-1)).mean(), gaps=np.bincount(gaps, minlength=8)[:8]/len(gaps),
                  edge=(occupied.mean()/L))
print()
print("направление (1,1) — слои x−y (диагонали). k2 = #диагоналей с ровно 2 точками")
print(f"{'n':>3} {'#реш':>7} {'k2':>7} {'k2/n':>7} {'занято':>7} {'ср.зазор(клеток)':>16}  доля зазоров g=1,2,3,4,5")
for n,v in out.items():
    g = " ".join(f"{x:.3f}" for x in v['gaps'][1:6])
    print(f"{n:>3} {v['S']:>7} {v['k2']:>7.3f} {v['k2n']:>7.4f} {v['occ']:>7.2f} {v['meangap']:>16.4f}  {g}")
