"""Спектр направлений + зависимость kappa от класса симметрии + n=35/40."""
import numpy as np, collections, math
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
lut = np.zeros(256, dtype=np.int16)
for i,c in enumerate(ALPHA): lut[ord(c)] = i
CLS = {'.':'iden', ':':'rot2', '/':'dia1', '-':'ort1', 'o':'rot4', 'c':'rct4', 'x':'dia2', '+':'ort2', '*':'full'}

data = collections.defaultdict(list)
for l in open('/Users/iwasborninbali/saturation/web/all_known_solutions'):
    l = l.strip()
    if not l: continue
    n = (len(l)-1)//2
    data[n].append((l[0], l[1:]))

def pts(n, entries):
    cols = lut[np.frombuffer(''.join(b for _,b in entries).encode(), dtype=np.uint8).reshape(len(entries), 2*n)].astype(np.int32)
    rows = np.tile(np.repeat(np.arange(n, dtype=np.int32), 2), (len(entries),1))
    return cols, rows

def kappa(n, entries, a=1, b=1):
    cols, rows = pts(n, entries)
    f = b*cols - a*rows; lo = f.min(); L = int(f.max()-lo+1); S = cols.shape[0]
    occ = np.bincount((np.arange(S, dtype=np.int64)[:,None]*L + (f-lo)).ravel(), minlength=S*L).reshape(S,L)
    k2 = (occ==2).sum(1)
    return k2.mean()/n, k2.std()/n/max(1,math.sqrt(S)), S, occ.max()

print("kappa = (#диагоналей x-y с ровно 2 точками)/n\n")
print("A. по классам симметрии при n=20 (полное перечисление):")
byc = collections.defaultdict(list)
for c,b in data[20]: byc[c].append((c,b))
for c, e in sorted(byc.items(), key=lambda kv:-len(kv[1])):
    k, se, S, mx = kappa(20, e)
    print(f"   {CLS[c]:>5} {S:7d} решений: kappa = {k:.5f} ± {se:.5f}")
k,se,S,_ = kappa(20, data[20]); print(f"   {'ВСЕ':>5} {S:7d} решений: kappa = {k:.5f} ± {se:.5f}")

print("\nB. n, где база НЕ полна (только симметричные решения):")
for n in (25, 30, 32, 35, 36, 39, 40, 44, 50, 56):
    if n in data:
        k,se,S,mx = kappa(n, data[n])
        cls = collections.Counter(CLS[c] for c,_ in data[n])
        print(f"   n={n:3d} {S:6d} решений {dict(cls)}: kappa = {k:.5f} ± {se:.5f}")

print("\nC. спектр направлений при n=20 (выборка 4000 решений): k2(a,b) по примитивным (a,b)")
ent = data[20][:4000]
cols, rows = pts(20, ent)
S = cols.shape[0]
spec = collections.Counter()
for i in range(S):
    x, y = cols[i], rows[i]
    dx = x[:,None]-x[None,:]; dy = y[:,None]-y[None,:]
    iu = np.triu_indices(40,1)
    dx, dy = dx[iu], dy[iu]
    g = np.gcd(np.abs(dx), np.abs(dy))
    ax, ay = dx//g, dy//g
    flip = (ax < 0) | ((ax == 0) & (ay < 0))
    ax = np.where(flip, -ax, ax); ay = np.where(flip, -ay, ay)
    for k in zip(ax.tolist(), ay.tolist()): spec[k] += 1
tot = sum(spec.values())
print(f"   сумма по всем направлениям = {tot/S:.1f} пар на решение (должно быть C(40,2)=780) — {'OK' if abs(tot/S-780)<1e-9 else 'РАСХОЖДЕНИЕ'}")
print(f"   различных примитивных направлений задействовано: {len(spec)}")
print("   топ-12 направлений (среднее число пар на решение):")
for d,c in spec.most_common(12):
    print(f"      {str(d):>10}: {c/S:8.3f}")
