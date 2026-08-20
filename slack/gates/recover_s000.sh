#!/bin/bash
# recover_s000.sh — забрать результаты ветки s000 с ВМ-2 после потери доступа.
#
# Предупреждение первого солвера, принятое буквально: забирать ПО ЖУРНАЛАМ, а не по счётчикам.
# Машина считала вслепую пять часов; всякий счётчик, который она печатала, мы не видели, а
# журналы писались. Поэтому здесь нет ни одного числа, взятого со слов машины: только строки.
#
#   recover_s000.sh          — забрать и показать, ничего не меняя
#   recover_s000.sh --apply  — дописать добытые факты в facts_second_solver.txt
set -u
R="$(cd "$(dirname "$0")/../.." && pwd)"; W=/tmp/recover_s000; mkdir -p $W
H=saturation-solver-2; Z=us-central1-b; PR=loyobondar-prod

echo "== забираю журналы (не счётчики)"
timeout 180 gcloud compute ssh "$H" --zone="$Z" --project="$PR" \
  --command='for f in /tmp/s000_split_res.txt /tmp/s000_res.txt /tmp/s000_split.log; do
               [ -f "$f" ] && { echo "#SRC $f $(wc -l < "$f") $(date -r "$f" +%H:%M)"; cat "$f"; }
             done' 2>/dev/null > $W/raw.txt
n=$(grep -c . $W/raw.txt 2>/dev/null); n=${n:-0}
if [ "$n" -eq 0 ]; then
  echo "ОТКАЗ: с машины не получено НИЧЕГО. Это НЕ значит «работы не было»."
  exit 3
fi
grep '^#SRC' $W/raw.txt
python3 - "$W" "${1:-}" <<'PY'
import sys, os, re
from collections import Counter
W, mode = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "")
st = Counter(); facts = []
for l in open(os.path.join(W, "raw.txt"), encoding="utf8", errors="replace"):
    p = l.split()
    if not p or p[0] == "#SRC" or not p[0].endswith(".cnf"): continue
    # строка вида <база.cnf> s<k> <статус> <время>
    if len(p) >= 3 and re.fullmatch(r"s\d+", p[1]):
        st[p[2]] += 1
        if p[2] == "UNSAT": facts.append(f"{p[0][:-4]}_{p[1]}")
print("\n  статусы в журналах:", dict(st))
uniq = sorted(set(facts))
print(f"  строк UNSAT: {len(facts)}, УНИКАЛЬНЫХ имён: {len(uniq)}"
      f"  (разница {len(facts)-len(uniq)} — повторный счёт, складывать было бы завышением)")
if "SAT" in st:
    print("  ВНИМАНИЕ: в журналах есть ВЫПОЛНИМЫЕ — проверить свидетеля НЕМЕДЛЕННО")
out = os.path.join(W, "recovered_facts.txt")
open(out, "w").write("\n".join(uniq) + "\n")
print(f"  добытые факты: {out}")
if mode == "--apply":
    p = "logs/a280537/facts_second_solver.txt"
    have = {l.strip() for l in open(p) if l.strip() and not l.startswith("#")}
    new = [x for x in uniq if x not in have]
    if new:
        with open(p, "a") as f: f.write("\n".join(new) + "\n")
    print(f"  дописано в {p}: {len(new)} новых имён (уже было {len(uniq)-len(new)})")
else:
    print("  (ничего не записано; для записи запустить с --apply)")
PY
