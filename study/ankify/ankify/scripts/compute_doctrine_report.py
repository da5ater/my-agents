#!/usr/bin/env python3
import argparse
import json
import math
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Compute doctrine_compliance_report from counts."
    )
    parser.add_argument("--counts", required=True, help="Path to JSON counts input.")
    parser.add_argument(
        "--budget", required=False, help="Path to card_budget_plan JSON."
    )
    parser.add_argument(
        "--run-stats", required=False, help="Path to run-level stats JSON."
    )
    parser.add_argument(
        "--require-run-stats",
        action="store_true",
        help="Fail if run-stats are missing in folder mode.",
    )
    args = parser.parse_args()

    with open(args.counts, "r", encoding="utf-8") as handle:
        data = json.load(handle)

    failures = []
    missing_fields = data.get("missing_fields", [])
    if missing_fields:
        failures.append("missing_fields")

    mapping_ok = bool(data.get("mapping_ok", True))
    elements_ok = bool(data.get("elements_ok", True))
    coverage_ok = bool(data.get("coverage_ok", True))
    tier1_ok = bool(data.get("tier1_ok", True))
    quality_ok = bool(data.get("quality_ok", True))
    output_purity_ok = bool(data.get("output_purity_ok", True))

    internalization_ok = bool(data.get("internalization_ok", False))
    internalization_linkage_ok = bool(data.get("internalization_linkage_ok", False))

    concept_count = int(data.get("concept_count", 0))
    h2_count = int(data.get("h2_count", 0))
    total_cards = int(data.get("total_cards", 0))

    synthesis_cards = int(data.get("synthesis_cards", 0))
    cross_h2_synthesis_cards = int(data.get("cross_h2_synthesis_cards", 0))
    model_cards = int(data.get("model_cards", 0))
    failure_mode_cards = int(data.get("failure_mode_cards", 0))
    negation_cards = int(data.get("negation_cards", 0))
    counter_evidence_cards = int(data.get("counter_evidence_cards", 0))
    connectivity_cards = int(data.get("connectivity_cards", 0))
    definition_cards = int(data.get("definition_cards", 0))
    procedure_cards = int(data.get("procedure_cards", 0))
    constructive_cards = int(
        data.get("constructive_cards", data.get("target_constructive", 0))
    )
    code_blocks = int(data.get("code_blocks", 0))

    mental_models_present = bool(data.get("mental_models_present", False))
    failure_modes_present = bool(data.get("failure_modes_present", False))
    contradictions_present = bool(data.get("contradictions_present", False))
    distinctions_present = bool(data.get("distinctions_present", False))
    failure_mode_triggers_present = bool(
        data.get("failure_mode_triggers_present", False)
    )

    minimums_ok = True
    if concept_count >= 2 and synthesis_cards < 1:
        minimums_ok = False
        failures.append("missing_synthesis")
    if concept_count >= 4 and synthesis_cards < 2:
        minimums_ok = False
        failures.append("insufficient_synthesis")
    if h2_count >= 2 and cross_h2_synthesis_cards < 1:
        minimums_ok = False
        failures.append("missing_cross_h2_synthesis")
    if mental_models_present and model_cards < 1:
        minimums_ok = False
        failures.append("missing_model")
    if failure_modes_present and failure_mode_cards < 1:
        minimums_ok = False
        failures.append("missing_failure_mode")
    if contradictions_present and counter_evidence_cards < 1:
        minimums_ok = False
        failures.append("missing_counter_evidence")
    if distinctions_present and negation_cards < 1:
        minimums_ok = False
        failures.append("missing_negation")

    connectivity_ok = True
    if concept_count >= 3:
        required_connectivity = max(2, int(math.floor(total_cards * 0.15)))
        if connectivity_cards < required_connectivity:
            connectivity_ok = False
            failures.append("missing_connectivity")

    caps_ok = True
    if total_cards > 0:
        if definition_cards > int(math.floor(total_cards * 0.35)):
            caps_ok = False
            failures.append("definition_cap_exceeded")
        if procedure_cards > int(math.floor(total_cards * 0.50)):
            caps_ok = False
            failures.append("procedure_cap_exceeded")

    global_failure_mode_ok = True
    if args.run_stats:
        with open(args.run_stats, "r", encoding="utf-8") as handle:
            run_stats = json.load(handle)
        required_global = int(run_stats.get("required_global_failure_mode_cards", 0))
        global_failure_cards = int(run_stats.get("global_failure_mode_cards", 0))
        if total_cards > 0 and global_failure_cards < required_global:
            global_failure_mode_ok = False
            failures.append("global_failure_mode_minimum")
    else:
        if args.require_run_stats:
            global_failure_mode_ok = False
            failures.append("run_stats_missing")

    if failure_mode_triggers_present and failure_mode_cards < 1:
        minimums_ok = False
        failures.append("failure_mode_trigger_missing")

    budget_ok = bool(data.get("budget_ok", True))
    if args.budget:
        with open(args.budget, "r", encoding="utf-8") as handle:
            budget = json.load(handle).get("card_budget_plan", {})
        budget_ok = (
            total_cards >= int(budget.get("target_total_cards", 0))
            and synthesis_cards >= int(budget.get("target_synthesis", 0))
            and cross_h2_synthesis_cards
            >= int(budget.get("target_cross_h2_synthesis", 0))
            and model_cards >= int(budget.get("target_model", 0))
            and failure_mode_cards >= int(budget.get("target_failure_mode", 0))
            and negation_cards >= int(budget.get("target_negation", 0))
            and counter_evidence_cards >= int(budget.get("target_counter_evidence", 0))
            and definition_cards
            <= int(budget.get("target_definition_max", total_cards))
            and procedure_cards <= int(budget.get("target_procedure_max", total_cards))
            and constructive_cards >= int(budget.get("target_constructive_min", 0))
            and constructive_cards
            <= int(budget.get("target_constructive_max", total_cards))
        )
        if not budget_ok:
            failures.append("budget_mismatch")

    max_cards_per_note = max(12, min(18, 10 + code_blocks * 2))
    if code_blocks == 0:
        max_cards_per_note = 12
    if total_cards > max_cards_per_note:
        failures.append("max_cards_exceeded")

    metadata_missing = total_cards > 0 and concept_count == 0 and h2_count == 0
    if metadata_missing:
        failures.append("metadata_missing")

    all_checks_passed = (
        internalization_ok
        and internalization_linkage_ok
        and mapping_ok
        and elements_ok
        and coverage_ok
        and tier1_ok
        and minimums_ok
        and connectivity_ok
        and caps_ok
        and global_failure_mode_ok
        and budget_ok
        and quality_ok
        and output_purity_ok
        and len(failures) == 0
    )

    report = {
        "doctrine_compliance_report": {
            "all_checks_passed": all_checks_passed,
            "internalization_ok": internalization_ok,
            "internalization_linkage_ok": internalization_linkage_ok,
            "mapping_ok": mapping_ok,
            "elements_ok": elements_ok,
            "coverage_ok": coverage_ok,
            "tier1_ok": tier1_ok,
            "minimums_ok": minimums_ok,
            "connectivity_ok": connectivity_ok,
            "caps_ok": caps_ok,
            "global_failure_mode_ok": global_failure_mode_ok,
            "budget_ok": budget_ok,
            "quality_ok": quality_ok,
            "output_purity_ok": output_purity_ok,
            "failures": failures,
        }
    }

    json.dump(report, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
