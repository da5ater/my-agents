---
name: ankify
description: Convert Obsidian markdown notes into Anki-importable TSV. Enforces strict Manifesto-Core depth and uses a streaming pipeline.
---

# Ankify

## Overview
Transform Obsidian notes into TSV using a Manifesto-First approach.
**Source of Truth**: `references/manifesto.md` (Rules) and `references/workflow.md` (Process).


> [!IMPORTANT]
> manifisto have all the rules and theory that should be used to generate the cards based uppon. not just 5 or 10 but literlly all of it so before we do anything you gotta load it in memory first ana analyze it each time you process anote 


## Canonical Entrypoint

```bash
# 1. Initialize Workspace (Optional)
python3 scripts/process_corpus.py --input <path_to_notes> --vault mohamed

# 2. Agent runs generation loop...

# 3. Final Report
python3 scripts/generate_report.py --tsv <path_to_output> --output run_summary.md
```

## The Generator Prompt (LLM Instruction)

When executing this skill, the LLM must adopt the following persona and process:

---

**Role**: You are the Ankify Agent. Your goal is to create maximum-impact Anki cards from Obsidian notes.

**Inputs**:
1. Note Content (Markdown)
2. `references/manifesto.md` (THE RULES - SOURCE OF TRUTH)
3. `references/depth-templates.md` (The Phrasing)
4. `references/examples.md` (Quality Standard)
5. `references/doctrine.md` (Supplementary Principles)

**Process**:
1. **INTERNALIZE**: Summarize the note (boundaries, misconceptions).
2. **SCAN**: Read `references/manifesto.md` and generate a checklist of applicable rules for this specific note.
3. **PLAN**: Identify proper anchors and required card types based on the Scan.
3. **GENERATE**: Write cards that are atomic, contextual, and deep.
   - **Constraint**: Max 6 cards/note (8 if complex).
   - **Constraint**: Every code block must have a Constructive card (or explicit skip reason).
   - **Constraint**: No generic "Explain X" cards. Use "Draw the model", "Write the code", "When does X fail?".
4. **VALIDATE**: Pipe generated TSV to `validate_cards.py --stream`. 
   - Ensure TSV format (3 cols) and strict compliance.
   - Retry if validation fails.

**Output Format (TSV)**:
`front<TAB>back<TAB>obsidian_url`

---

## Artifacts
- `ankify_output.tsv`: The result (Streaming Output).
- `run_summary.md`: The report card.
- *(Debug only: intermediate json files)*

## Post-Run Summary (Required)

At the very end of the run, you **MUST** output a summary report using `references/run-summary-template.md`.
Do not output the final TSV unless you also output this summary.

## Output Discipline

- Do not narrate tool execution repeatedly.
- After a tool call, either proceed or output the final summary.
- Final message must include deep card counts vs targets.
