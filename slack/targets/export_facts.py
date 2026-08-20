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

# ОТОБРАЖЕНИЕ ИСПОРЧЕННЫХ СТЕБЛЕЙ. Если базовый файл ветки был скопирован под другим именем,
# все её потомки получают чужой стебель и с деревом не связываются — покрытие занижается молча.
# Отображение допустимо ТОЛЬКО после побайтовой сверки базы с настоящим узлом; здесь она сделана
# (cmp показал равенство), и потому подстановка законна, а не удобна.
REMAP = {"node_s006_s000": "case_00000_s006_s000"}

out, logs = sys.argv[1], sys.argv[2:]
facts, sat, other = set(), [], 0
by_src = {}
for path in logs:
    try:
        fh = open(path, errors="replace")
    except OSError:
        print(f"  пропущен (нет файла): {path}"); continue
    for ln in fh:
        t = ln.split()
        # Формат solve_or_split: «ЗАКРЫТ <узел>» — прямое закрытие, атомарный факт.
        # «ЗАКРЫТ ЧЕРЕЗ ПРОДОЛЖЕНИЯ <узел>» — ВЫВОД из фактов о потомках, а не измерение:
        # в файл фактов он идти НЕ должен, иначе читающий получит вывод под видом наблюдения.
        if t and t[0] == "ЗАКРЫТ":
            if len(t) == 2 and t[1].startswith("case_"):
                t = [t[1], "UNSAT"]
            else:
                continue
        if t and t[0] in ("ВЫПОЛНИМ", "ПРЕДЕЛ", "ДРОБЛЮ", "НЕ", "ОТКАЗ"):
            if t[0] == "ВЫПОЛНИМ" and len(t) > 1:
                sat.append((t[1], path))
            continue
        if not t or not t[0].startswith("case_"):
            continue
        name = t[0][:-4] if t[0].endswith(".cnf") else t[0]
        for _bad, _good in REMAP.items():
            if name.startswith(_bad):
                name = _good + name[len(_bad):]
                break
        w = set(t)
        if "UNSAT" in w:
            facts.add(name); by_src.setdefault(path.split("/")[-1], set()).add(name)
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
    f.write("# Атомарные факты первого солвера: узлы с СОБСТВЕННЫМ UNSAT.\n")
    f.write("# ВАЖНО: решатель указан ПО ИСТОЧНИКУ, а не общей строкой — часть узлов закрыта\n")
    f.write("#   Glucose (неродственная линия), часть kissat. Смешивать в одну подпись нельзя:\n")
    f.write("#   утверждение «подтверждено вторым решателем» верно не для всех строк.\n")
    for src_path, names in sorted(by_src.items()):
        f.write(f"#   {src_path}: {len(names)}\n")
    f.write("# Одно имя в строке. Покрытие НЕ выводится здесь — пересчитывайте своим правилом:\n")
    f.write("#   узел закрыт, если он в объединении фактов ЛИБО если закрыты все 64 его потомка _sK.\n")
    f.write(f"# Всего {len(facts)}; по глубинам {dict(sorted(depth.items()))}.\n")
    for n in sorted(facts):
        f.write(n + "\n")
print(f"выгружено фактов: {len(facts)}, по глубинам {dict(sorted(depth.items()))}, "
      f"строк «нет сведений» пропущено {other} -> {out}")
