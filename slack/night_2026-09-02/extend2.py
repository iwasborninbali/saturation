"""Достройка n -> n+2 без сдвига старых точек: 4 новые точки = пересечение 2 новых строк и 2 новых столбцов (края).
9 размещений. Проверяем на всей базе: доля успешных по n; любой успех при n>=40 печатаем целиком."""
import numpy as np, collections, sys
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
lut = np.zeros(256, dtype=np.int64)
for i,c in enumerate(ALPHA): lut[ord(c)] = i
CLS = {'.':'iden', ':':'rot2', '/':'dia1', '-':'ort1', 'o':'rot4', 'c':'rct4', 'x':'dia2', '+':'ort2', '*':'full'}
data = collections.defaultdict(list)
for l in open('/Users/iwasborninbali/saturation/web/all_known_solutions'):
    l = l.strip()
    if l: data[(len(l)-1)//2].append(l)

def alive_table(x, y, cells):
    """для каждой клетки: жива ли (нет пары старых точек на одной прямой с ней). x,y: (S,2n)"""
    out = {}
    for (cx, cy) in cells:
        dx, dy = x - cx, y - cy
        g = np.gcd(np.abs(dx), np.abs(dy)); dx //= g; dy //= g
        flip = (dx < 0) | ((dx == 0) & (dy < 0)); dx = np.where(flip, -dx, dx); dy = np.where(flip, -dy, dy)
        key = np.sort((dx + 200) * 401 + (dy + 200), axis=1)
        out[(cx, cy)] = ~(key[:, 1:] == key[:, :-1]).any(axis=1)
    return out

total_hits = collections.Counter(); total = collections.Counter(); hits_list = []
for n in sorted(data):
    L = data[n]; S = len(L)
    x = lut[np.frombuffer(''.join(l[1:] for l in L).encode(), dtype=np.uint8).reshape(S, 2*n)]
    y = np.tile(np.repeat(np.arange(n, dtype=np.int64), 2), (S, 1))
    opts = {'B': (n, n+1), 'T': (-2, -1), 'S': (-1, n)}
    cells = sorted({(cx, cy) for C in opts.values() for R in opts.values() for cx in C for cy in R})
    alive = alive_table(x, y, cells)
    ok_any = np.zeros(S, dtype=bool)
    for rn, R in opts.items():
        for cn, C in opts.items():
            ok = alive[(C[0], R[0])] & alive[(C[1], R[0])] & alive[(C[0], R[1])] & alive[(C[1], R[1])]
            # старые точки на двух «диагоналях» прямоугольника новых точек
            for (c1, r1, c2, r2) in ((C[0], R[0], C[1], R[1]), (C[1], R[0], C[0], R[1])):
                cross = (x - c1) * (r2 - r1) - (y - r1) * (c2 - c1)
                ok &= ~(cross == 0).any(axis=1)
            ok_any |= ok
            for i in np.nonzero(ok)[0]:
                if n >= 40: hits_list.append((n, CLS[L[i][0]], rn + cn, L[i]))
    total[n] = S; total_hits[n] = int(ok_any.sum())
print(f"{'n':>3} {'решений':>8} {'достраиваемых на +2':>20} {'доля':>10}")
for n in sorted(total):
    if total[n] >= 50 or n >= 40:
        print(f"{n:>3} {total[n]:>8} {total_hits[n]:>20} {total_hits[n]/total[n]:>10.2e}")
print(f"\nвсего: {sum(total_hits.values())} достраиваемых из {sum(total.values())}")
print("успехи при n>=40:", hits_list if hits_list else "нет")
