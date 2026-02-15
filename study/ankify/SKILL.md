---
name: ankify
description: Convert Obsidian markdown notes into Anki-importable TSV. REQUIRED: Must enforce doctrine depth (Model/FailureMode/Negation/Synthesis), perform full pipeline artifacts (internalization, budget, compliance), and use conversion quotas. Do not produce purely constructive decks.
---

# Ankify
> important note : other than the folder being processed, this skill is entirely separate from obsidianize. It does not share doctrine, gating, or structure. It is a standalone skill that takes Obsidian notes as input and produces TSV for Anki. Do not apply obsidianize rules or structure to ankify output.
> > meanning all the references and scripts are in folder of the skill which is in the same folder as this SKILL.md, not shared with obsidianize.[inside the skills folder which is in the opencode configuration folder]



## Overview
Transform Obsidian notes into TSV with anchored depth and strict caps.
`references/manifesto_core.md` is the runtime rule-set and is execution-blocking.

## Core Workflow (Non-Negotiable)

Execute these steps verbatim. **Do not skip artifacts.**

1. **Load Rules**: Read `references/manifesto_core.md` and `references/doctrine.md`.
2. **Discovery**: Identify input mode and build `file_manifest`.
3. **Analysis**: Parse note and produce `element_inventory` and anchors.
4. **Internalization**: Generate `internalization_report` (Summary, Boundaries, Misconceptions, Links).
5. **Planning**: Create `card_budget_plan` and `rule_application_plan`.
6. **Generation**: Generate anchored cards using `references/depth-templates.md`.
7. **Enforcement Loop (Iterate until compliant)**:
   - Compute counts and quality checks.
   - **Convert** shallow cards by replacement (front + back) to meet missing types.
   - **Append** only if conversion pool is exhausted and total < max cap.
   - Re-validate.
   - Repeat up to **MAX_ITER (5)** times.
8. **Serialization**: Write TSV (exactly 3 columns per line).
9. **Validation**: Run `validate_tsv.sh` AND `validate_cards.py` (blocking).

**Best-Effort Protocol**: If compliance still fails after **5 iterations**, output best-effort TSV and mark **FAIL** in the final summary.

## Manifesto Enforcement (Blocking)

- `references/manifesto_core.md` is not informational. If any rule fails validation, set `quality_ok=false` and fail the run.

## Depth Enforcement (Anchored, Per-Card)

- No statistical depth ratios or cross-note quotas.
- Deep cards must be anchored to note tokens and use closed prompts.
- Q/A alignment is required for model/compare/negation prompts.

## Conversion Rules (Replace, Don't Grow)

- Replacement is mandatory.
- Append only if **total_cards < max_total** and no eligible shallow cards remain.

## Hard Caps

- Basic notes: max 6 cards.
- High-complexity notes: max 8 cards (only when heuristic flags high complexity).

## TSV Stability (Non-Negotiable)

- Every line: `front\tback\turl\n` (exactly 3 columns).
- No tabs inside fields.
- Replace raw newlines inside fields with `<br>`.
- Validation failure stops the run.

## References

1. `references/manifesto_core.md`: Runtime rules (blocking).
2. `references/doctrine.md`: Source of truth.
3. `references/depth-templates.md`: **REQUIRED** phrasing for deep cards.
4. `references/run-summary-template.md`: Format for the mandatory final output.
5. `references/schema.md`: Executable rules.
6. `references/implementation.md`: Pipeline details.

## Required Artifacts

- file_manifest
- element_inventory
- internalization_report (Must exist before generation)
- card_budget_plan
- doctrine_compliance_report (Must pass all checks)
- run_summary.md
- manifesto_actualization_report.md

## Post-Run Summary (Required)

At the very end of the run, you **MUST** output a summary report using `references/run-summary-template.md`.
Do not output the final TSV unless you also output this summary.

## Output Discipline

- Do not narrate tool execution repeatedly.
- After a tool call, either proceed or output the final summary.
- Final message must include deep card counts vs targets.
