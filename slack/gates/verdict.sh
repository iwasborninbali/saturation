#!/bin/bash
# verdict.sh — ОБОБЩЁННЫЙ источник вердикта: по манифесту и журналам, без привязки к задаче.
#
# Существует потому, что правило «считать уникальные закрытия, а не строки» я нарушил в отчёте
# ЧЕРЕЗ ПОЛЧАСА после того, как записал его в README из-за вранья монитора. Правило в голове
# нарушается; правило в инструменте — нет. Для решающего вопроса такой инструмент был
# (verdict19.sh) и поймал бы; для калибровки я считал руками и ошибся руками.
#
#   usage: verdict.sh <файл-манифеста-или-каталог> <журнал> [журнал...]
#     манифест: список ожидаемых имён (по одному в строке) ЛИБО каталог с *.cnf
#     журнал:   строки вида "<имя> <статус> ..."; закрывает ТОЛЬКО статус UNSAT
set -u
[ $# -ge 2 ] || { echo "usage: verdict.sh <манифест|каталог> <журнал>..."; exit 1; }
M=$1; shift
if [ -d "$M" ]; then ls "$M"/*.cnf 2>/dev/null | xargs -n1 basename | sort > /tmp/_verdict_exp.txt
else grep -o '[^/ ]*\.cnf' "$M" | sort -u > /tmp/_verdict_exp.txt; fi
cat "$@" 2>/dev/null | grep -o '^[^ ]*\.cnf [^ ]*' > /tmp/_verdict_res.txt
awk '$2=="UNSAT"{print $1}' /tmp/_verdict_res.txt | sort -u > /tmp/_verdict_ok.txt
SAT=$(awk '$2=="SAT"{print $1}' /tmp/_verdict_res.txt | sort -u | wc -l | tr -d ' ')
OTH=$(awk '$2!="UNSAT" && $2!="SAT"{print $2}' /tmp/_verdict_res.txt | sort | uniq -c | tr '\n' ' ')
EXP=$(wc -l < /tmp/_verdict_exp.txt | tr -d ' '); OK=$(wc -l < /tmp/_verdict_ok.txt | tr -d ' ')
MISS=$(comm -13 /tmp/_verdict_ok.txt /tmp/_verdict_exp.txt | head -5 | tr '\n' ' ')
NMISS=$(comm -13 /tmp/_verdict_ok.txt /tmp/_verdict_exp.txt | wc -l | tr -d ' ')
echo "ожидалось кусков: $EXP"
echo "  закрыто УНИКАЛЬНЫХ (UNSAT): $OK"
echo "  выполнимых (SAT):           $SAT"
echo "  прочих статусов:            ${OTH:-нет}   <- не закрывают и не опровергают"
echo "  не закрыто:                 $NMISS  ${MISS:+например $MISS}"
if [ "$SAT" -gt 0 ]; then echo; echo "ВЕРДИКТ: ЕСТЬ ВЫПОЛНИМЫЕ КУСКИ — утверждение о невыполнимости ЛОЖНО"; exit 2; fi
if [ "$NMISS" -gt 0 ]; then echo; echo "ВЕРДИКТ: НЕЛЬЗЯ заявлять — покрытие неполно"; exit 1; fi
echo; echo "ВЕРДИКТ: покрытие ПОЛНОЕ, все $EXP кусков невыполнимы"
