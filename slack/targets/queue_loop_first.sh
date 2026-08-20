#!/bin/bash
# queue_loop_first.sh — самопополняющаяся очередь: фронт ПЕРЕСЧИТЫВАЕТСЯ из фактов каждый круг.
#
# Очередь конечна, и это ловушка: когда список кончается, xargs выходит и машина молча встаёт.
# Поэтому фронт не назначается однажды, а вычисляется заново — и у пересчёта ТРИ исхода, не два:
# «пересчёт не состоялся» это НЕ «фронт пуст», иначе цикл объявит победу при первой ошибке чтения.
#
#   queue_loop_first.sh [параллелизм] [лимит-с] [кругов]
SP=/tmp/claude-1000/-home-pmbot-projects-solver-kit/df30d6f4-57eb-4267-abb8-3e2d3cd04a69/scratchpad
R=/home/pmbot/projects/saturation_peer
P="${1:-10}"; LIM="${2:-120}"; ROUNDS="${3:-999}"
cd $R
for r in $(seq 1 "$ROUNDS"); do
  # 1) обновить факты из журналов, иначе фронт пересчитается по вчерашним данным
  # ИСТОЧНИКИ ПЕРЕЧИСЛЯЮТСЯ ЯВНО. Образец каталога захватил бы всё, что появится завтра, — и уже
  # захватил: журналы задачи n=5 о ТРЁХ ТОЧКАХ НА ПРЯМОЙ, где куски называются так же (case_00000),
  # плюс отвергнутый эксперимент со столбцом 7. Их закрытия засчитались как закрытия ЭТОЙ задачи,
  # вердикт перевернулся на «ЗАКРЫТО ЦЕЛИКОМ», мера показала ровно 1.0. Направление ошибки здесь
  # НЕ безопасное: чужие закрытия добавляются, а не теряются, то есть покрытие ЗАВЫШАЕТСЯ.
  L=""; while read f; do [ -f "$SP/logs/$f.txt" ] && L="$L $SP/logs/$f.txt"; done < $SP/whitelist.txt
  if [ -z "$L" ]; then echo "круг $r: ОТКАЗ — список источников пуст, это НЕ повод считать"; sleep 30; continue; fi
  python3 slack/targets/export_facts.py logs/a280537/facts_first_solver.txt $L > $SP/logs/_export.txt 2>&1
  # 2) пересчитать фронт; отличить неудачу пересчёта от пустого фронта
  if ! python3 slack/targets/open_frontier.py > $SP/queue_live.txt 2>$SP/queue_live.err; then
      echo "круг $r: ОТКАЗ — пересчёт фронта не состоялся, это НЕ пустой фронт"; sleep 30; continue
  fi
  n=$(awk 'END{print NR+0}' $SP/queue_live.txt)
  m=$(python3 slack/targets/closed_measure.py 2>/dev/null | awk '/закрытая масса/{print $NF}')
  echo "круг $r: во фронте $n кусков, закрытая масса $m"
  if [ "$n" -eq 0 ]; then echo "круг $r: фронт ПУСТ — проверь вердикт, возможно всё закрыто"; break; fi
  # 3) отработать круг
  cat $SP/queue_live.txt | xargs -P "$P" -I{} $R/slack/targets/work_unit_first_solver.sh {} "$LIM" 49 >> $SP/logs/queue_live_out.txt 2>&1
done
echo "ЦИКЛ ЗАВЕРШЁН"
