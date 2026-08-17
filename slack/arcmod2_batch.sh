#!/bin/bash
# A(m) batch on linux-12c: (m, s, secs, flag) jobs in parallel; results appended to slack/results_linux.txt
cd "$(dirname "$0")/.."
out=slack/results_linux.txt
{
echo "8 7 600"; echo "8 8 600";
for s in 14 15 16; do echo "14 $s 1800"; done
for s in 15 16 17; do echo "15 $s 1800"; done
for s in 16 17 18; do echo "16 $s 1800"; done
for s in 18 19 20; do echo "18 $s 1800"; done
for s in 20 21 22; do echo "20 $s 1800"; done
for s in 21 22 23; do echo "21 $s 1800"; done
for s in 22 23 24; do echo "22 $s 1800"; done
for s in 24 25 26; do echo "24 $s 1800"; done
for s in 25 26 27 28 29 30; do echo "25 $s 2400 FIX1"; done
for s in 27 28 29 30; do echo "27 $s 1800"; done
for s in 49 50 52 55 60; do echo "49 $s 3600 FIX1"; done
} | xargs -P 12 -L 1 sh -c 'python3 slack/arcmod2.py $0 $1 $2 $3 | cut -c1-200' >> $out
echo "# batch done $(date -u +%FT%TZ)" >> $out
