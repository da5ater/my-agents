#!/usr/bin/env python3
import argparse
import json
import sys


REQUIRED_FIELDS = {
    "concept_count": 0,
    "h2_count": 0,
    "total_cards": 0,
    "synthesis_cards": 0,
    "cross_h2_synthesis_cards": 0,
    "model_cards": 0,
    "failure_mode_cards": 0,
    "negation_cards": 0,
    "counter_evidence_cards": 0,
    "connectivity_cards": 0,
    "definition_cards": 0,
    "procedure_cards": 0,
    "constructive_cards": 0,
    "theory_cards": 0,
    "mental_models_present": False,
    "failure_modes_present": False,
    "contradictions_present": False,
    "distinctions_present": False,
    "failure_mode_triggers_present": False,
    "mapping_ok": False,
    "elements_ok": False,
    "coverage_ok": False,
    "tier1_ok": False,
    "quality_ok": False,
    "output_purity_ok": False,
    "internalization_ok": False,
    "internalization_linkage_ok": False,
    "budget_ok": False,
    "code_blocks": 0,
    "structural_elements": 0,
    "h3_count": 0,
}


def normalize(raw):
    normalized = {}
    missing_fields = []
    for key, default in REQUIRED_FIELDS.items():
        if key not in raw:
            normalized[key] = default
            missing_fields.append(key)
            continue
        value = raw[key]
        if isinstance(default, bool):
            normalized[key] = bool(value)
        else:
            try:
                normalized[key] = int(value)
            except (TypeError, ValueError):
                normalized[key] = default
    normalized["missing_fields"] = missing_fields
    return normalized


def main():
    parser = argparse.ArgumentParser(
        description="Normalize raw stats into counts.json."
    )
    parser.add_argument("--input", required=True, help="Path to raw stats JSON.")
    parser.add_argument("--output", required=True, help="Path to write counts.json.")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as handle:
        raw = json.load(handle)

    counts = normalize(raw)

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(counts, handle, indent=2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
