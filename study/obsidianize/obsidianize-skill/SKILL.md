---
name: obsidianize
description: >
  Turn any input into an Obsidian-ready note using the obsidianize doctrine:
  arbitration -> weight/mode gating -> signal-based activation -> budgeted plan -> validated output.
  Trigger when the user says "obsidianize ..." or asks to convert raw text/files into an Obsidian note.
---

# Obsidianize

Follow the 5-stage Ankify pipeline: (1) extract elements + classify, (2) produce Tier-1 rule_application_plan for all Tier-1 rules, (2.5) produce internalization_report, (2.7) produce card_budget_plan, (3) generate cards, (4) validate against doctrine checklist and minimums/caps, (5) serialize. Do not generate final output until internalization_report + card_budget_plan exist. If any doctrine check fails, do targeted regeneration only, max 3 attempts.

## Required References (Load First, In Order)
1. `references/01-identity-scope.md`
2. `references/02-arbitration-and-weighting.md`
3. `references/03-activation-and-budget.md`
4. `references/04-rule-library.md`
5. `references/05-output-structure.md`
6. `references/obsidian-markdown.md` (syntax only)

## Authority
- `references/01-identity-scope.md` through `references/05-output-structure.md` are the single source of truth for doctrine, gating, and structure.
- `references/obsidian-markdown.md` is syntax-only (formatting correctness), not doctrine.

## Execution Modes (IMPORTANT)
This skill supports two execution modes:

- **emit=chat (default):** Return the final note as Markdown in chat.
- **emit=file:** If file-writing capability exists, write the final note as a `.md` file (single atomic write). If not available, fallback to emit=chat.

Users can specify:
- `--emit chat`
- `--emit file`


## User Controls (Optional)
- `--weight W1|W2|W3|W4` (otherwise auto-classify per doctrine)
- `--mode Lightweight|Tactical|Research|DeepDrill` (otherwise auto-detect per doctrine)
- `--title "..."` (override derived title if needed)
- `--batch` (enable folder processing)
- `--max-files N` (limit batch size)

## Operational Quickstart (How to NOT get stuck)
1) **Phase 1 (silent):** Read everything -> map structure -> extract elements (definitions, procedures, code, models, counter-evidence) -> de-contextualize -> Feynman-check.
2) **Weight + Mode:** Auto-classify weight. Round DOWN when unsure. Respect mode limits.
3) **Arbitration:** Apply priority order; lock:
   - Activation Set (eligible + signal-present rules only)
   - Budgeted Section Plan (must fit ceilings; no post-trim)
4) **Generate required pre-generation artifacts** (stage2_analysis_artifacts, internalization_report, card_budget_plan, doctrine_compliance_report) and emit a summarized view in output before the note.
5) **Generate note** using the output structure rules + Obsidian Markdown syntax.
6) **Validate** with guardrail audit.


## Output Requirements
- Always follow `05-output-structure.md` hierarchy rules (no H1 in body; H2 sections; H3 subsections).
- Conditional sections must pass the "section necessity test" (only add if new information beyond Notes).
- No fabrication; signal-only extraction.
- If code exists, code must be runnable and include context and file path citation.

## Troubleshooting (Common failure loops)
If you feel "blocked":
- You are probably trying to activate too many rules. Re-run Arbitration:
  - Re-check weight (round down).
  - Drop to minimum viable structure.
  - Lock a smaller Budgeted Section Plan.
- If the runtime can't write files:
  - Use emit=chat (default) and manually save into Obsidian.
