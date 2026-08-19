"""audit_coverage_indep.py — НЕЗАВИСИМАЯ пересборка вердикта о покрытии из сырых журналов.

Пишется намеренно с нуля и не импортирует ничего из check_split.py / check_hier.py: смысл в том,
чтобы два разных кода, читая одни и те же строки, пришли к одному выводу. Правило трёх статусов:
    UNSAT      — единственное, что закрывает кусок;
    SAT        — рушит всё заявление, где бы ни встретился;
    всё прочее — ОТСУТСТВИЕ СВЕДЕНИЙ: не закрывает и не опровергает.
Доразбитый кусок закрыт, только если ВСЕ его продолжения закрыты; ожидаемое их число вычисляется
независимо как число подмножеств размера <= 2 из n.

    python3 audit_coverage_indep.py n
"""
import os, re, sys
from itertools import combinations

n = int(sys.argv[1])
d = os.path.join("logs", "no3_3d", f"proof_n{n}")
per_col = len([s for k in range(3) for s in combinations(range(n), k)])
top_expected = per_col ** 2
sub_expected = per_col

status = {}          # имя куска -> множество увиденных статусов
subs = {}            # родитель -> {j: статусы}
lines_read = 0
for fn in sorted(os.listdir(d)):
    if not fn.endswith(".txt") or fn == "MANIFEST.txt":
        continue
    for ln in open(os.path.join(d, fn)):
        parts = ln.split()
        if not parts or not parts[0].startswith("case_"):
            continue
        lines_read += 1
        name, st = parts[0], (parts[1] if len(parts) > 1 else "")
        m = re.match(r"(case_\d+)_s(\d+)\.cnf$", name)
        if m:
            subs.setdefault(m.group(1), {}).setdefault(int(m.group(2)), set()).add(st)
        else:
            status.setdefault(name[:-4] if name.endswith(".cnf") else name, set()).add(st)

sat_anywhere = [k for k, v in status.items() if "SAT" in v] + \
               [f"{p}_s{j}" for p, dd in subs.items() for j, v in dd.items() if "SAT" in v]
closed_direct = {k for k, v in status.items() if "UNSAT" in v}
closed_via_sub, partial = set(), {}
for p, dd in subs.items():
    done = {j for j, v in dd.items() if "UNSAT" in v}
    if len(done) == sub_expected and set(done) == set(range(sub_expected)):
        closed_via_sub.add(p)
    else:
        partial[p] = sorted(set(range(sub_expected)) - done)
closed = closed_direct | closed_via_sub
expected_names = {f"case_{i:05d}" for i in range(top_expected)}
absent = sorted(expected_names - closed)
unknown = [(k, v) for k, v in status.items() if not (v & {"UNSAT", "SAT"})]
unknown_uncovered = [k for k, _ in unknown if k not in closed]

print(f"n={n}: строк журналов прочитано {lines_read}; ожидается кусков {per_col}^2 = {top_expected}, "
      f"продолжений на доразбитый кусок {sub_expected}")
print(f"  закрыто напрямую {len(closed_direct & expected_names)}, через продолжения {len(closed_via_sub)}, "
      f"всего {len(closed & expected_names)}")
print(f"  доразбитых кусков {len(subs)}, из них закрыты ПОЛНОСТЬЮ {len(closed_via_sub)}, частично {len(partial)}"
      f"  {list(partial.items())[:2]}")
print(f"  ВЫПОЛНИМЫХ строк: {len(sat_anywhere)}   не закрыто кусков: {len(absent)}  {absent[:5]}")
print(f"  строк «нет сведений»: {len(unknown)}, из них по НЕзакрытым кускам: {len(unknown_uncovered)}")
ok = not sat_anywhere and not absent and not partial
print("ВЕРДИКТ:", f"покрытие ПОЛНОЕ, все {top_expected} кусков невыполнимы" if ok else "ПОКРЫТИЕ НЕПОЛНОЕ")
