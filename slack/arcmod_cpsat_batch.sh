#!/bin/bash
cd "$(dirname "$0")/.."
out=slack/results_linux.txt
echo "# $(date -u +%FT%TZ) CP-SAT batch (arcmod_cpsat.py, 8 workers, triple clauses)" >> $out
for m in 14 15 16 18 20 21 22 24; do timeout 3000 python3 slack/arcmod_cpsat.py $m 2400 8 | cut -c1-240 >> $out; done
timeout 5400 python3 slack/arcmod_cpsat.py 25 4800 8 FIX1 | cut -c1-240 >> $out
for m in 27 26 28; do timeout 3000 python3 slack/arcmod_cpsat.py $m 2400 8 | cut -c1-240 >> $out; done
echo "# cpsat batch done $(date -u +%FT%TZ)" >> $out
