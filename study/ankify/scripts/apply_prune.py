#!/usr/bin/env python3
import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="Apply prune_plan to a TSV file.")
    parser.add_argument("--tsv", required=True, help="Path to TSV file.")
    parser.add_argument("--prune", required=True, help="Path to prune_plan.json.")
    parser.add_argument("--output", required=True, help="Path to write pruned TSV.")
    args = parser.parse_args()

    with open(args.prune, "r", encoding="utf-8") as handle:
        prune = json.load(handle)

    drop_indices = {entry.get("drop_index") for entry in prune.get("prune_plan", [])}
    drop_indices = {idx for idx in drop_indices if isinstance(idx, int)}

    with open(args.tsv, "r", encoding="utf-8") as handle:
        lines = handle.readlines()

    output_lines = []
    for index, line in enumerate(lines):
        if index in drop_indices:
            continue
        if line.endswith("\n"):
            output_lines.append(line)
        else:
            output_lines.append(f"{line}\n")

    with open(args.output, "w", encoding="utf-8") as handle:
        handle.writelines(output_lines)

    return 0


if __name__ == "__main__":
    sys.exit(main())
