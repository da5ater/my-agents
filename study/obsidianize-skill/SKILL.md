---
name: obsidianize
description: >
  Turn any input into an Obsidian-ready note using the obsidianize doctrine:
  arbitration -> signal-based activation -> budgeted plan -> validated output (fixed W4 + DeepDrill).
  Trigger when the user says "obsidianize ..." or asks to convert raw text/files into an Obsidian note.
---

# Obsidianize

Follow the 5-stage Obsidianize pipeline: (1) extract elements + classify, (2) produce Tier-1 rule_application_plan for all Tier-1 rules, (2.5) produce internalization_report, (2.7) produce extraction_budget_plan, (3) generate the note, (4) validate against doctrine checklist and minimums/caps, (5) write the file. Do not generate final output until internalization_report + extraction_budget_plan exist. If any doctrine check fails, do targeted regeneration only, max 3 attempts.

## Doctrine Philosophy (Authority)
- **Cognition over transcription:** Notes reshape thinking, not store text. This derives PR-0003 and PR-0046.
- **Signal gating prevents hallucination:** Only create structure when signal is explicit. This derives signal-only extraction and section necessity tests.
- **Budgets prevent explosion:** Depth comes from prioritization under ceilings, not extra breadth. This derives arbitration lock and density ratio.
- **Verification must be executable:** If a check can be scripted, it must be validated by script.
- **Atomicity enables reuse:** One core idea per H2; declarative statements enable downstream extraction.

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

## Execution Mode (Fixed)
This skill always runs at maximum depth and always writes to file.

- **emit=file only:** Write the final note as a `.md` file (single atomic write). If file-writing capability is absent, stop and report the limitation.
- **Chat output:** Use chat only for process artifacts (plans, audits, compliance). The file contains only the final note.


## User Controls (Optional)
- `--title "..."` (override derived title if needed)
- `--batch` (enable folder processing)
- `--max-files N` (limit batch size)

## Operational Quickstart (How to NOT get stuck)
1) **Phase 1 (silent):** Read everything -> map structure -> extract elements (definitions, procedures, code, models, counter-evidence) -> de-contextualize -> Feynman-check.
2) **Depth:** Fixed to maximum depth (W4 + DeepDrill).
3) **Arbitration:** Apply priority order; lock:
   - Activation Set (eligible + signal-present rules only)
   - Budgeted Section Plan (must fit ceilings; no post-trim)
4) **Generate required pre-generation artifacts** (stage2_analysis_artifacts, internalization_report, extraction_budget_plan, doctrine_compliance_report) and emit a summarized view in chat.
5) **Generate note string** using the output structure rules + Obsidian Markdown syntax.
6) **Validate note string** via validator script.
7) **Write file** in a single atomic operation.


## Output Requirements
- Always follow `05-output-structure.md` hierarchy rules (no H1 in body; H2 sections; H3 subsections).
- Conditional sections must pass the "section necessity test" (only add if new information beyond Notes).
- No fabrication; signal-only extraction.
- If code exists, code must be runnable and include context and file path citation.
- Chat contains process artifacts only; the file contains only the final note.

## Troubleshooting (Common failure loops)
If you feel "blocked":
- You are probably trying to activate too many rules. Re-run Arbitration:
  - Re-check signal and eligibility (W4).
  - Drop to minimum viable structure.
  - Lock a smaller Budgeted Section Plan.
- If the runtime can't write files:
  - Stop and report the limitation.
