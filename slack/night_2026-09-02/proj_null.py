"""Нуль-модели против настоящих решений: занятость диагоналей при n=20."""
import numpy as np, collections
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
IDX = {c: i for i, c in enumerate(ALPHA)}
n = 20
bodies = [l.strip()[1:] for l in open('/Users/iwasborninbali/saturation/web/all_known_solutions') if len(l.strip()) == 2*n+1]
lut = np.zeros(256, dtype=np.int16)
for c,i in IDX.items(): lut[ord(c)] = i
cols = lut[np.frombuffer(''.join(bodies).encode(), dtype=np.uint8).reshape(len(bodies), 2*n)].astype(np.int32)
rows = np.tile(np.repeat(np.arange(n, dtype=np.int32), 2), (len(bodies),1))

def occ_of(cols, rows, a=1, b=1):
    f = b*cols - a*rows; lo = f.min(); L = int(f.max()-lo+1); S = cols.shape[0]
    idx = (np.arange(S, dtype=np.int64)[:,None]*L + (f-lo)).ravel()
    return np.bincount(idx, minlength=S*L).reshape(S, L)

real = occ_of(cols, rows)
print(f"РЕАЛЬНЫЕ n=20, {len(bodies)} решений (полное перечисление, орбиты D4)")
print(f"  k2 (дважды занятых диагоналей): среднее {(real==2).sum(1).mean():.4f}  σ {(real==2).sum(1).std():.3f}"
      f"  k2/n = {(real==2).sum(1).mean()/n:.5f}")

# нуль-A: случайные 2-в-строке / 2-в-столбце (объединение двух непересекающихся перестановок)
rng = np.random.default_rng(20260902)
M = 200000
p1 = np.argsort(rng.random((M, n)), axis=1).astype(np.int32)
p2 = np.argsort(rng.random((M, n)), axis=1).astype(np.int32)
ok = (p1 != p2).all(axis=1)
p1, p2 = p1[ok], p2[ok]
ncols = np.empty((p1.shape[0], 2*n), dtype=np.int32)
ncols[:, 0::2] = p1; ncols[:, 1::2] = p2
nrows = np.tile(np.repeat(np.arange(n, dtype=np.int32), 2), (p1.shape[0],1))
nul = occ_of(ncols, nrows)
print(f"\nНУЛЬ-A: случайные 2/строку+2/столбец, {p1.shape[0]} шт (без запрета трёх на линии)")
print(f"  k2 среднее {(nul==2).sum(1).mean():.4f}   k2/n = {(nul==2).sum(1).mean()/n:.5f}")
print(f"  доля выборок, где какая-то диагональ несёт >=3 точек: {(nul.max(1)>=3).mean():.4f}")

# нуль-B: то же, но обусловленное <=2 на каждой диагонали (1,1)
sel = nul.max(1) <= 2
print(f"\nНУЛЬ-B: то же, обусловленное <=2 на диагоналях (1,1), {sel.sum()} шт")
print(f"  k2 среднее {(nul[sel]==2).sum(1).mean():.4f}   k2/n = {(nul[sel]==2).sum(1).mean()/n:.5f}")

# нуль-C: настоящие решения, но перемешанные столбцы (сохраняет 2/строку, ломает всё остальное)
print()
for a,b,name in [(1,1,'(1,1) диагональ'), (1,-1,'(1,-1) антидиагональ'), (1,2,'(1,2)'), (2,1,'(2,1)'), (1,3,'(1,3)'), (1,0,'(1,0) строки'), (0,1,'(0,1) столбцы')]:
    o = occ_of(cols, rows, a, b)
    print(f"  реальные, направление {name:>20}: k2 = {(o==2).sum(1).mean():8.3f}  k2/n = {(o==2).sum(1).mean()/n:7.4f}  слоёв {o.shape[1]:4d}  max занятость {o.max()}")
