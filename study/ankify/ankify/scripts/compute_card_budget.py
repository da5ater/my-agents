#!/usr/bin/env python3
import argparse
import json
import math
import sys


def main():
    parser = argparse.ArgumentParser(
        description="DEPRECATED: use compute_card_budget_pre.py for pre-generation budgets."
    )
    parser.add_argument("--counts", required=True, help="Path to JSON counts input.")
    args = parser.parse_args()

    with open(args.counts, "r", encoding="utf-8") as handle:
        data = json.load(handle)

    concept_count = int(data.get("concept_count", 0))
    h2_count = int(data.get("h2_count", 0))
    mental_models_present = bool(data.get("mental_models_present", False))
    contradictions_present = bool(data.get("contradictions_present", False))
    distinctions_present = bool(data.get("distinctions_present", False))

    target_synthesis = 1 if concept_count >= 2 else 0
    if concept_count >= 4:
        target_synthesis = 2

    target_cross_h2_synthesis = 1 if h2_count >= 2 else 0
    target_model = 1 if mental_models_present else 0
    target_failure_mode = 0
    target_counter_evidence = 1 if contradictions_present else 0
    target_negation = 1 if distinctions_present else 0

    target_total_cards = max(1, concept_count)

    target_definition_max = int(math.floor(target_total_cards * 0.35))
    target_procedure_max = int(math.floor(target_total_cards * 0.50))

    plan = {
        "card_budget_plan": {
            "target_total_cards": target_total_cards,
            "target_synthesis": target_synthesis,
            "target_cross_h2_synthesis": target_cross_h2_synthesis,
            "target_model": target_model,
            "target_failure_mode": target_failure_mode,
            "target_negation": target_negation,
            "target_counter_evidence": target_counter_evidence,
            "target_constructive": int(data.get("target_constructive", 0)),
            "target_theory": int(data.get("target_theory", 0)),
            "target_definition_max": target_definition_max,
            "target_procedure_max": target_procedure_max,
        }
    }

    print(
        "WARNING: compute_card_budget.py is deprecated; use compute_card_budget_pre.py.",
        file=sys.stderr,
    )
    json.dump(plan, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
