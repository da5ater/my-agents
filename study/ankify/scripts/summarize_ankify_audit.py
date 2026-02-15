#!/usr/bin/env python3
import argparse
import json
import os
import sys


def safe_load(path, default):
    if not path or not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, OSError):
        return default


def main():
    parser = argparse.ArgumentParser(description="Summarize ankify audits.")
    parser.add_argument(
        "--doctrine", required=True, help="Path to doctrine_report.json."
    )
    parser.add_argument("--prune", required=True, help="Path to prune_plan.json.")
    parser.add_argument(
        "--conversion", required=False, help="Path to conversion_audit.json."
    )
    parser.add_argument(
        "--cap-prune", required=False, help="Path to cap_prune_plan.json."
    )
    parser.add_argument("--output", required=True, help="Path to write summary text.")
    args = parser.parse_args()

    doctrine = safe_load(args.doctrine, {})
    prune = safe_load(args.prune, {})
    conversion = safe_load(args.conversion, [])
    cap_prune = safe_load(args.cap_prune, {})

    report = doctrine.get("doctrine_compliance_report", {})
    failures = report.get("failures", [])

    prune_plan = prune.get("prune_plan", [])
    cap_prune_plan = cap_prune.get("prune_plan", [])
    redundancy = prune.get("redundancy_report", [])

    conversions_by_type = {}
    for entry in conversion:
        to_type = entry.get("to_type", "UNKNOWN")
        conversions_by_type[to_type] = conversions_by_type.get(to_type, 0) + 1

    lines = []
    lines.append("ANKIFY AUDIT SUMMARY")
    lines.append("--------------------")
    lines.append(f"All checks passed: {bool(report.get('all_checks_passed', False))}")
    lines.append(f"Failures: {', '.join(failures) if failures else 'none'}")
    lines.append("")
    lines.append(f"Prune candidates: {len(prune_plan)}")
    lines.append(f"Cap prune candidates: {len(cap_prune_plan)}")
    lines.append(f"Redundancy pairs: {len(redundancy)}")
    lines.append("")
    lines.append(f"Conversions applied: {sum(conversions_by_type.values())}")
    if conversions_by_type:
        for key in sorted(conversions_by_type.keys()):
            lines.append(f"- {key}: {conversions_by_type[key]}")
    else:
        lines.append("- none")

    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))

    return 0


if __name__ == "__main__":
    sys.exit(main())
