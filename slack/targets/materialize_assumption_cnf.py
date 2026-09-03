"""Append assumption literals as units to a DIMACS CNF with a corrected header."""

import argparse
from pathlib import Path


def materialize(source, target, assumptions, strip_comments=False):
    raw = source.read_bytes()
    header_start = raw.index(b"p cnf ")
    header_end = raw.index(b"\n", header_start)
    fields = raw[header_start:header_end].split()
    if len(fields) != 4:
        raise ValueError("invalid DIMACS header")
    variables, clauses = int(fields[2]), int(fields[3])
    if any(not literal or abs(literal) > variables for literal in assumptions):
        raise ValueError("assumption literal outside declared variable range")
    header = f"p cnf {variables} {clauses + len(assumptions)}\n".encode()
    units = b"".join(f"{literal} 0\n".encode() for literal in assumptions)
    output = raw[:header_start] + header + raw[header_end + 1:] + units
    if strip_comments:
        output = b"".join(
            line for line in output.splitlines(keepends=True) if not line.startswith(b"c ")
        )
    target.write_bytes(output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("literals", help="comma-separated non-zero DIMACS literals")
    parser.add_argument("--strip-comments", action="store_true")
    args = parser.parse_args()
    assumptions = [int(value) for value in args.literals.split(",") if value]
    materialize(args.source, args.target, assumptions, strip_comments=args.strip_comments)


if __name__ == "__main__":
    main()
