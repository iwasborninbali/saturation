#!/bin/bash
# deep5.sh — спуск от case_00000_s007_s000 к внукам _s000_s00X и дробление их столбцом 5.
# Столбцы берутся ПОСЛЕДОВАТЕЛЬНО (3, 4, 5) — измерение показало, что столбцы того же слоя
# ограничивают сильнее, чем столбцы других слоёв (docs/research/negative/column_choice.md).
SP=/tmp/claude-1000/-home-pmbot-projects-solver-kit/df30d6f4-57eb-4267-abb8-3e2d3cd04a69/scratchpad
R=/home/pmbot/projects/saturation_peer
W=$SP/d5; rm -rf $W; mkdir -p $W/a $W/b
python3 $R/slack/targets/subsplit.py $SP/wfront/l2/case_00000_s007_s000.cnf 7 3 3 $W/a >/dev/null 2>&1
[ "$(ls $W/a/*.cnf | wc -l)" -eq 64 ] || { echo "ОТКАЗ уровень 3"; exit 2; }
python3 $R/slack/targets/subsplit.py $W/a/case_00000_s007_s000_s000.cnf 7 4 3 $W/b >/dev/null 2>&1
[ "$(ls $W/b/*.cnf | wc -l)" -eq 64 ] || { echo "ОТКАЗ уровень 4"; exit 3; }
rm -f $W/a/*.cnf
for i in 000 001 002 003 004 005 006; do
  node=case_00000_s007_s000_s000_s$i
  C=$W/c$i; mkdir -p $C
  python3 $R/slack/targets/subsplit.py $W/b/$node.cnf 7 5 3 $C >/dev/null 2>&1
  k=$(ls $C/*.cnf 2>/dev/null | wc -l)
  [ "$k" -eq 64 ] || { echo "ОТКАЗ $node: детей $k"; rm -rf $C; continue; }
  f0=$C/${node}_s000.cnf; hdr=$(awk '/^p cnf/{print $4; exit}' $f0); body=$(awk '!/^c |^p cnf/ && NF>0' $f0|wc -l)
  [ "$hdr" = "$body" ] || { echo "ОТКАЗ $node: повреждён"; rm -rf $C; continue; }
  echo "== $node раздроблён столбцом 5 на 64, целостность ДА"
  # ПОРЯДОК ВАЖЕН. Низкие индексы — малые подмножества, то есть ВЫЖИВШИЕ и трудные; высокие —
  # тройки, которые при уже занятой ёмкости слоя невыполнимы даром. Имена сортируются по
  # возрастанию, поэтому очередь по умолчанию ставит трудные первыми и до дармовых не доходит.
  ls -r $C/*.cnf | xargs -P 6 -I{} $SP/kis.sh {}
  rm -rf $C
done
rm -rf $W
echo "УРОВЕНЬ 5 ПРОЙДЕН"
