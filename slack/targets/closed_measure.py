"""closed_measure.py — МОНОТОННАЯ мера продвижения: доля пространства поиска, закрытая насовсем.

Все наши прежние меры мерили активность, а не продвижение, и потому могли расти: «не посчитано
детей» растёт при каждом дроблении, «фронт» вырос с 1239 до 17132, число закрытий растёт всегда.
Ни одна не говорит, приближаемся ли мы.

Здесь мера строится из самого разбиения. Дробление узла на 64 куска — ТОЧНОЕ разбиение его
пространства, поэтому каждому ребёнку принадлежит 1/64 массы родителя. Положим массу корня равной
единице; тогда узел глубины d несёт 64^(-d). Мера продвижения — суммарная масса ЗАКРЫТЫХ узлов.

Она монотонна по построению: закрытие никогда не отменяется, дробление не меняет массы (сумма
детей равна родителю), и достигает единицы ровно тогда, когда закрыт весь вопрос. Считать надо по
МАКСИМАЛЬНЫМ закрытым узлам, иначе масса удвоится: закрытый потомок уже учтён в закрытом предке.

    python3 closed_measure.py
"""
import glob
from collections import defaultdict

def norm(nm):
    """Нормализация имени: каждое звено _sN к трёхзначному виду.
    У сторон разная запись индексов — _s7 против _s007, — и один узел под двумя именами даёт
    родителю 128 детей вместо 64, после чего правило «закрыт при всех 64» не сработает НИКОГДА.
    Нормализуем при ЧТЕНИИ, чтобы старые файлы не пришлось переписывать."""
    import re as _re
    return _re.sub(r"_s(\d+)", lambda m: "_s%03d" % int(m.group(1)), nm)
from fractions import Fraction

BRANCH = 64
facts = set()
for p in glob.glob("logs/a280537/facts_*solver*.txt"):
    if "ОТОЗВАН" in p: continue
    for ln in open(p, errors="replace"):
        s = ln.strip()
        if not s or s.startswith("#"): continue
        nm = s.split()[0]
        facts.add(norm(nm[:-4] if nm.endswith(".cnf") else nm))

children = defaultdict(set)
for nm in facts:
    cur = nm
    while "_s" in cur:
        par = cur.rsplit("_s", 1)[0]
        children[par].add(cur)
        cur = par

memo = {}
def closed(nm):
    if nm in memo: return memo[nm]
    memo[nm] = False
    if nm in facts: memo[nm] = True; return True
    k = children.get(nm, set())
    r = len(k) == BRANCH and all(closed(x) for x in k)
    memo[nm] = r
    return r

def mass(nm):
    """масса узла: корень 1, каждый уровень делит на 64"""
    return Fraction(1, BRANCH ** (nm.count("_s") + 1))

total = Fraction(0)
def walk(nm):
    """спускаемся, суммируя массу МАКСИМАЛЬНЫХ закрытых узлов"""
    global total
    if closed(nm):
        total += mass(nm); return
    for ch in children.get(nm, ()):
        walk(ch)

for i in range(BRANCH):
    walk(f"case_{i:05d}")

f = float(total)
print(f"закрытая масса пространства поиска: {f:.12f}")
print(f"  то есть {100*f:.10f} %")
print(f"  осталось: {float(1-total):.3e} — это доля, а не число кусков")
print("МОНОТОННА по построению: дробление не меняет массы, закрытие не отменяется.")
