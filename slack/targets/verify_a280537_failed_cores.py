"""Replay useful failed cores with Kissat and independently check their DRAT proofs."""

import argparse
import csv
import hashlib
import subprocess
import time
from itertools import combinations
from pathlib import Path

from materialize_assumption_cnf import materialize


def read_facts(paths):
    result = set()
    for path in paths:
        for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = raw.strip()
            if line.startswith("plx0_"):
                result.add(line)
    return result


def cube_name(subset):
    suffix = "-".join(f"{index:02d}" for index in subset) if subset else "пусто"
    return "plx0_" + suffix


def cube_assumptions(subset):
    selected = set(subset)
    return {index + 1 if index in selected else -(index + 1) for index in range(49)}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("base", type=Path)
    parser.add_argument("results", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("facts", nargs="+", type=Path)
    parser.add_argument("--kissat", default="kissat")
    parser.add_argument("--drat-trim", default="drat-trim")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    known = read_facts(args.facts)
    subsets = tuple(subset for size in range(4) for subset in combinations(range(49), size))
    with args.results.open(encoding="utf-8") as source:
        rows = [row for row in csv.DictReader(source, delimiter="\t") if row["result"] == "20"]

    useful = []
    for row in rows:
        core = tuple(int(value) for value in row["core"].split(",") if value)
        covered = {
            cube_name(subset)
            for subset in subsets
            if set(core) <= cube_assumptions(subset)
        }
        novel = covered - known
        if novel:
            useful.append((row, core, len(covered), len(novel)))

    args.output_dir.mkdir(parents=True, exist_ok=True)
    print(
        "source_cube\tcore_p\tcore_q\tcoverage\tnovel\tsolver_rc\tsolve_s\t"
        "proof_bytes\tchecker_rc\tcheck_s\tverified\tcnf_sha256\tcore"
    )
    for row, core, coverage, novel in useful:
        stem = row["name"].replace("plx0_", "core_")
        cnf = args.output_dir / f"{stem}.cnf"
        proof = args.output_dir / f"{stem}.drat"
        materialize(args.base, cnf, core)

        solve_start = time.monotonic()
        try:
            solved = subprocess.run(
                [args.kissat, "-q", str(cnf), str(proof)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                timeout=args.timeout,
            )
            solver_rc = solved.returncode
        except subprocess.TimeoutExpired:
            solver_rc = 124
        solve_seconds = time.monotonic() - solve_start

        checker_rc = -1
        checker_seconds = 0.0
        verified = False
        if solver_rc == 20 and proof.exists():
            check_start = time.monotonic()
            try:
                checked = subprocess.run(
                    [args.drat_trim, str(cnf), str(proof)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    timeout=args.timeout,
                    text=True,
                )
                checker_rc = checked.returncode
                verified = checker_rc == 0 and "VERIFIED" in checked.stdout
            except subprocess.TimeoutExpired:
                checker_rc = 124
            checker_seconds = time.monotonic() - check_start

        print(
            f"{row['name']}\t{row['core_p']}\t{row['core_q']}\t{coverage}\t{novel}\t"
            f"{solver_rc}\t{solve_seconds:.6f}\t"
            f"{proof.stat().st_size if proof.exists() else 0}\t{checker_rc}\t"
            f"{checker_seconds:.6f}\t{int(verified)}\t{sha256(cnf)}\t"
            + ",".join(map(str, core))
        )


if __name__ == "__main__":
    main()
