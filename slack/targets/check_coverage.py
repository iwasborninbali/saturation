"""check_coverage.py — механическая проверка ПОЛНОТЫ покрытия перед любым заявлением об оптимальности.

Вход: файлы результатов. Две формы строки, обе допустимы и могут смешиваться:
    "m0 m1 :: OK <… MAX=v …>"          — префикс = содержимое первых ДВУХ z-столбцов
    "m0 m1 m2 :: OK <… MAX=v …>"       — префикс удлинён третьим z-столбцом (разбиение тяжёлых кусков)

Проверяет: (1) присутствуют ВСЕ ожидаемые пары (m0,m1); (2) пара закрыта либо своей собственной OK-строкой,
либо ПОЛНЫМ набором всех 16 продолжений (m0,m1,m2) — частичное продолжение НЕ закрывает пару;
(3) все со статусом OK; (4) нет дубликатов с расхождением; (5) максимум = максимум по кускам.

Ожидаемое множество строится независимо от содержимого файлов: в каждом z-столбце не более двух точек,
поэтому подмножества размера ≤ 2 исчерпывают столбец, а их произведение — пространство префиксов.

usage: python3 check_coverage.py n expected_best file1 [file2 ...]"""
import sys, re
n=int(sys.argv[1]); claim=int(sys.argv[2]); files=sys.argv[3:]
masks=[m for m in range(1<<n) if bin(m).count('1')<=2]
MSET=set(masks)
expected={(a,b) for a in masks for b in masks}
seen2={}; seen3={}; fails=[]; dups=[]
def note(key,v,store):
    if key in store and store[key]!=v: dups.append((key,store[key],v))
    store[key]=v
for f in files:
    for line in open(f):
        line=line.strip()
        if not line or line.startswith('#') or line=='ALLDONE': continue
        m=re.match(r'^(\d+)\s+(\d+)(?:\s+(\d+))?\s+::\s+(OK|FAIL)\s+(.*)$', line)
        if m:
            a,b,c,st,rest=int(m.group(1)),int(m.group(2)),m.group(3),m.group(4),m.group(5)
        else:
            # legacy wrapper: "m0 m1 [m2] :: <text>" — считается OK только если несёт маркер завершения
            m2=re.match(r'^(\d+)\s+(\d+)(?:\s+(\d+))?\s+::\s*(.*)$', line)
            if not m2: fails.append(('UNPARSED',line[:80])); continue
            a,b,c,rest=int(m2.group(1)),int(m2.group(2)),m2.group(3),m2.group(4)
            st='OK' if 'MAX=' in rest else 'FAIL'
        key=(a,b) if c is None else (a,b,int(c))
        if st!='OK': fails.append((key,rest[:60])); continue
        mm=re.search(r'MAX=(\d+)',rest)
        if not mm: fails.append((key,'no MAX in OK line')); continue
        v=int(mm.group(1))
        if c is None: note((a,b),v,seen2)
        else:
            if int(c) not in MSET: fails.append((key,'третья маска недопустима (popcount>2)')); continue
            note((a,b,int(c)),v,seen3)
# пара закрыта продолжениями только если присутствуют ВСЕ 16 (частичное продолжение не закрывает)
from collections import defaultdict
kids=defaultdict(dict)
for (a,b,c),v in seen3.items(): kids[(a,b)][c]=v
closed=dict(seen2); partial=[]
for pair,d in kids.items():
    if len(d)==len(masks): closed.setdefault(pair, max(d.values()))
    elif pair not in seen2: partial.append((pair,len(d),len(masks)))
missing=sorted(expected-set(closed))
print(f"n={n}: ожидалось пар префиксов {len(expected)}; закрыто {len(closed)}"
      f"  (напрямую {len(seen2)}, через третью маску {len(closed)-len(seen2)}; всего строк-продолжений {len(seen3)})")
print(f"  отсутствуют полностью: {len(missing)}" + (f"  например {missing[:5]}" if missing else ""))
print(f"  закрыты ЧАСТИЧНО (есть продолжения, но не все 16): {len(partial)}" + (f"  например {partial[:3]}" if partial else ""))
print(f"  неуспешных (FAIL/непарсибельных): {len(fails)}" + (f"  например {fails[:3]}" if fails else ""))
print(f"  дубликатов с расхождением: {len(dups)}" + (f"  {dups[:3]}" if dups else ""))
if closed:
    g=max(closed.values()); arg=[k for k,v in closed.items() if v==g][:3]
    print(f"  максимум по кускам = {g} (достигается на {arg})")
ok = not missing and not partial and not fails and not dups
if ok and closed:
    g=max(closed.values())
    print(f"\nВЕРДИКТ: покрытие ПОЛНОЕ. alpha([{n}]^3) = {g}." + ("" if g==claim else f"  ВНИМАНИЕ: заявлено {claim}, получено {g}!"))
else:
    print("\nВЕРДИКТ: покрытие НЕПОЛНОЕ — заявлять оптимальность НЕЛЬЗЯ.")
