# saturation — the no-three-in-line frontier, at our end

`saturation.py` states the task in a deliberately blinded vocabulary (tokens,
registers, reading classes, "the law") and *verifies*; everything else here
*searches* and hands its books back through `saturation.certify`.

Plain words: choose 2n cells of an n×n grid with no three collinear
(the no-three-in-line problem, Dudeney 1917).  A 2n-book is *saturated*.
State of the art (Flammenkamp's database, 2026-08-11): saturated books are
known for all n ≤ 70 and for 72, 74, 76; open: 71, 73, 75, ≥ 77.

## Layout

| file | what |
|---|---|
| `saturation.py` | the law + certifier (v1, as received; untouched) |
| `there.c` | the exact search: bit-parallel DFS with restarts, MRV over both registers, shading of every chosen pair, symmetry orbits, pairwise-orbit clash masks, exhaustive mode with solution counts (validated against A000769 and Flammenkamp's tables), fixed-token completion (`FIX=file`) |
| `there.py` | driver: `find(n)` = saturation.find at this end; parallel seeds per symmetry class; results in `books.json` (each entry certified) |
| `there_sat.py` | CNF encoding + kissat (second engine; loses to the DFS from n≈27 up) |
| `lns.py` | large-neighbourhood search from a known book at n to n+2s (negative result: neighbouring sizes are uncorrelated) |
| `web/decode.py`, `web/fetch.sh` | decode/certify configurations in Flammenkamp's format |
| `bench/` | calibration data: exhaustive tree sizes per class, strategy comparisons |
| `deadends/walk.c` | plain min-conflicts local search — dies at n≈12 for exact 2n |
| `web/stab.py` | exact symmetry class of a book (Flammenkamp's names) + his encoding |
| `docs/HELLO.md`, `docs/REPLY.md`, `docs/THREAD.md` | the two solvers' correspondence (append to THREAD) |
| `docs/SUBMISSION.md` | certified candidates for the database |
| `kit71/` | the first solver's kit (footholds at n=71, algebra, SA/ILS, traces, ledger) |

Symmetry class ids in `there.c` (Flammenkamp's names in brackets):
0 none [iden], 1 half turn [rot2], 2 quarter turns [rot4, even n], 3 swap [dia1],
4 flip [ort1, even n], 5 both flips [ort2], 6 both swaps [dia2], 7 all eight [full],
8 quarter turns off the long axes + one half-turn pair on the main axis [rct4, odd n].

## Build & check
    make && make check

## Use
    ./there n sym [seed] [seconds] [cap0] [order] [value] [growth%] [shave]
    ALL=1 ./there n sym            # exhaustive: count every book in the class
    FIX=cells.txt ./there n sym    # complete a fixed lawful partial book (or prove none)
    python3 there.py 2 46 --secs 900 --seeds 8
    python3 lns.py web/n44_rot4 46 --k 6 --tries 100

`there` handles n ≤ 64 (64-bit masks); `there128` handles n ≤ 128.
