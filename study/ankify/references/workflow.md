# Ankify Canonical Workflow

This document defines the single, authoritative pipeline for transforming Obsidian notes into Anki cards.

**Philosophy**:
1.  **Manifesto-First**: `manifesto.md` is the only source of truth for *what* to generate.
2.  **LLM-Driven**: We trust the LLM to understand the note and apply the rules. We do not use regex/templates to write content.
3.  **Script-Validated**: We use scripts *only* to measure compliance (format), not to author content.

## The 5-Step Pipeline

### 1. Parse & Discover
-   **Input**: Markdown Note (text).
-   **Tooling**: `read` (Agent reads file content).
-   **Process**:
    -   Identify code blocks (language, line count).
    -   Identify headings (H1/H2/H3).
    -   Read full text.
    -   **Outcome**: A clean text representation of the note and an inventory of elements. with a highligt of the signal and core conecpts to be used in the cards as a sugestion.

### 2. Internalize (LLM)
-   **Input**: Note Text.
-   **Rule**: `manifesto.md` -> Internalization
-   **Process**: LLM summarizes the concept, defines boundaries, predicts misconceptions, and links to related concepts. pay great ayyention to the code blocks and the signal, and most important atomic logic inside this codeblock
-   **Outcome**: *Conceptual Internalization*.

### 3. Plan (LLM)
-   **Input**: Internalization + Inventory + Manifesto Core.
-   **Process**:
    -   **Step 3.1: Manifesto Scan**: Scan `manifesto.md` and give it your best shot to use as much as possible [sometimes it is not possible to use all the manifesto] from the manifesto to plan the cards.
    -   **Step 3.2: Selection**: LLM decides *which* concepts serve as anchors.
    -   **Step 3.3: Type Check**: LLM selects *which* card types apply based on `manifesto.md` triggers.
    -   **Constraint**: Must respect Hard Caps (max 6-8 cards).
    -   **Constraint**: Must respect the signal and the core concepts.
    -   **Constraint**: Must respect the code blocks and the signal, and most important atomic logic inside this codeblock.
    -   **Constraint**: code blocks has the highest priority in the note
-   **Outcome**: *Target Budget*.

### 4. Generate (LLM)
-   **Input**: Internalization +  Manifesto Core + Plan + `manifesto.md` insights + `examples.md` (patterns & constraints).
-   **Process**:
    -   LLM generates `front`, `back`, `url` for each card.
    -   **Strict Rule**: Every card must map to a Manifesto Rule ID (e.g., `[PR-0014]`) that justifies its existence in the thought process.
    -   **Strict Rule**: No generic templates ("Explain how X works"). Use "atomic" prompts.
    -   **Strict Rule**: Meaningful content only. No "filler" cards to hit quotas.
-   **Outcome**: Raw TSV lines.

### 5. Validate (Script Loop)
-   **Input**: Raw TSV.
-   **Tooling**: `validate_cards.py`.
-   **Checks**:
    -   **Manifesto Compliance**: Checks for banned phrases, bad patterns, and missing fields.
    -   **Format**: 3 columns, no raw newlines.
-   **Behavior**:
    -   **Pass**: Append to `ankify_output.tsv`.
    -   **Fail**: Read stderr for specific line errors -> **GOTO Step 4** (Fix specific cards and retry until clean).

## Artifacts
-   `ankify_output.tsv`: Final cards.

## Post-Run Summary (Required)
At the very end of the run, you **MUST** output a summary report using `references/run-summary-template.md`.
- make sure the .tsv file is in given input path