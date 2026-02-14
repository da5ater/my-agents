#!/usr/bin/env python3
import argparse
import json
import math
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
    structural_elements = int(meta.get("structural_elements", 0))

    mental_models_present = bool(meta.get("mental_models_present", False))
    failure_mode_triggers_present = bool(
        meta.get("failure_mode_triggers_present", False)
    )
    contradictions_present = bool(meta.get("contradictions_present", False))
    distinctions_present = bool(meta.get("distinctions_present", False))

    target_synthesis = 1 if concept_count >= 2 else 0
    if concept_count >= 4:
        target_synthesis = 2

    target_cross_h2_synthesis = 1 if h2_count >= 2 else 0
    target_model = 1 if mental_models_present else 0
    target_failure_mode = 1 if failure_mode_triggers_present else 0
    target_counter_evidence = 1 if contradictions_present else 0
    target_negation = 1 if distinctions_present else 0

    max_cards_per_note = max(12, min(18, 10 + code_blocks * 2))
    if code_blocks == 0:
        max_cards_per_note = 12

    target_total_cards = min(max(structural_elements, 8), max_cards_per_note)
    target_definition_max = int(math.floor(target_total_cards * 0.25))
    target_procedure_max = int(math.floor(target_total_cards * 0.35))

    target_constructive_min = 0
    target_constructive_max = 0
    if code_blocks > 0:
        target_constructive_min = code_blocks * 2
        target_constructive_max = code_blocks * 4

    plan = {
        "card_budget_plan": {
            "target_total_cards": target_total_cards,
            "target_synthesis": target_synthesis,
            "target_cross_h2_synthesis": target_cross_h2_synthesis,
            "target_model": target_model,
            "target_failure_mode": target_failure_mode,
            "target_negation": target_negation,
            "target_counter_evidence": target_counter_evidence,
            "target_constructive_min": target_constructive_min,
            "target_constructive_max": target_constructive_max,
            "target_theory": concept_count,
            "target_definition_max": target_definition_max,
            "target_procedure_max": target_procedure_max,
        }
    }

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(plan, handle, indent=2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
