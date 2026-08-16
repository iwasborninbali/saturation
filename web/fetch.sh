#!/bin/bash
# fetch a few record files from Flammenkamp's database (see web/README.txt)
cd "$(dirname "$0")"
B=https://wwwhomes.uni-bielefeld.de/achim/no3in/download/solutions_by_symmetry
for f in rot4/n76_rot4.few rot4/n74_rot4.few rot4/n72_rot4.few rot4/n70_rot4.few rct4/n69_rct4.few rct4/n67_rct4.few rct4/n65_rct4.few rot4/n44_rot4 rct4/n57_rct4; do
  curl -sL "$B/$f" -o "$(basename $f)"
done
curl -sL https://wwwhomes.uni-bielefeld.de/achim/no3in/table.txt -o table.txt
