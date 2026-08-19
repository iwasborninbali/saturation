"""check_coverage.py — механическая проверка ПОЛНОТЫ покрытия перед любым заявлением об оптимальности.
Вход: файлы результатов (формат "m0 m1 :: OK <строка с MAX=…>" или "… :: FAIL …").
Проверяет: (1) присутствуют ВСЕ ожидаемые префиксы; (2) все со статусом OK; (3) нет дубликатов с разными
ответами; (4) считает глобальный максимум как максимум по кускам.
Ожидаемое множество префиксов строится независимо от того, что лежит в файлах.
usage: python3 check_coverage.py n expected_best file1 [file2 ...]"""
import sys, re
n=int(sys.argv[1]); claim=int(sys.argv[2]); files=sys.argv[3:]
masks=[m for m in range(1<<n) if bin(m).count('1')<=2]
expected={(a,b) for a in masks for b in masks}
seen={}; fails=[]; dups=[]
for f in files:
    for line in open(f):
        line=line.strip()
        if not line or line.startswith('#') or line=='ALLDONE': continue
        m=re.match(r'^(\d+)\s+(\d+)\s+::\s+(OK|FAIL)\s+(.*)$', line)
        if m:
            a,b,st,rest=int(m.group(1)),int(m.group(2)),m.group(3),m.group(4)
        else:
            # legacy wrapper: "m0 m1 :: <text>"; treated as OK only if it carries a completion marker
            m2=re.match(r'^(\d+)\s+(\d+)\s+::\s*(.*)$', line)
            if not m2: fails.append(('UNPARSED',line[:80])); continue
            a,b,rest=int(m2.group(1)),int(m2.group(2)),m2.group(3)
            st='OK' if 'MAX=' in rest else 'FAIL'
        if st!='OK': fails.append(((a,b),rest[:60])); continue
        mm=re.search(r'MAX=(\d+)',rest)
        if not mm: fails.append(((a,b),'no MAX in OK line')); continue
        v=int(mm.group(1))
        if (a,b) in seen and seen[(a,b)]!=v: dups.append(((a,b),seen[(a,b)],v))
        seen[(a,b)]=v
missing=sorted(expected-set(seen))
print(f"n={n}: ожидалось префиксов {len(expected)}, есть со статусом OK {len(seen)}")
print(f"  отсутствуют: {len(missing)}" + (f"  например {missing[:5]}" if missing else ""))
print(f"  неуспешных (FAIL/непарсибельных): {len(fails)}" + (f"  например {fails[:3]}" if fails else ""))
print(f"  дубликатов с расхождением: {len(dups)}" + (f"  {dups[:3]}" if dups else ""))
if seen:
    g=max(seen.values()); arg=[k for k,v in seen.items() if v==g][:3]
    print(f"  максимум по кускам = {g} (достигается на {arg})")
ok = not missing and not fails and not dups
if ok and seen:
    g=max(seen.values())
    print(f"\nВЕРДИКТ: покрытие ПОЛНОЕ. alpha([{n}]^3) = {g}." + ("" if g==claim else f"  ВНИМАНИЕ: заявлено {claim}, получено {g}!"))
else:
    print("\nВЕРДИКТ: покрытие НЕПОЛНОЕ — заявлять оптимальность НЕЛЬЗЯ.")
