"""check_hier.py — агрегатор ДВУХУРОВНЕВОГО покрытия.

Тяжёлые куски разбиения доразбивались по следующему столбцу, поэтому кусок верхнего уровня закрыт,
если ЛИБО у него есть собственная строка UNSAT, ЛИБО присутствуют ВСЕ его продолжения и все они UNSAT.
Частичное продолжение НЕ закрывает кусок — это отдельный явный режим отказа.

Ожидаемое множество верхнего уровня строится НЕЗАВИСИМО от результатов: из манифеста разбиения.
Ожидаемое число продолжений задаётся арифметикой столбца (число подмножеств размера <= cap), а не
тем, сколько их нашлось в файлах.

usage: check_hier.py <manifest_dir> <n> <cap> <результаты...>
   имена продолжений имеют вид case_XXXXX_sYYY.cnf
"""
import sys, os, re
from math import comb
from collections import defaultdict

mdir, n, cap = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
files = sys.argv[4:]
expected = [l.strip() for l in open(os.path.join(mdir, "MANIFEST.txt")) if l.strip().endswith(".cnf")]
nsub = sum(comb(n, k) for k in range(cap+1))          # сколько продолжений обязано быть у куска

# ТРИ статуса, а не два (ловушка 6): UNSAT закрывает; SAT рушит всё; прочее — «не знаю»,
# оно не закрывает и не опровергает, но обязано быть показано.
top, sub, fatal, unknown, dup = {}, defaultdict(dict), [], [], []
for f in files:
    for line in open(f):
        p = line.split()
        if len(p) < 2 or not p[0].endswith(".cnf"): continue
        name, st = p[0], p[1]
        m = re.match(r'^(case_\d+)_s(\d+)\.cnf$', name)
        if st == "SAT":
            fatal.append((name, st)); continue
        if st != "UNSAT":
            unknown.append((name, st)); continue
        if m:
            base, j = m.group(1) + ".cnf", int(m.group(2))
            sub[base][j] = st
        else:
            top[name] = st

closed, partial, missing = set(top), [], []
for e in expected:
    if e in closed: continue
    d = sub.get(e, {})
    if len(d) == nsub: closed.add(e)
    elif d: partial.append((e, len(d), nsub))
    else: missing.append(e)

print(f"кусков верхнего уровня ожидалось {len(expected)}")
print(f"  закрыто напрямую {len(top)}, закрыто продолжениями {len(closed)-len(top)}, всего {len(closed)}")
print(f"  каждый доразбитый кусок обязан иметь {nsub} продолжений (подмножества размера <= {cap} из {n})")
print(f"  отсутствуют полностью: {len(missing)}" + (f"  например {missing[:3]}" if missing else ""))
print(f"  закрыты ЧАСТИЧНО: {len(partial)}" + (f"  например {partial[:3]}" if partial else ""))
unknown_uncovered = [(nm, st) for nm, st in unknown
                     if (re.match(r'^(case_\d+)_s\d+\.cnf$', nm).group(1)+".cnf" if "_s" in nm else nm) not in closed]
print(f"  ВЫПОЛНИМЫХ (SAT) строк: {len(fatal)}" + (f"  {fatal[:3]}" if fatal else "  — ни одной, это и требовалось"))
print(f"  строк «не знаю» (убит/таймаут): {len(unknown)}" + (f"  например {unknown[:3]}" if unknown else ""))
print(f"     из них относящихся к НЕзакрытым кускам: {len(unknown_uncovered)}"
      + ("  — все они перекрыты явным UNSAT из другого прогона" if unknown and not unknown_uncovered else ""))
ok = not missing and not partial and not fatal and not unknown_uncovered and len(closed) == len(expected)
print("\nВЕРДИКТ: " + ("покрытие ПОЛНОЕ, каждый кусок НЕВЫПОЛНИМ." if ok
      else "НЕЛЬЗЯ заявлять невыполнимость."))
sys.exit(0 if ok else 1)
