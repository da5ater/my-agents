---
name: ankify
description: Convert Obsidian markdown notes into high-quality Anki cards using the Manifesto-Core methodology. Enforces strict atomicity, context, and depth. Trigger with `/ankify <path>` to process a directory.
---

# Ankify

Transform Obsidian notes into rigorous Anki cards.

## Batch Execution Trigger

**Trigger**: `/ankify <path>` (e.g., `/ankify .` or `/ankify /path/to/notes`)

When this command is invoked, you **MUST** execute the following workflow immediately:

1.  **Discover**: read all notes in the given path [input], to get the list of notes.
2.  **Iterate**: For each note in the list, execute the **5-Step Pipeline** (Internalize -> Plan -> Generate -> Validate) defined in `references/workflow.md`.
3.  **Validate** [loop after .TSV is done]: run the validator script on the generated TSV lines, when error occurs correct the cards and retry. 
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
# List all notes in the given path
find <path> -type f -name "*.md"
```

### 2. Generate Cards (Per Note)
For each note, follow the **5-Step Pipeline**:
1.  **Read** the note and `references/manifesto.md`.
2.  **Internalize** key concepts and boundaries.
3.  **Plan** how are going to apply the manifesto to the note.
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
-   **Manifesto-First**: You must follow the manifesto as the brain to create the cards.
-   **No "Explain X" cards**.
-   **No Yes/No questions**.
-   **No Orphan Pronouns** ("It", "This").
-   **Strict TSV Format**: `Front <TAB> Back <TAB> URL`. No raw newlines in fields (use `<br>`).
-   **Validation Loop**: You must run the validation script and fix any reported errors until the script passes with exit code 0.

