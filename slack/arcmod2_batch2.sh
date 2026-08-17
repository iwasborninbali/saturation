#!/bin/bash
cd "$(dirname "$0")/.."
out=slack/results_linux.txt
{ for s in 15 16; do echo "14 $s 5400"; done; for s in 16 17; do echo "15 $s 5400"; done; for s in 17 18; do echo "16 $s 5400"; done;
  for s in 19 20; do echo "18 $s 5400"; done; for s in 21 22; do echo "20 $s 5400"; done; for s in 22 23; do echo "21 $s 5400"; done;
  for s in 24 25; do echo "22 $s 5400"; done; for s in 26 27; do echo "24 $s 5400"; done; for s in 27 28 30; do echo "25 $s 7200 FIX1"; done; } |
xargs -P 5 -L 1 sh -c 'python3 slack/arcmod2.py $0 $1 $2 $3 | cut -c1-200' >> $out
echo "# batch2 done $(date -u +%FT%TZ)" >> $out
