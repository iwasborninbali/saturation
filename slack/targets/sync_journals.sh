#!/bin/bash
# sync_journals.sh — стягивает журналы счёта с вычислительных машин в репозиторий.
# Существует потому, что «всё в git» не должно держаться на чьей-то памяти: незалитый журнал
# мы уже теряли один раз (таблица k<=9 была перезаписана и восстанавливалась заново).
# Правило: журнал в репозитории — единственный допустимый источник числа в тексте.
set -u
R="$(cd "$(dirname "$0")/../.." && pwd)"
mkdir -p "$R/logs/no3_3d" "$R/logs/a280537"

pull () {  # pull <имя-вм> <зона> <проект> <метка>
  local vm=$1 zone=$2 proj=$3 tag=$4
  echo "── $tag ($vm)"
  for f in n5_results.txt n5_done.txt tasks_mine.txt n5_results_VOID_killed.txt; do
    timeout 90 gcloud compute scp "$vm:/tmp/$f" "$R/logs/no3_3d/${tag}_$f" \
      --zone="$zone" --project="$proj" 2>/dev/null && echo "   ✓ $f" || echo "   — $f нет"
  done
}

pull saturation-solver-2 us-central1-b loyobondar-prod vm2
pull saturation-solver-3 us-west1-b   eg-multi-domain  vm3

# локальные журналы
for f in /tmp/st5.txt /tmp/st6.txt /tmp/st7.txt; do
  [ -s "$f" ] && cp "$f" "$R/logs/a280537/estimate_$(basename $f)" && echo "   ✓ $(basename $f)"
done
for f in /tmp/lb_*.txt; do
  [ -s "$f" ] && cp "$f" "$R/logs/no3_3d/lower_bound_$(basename $f)" && echo "   ✓ $(basename $f)"
done
echo "готово; не забыть: git add -A && git commit && git push"
