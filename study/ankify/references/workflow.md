# Ankify Canonical Workflow

This document defines the single, authoritative pipeline for transforming Obsidian notes into Anki cards.

**Philosophy**:
1. **Manifesto-First**: `manifesto.md` is the only source of truth for *what* to generate.
2. **LLM-Driven**: We trust the LLM to understand the note and apply the rules. We do not use regex/templates to write content.
3. **Script-Validated**: We use scripts *only* to measure compliance (counts, formatting, banned patterns), not to author content.

## The 5-Step Pipeline

### 1. Parse & Discover
- **Input**: Markdown Note (text).
- **Tooling**: `process_corpus.py` (File discovery), Python String/Regex (Parsing).
- **Process**:
    - Identify code blocks (language, line count).
    - Identify headings (H1/H2/H3).
    - Read full text.
    - **Outcome**: A clean text representation of the note and an inventory of elements.

### 2. Internalize (LLM)
- **Input**: Note Text.
- **Rule**: `manifesto.md` -> Internalization
- **Process**: LLM summarizes the concept, defines boundaries, predicts misconceptions, and links to related concepts.
- **Outcome**: *Conceptual Internalization* (Debug: `internalization.json`).

### 3. Plan (LLM)
- **Input**: Internalization + Inventory + Manifesto Core.
- **Process**:
    - **Step 3.1: Manifesto Scan**: Scan `manifesto.md` and explicitly output a list of *every* Rule ID (e.g., [PR-0038]) that applies to the concepts in this note.
    - **Step 3.2: Selection**: LLM decides *which* concepts serve as anchors.
    - **Step 3.3: Type Check**: LLM selects *which* card types (Tier 1) apply based on `manifesto.md` triggers.

> you have got to use all the manifisto rules . but triggered based on each concept in the note.
    - **Constraint**: Must respect Hard Caps (max 6-8 cards).
- **Outcome**: *Target Budget* (Debug: `card_budget.json`).

### 4. Generate (LLM)
- **Input**: Note + Plan + Breadth/Depth Templates (from `depth-templates.md` and `manifesto.md`).
- **Process**: 
    - LLM generates `front`, `back`, `url` for each card.
    - **Strict Rule**: Every card must cite the Manifesto Rule ID (e.g., `[PR-0014]`) that justifies its existence in the thought process.
    - **Strict Rule**: No generic templates ("Explain how X works"). Use "atomic" prompts.
    - **Strict Rule**: Meaningful content only. No "filler" cards to hit quotas.
- **Outcome**: Raw TSV lines.

### 5. Validate (Script)
- **Input**: Raw TSV.
- **Tooling**: `validate_cards.py --stream`.
- **Checks**:
    - **Format**: 3 columns, no tabs, no raw newlines.
    - **Banned Patterns**: Does it contain "misused" or "end-to-end"? (Reject if yes).
- **Behavior**:
    - **Pass**: Append to `ankify_output.tsv`.
    - **Fail**: Return failure list to LLM -> **GOTO Step 4** (Retry with specific feedback).

## Artifacts
- `ankify_output.tsv`: Final cards.
- `run_summary.md`: Execution report.
- *(Intermediate files like `internalization.json` are optional debug artifacts)*
