---
name: ankify
description: Convert Obsidian markdown notes into high-quality Anki cards using the Manifesto-Core methodology. Enforces strict atomicity, context, and depth. Trigger with `/ankify <path>` to process a directory.
---

# Ankify

Transform Obsidian notes into rigorous Anki cards.

## Batch Execution Trigger

**Trigger**: `/ankify <path>` (e.g., `/ankify .` or `/ankify /path/to/notes`)

When this command is invoked, you **MUST** execute the following workflow immediately:

1.  **Discover**: Run `python3 scripts/process_corpus.py --input <path>` to get the list of notes.
2.  **Iterate**: For each note in the list, execute the **5-Step Pipeline** (Internalize -> Plan -> Generate -> Validate) defined in `references/workflow.md`.
3.  **Stream**: Valid cards must be piped to `scripts/validate_cards.py` and appended to `ankify_output.tsv` in real-time.
4.  **Report**: After all notes are processed, output a final summary using `references/run-summary-template.md`.

## Core Rules & Process

This skill enforces a **Manifesto-First** approach. You must consult the following references before generating any content:

> refrences are in the CWD of the skill itself which is in `/home/mohamed/.config/opencode/skills/ankify/references`

1.  **Read the Rules**: `references/manifesto.md` (The absolute source of truth for card quality).
2.  **Follow the Process**: `references/workflow.md` (The step-by-step generation pipeline).
3.  **Use Templates**: `references/depth-templates.md` (Required phrasing patterns).
4.  **See Examples**: `references/examples.md` (High-quality output examples).

## Tools & Usage

### 1. Discover Notes
```bash
python3 scripts/process_corpus.py --input <path_to_notes>
```

### 2. Generate Cards (Per Note)
For each note, follow the **5-Step Pipeline**:
1.  **Read** the note and `manifesto.md`.
2.  **Internalize** key concepts and boundaries.
3.  **Plan** the card budget and types.
4.  **Generate** TSV lines (Front/Back/URL).
5.  **Validate** using the script:

```bash
# Pipe your generated TSV block to the validator
echo "<your_tsv_content>" | python3 scripts/validate_cards.py --vault mohamed --default-file "<relative_path_to_note>" >> ankify_output.tsv
```

### Output
-   **Success**: Append valid output to `ankify_output.tsv`.
-   **Failure**: If validation fails (check stderr), correct the cards and retry.
-   **Summary**: After processing all notes, write a summary report using `references/run-summary-template.md`.

## Critical Constraints
-   **No "Explain X" cards**.
-   **No Yes/No questions**.
-   **No Orphan Pronouns** ("It", "This").
-   **Strict TSV Format**: `Front <TAB> Back <TAB> URL`. No raw newlines in fields (use `<br>`).
