#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return default


def main():
    parser = argparse.ArgumentParser(description="Write ankify run summary markdown.")
    parser.add_argument("--manifest", required=True, help="Path to manifest JSON.")
    parser.add_argument("--run-stats", required=False, help="Path to run_stats.json.")
    parser.add_argument("--output", required=True, help="Path to write run_summary.md.")
    args = parser.parse_args()

    manifest = load_json(args.manifest, [])
    run_stats = load_json(args.run_stats, {}) if args.run_stats else {}

    total_notes = len(manifest)
    processed = 0
    total_cards = 0
    note_rows = []
    banned_hits = {}
    type_counts = {
        "MODEL": 0,
        "FAILURE_MODE": 0,
        "COUNTER_EVIDENCE": 0,
        "NEGATION": 0,
        "SYNTHESIS": 0,
        "CONSTRUCTIVE": 0,
        "PROCEDURE": 0,
        "DEFINITION": 0,
    }

    tsv_paths = set()

    for entry in manifest:
        note = entry.get("note")
        tsv = entry.get("tsv")
        if tsv:
            tsv_paths.add(tsv)
        if not note:
            continue
        counts_path = f"{note}.counts.json"
        doctrine_path = f"{note}.doctrine_report.json"
        raw_stats_path = f"{note}.raw_stats.json"

        if not os.path.exists(counts_path):
            note_rows.append((note, "-", "SKIP", "Missing counts"))
            continue

        counts = load_json(counts_path, {})
        total_cards += int(counts.get("total_cards", 0))
        processed += 1

        type_counts["MODEL"] += int(counts.get("model_cards", 0))
        type_counts["FAILURE_MODE"] += int(counts.get("failure_mode_cards", 0))
        type_counts["COUNTER_EVIDENCE"] += int(counts.get("counter_evidence_cards", 0))
        type_counts["NEGATION"] += int(counts.get("negation_cards", 0))
        type_counts["SYNTHESIS"] += int(counts.get("synthesis_cards", 0))
        type_counts["CONSTRUCTIVE"] += int(counts.get("constructive_cards", 0))
        type_counts["PROCEDURE"] += int(counts.get("procedure_cards", 0))
        type_counts["DEFINITION"] += int(counts.get("definition_cards", 0))

        doctrine = load_json(doctrine_path, {})
        report = doctrine.get("doctrine_compliance_report", {})
        compliance = "PASS" if report.get("all_checks_passed") else "FAIL"
        failure_reason = ", ".join(report.get("failures", [])) or "-"

        note_rows.append(
            (note, str(counts.get("total_cards", 0)), compliance, failure_reason)
        )

        raw_stats = load_json(raw_stats_path, {})
        for key, value in raw_stats.get("banned_pattern_hits", {}).items():
            banned_hits[key] = banned_hits.get(key, 0) + int(value)

    skipped = total_notes - processed
    compliance_overall = "PASS"
    for _, _, compliance, _ in note_rows:
        if compliance == "FAIL":
            compliance_overall = "FAIL"
            break

    tsv_output = "multiple"
    if len(tsv_paths) == 1:
        tsv_output = next(iter(tsv_paths))

    note_rows_sorted = sorted(
        note_rows, key=lambda row: int(row[1]) if row[1].isdigit() else -1, reverse=True
    )
    top_notes = note_rows_sorted[:5]

    banned_sorted = sorted(banned_hits.items(), key=lambda item: item[1], reverse=True)
    top_banned = banned_sorted[:5]

    lines = []
    lines.append("## Run Summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Total Notes Discovered | {total_notes} |")
    lines.append(f"| Notes Processed | {processed} |")
    lines.append(f"| Notes Skipped | {skipped} |")
    lines.append(f"| **Total Cards Generated** | **{total_cards}** |")
    lines.append(f"| **Doctrine Compliance** | {compliance_overall} |")
    lines.append("")

    lines.append("### Card Type Distribution")
    lines.append("")
    lines.append("| Type | Count | Target | Status |")
    lines.append("|------|-------|--------|--------|")
    lines.append(
        f"| MODEL | {type_counts['MODEL']} | >0 if trig | {'PASS' if type_counts['MODEL'] > 0 else 'FAIL'} |"
    )
    lines.append(
        f"| FAILURE_MODE | {type_counts['FAILURE_MODE']} | >0 if trig | {'PASS' if type_counts['FAILURE_MODE'] > 0 else 'FAIL'} |"
    )
    lines.append(
        f"| COUNTER_EVIDENCE | {type_counts['COUNTER_EVIDENCE']} | >0 if trig | {'PASS' if type_counts['COUNTER_EVIDENCE'] > 0 else 'FAIL'} |"
    )
    lines.append(
        f"| NEGATION | {type_counts['NEGATION']} | >0 if trig | {'PASS' if type_counts['NEGATION'] > 0 else 'FAIL'} |"
    )
    lines.append(
        f"| SYNTHESIS | {type_counts['SYNTHESIS']} | >0 if trig | {'PASS' if type_counts['SYNTHESIS'] > 0 else 'FAIL'} |"
    )
    lines.append(f"| CONSTRUCTIVE | {type_counts['CONSTRUCTIVE']} | Cap | - |")
    lines.append(f"| PROCEDURE | {type_counts['PROCEDURE']} | - | - |")
    lines.append(f"| DEFINITION | {type_counts['DEFINITION']} | - | - |")
    lines.append("")

    lines.append("### Note Status Table")
    lines.append("")
    lines.append("| Note | Cards | Compliance | Failure Reason (if any) |")
    lines.append("|------|-------|------------|-------------------------|")
    for note, cards, compliance, reason in note_rows:
        status = (
            "PASS"
            if compliance == "PASS"
            else ("FAIL" if compliance == "FAIL" else "SKIP")
        )
        lines.append(f"| `{note}` | {cards} | {status} | {reason} |")
    lines.append("")

    lines.append("### Top 5 Largest Notes")
    lines.append("")
    lines.append("| Note | Cards | Compliance |")
    lines.append("|------|-------|------------|")
    for note, cards, compliance, _ in top_notes:
        status = (
            "PASS"
            if compliance == "PASS"
            else ("FAIL" if compliance == "FAIL" else "SKIP")
        )
        lines.append(f"| `{note}` | {cards} | {status} |")
    lines.append("")

    lines.append("### Top Banned Pattern Hits")
    lines.append("")
    if top_banned:
        lines.append("| Pattern | Count |")
        lines.append("|---------|-------|")
        for pattern, count in top_banned:
            lines.append(f"| `{pattern}` | {count} |")
    else:
        lines.append("No banned pattern hits.")
    lines.append("")

    lines.append("### Execution Artifacts")
    lines.append(f"- TSV Output: `{tsv_output}`")
    lines.append(f"- Manifest: `{args.manifest}`")
    if args.run_stats:
        lines.append(f"- Run Stats: `{args.run_stats}`")

    Path(args.output).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
