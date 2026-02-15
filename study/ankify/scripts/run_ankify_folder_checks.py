#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys


def run_cmd(cmd):
    result = subprocess.run(cmd, check=False)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run ankify checks for a folder run.")
    parser.add_argument(
        "--manifest", required=True, help="JSON list of note/tsv pairs."
    )
    parser.add_argument(
        "--run-stats", required=True, help="Path to run_stats.json output."
    )
    parser.add_argument(
        "--summary-output", required=False, help="Path to write run_summary.md."
    )
    parser.add_argument(
        "--manifesto-output",
        required=False,
        help="Path to write manifesto_actualization_report.md.",
    )
    args = parser.parse_args()

    with open(args.manifest, "r", encoding="utf-8") as handle:
        manifest = json.load(handle)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    raw_stats_files = []

    for entry in manifest:
        note = entry.get("note")
        tsv = entry.get("tsv")
        if not note or not tsv:
            continue
        rc = run_cmd([os.path.join(script_dir, "run_ankify_checks_loop.sh"), note, tsv])
        if rc != 0:
            return rc
        raw_stats_files.append(f"{note}.raw_stats.json")

    if raw_stats_files:
        rc = run_cmd(
            [
                os.path.join(script_dir, "aggregate_run_stats.py"),
                "--inputs",
                *raw_stats_files,
                "--output",
                args.run_stats,
            ]
        )
        if rc != 0:
            return rc

    for entry in manifest:
        note = entry.get("note")
        if not note:
            continue
        counts = f"{note}.counts.json"
        budget = f"{note}.card_budget.json"
        doctrine = f"{note}.doctrine_report.json"
        with open(doctrine, "w", encoding="utf-8") as handle:
            rc = subprocess.run(
                [
                    os.path.join(script_dir, "compute_doctrine_report.py"),
                    "--counts",
                    counts,
                    "--budget",
                    budget,
                    "--run-stats",
                    args.run_stats,
                    "--require-run-stats",
                ],
                check=False,
                stdout=handle,
            ).returncode
        if rc != 0:
            return rc

    if args.summary_output:
        rc = run_cmd(
            [
                os.path.join(script_dir, "write_run_summary.py"),
                "--manifest",
                args.manifest,
                "--run-stats",
                args.run_stats,
                "--output",
                args.summary_output,
            ]
        )
        if rc != 0:
            return rc

    if args.manifesto_output:
        rc = run_cmd(
            [
                os.path.join(script_dir, "write_manifesto_actualization_report.py"),
                "--manifest",
                args.manifest,
                "--output",
                args.manifesto_output,
            ]
        )
        if rc != 0:
            return rc

    return 0


if __name__ == "__main__":
    sys.exit(main())
