"""export_facts.py — выгрузка АТОМАРНЫХ ФАКТОВ из журналов: узлы с СОБСТВЕННЫМ UNSAT.

Факт — то, что измерено; покрытие — вывод из фактов. Обмениваться между машинами надо первым,
тогда каждая сторона пересчитывает вывод своим правилом, и расхождение поймает ошибку в ПРАВИЛЕ,
а не только в измерении. Складывать числа нельзя (пересечение удвоится), объединять имена можно:
объединение множеств идемпотентно.

Выгружаются ТОЛЬКО собственные UNSAT. Узлы, закрытые через все 64 продолжения, сюда не идут —
это уже вывод, и пусть его делает тот, кто читает.

    python3 export_facts.py out.txt журнал [журнал ...]
"""
import sys

out, logs = sys.argv[1], sys.argv[2:]
facts, sat, other = set(), [], 0
for path in logs:
    try:
        fh = open(path, errors="replace")
    except OSError:
        print(f"  пропущен (нет файла): {path}"); continue
    for ln in fh:
        t = ln.split()
        if not t or not t[0].startswith("case_"):
            continue
        name = t[0][:-4] if t[0].endswith(".cnf") else t[0]
        w = set(t)
        if "UNSAT" in w:
            facts.add(name)
        elif "SAT" in w or "ВЫПОЛНИМ" in ln:
            sat.append((name, path))
        else:
            other += 1
if sat:
    print("ОТКАЗ: найден ВЫПОЛНИМЫЙ кусок —", sat[:2]); sys.exit(9)
depth = {}
for n in facts:
    depth[n.count("_s")] = depth.get(n.count("_s"), 0) + 1
with open(out, "w") as f:
    f.write("# Атомарные факты первого солвера: узлы с СОБСТВЕННЫМ UNSAT (решатель Glucose).\n")
    f.write("# Одно имя в строке. Покрытие НЕ выводится здесь — пересчитывайте своим правилом:\n")
    f.write("#   узел закрыт, если он в объединении фактов ЛИБО если закрыты все 64 его потомка _sK.\n")
    f.write(f"# Всего {len(facts)}; по глубинам {dict(sorted(depth.items()))}.\n")
    for n in sorted(facts):
        f.write(n + "\n")
print(f"выгружено фактов: {len(facts)}, по глубинам {dict(sorted(depth.items()))}, "
      f"строк «нет сведений» пропущено {other} -> {out}")
