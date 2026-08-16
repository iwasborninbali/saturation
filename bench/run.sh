#!/bin/bash
# usage: run.sh n sym secs  -> tries all (order,value) combos x 3 seeds, 8 in parallel
n=$1; sym=$2; secs=$3
for order in 0 1 2 3 4; do for value in 0 1 2; do for seed in 1 2 3; do
  echo "$n $sym $seed $secs 2000 $order $value"
done; done; done | xargs -P 8 -L 1 sh -c './there $0 $1 $2 $3 $4 $5 $6 | cut -c1-110'
