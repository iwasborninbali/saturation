"""check_split.py — агрегатор разбиения. Объявляет UNSAT только если КАЖДЫЙ кусок из манифеста
закрыт со статусом UNSAT. Любой пропуск, любой таймаут, любой нераспознанный код — вердикт «нельзя».
Строится независимо от того, что лежит в результатах: ожидаемое множество берётся из MANIFEST.txt.
usage: python3 check_split.py <outdir> <results.txt>
Формат строки результата: "<имя.cnf> <SAT|UNSAT|TIMEOUT|rc=N> [секунды]"
"""
import sys, os
d, res = sys.argv[1], sys.argv[2]
expected = [l.strip() for l in open(os.path.join(d, "MANIFEST.txt")) if l.strip().endswith(".cnf")]
seen = {}
for line in open(res):
    p = line.split()
    if len(p) >= 2: seen[p[0]] = p[1]
missing = [e for e in expected if e not in seen]
bad = {k: v for k, v in seen.items() if v not in ("UNSAT",)}
print(f"кусков ожидалось {len(expected)}, есть результатов {len(seen)}")
print(f"  отсутствуют: {len(missing)}" + (f"  например {missing[:3]}" if missing else ""))
print(f"  не-UNSAT: {len(bad)}" + (f"  {list(bad.items())[:3]}" if bad else ""))
if missing or bad:
    print("\nВЕРДИКТ: НЕЛЬЗЯ заявлять невыполнимость — покрытие неполное или есть выполнимые куски.")
    sys.exit(1)
print("\nВЕРДИКТ: все куски UNSAT — исходный экземпляр НЕВЫПОЛНИМ.")
