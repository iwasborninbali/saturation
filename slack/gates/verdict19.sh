#!/bin/bash
# verdict19.sh — ЕДИНСТВЕННЫЙ источник вердикта по решающему вопросу A280537 n=7 M=19.
#
# Существует потому, что монитор объявил «закрыто 584» при 448 кусках: он сложил счётчики двух
# машин, работавших по одному списку с разных концов. Здесь считаются УНИКАЛЬНЫЕ закрытые куски
# и сверяются с манифестом; «убит» и «таймаут» не закрывают ничего.
#
# Уровни: 448 кусков четвёртого уровня; тяжёлые из них дробятся на 64 подкуска каждый,
# и такой кусок закрыт ТОЛЬКО когда закрыты все 64.
set -u
R="$(cd "$(dirname "$0")/../.." && pwd)"; W=/tmp/verdict19; mkdir -p $W
gc () { timeout 90 gcloud compute scp "$1:$2" "$3" --zone="$4" --project="$5" 2>/dev/null; }
gc saturation-solver-2 /tmp/r4_19.txt  $W/l4_a.txt us-central1-b loyobondar-prod
gc saturation-solver-3 /tmp/rs4b.txt   $W/l4_b.txt us-west1-b   eg-multi-domain
gc saturation-solver-2 /tmp/ss_a.txt   $W/l5_a1.txt us-central1-b loyobondar-prod
gc saturation-solver-2 /tmp/ss_a2.txt  $W/l5_a2.txt us-central1-b loyobondar-prod
gc saturation-solver-3 /tmp/ss_b.txt   $W/l5_b.txt us-west1-b   eg-multi-domain
python3 - "$W" <<'PY'
import sys, os, glob
from collections import defaultdict
W = sys.argv[1]
SUBS = 64                                   # подмножеств размера <=3 из 7
lvl4 = set()
for f in glob.glob(os.path.join(W, "l4_*.txt")):
    for l in open(f):
        p = l.split()
        if len(p) >= 2 and p[0].endswith(".cnf") and p[1] == "UNSAT": lvl4.add(p[0])
lvl5 = defaultdict(set); sat = []
for f in glob.glob(os.path.join(W, "l5_*.txt")):
    for l in open(f):
        p = l.split()
        if len(p) >= 3 and p[0].endswith(".cnf"):
            if p[2] == "UNSAT": lvl5[p[0]].add(p[1])
            elif p[2] == "SAT": sat.append((p[0], p[1]))
by5 = {b for b, s in lvl5.items() if len(s) == SUBS}
closed = lvl4 | by5
partial = {b: len(s) for b, s in lvl5.items() if len(s) < SUBS and b not in lvl4}
print(f"кусков четвёртого уровня всего: 448")
print(f"  закрыто напрямую:            {len(lvl4)}")
print(f"  закрыто через все {SUBS} подкуска: {len(by5)}")
print(f"  ЗАКРЫТО УНИКАЛЬНЫХ:          {len(closed)}")
print(f"  дробится, но не закончено:   {len(partial)}" + (f"  например {list(partial.items())[:2]}" if partial else ""))
print(f"  ВЫПОЛНИМЫХ:                  {len(sat)}" + (f"  {sat[:2]}" if sat else "  — ни одного"))
if sat:
    print("\nВЕРДИКТ: НАЙДЕН ВЫПОЛНИМЫЙ КУСОК — 19 точек СУЩЕСТВУЮТ, утверждение a(7)<=18 ЛОЖНО"); sys.exit(2)
if len(closed) < 448:
    print(f"\nВЕРДИКТ: НЕЛЬЗЯ заявлять — не закрыто {448-len(closed)} кусков"); sys.exit(1)
print("\nВЕРДИКТ: все 448 кусков невыполнимы => a(7) <= 18")
PY
