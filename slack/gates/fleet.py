"""fleet.py — учёт вычислительных ресурсов и РАЗДЕЛЕНИЕ РАБОТЫ без пересечений.

Существует потому, что 2026-08-21 обнаружилось: мы месяц считали на 44 ядрах, имея квоту
на 1200, и не знали об этом — никто не смотрел. Ресурс, о котором не ведётся запись,
считается отсутствующим.

Второе назначение важнее первого: РАЗДЕЛЕНИЕ РАБОТЫ. Мы дважды за сутки устраивали себе
дублирование, раздав пересекающиеся списки. Здесь разбиение вычисляется по индексу машины,
и пересечься нельзя по построению: кусок i достаётся машине i mod N, других правил нет.
"""
import json, os, sys
from itertools import combinations

N, M, COLS = 7, 19, 49
SUBS = [s for k in range(4) for s in combinations(range(N), k)]

def my_nodes():
    """Мои узлы по разделению с первым солвером (его: s026, s027, s007_*)."""
    return [f"case_00000_s000_s{k:03d}" for k in (0, 4, 5, 6, 7, 28)]

def work_units():
    """Все дети моих узлов — плоский список, порядок ФИКСИРОВАН и воспроизводим."""
    return [(nd, j) for nd in my_nodes() for j in range(len(SUBS))]

def shard(machine_index: int, machine_count: int):
    """Доля машины. Пересечение невозможно: i-я берёт units[i::N]."""
    if not (0 <= machine_index < machine_count):
        raise ValueError(f"индекс {machine_index} вне диапазона 0..{machine_count-1}")
    return work_units()[machine_index::machine_count]

def verify_partition(machine_count: int):
    """ПРОВЕРКА, а не обещание: объединение долей равно целому, пересечения пусты."""
    all_u = work_units()
    seen, dup = set(), []
    for i in range(machine_count):
        for u in shard(i, machine_count):
            if u in seen: dup.append(u)
            seen.add(u)
    ok = (len(seen) == len(all_u)) and not dup
    return ok, len(all_u), len(seen), len(dup)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        for cnt in (1, 2, 5, 13, 37, 40):
            ok, tot, seen, dup = verify_partition(cnt)
            print(f"  машин {cnt:3d}: единиц {tot}, покрыто {seen}, дублей {dup} -> "
                  f"{'ЦЕЛО И БЕЗ ПЕРЕСЕЧЕНИЙ' if ok else 'ОШИБКА РАЗБИЕНИЯ'}")
    elif len(sys.argv) > 2:
        i, n = int(sys.argv[1]), int(sys.argv[2])
        for nd, j in shard(i, n):
            print(f"{nd} {j}")
    else:
        print(f"единиц работы всего: {len(work_units())}")
        print(f"мои узлы: {my_nodes()}")
