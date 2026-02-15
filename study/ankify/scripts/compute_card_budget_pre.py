#!/usr/bin/env python3
import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Compute pre-generation card_budget_plan."
    )
    parser.add_argument(
        "--note-meta", required=True, help="Path to parse_note.py output JSON."
    )
    parser.add_argument(
        "--output", required=True, help="Path to write card_budget_plan JSON."
    )
    args = parser.parse_args()

    with open(args.note_meta, "r", encoding="utf-8") as handle:
        meta = json.load(handle)

    concept_count = int(meta.get("concept_count", 0))
    h2_count = int(meta.get("h2_count", 0))
    code_blocks = int(meta.get("code_blocks", 0))
    anchors = meta.get("anchors", {})
    anchor_methods = anchors.get("methods", []) if isinstance(anchors, dict) else []
    anchor_keywords = anchors.get("keywords", []) if isinstance(anchors, dict) else []
    anchors_total = len(anchor_methods) + len(anchor_keywords)

    target_synthesis = 1 if concept_count >= 2 else 0
    if concept_count >= 4:
        target_synthesis = 2

    target_cross_h2_synthesis = 1 if h2_count >= 2 else 0

    target_model = 1
    target_failure_mode = 1
    target_counter_evidence = 1
    target_negation = 1

    required_deep_min = 4
    if concept_count >= 2:
        required_deep_min += 1

    target_constructive_max = min(2, code_blocks)
    target_constructive_min = 1 if code_blocks > 0 else 0

    target_definition_max = 1
    target_theory_max = 4 if code_blocks == 0 else 2
    target_procedure_max = 1

    is_high_complexity = bool(anchors_total >= 8 or h2_count >= 3 or code_blocks > 1)
    target_total_cards_max = 8 if is_high_complexity else 6
    target_total_cards_min = min(
        target_total_cards_max, required_deep_min + target_constructive_min
    )

    plan = {
        "card_budget_plan": {
            "target_total_cards_min": target_total_cards_min,
            "target_total_cards_max": target_total_cards_max,
            "target_synthesis": target_synthesis,
            "target_cross_h2_synthesis": target_cross_h2_synthesis,
            "target_model": target_model,
            "target_failure_mode": target_failure_mode,
            "target_negation": target_negation,
            "target_counter_evidence": target_counter_evidence,
            "target_constructive_min": target_constructive_min,
            "target_constructive_max": target_constructive_max,
            "target_definition_max": target_definition_max,
            "target_theory_max": target_theory_max,
            "target_procedure_max": target_procedure_max,
        }
    }

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(plan, handle, indent=2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
