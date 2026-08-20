#!/bin/bash
# killer.sh — остановка прогонов на удалённой машине БЕЗ убийства собственной сессии.
#
# ПОЧЕМУ ОТДЕЛЬНЫЙ СКРИПТ, А НЕ УБИЙСТВО ПО ОБРАЗЦУ КОМАНДНОЙ СТРОКИ
#   Образец ищется по ВСЕЙ командной строке. Командная строка удалённой оболочки содержит
#   команду, которой её позвали, поэтому такое убийство, посланное через gcloud compute ssh,
#   совпадает САМО С СОБОЙ и убивает мою сессию. Было дважды за сутки.
#   Третий случай был хуже: образец решателя совпал и с ним, и с обёрткой timeout, пара
#   родитель-ребёнок выглядела как два конкурирующих прогона; я остановил ЗДОРОВЫЙ расчёт
#   и отправил в карантин 1614 верных фактов. Решение было верным, улика — ничего не стоила.
#   Запрет стоит хуком в среде (~/.claude/hooks/no_pkill_f.py), а не в памяти.
#
# ПОЧЕМУ ДОСТАВЛЯЕТСЯ ФАЙЛОМ
#   Кавычки через gcloud compute ssh — отдельный источник ожогов: строка проходит через
#   локальную оболочку, ssh и удалённую оболочку, и экранирование по дороге теряется.
#   Файл через scp не проходит ни через одну из них.
#
#   killer.sh <что-убивать-через-|> [что-KEEP_RE-через-|]
# Пример: killer.sh 'kissat|sos_named|xargs' '/dev/shm/ps/|direct/target.cnf'
set -u
KILL_RE="${1:-kissat}"
KEEP_RE="${2:-}"
MYPID=$$; MYPPID=$PPID
n_killed=0; n_kept=0
for P in /proc/[0-9]*; do
  pid=${P#/proc/}
  [ "$pid" = "$MYPID" ] && continue          # свой pid — ЯВНО, а не по образцу
  [ "$pid" = "$MYPPID" ] && continue         # и родителя: это оболочка ssh
  cl=$(tr '\0' ' ' < "$P/cmdline" 2>/dev/null)
  [ -z "$cl" ] && continue                   # процесс уже умер либо это поток ядра
  if [ -n "$KEEP_RE" ] && echo "$cl" | grep -qE "$KEEP_RE"; then
    n_kept=$((n_kept+1)); continue
  fi
  if echo "$cl" | grep -qE "$KILL_RE"; then
    kill -9 "$pid" 2>/dev/null && n_killed=$((n_killed+1))
  fi
done
sleep 3
n_left=$(for P in /proc/[0-9]*; do tr '\0' ' ' < "$P/cmdline" 2>/dev/null; echo; done | grep -cE "$KILL_RE")
echo "n_killed: $n_killed, n_kept по списку: $n_kept, n_left подходящих: $n_left"
echo "load: $(cut -d' ' -f1 /proc/loadavg)"
