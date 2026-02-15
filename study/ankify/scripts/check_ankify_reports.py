#!/usr/bin/env python3
import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Check doctrine_report and prune_plan."
    )
    parser.add_argument(
        "--doctrine", required=True, help="Path to doctrine_report.json."
    )
    parser.add_argument("--prune", required=True, help="Path to prune_plan.json.")
    args = parser.parse_args()

    with open(args.doctrine, "r", encoding="utf-8") as handle:
        doctrine = json.load(handle)

    with open(args.prune, "r", encoding="utf-8") as handle:
        prune = json.load(handle)

    report = doctrine.get("doctrine_compliance_report", {})
    all_checks_passed = bool(report.get("all_checks_passed", False))

    prune_plan = prune.get("prune_plan", [])
    prune_ok = len(prune_plan) == 0

    if all_checks_passed and prune_ok:
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
