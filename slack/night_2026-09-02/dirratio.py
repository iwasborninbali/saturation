"""Спектр направлений на ВСЕХ 118057 решениях n=20 против ожидания для случайного 2n-подмножества."""
import numpy as np, collections, math
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
lut = np.zeros(256, dtype=np.int16)
for i,c in enumerate(ALPHA): lut[ord(c)] = i
n = 20
e = [l.strip()[1:] for l in open('/Users/iwasborninbali/saturation/web/all_known_solutions') if len(l.strip())==2*n+1]
cols = lut[np.frombuffer(''.join(e).encode(), dtype=np.uint8).reshape(len(e), 2*n)].astype(np.int32)
rows = np.tile(np.repeat(np.arange(n, dtype=np.int32), 2), (len(e),1))
S = len(e)
iu = np.triu_indices(2*n, 1)
W = 2*n+1; off = n
hist = np.zeros(W*W, dtype=np.int64)
for s in range(0, S, 2000):
    x, y = cols[s:s+2000], rows[s:s+2000]
    dx = (x[:,:,None]-x[:,None,:])[:, iu[0], iu[1]]
    dy = (y[:,:,None]-y[:,None,:])[:, iu[0], iu[1]]
    g = np.gcd(np.abs(dx), np.abs(dy))
    ax, ay = dx//g, dy//g
    flip = (ax < 0) | ((ax == 0) & (ay < 0))
    ax = np.where(flip, -ax, ax); ay = np.where(flip, -ay, ay)
    hist += np.bincount(((ax+off)*W + (ay+off)).ravel(), minlength=W*W)
assert hist.sum() == S*780
meas = {}
for k in np.nonzero(hist)[0]:
    a, b = divmod(int(k), W); meas[(a-off, b-off)] = hist[k]/S

def expected(a, b):
    N = n*n; tot = 0
    s = 1
    while n - s*abs(a) > 0 and n - s*abs(b) > 0:
        tot += (n - s*abs(a))*(n - s*abs(b)); s += 1
    return tot * (2*n)*(2*n-1)/(N*(N-1))

print(f"n=20, все {S} решений; направлений с ненулевым счётом: {len(meas)}")
print(f"{'(a,b)':>9} {'измерено':>9} {'ожид.случ.':>10} {'отношение':>9}")
for d in sorted(meas, key=lambda d: -meas[d])[:16]:
    ex = expected(*d)
    print(f"{str(d):>9} {meas[d]:9.3f} {ex:10.3f} {meas[d]/ex:9.4f}")
# отношение по «уровню» max(|a|,|b|)
print("\nсреднее отношение измерено/ожидание по уровню m=max(|a|,|b|):")
lv = collections.defaultdict(lambda: [0.0, 0.0])
for d, v in meas.items():
    m = max(abs(d[0]), abs(d[1])); lv[m][0] += v; lv[m][1] += expected(*d)
for m in sorted(lv)[:12]:
    print(f"   m={m:2d}: измерено {lv[m][0]:8.3f}  ожидание {lv[m][1]:8.3f}  отношение {lv[m][0]/lv[m][1]:.4f}")
# проверка: сумма ожиданий по всем примитивным направлениям = 780
tot_ex = sum(expected(a,b) for a in range(-(n-1), n) for b in range(-(n-1), n) if (a,b)!=(0,0) and math.gcd(abs(a),abs(b))==1 and (a>0 or (a==0 and b>0)))
print(f"\nконтроль: сумма ожиданий по всем примитивным направлениям = {tot_ex:.3f} (должно быть 780)")
