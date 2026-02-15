#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


RULES = {
    "MC-CTX-001": {
        "name": "Context Mandate",
        "validator": "scripts/validate_cards.py (context_mandate, Given/Task, anchor check)",
    },
    "MC-WHITEBOARD-001": {
        "name": "Whiteboard Rule",
        "validator": "scripts/validate_cards.py (closed prompt, <=2 lines)",
    },
    "MC-INTERVIEW-001": {
        "name": "Interview Readiness",
        "validator": "scripts/validate_cards.py (no yes/no prompts)",
    },
    "MC-SIGNAL-001": {
        "name": "Signal-to-Noise",
        "validator": "scripts/validate_cards.py (banned fillers, anchored depth, Q/A alignment)",
    },
}


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return default


def main():
    parser = argparse.ArgumentParser(
        description="Write manifesto actualization report."
    )
    parser.add_argument("--manifest", required=True, help="Path to manifest JSON.")
    parser.add_argument(
        "--output", required=True, help="Path to write report markdown."
    )
    args = parser.parse_args()

    manifest = load_json(args.manifest, [])
    failures = {rule_id: False for rule_id in RULES}
    samples = {rule_id: [] for rule_id in RULES}

    for entry in manifest:
        note = entry.get("note")
        if not note:
            continue
        raw_stats_path = f"{note}.raw_stats.json"
        raw_stats = load_json(raw_stats_path, {})
        for rule_id in raw_stats.get("manifesto_failures", []):
            if rule_id in failures:
                failures[rule_id] = True
        raw_samples = raw_stats.get("manifesto_samples", {})
        if isinstance(raw_samples, dict):
            for rule_id, ids in raw_samples.items():
                if rule_id not in samples:
                    continue
                for card_id in ids:
                    if card_id not in samples[rule_id] and len(samples[rule_id]) < 3:
                        samples[rule_id].append(card_id)

    lines = []
    lines.append("# Manifesto Actualization Report")
    lines.append("")
    for rule_id, meta in RULES.items():
        status = "FAIL" if failures.get(rule_id) else "PASS"
        lines.append(f"## {rule_id}: {meta['name']}")
        lines.append("")
        lines.append(f"- Validator: {meta['validator']}")
        lines.append(f"- Status: {status}")
        if samples.get(rule_id):
            lines.append("- Sample cards:")
            for card_id in samples[rule_id]:
                lines.append(f"  - `{card_id}`")
        else:
            lines.append("- Sample cards: none")
        lines.append("")

    Path(args.output).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
