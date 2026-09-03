"""Create comparable 64-leaf partition manifests for a plane parent cube."""

import argparse
import random
from itertools import combinations, product
from pathlib import Path


def write_manifest(path, method, cubes):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as target:
        target.write("# name\tstratum\tmanifest_index\tassumptions\n")
        for index, cube in enumerate(cubes):
            target.write(
                f"{method}_{index:03d}\t{method}\t{index}\t"
                + ",".join(map(str, cube))
                + "\n"
            )


def hypercube(variables):
    return [
        tuple(variable if bit else -variable for variable, bit in zip(variables, bits))
        for bits in product((0, 1), repeat=len(variables))
    ]


def column_cubes():
    # First untouched z-column after plane x=0: (x,y)=(1,0), z=0..6.
    variables = tuple(range(50, 57))
    cubes = []
    for size in range(4):
        for selected in combinations(variables, size):
            chosen = set(selected)
            cubes.append(tuple(variable if variable in chosen else -variable for variable in variables))
    assert len(cubes) == 64
    return cubes


def proofix_cubes(path):
    cubes = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        fields = raw.split()
        if not fields:
            continue
        if fields[0] != "a" or fields[-1] != "0":
            raise ValueError(f"invalid Proofix ICNF row: {raw}")
        cubes.append(tuple(map(int, fields[1:-1])))
    if len(cubes) != 64 or any(len(cube) != 6 for cube in cubes):
        raise ValueError(f"expected 64 depth-6 Proofix cubes, got {len(cubes)}")
    return cubes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("method", choices=("column", "random", "proofix"))
    parser.add_argument("output", type=Path)
    parser.add_argument("--icnf", type=Path)
    parser.add_argument("--seed", type=int, default=20260902)
    args = parser.parse_args()

    if args.method == "column":
        cubes = column_cubes()
    elif args.method == "random":
        variables = random.Random(args.seed).sample(range(50, 344), 6)
        cubes = hypercube(variables)
    else:
        if args.icnf is None:
            parser.error("--icnf is required for method=proofix")
        cubes = proofix_cubes(args.icnf)

    write_manifest(args.output, args.method, cubes)
    print(f"{args.method}: {len(cubes)} cubes -> {args.output}")


if __name__ == "__main__":
    main()
