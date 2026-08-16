Third-party data (Achim Flammenkamp's no-three-in-line database) is NOT stored here.
Fetch what you need, e.g.:
  curl -sL https://wwwhomes.uni-bielefeld.de/achim/no3in/download/solutions_by_symmetry/rot4/n76_rot4.few -o web/n76_rot4.few
and decode/certify with:  python3 web/decode.py web/n76_rot4.few
