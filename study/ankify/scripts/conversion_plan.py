#!/usr/bin/env python3
import argparse
import json
import sys


PRIORITY = [
    "COUNTER_EVIDENCE",
    "FAILURE_MODE",
    "MODEL",
    "SYNTHESIS",
    "NEGATION",
]


def main():
    parser = argparse.ArgumentParser(
        description="Compute conversion plan for depth without growth."
    )
    parser.add_argument("--counts", required=True, help="Path to counts.json.")
    parser.add_argument("--budget", required=True, help="Path to card_budget.json.")
    args = parser.parse_args()

    with open(args.counts, "r", encoding="utf-8") as handle:
        counts = json.load(handle)

    with open(args.budget, "r", encoding="utf-8") as handle:
        budget = json.load(handle).get("card_budget_plan", {})

    total_cards = int(counts.get("total_cards", 0))

    targets = {
        "MODEL": int(budget.get("target_model", 0)),
        "FAILURE_MODE": int(budget.get("target_failure_mode", 0)),
        "COUNTER_EVIDENCE": int(budget.get("target_counter_evidence", 0)),
        "SYNTHESIS": int(budget.get("target_synthesis", 0)),
        "NEGATION": int(budget.get("target_negation", 0)),
    }

    current = {
        "MODEL": int(counts.get("model_cards", 0)),
        "FAILURE_MODE": int(counts.get("failure_mode_cards", 0)),
        "COUNTER_EVIDENCE": int(counts.get("counter_evidence_cards", 0)),
        "SYNTHESIS": int(counts.get("synthesis_cards", 0)),
        "NEGATION": int(counts.get("negation_cards", 0)),
    }

    plan = []
    missing = []
    for card_type in PRIORITY:
        gap = max(0, targets[card_type] - current[card_type])
        if gap > 0:
            missing.extend([card_type] * gap)

    target_total_max = int(budget.get("target_total_cards_max", total_cards))
    over_cap = max(0, total_cards - target_total_max)

    conversions_needed = len(missing) + over_cap
    for card_type in missing:
        if conversions_needed <= 0:
            break
        plan.append({"convert": 1, "to": card_type})
        conversions_needed -= 1

    while conversions_needed > 0:
        for card_type in PRIORITY:
            if conversions_needed <= 0:
                break
            plan.append({"convert": 1, "to": card_type})
            conversions_needed -= 1

    output = {
        "required_conversions": len(plan),
        "plan": plan,
    }

    json.dump(output, sys.stdout, indent=2)


if __name__ == "__main__":
    sys.exit(main())
