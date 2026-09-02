"""Достройки n -> n+2 углами: сертификация верификатором репо, класс симметрии, новизна против базы (с точностью до D4)."""
import sys, collections, numpy as np
sys.path.insert(0, '/Users/iwasborninbali/saturation'); sys.path.insert(0, '/Users/iwasborninbali/saturation/web')
import saturation as S
from decode import decode, ALPHA
from stab import classify, encode, images
IDX = {c:i for i,c in enumerate(ALPHA)}
db = collections.defaultdict(set)
for l in open('/Users/iwasborninbali/saturation/web/all_known_solutions'):
    l = l.strip()
    if l: db[(len(l)-1)//2].add(l)

def corner_extend(line):
    cls, n, book = decode(line)
    pts = {divmod(t, n) for t in book}                       # (row u, col v)
    m = n + 2
    new = {(u+1, v+1) for u, v in pts} | {(0,0), (0,m-1), (m-1,0), (m-1,m-1)}
    return m, frozenset(u*m + v for u, v in new)

def d4_encodings(book, m):
    pts = {divmod(t, m) for t in book}
    out = set()
    for f in images(m):
        img = frozenset(u*m + v for (u, v) in (f(a, b) for a, b in pts))
        out.add(encode(img, m)[1:])                              # без символа класса
    return out

# кандидаты: все решения, у которых 4 угла (n+2)-сетки живы и диагонали пусты — берём из extend2 логики заново, но только 'SS'
def extendable(line):
    cls, n, book = decode(line)
    m, ext = corner_extend(line)
    try:
        S.certify(ext, m)
        return m, ext
    except Exception:
        return None

per = collections.defaultdict(lambda: [0, 0, 0, 0])   # n+2 -> [кандидатов, сертифицировано, уже в базе, новых]
new_lines = []
for n in sorted(db):
    for line in db[n]:
        r = extendable(line)
        if r is None: continue
        m, ext = r
        per[m][0] += 1; per[m][1] += 1
        encs = d4_encodings(ext, m)
        present = any(e in {x[1:] for x in db.get(m, ())} for e in encs)
        if present: per[m][2] += 1
        else:
            per[m][3] += 1
            cl = classify(ext, m)
            new_lines.append((m, cl, encode(ext, m)))
print(f"{'n+2':>4} {'достроек':>9} {'сертиф.':>8} {'уже в базе':>11} {'НОВЫХ':>6}   (полнота базы для класса rot4/всех)")
full = {m: 'полная' if m <= 20 else ('rot4 полн.' if m in (22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56) else 'НЕПОЛНАЯ') for m in per}
for m in sorted(per):
    print(f"{m:>4} {per[m][0]:>9} {per[m][1]:>8} {per[m][2]:>11} {per[m][3]:>6}   {full[m]}")
print()
for m, cl, enc in new_lines:
    print(f"НОВОЕ n={m} класс={cl}: {enc}")
# контроль: в базе при n=58 сколько решений с четырьмя занятыми углами
for m in (56, 58):
    cnt = 0
    for l in db[m]:
        cls, n, book = decode(l); pts = {divmod(t, n) for t in book}
        if {(0,0),(0,n-1),(n-1,0),(n-1,n-1)} <= pts: cnt += 1
    print(f"контроль: в базе при n={m} решений с 4 занятыми углами: {cnt}")
