"""test_false_alarms.py — испытание ворот на ЛОЖНОЕ СРАБАТЫВАНИЕ.

Мы весь день 2026-08-20 проверяли, ЛОВЯТ ли ворота плохое, и ни разу — не отвергают ли они
хорошее. Повод: мой детектор столкновений принял цепочку `bash -> timeout -> kissat` за две
конкурирующие задачи (все три несут один путь в командной строке), я остановил здоровый счёт
и отложил 1614 верных фактов. Два часа работы стоили ложной тревоги.

Правило, выведенное оттуда: направление ошибки задаётся тем, ЧТО ИНСТРУМЕНТ ИЩЕТ. Счётчик
результатов занижает; детектор тревоги — тревожит. Значит к детекторам нужна та же строгость.

Здесь каждым воротам подаётся ЗАВЕДОМО ХОРОШИЙ вход, и они обязаны ПРОПУСТИТЬ.
"""
import os, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gates as G

ok = fail = 0
def check(name, fn):
    global ok, fail
    try:
        fn(); print(f"  ПРОПУСТИЛ (верно): {name}"); ok += 1
    except G.Refusal as e:
        print(f"  ЛОЖНАЯ ТРЕВОГА: {name} -> {str(e)[:80]}"); fail += 1
    except Exception as e:
        print(f"  СЛОМАЛСЯ: {name} -> {type(e).__name__}: {str(e)[:60]}"); fail += 1

d = tempfile.mkdtemp()
good = os.path.join(d, "good.cnf")
open(good, "w").write("c ok\np cnf 4 3\n1 2 0\n-1 3 0\n4 0\n")

print("ворота на ЗАВЕДОМО ХОРОШЕМ входе — обязаны пропустить:\n")
check("gate_cnf_intact на целом CNF", lambda: G.gate_cnf_intact(good))
check("gate_disk при запросе 0.001 ГБ", lambda: G.gate_disk(d, 0.001))
check("gate_kill_pattern на безобидном шаблоне", lambda: G.gate_kill_pattern("zzz_nonexistent_pattern_9137"))
check("gate_three_valued: UNSAT закрывает", lambda: (_ for _ in ()).throw(AssertionError()) if G.gate_three_valued("UNSAT") != "CLOSED" else None)
check("gate_coverage при полном покрытии",
      lambda: G.gate_coverage(["a", "b"], {"a": "UNSAT", "b": "UNSAT"}))
check("gate_witness на верном свидетеле (n=2, 8 точек, нет трёх коллинеарных)",
      lambda: G.gate_witness([(x, y, z) for x in range(2) for y in range(2) for z in range(2)], 2, 8, "no3"))
check("gate_sibling_columns при однородном столбце",
      lambda: G.gate_sibling_columns({0, 1}, [{0, 1, 2}] * 5))
# gate_load ЧЕСТНО ИСПЫТАТЬ ЗДЕСЬ НЕЛЬЗЯ: машина сейчас нагружена, и отказ был бы ВЕРНЫМ,
# а не ложным. Проверять его с override бессмысленно — override отключает сами ворота,
# и такая «проверка» проверяет ничто. Отмечаем как НЕИСПЫТАННЫЕ, а не засчитываем.
print("  НЕ ИСПЫТАНО: gate_load — нужна незагруженная машина; с override проверка пуста")
check("gate_log_is_stale на свежем журнале",
      lambda: (open(os.path.join(d, "f.log"), "w").write("x"), G.gate_log_is_stale(os.path.join(d, "f.log")))[1])

print(f"\nИТОГ: пропущено {ok}, ЛОЖНЫХ ТРЕВОГ {fail}, не испытано 1 (gate_load)")
sys.exit(1 if fail else 0)
