"""Build the frozen, stratified plane-cube manifest for the follow-up audit.

The output is deliberately small and deterministic.  It balances historical
easy/stubborn labels and plane contents of size 0--2/3, then shuffles the
selected rows with a recorded seed to avoid the old lexicographic-order bias.
"""

import argparse
import hashlib
import json
import random
from itertools import combinations
from pathlib import Path


def plane_subsets():
    return tuple(subset for size in range(4) for subset in combinations(range(49), size))


def parse_name(name):
    prefix = "plx0_"
    if not name.startswith(prefix):
        raise ValueError(f"not a plane cube: {name}")
    suffix = name[len(prefix):]
    if suffix == "пусто":
        return ()
    result = tuple(int(value) for value in suffix.split("-"))
    if result != tuple(sorted(set(result))) or any(not 0 <= value < 49 for value in result):
        raise ValueError(f"invalid plane cube: {name}")
    return result


def read_names(path):
    names = set()
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if line.startswith("plx0_"):
            parse_name(line)
            names.add(line)
    return names


def quantile_sample(names, index_by_subset, count):
    ordered = sorted(names, key=lambda name: index_by_subset[parse_name(name)])
    if len(ordered) < count:
        raise ValueError(f"need {count} rows, only {len(ordered)} available")
    if count == 1:
        return [ordered[len(ordered) // 2]]
    positions = [round(i * (len(ordered) - 1) / (count - 1)) for i in range(count)]
    return [ordered[position] for position in positions]


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--per-stratum", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20260902)
    args = parser.parse_args()

    log_dir = args.repo / "logs" / "a280537"
    sources = {
        "closed_first": log_dir / "facts_plane_first_solver.txt",
        "closed_second": log_dir / "facts_plane_second_solver.txt",
        "stubborn": log_dir / "plane_stubborn_pieces.txt",
    }
    closed = read_names(sources["closed_first"]) | read_names(sources["closed_second"])
    stubborn = read_names(sources["stubborn"])
    closed -= stubborn

    subsets = plane_subsets()
    index_by_subset = {subset: index for index, subset in enumerate(subsets)}
    groups = {
        "easy_low": {name for name in closed if len(parse_name(name)) <= 2},
        "easy_triple": {name for name in closed if len(parse_name(name)) == 3},
        "stubborn_low": {name for name in stubborn if len(parse_name(name)) <= 2},
        "stubborn_triple": {name for name in stubborn if len(parse_name(name)) == 3},
    }

    rows = []
    for stratum, names in groups.items():
        for name in quantile_sample(names, index_by_subset, args.per_stratum):
            subset = parse_name(name)
            selected = set(subset)
            assumptions = [index + 1 if index in selected else -(index + 1) for index in range(49)]
            rows.append(
                {
                    "name": name,
                    "stratum": stratum,
                    "manifest_index": index_by_subset[subset],
                    "assumptions": assumptions,
                }
            )

    random.Random(args.seed).shuffle(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as target:
        target.write("# name\tstratum\tmanifest_index\tassumptions\n")
        for row in rows:
            target.write(
                f"{row['name']}\t{row['stratum']}\t{row['manifest_index']}\t"
                + ",".join(map(str, row["assumptions"]))
                + "\n"
            )

    metadata = {
        "output": str(args.output),
        "output_sha256": sha256(args.output),
        "seed": args.seed,
        "per_stratum": args.per_stratum,
        "rows": len(rows),
        "source_sha256": {name: sha256(path) for name, path in sources.items()},
        "group_population": {name: len(values) for name, values in groups.items()},
    }
    print(json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
