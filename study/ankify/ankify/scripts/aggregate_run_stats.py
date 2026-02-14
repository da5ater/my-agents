#!/usr/bin/env python3
import argparse
import json
import math
import sys


def main():
    parser = argparse.ArgumentParser(description="Aggregate raw stats for a run.")
    parser.add_argument(
        "--inputs", nargs="+", required=True, help="List of raw stats JSON files."
    )
    parser.add_argument("--output", required=True, help="Path to write run_stats.json.")
    args = parser.parse_args()

    total_cards = 0
    failure_mode_cards = 0

    for path in args.inputs:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        total_cards += int(data.get("total_cards", 0))
        failure_mode_cards += int(data.get("failure_mode_cards", 0))

    required_global = 0
    if total_cards > 0:
        required_global = int(math.ceil(total_cards / 25.0))

    run_stats = {
        "total_cards": total_cards,
        "global_failure_mode_cards": failure_mode_cards,
        "required_global_failure_mode_cards": required_global,
    }

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(run_stats, handle, indent=2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
