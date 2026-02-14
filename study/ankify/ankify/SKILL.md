---
name: ankify
description: Convert Obsidian markdown notes into Anki-importable TSV using the ANKIFY schema. Use when the user asks to Ankify a file or folder, generate TSV for Anki, apply ANKIFY card rules, or build obsidian:// links for a vault-bound export.
---

# Ankify

## Overview
Transform Obsidian notes into a single TSV file that follows the ANKIFY schema, including card-type mapping, coverage rules, and Obsidian deep links.

## Core Workflow

1. Identify input mode and output naming.
2. Load doctrine first, then schema, then implementation, then examples.
3. Extract structural elements and map to card types.
4. Produce internalization_report and card_budget_plan.
5. Generate cards that satisfy coverage, depth, and budget constraints.
6. Run doctrine compliance checks and targeted regeneration if needed.
7. Serialize into a TSV that passes validation.

## References

Read these in order based on need:

1. `references/doctrine.md`: Source of truth for card intent, mapping, and quality. Load this before any schema checks.
2. `references/schema.md`: Executable rules, ordering, and conflicts. If a schema rule conflicts with doctrine, follow doctrine and treat the schema rule as stale.
3. `references/implementation.md`: Pipeline steps, input modes, card mapping, TSV format, validation steps.
4. `references/examples.md`: Non-normative examples for patterns and edge cases.

## Generation Notes

- Treat H2 sections as atomic concepts, and H3 subsections as card-type cues per schema mapping.
- Ensure coverage: every structural element yields at least one card; do not silently skip.
- Enforce atomicity: one idea per card; code answers no more than 6 lines.
- Avoid yes/no, list-of-things, or recognition-only prompts.
- Always include the Obsidian deep link in column 3, with the vault name and URL encoding per schema.
- For code answers, serialize with HTML-safe `<pre><code>` and replace newlines/spaces as specified.
- Run the doctrine compliance checklist before TSV serialization.
- Use targeted regeneration only: add missing classes or convert excess cards per doctrine; do not rewrite valid cards unless TSV validation fails.
- Apply POST-GEN PRUNE before serialization to enforce per-note caps and remove redundancy.

## Required Artifacts

- file_manifest
- element_inventory
- rule_application_plan
- internalization_report
- card_budget_plan
- doctrine_compliance_report

## Serialization and Validation

- TSV must have exactly 3 columns per line, no raw newlines, and no literal tabs in content.
- Run `scripts/validate_tsv.sh` and fix any failures before final output.

## Output

- Produce one unified TSV file per invocation.
- Do not include rule metadata or diagnostic chatter inside TSV rows.
