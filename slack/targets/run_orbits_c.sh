#!/bin/bash
# run_orbits_c.sh — решающий счёт по орбитам трёхосных профилей, генератор на C, без хранения.
# Кусок генерируется, решается и удаляется. Выполнимый сохраняется НЕМЕДЛЕННО.
#   usage: run_orbits_c.sh <файл-орбит> <n> <M> <результаты> <параллелизм>
set -u
ORB=$1; N=$2; M=$3; OUT=$4; P=$5
GEN=$(dirname "$0")/p4gen; [ -x "$GEN" ] || GEN=~/sat/p4gen
W=$(mktemp -d /tmp/orbrun_XXXX)
TOT=$(grep -c . "$ORB")
echo "# орбит $TOT, n=$N M=$M, параллелизм $P" > "$OUT"
one () {
  i=$1; spec=$2
  px=$(echo "$spec" | tr ';' '\n' | grep '^0=' | cut -d= -f2)
  py=$(echo "$spec" | tr ';' '\n' | grep '^1=' | cut -d= -f2)
  pz=$(echo "$spec" | tr ';' '\n' | grep '^2=' | cut -d= -f2)
  f="$W/o$i.cnf"
  "$GEN" "$N" "$f" "$px" "$py" "$pz" >/dev/null 2>&1 || { echo "$i GENFAIL" >> "$OUT"; return; }
  s=$(date +%s); timeout 36000 kissat -q "$f" > "$W/o$i.out" 2>&1; rc=$?; e=$(date +%s)
  case $rc in
    20) echo "$i UNSAT $((e-s))s" >> "$OUT" ;;
    10) echo "$i SAT $((e-s))s" >> "$OUT"; cp "$W/o$i.out" "$W/SAT_$i.txt"; echo "$spec" > "$W/SAT_$i.spec" ;;
    *)  echo "$i rc=$rc $((e-s))s" >> "$OUT" ;;
  esac
  rm -f "$f" "$W/o$i.out"
}
export -f one; export W N M OUT GEN
nl -ba "$ORB" | awk '{print $1"\t"$2}' | xargs -P "$P" -I{} bash -c 'IFS=$'"'"'\t'"'"' read -r i s <<< "{}"; one "$i" "$s"'
echo ALLDONE >> "$OUT"
