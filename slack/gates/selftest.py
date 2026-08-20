"""Самопроверка ворот: каждое обязано ОТКАЗАТЬ на своём случае и пропустить корректный."""
import sys, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gates import *

ok = fail = 0
def case(name, fn, must_refuse):
    global ok, fail
    try:
        fn(); refused = False
    except Refusal:
        refused = True
    good = (refused == must_refuse)
    print(f"  [{'ok ' if good else 'ПРОВАЛ'}] {name}: {'отказано' if refused else 'пропущено'}"
          f" (ожидалось {'отказ' if must_refuse else 'пропуск'})")
    ok, fail = ok + good, fail + (not good)

print("ворота на утверждения:")
case("покрытие полное",           lambda: gate_coverage(["a","b"], {"a":"UNSAT","b":"UNSAT"}), False)
case("кусок пропущен",            lambda: gate_coverage(["a","b"], {"a":"UNSAT"}), True)
case("кусок убит (rc=137)",       lambda: gate_coverage(["a","b"], {"a":"UNSAT","b":"rc=137"}), True)
case("кусок по таймауту",         lambda: gate_coverage(["a","b"], {"a":"UNSAT","b":"TIMEOUT"}), True)
case("есть выполнимый",           lambda: gate_coverage(["a","b"], {"a":"UNSAT","b":"SAT"}), True)
good3 = [(0,0,0),(0,0,1),(0,1,0),(1,0,0),(1,1,1)]
case("свидетель верный",          lambda: gate_witness(good3, 2, 5, "no4"), False)
case("свидетель пустой",          lambda: gate_witness([], 2, 0, "no4"), True)
case("свидетель не того размера", lambda: gate_witness(good3, 2, 8, "no4"), True)
case("свидетель с повтором",      lambda: gate_witness(good3+[(0,0,0)], 2, 6, "no4"), True)
case("точка вне куба",            lambda: gate_witness([(0,0,0),(0,0,1),(0,1,0),(9,9,9)], 2, 4, "no4"), True)
case("коллинеарная тройка",       lambda: gate_witness([(0,0,0),(1,0,0),(2,0,0)], 3, 3, "no3"), True)
case("закономерность по 3 точкам",lambda: gate_pattern({2:8,3:16,4:28}, lambda n: 2*n*n-2*n+4), True)
case("формула расходится",        lambda: gate_pattern({2:8,3:16,4:28,5:40,6:64,7:88}, lambda n: 2*n*n-2*n+4), True)

print("толкование сужений (не отказ, а переименование вердикта):")
for k,a,v,exp in (("profile",3,"UNSAT","UNSAT_ONLY_FOR_SYMMETRIC_PROFILES"),
                  ("profile",1,"UNSAT","UNSAT"),
                  ("invariant",1,"UNSAT","UNSAT_ONLY_WITHIN_THE_SYMMETRIC_STRATUM")):
    got = gate_restriction(k,a,v); good = got==exp
    print(f"  [{'ok ' if good else 'ПРОВАЛ'}] {k}, осей {a}: {got}")
    ok, fail = ok+good, fail+(not good)

print("ворота на запуски:")
with tempfile.TemporaryDirectory() as d:
    open(os.path.join(d,"case_0.cnf"),"w").write("p cnf 1 1\n1 0\n")
    case("файлов ровно сколько просили", lambda: gate_generated(d,"case_",1), False)
    case("файлов меньше",                lambda: gate_generated(d,"case_",2), True)
    case("журнал внутри дерева git",     lambda: gate_log_location(os.path.join(d,"log.txt"), d), True)
    case("журнал вне дерева",            lambda: gate_log_location("/tmp/log.txt", d), False)
case("диска мало",                   lambda: gate_disk("/tmp", 10**6), True)
case("диска хватает",                lambda: gate_disk("/tmp", 0.001), False)
case("долгий прогон на переднем плане", lambda: gate_background("kissat big.cnf", 3600), True)
case("долгий прогон в фоне",            lambda: gate_background("nohup kissat big.cnf &", 3600), False)

print(f"\nИТОГ: пройдено {ok}, провалено {fail}")
sys.exit(0 if fail==0 else 1)
