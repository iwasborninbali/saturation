#!/bin/bash
# verdict19.sh — ЕДИНСТВЕННЫЙ источник вердикта по решающему вопросу A280537 n=7 M=19.
#
# Существует потому, что монитор объявил «закрыто 584» при 448 кусках: он сложил счётчики двух
# машин, работавших по одному списку с разных концов. Здесь считаются УНИКАЛЬНЫЕ закрытые куски
# и сверяются с манифестом; «убит» и «таймаут» не закрывают ничего.
#
# 2026-08-20, ВТОРАЯ ошибка того же рода и хуже первой: имена файлов результатов были ЗАШИТЫ
# (/tmp/ss_a.txt, /tmp/ss_a2.txt, /tmp/ss_b.txt), а живой счёт писал в /tmp/need_a_res.txt и
# /tmp/need_b_res.txt. Три часа инструмент показывал «402, движения нет», пока 45 решателей
# работали и писали в файлы, которых он не читал. Занижение было СИСТЕМАТИЧЕСКИМ и в одну
# сторону — и заметить его по выходу инструмента было нельзя: «нет движения» и «я не смотрю
# туда, куда пишут» выглядят одинаково.
# Поэтому теперь файлы результатов НАХОДЯТСЯ ПО ОБРАЗЦУ на самой машине, а не перечисляются здесь.
#
#   usage: verdict19.sh [--list]
set -u
R="$(cd "$(dirname "$0")/../.." && pwd)"; W=/tmp/verdict19; mkdir -p $W; rm -f $W/host_*.txt

# Забираем ВСЁ, что похоже на файл результатов, и печатаем имя каждого — чтобы «инструмент
# смотрит не туда» было видно в выводе, а не только в последствиях.
pull () { # host zone project tag
  timeout 120 gcloud compute ssh "$1" --zone="$2" --project="$3" --command='
    for f in /tmp/r4_19.txt /tmp/rs4b.txt /tmp/ss*.txt /tmp/need*_res.txt; do
      [ -f "$f" ] || continue
      echo "#SRC $f $(wc -l < "$f") $(date -r "$f" +%H:%M)"
      cat "$f"
    done' 2>/dev/null > "$W/host_$4.txt"
  if [ ! -s "$W/host_$4.txt" ]; then
    echo "  ВНИМАНИЕ: с $1 не получено НИЧЕГО — молчание машины НЕ означает отсутствия работы"
  fi
}
pull saturation-solver-2 us-central1-b loyobondar-prod a
pull saturation-solver-3 us-west1-b   eg-multi-domain  b

python3 - "$W" "${1:-}" <<'PY'
import sys, os, glob
from collections import defaultdict
W = sys.argv[1]
LIST = len(sys.argv) > 2 and sys.argv[2] == "--list"
SUBS = 64                                   # подмножеств размера <=3 из 7
TOTAL = 448

lvl4, sat = set(), []
lvl5 = defaultdict(set)
noinfo4 = set()
print("  источники, с которых читано:")
for f in sorted(glob.glob(os.path.join(W, "host_*.txt"))):
    host = os.path.basename(f)[5:-4]
    for l in open(f):
        p = l.split()
        if not p: continue
        if p[0] == "#SRC":
            print(f"    {host}: {p[1]}  строк {p[2]}, изменён {p[3]}")
            continue
        if not p[0].endswith(".cnf"): continue
        # Различаем уровень ПО ФОРМЕ строки, а не по имени файла: имя файла уже подвело.
        if len(p) >= 3 and p[1].startswith("s") and p[1][1:].isdigit():
            if   p[2] == "UNSAT": lvl5[p[0]].add(p[1])
            elif p[2] == "SAT":   sat.append((p[0], p[1]))
        elif len(p) >= 2:
            if   p[1] == "UNSAT": lvl4.add(p[0])
            elif p[1] == "SAT":   sat.append((p[0], "-"))
            else:                 noinfo4.add(p[0])

by5     = {b for b, s in lvl5.items() if len(s) == SUBS}
closed  = lvl4 | by5
partial = {b: len(s) for b, s in lvl5.items() if len(s) < SUBS and b not in lvl4}

print(f"\n  кусков четвёртого уровня всего: {TOTAL}")
print(f"  закрыто напрямую:            {len(lvl4)}")
print(f"  закрыто через все {SUBS} подкуска: {len(by5)}")
print(f"  ЗАКРЫТО УНИКАЛЬНЫХ:          {len(closed)}")
print(f"  не закрыто (убит/таймаут):   {len(noinfo4 - closed)}")
print(f"  дробится, но не закончено:   {len(partial)}" +
      (f"  {sorted(partial.items())[:3]}" if partial else ""))
print(f"  ВЫПОЛНИМЫХ:                  {len(sat)}" + (f"  {sat[:2]}" if sat else "  — ни одного"))

if LIST:
    # Список выдаётся ТЕМ ЖЕ инструментом, что и вердикт: отдельный разошёлся бы с ним ровно
    # тогда, когда это опаснее всего — при сверке с чужой машиной.
    out = os.path.join(W, "closed.txt")
    with open(out, "w") as fh:
        for nm in sorted(closed): fh.write(nm + "\n")
    print(f"\n  список закрытых записан: {out}  ({len(closed)} имён)")
    op = os.path.join(W, "open.txt")
    with open(op, "w") as fh:
        for nm in sorted(noinfo4 - closed): fh.write(nm + "\n")
    print(f"  список НЕзакрытых:       {op}  ({len(noinfo4 - closed)} имён)")
    if partial:
        po = os.path.join(W, "partial.txt")
        with open(po, "w") as fh:
            for b, k in sorted(partial.items()): fh.write(f"{b} {k}/{SUBS}\n")
        print(f"  список недодробленных:   {po}  ({len(partial)} имён)")

if sat:
    print("\nВЕРДИКТ: НАЙДЕН ВЫПОЛНИМЫЙ КУСОК — 19 точек СУЩЕСТВУЮТ, утверждение a(7)<=18 ЛОЖНО"); sys.exit(2)
if len(closed) < TOTAL:
    print(f"\nВЕРДИКТ: НЕЛЬЗЯ заявлять — не закрыто {TOTAL-len(closed)} кусков"); sys.exit(1)
print(f"\nВЕРДИКТ: все {TOTAL} кусков невыполнимы => a(7) <= 18")
PY
