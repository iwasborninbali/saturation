#!/usr/bin/env python3
"""Точное множество решёточных плоскостей куба [n]^3, содержащих >= 4 клеток. Перебор троек клеток (numpy, по i), нормаль —
векторное произведение, примитивная, знак канонический (первая ненулевая компонента > 0); (a,b,c,d) пакуется в int64;
плоскость с c клетками встречается C(c,3) раз, оставляем кратность >= 4 (<=> c >= 4). Коллинеарные тройки пропускаются
(это прямые, они ограничены отдельно). usage: planes_exact.py n [out.json]"""
import sys, json, time, numpy as np
n = int(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else f"planes_n{n}.json"
t0 = time.time()
cells = np.array([(x, y, z) for x in range(n) for y in range(n) for z in range(n)], dtype=np.int64)
N = len(cells); B = 2 * (n - 1) ** 2 + 1; W = 2 * B + 1; DB = 3 * B * (n - 1) + 1
packed = []
for i in range(N - 2):
    p = cells[i]; rest = cells[i + 1:]
    jj, kk = np.triu_indices(len(rest), k=1)
    nm = np.cross(rest[jj] - p, rest[kk] - p)
    nm = nm[np.any(nm != 0, axis=1)]
    g = np.gcd(np.gcd(np.abs(nm[:, 0]), np.abs(nm[:, 1])), np.abs(nm[:, 2])); nm //= g[:, None]
    s = np.sign(nm[:, 0]); z = s == 0; s[z] = np.sign(nm[z, 1]); z = s == 0; s[z] = np.sign(nm[z, 2]); nm *= s[:, None]
    d = nm @ p
    packed.append(((nm[:, 0] + B) * W + (nm[:, 1] + B)) * W * DB + (nm[:, 2] + B) * DB + (d + DB // 2))
packed = np.concatenate(packed)
vals, cnt = np.unique(packed, return_counts=True)
keep = vals[cnt >= 4]
dd = keep % DB - DB // 2; r = keep // DB; c = r % W - B; r //= W; b = r % W - B; a = r // W - B
planes = np.stack([a, b, c, dd], axis=1)
assert np.all(np.gcd(np.gcd(np.abs(a), np.abs(b)), np.abs(c)) == 1)
json.dump(planes.tolist(), open(out, "w"))
print(f"n={n}: троек {len(packed)}, плоскостей с >=3 клетками {len(vals)}, с >=4 клетками {len(keep)}, "
      f"max|компонента нормали| {int(np.abs(planes[:, :3]).max())}, {time.time()-t0:.1f}s -> {out}", flush=True)
