#!/usr/bin/env python3
import argparse
import json
import re
import sys


DROP_ORDER = [
    "DEFINITION",
    "THEORY",
    "PROCEDURE",
    "CONSTRUCTIVE",
    "SYNTHESIS",
]


def strip_html(text):
    return re.sub(r"<[^>]+>", "", text)


def classify(front, back):
    if "<pre" in back and "<code>" in back:
        return "CONSTRUCTIVE"
    text = strip_html(front).lower()
    if text.startswith("what is "):
        return "DEFINITION"
    if text.startswith("how do you") or text.startswith("how to"):
        return "PROCEDURE"
    if "what goes wrong" in text or "breaks if" in text:
        return "FAILURE_MODE"
    if "what contradicts" in text or "not apply" in text:
        return "COUNTER_EVIDENCE"
    if " not " in text or "differs from" in text:
        return "NEGATION"
    if "explain/visualize how" in text or "stages" in text:
        return "MODEL"
    if "compare" in text or "tradeoff" in text or "affect" in text:
        return "SYNTHESIS"
    return "THEORY"


def main():
    parser = argparse.ArgumentParser(
        description="Prune to cap per note while preserving minimums."
    )
    parser.add_argument("--cards", required=True, help="Path to cards.json.")
    parser.add_argument("--budget", required=True, help="Path to card_budget.json.")
    parser.add_argument("--output", required=True, help="Path to prune_plan.json.")
    args = parser.parse_args()

    with open(args.cards, "r", encoding="utf-8") as handle:
        cards = json.load(handle)

    with open(args.budget, "r", encoding="utf-8") as handle:
        budget = json.load(handle).get("card_budget_plan", {})

    target_total_max = int(budget.get("target_total_cards_max", 10))
    target_constructive_max = int(budget.get("target_constructive_max", 2))
    target_synthesis_min = int(budget.get("target_synthesis", 0))
    target_model_min = int(budget.get("target_model", 1))
    target_failure_min = int(budget.get("target_failure_mode", 1))
    target_negation_min = int(budget.get("target_negation", 1))
    target_counter_min = int(budget.get("target_counter_evidence", 1))

    grouped = {}
    for card in cards:
        url = card.get("url", "")
        grouped.setdefault(url, []).append(card)

    drops = []
    for _, group in grouped.items():
        if len(group) <= target_total_max:
            continue

        counts = {}
        for card in group:
            card_type = card.get("type") or classify(
                card.get("front", ""), card.get("back", "")
            )
            counts[card_type] = counts.get(card_type, 0) + 1

        protected_min = {
            "MODEL": target_model_min,
            "FAILURE_MODE": target_failure_min,
            "NEGATION": target_negation_min,
            "COUNTER_EVIDENCE": target_counter_min,
            "SYNTHESIS": target_synthesis_min,
        }

        needed = len(group) - target_total_max
        for drop_type in DROP_ORDER:
            if needed <= 0:
                break
            for card in group:
                if needed <= 0:
                    break
                card_type = card.get("type") or classify(
                    card.get("front", ""), card.get("back", "")
                )
                if card_type != drop_type:
                    continue
                if card_type == "CONSTRUCTIVE":
                    if counts.get(card_type, 0) <= target_constructive_max:
                        continue
                if card_type == "SYNTHESIS":
                    if counts.get(card_type, 0) <= protected_min.get("SYNTHESIS", 0):
                        continue
                if (
                    card_type in protected_min
                    and counts.get(card_type, 0) <= protected_min[card_type]
                ):
                    continue
                drops.append({"drop_index": card.get("index"), "reason": "cap_prune"})
                counts[card_type] = counts.get(card_type, 0) - 1
                needed -= 1

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump({"prune_plan": drops}, handle, indent=2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
