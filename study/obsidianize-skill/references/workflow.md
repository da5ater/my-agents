# Workflow: The Obsidianize Doctrine (v3)

This workflow defines the **strict execution path** for transforming raw input into high-signal Obsidian notes. It enforces the `manifesto.md` as the supreme authority on rules and `obsidian-markdown.md` as the authority on syntax.

> [!IMPORTANT] DOCTRINE HIERARCHY
> 1.  **Manifesto (`manifesto.md`)**: The "Mind" - Contains ALL rules for thinking, extraction, and synthesis.
> 2.  **Constraints (`obsidian-markdown.md`)**: The "Body" - Contains ALL rules for formatting and syntax.
> 3.  **Template (`output-structure.md`)**: The "Skeleton" - Contains the required output structure.

## Phase 0: BOOT (Kernel Load)
1.  **Load Process**: Read `references/workflow.md`.
2.  **Load Logic**: Read `references/manifesto.md`.
3.  **Load Safety**: Read `references/constraints.md`.


## Phase 1: Doctrine Loading (The Setup)

Before processing ANY content, ensure Phase 0 is complete. Then:

1.  **Load Rules**: Read `reference/manifesto.md`. This is the Single Source of Truth.
2.  **Load Syntax**: Read `reference/obsidian-markdown.md`.
3.  **Load Template**: Read `reference/output-structure.md`.
4.  **Load Constraints**: Read `reference/constraints.md`.

## Phase 2: Execution (The Process)

### Step 1: Input Analysis & Manifesto Scan
**Goal**: Understand the input and identify which Doctrine Rules apply.

1.  Read the Raw Input (Text, Transcript, File).
2.  **Manifesto Scan**: Scan `manifesto.md` for rules applicable to this specific content.
    *   *Does this require a creative challenge? (Rule X)*
    *   *Is this a procedure? (Rule Y)*
    *   *Is this a conceptual definition? (Rule Z)*
3.  **Signal Check**: Verify that the input actually contains the signal required to trigger these rules. Do not hallucinate signal.

### Step 2: Structural Planning
**Goal**: Map the valid signal to the `output-structure.md`.

1.  Select the `output-structure.md` template.
2.  Identify which **Conditional Sections** (H3) are triggered based on the Manifesto Rules and Input Signal.
3.  **Constraint Check**: Ensure the plan adheres to `obsidian-markdown.md` (e.g., no H1 in body, correct callout syntax).

### Step 3: Drafting (The Synthesis)
**Goal**: Write the note.

1.  **De-contextualize**: Strip original context (e.g., "In this video...", "The speaker says...").
2.  **Re-contextualize**: Apply the "Identity" (Senior Engineering Mentor) to rewrite the content as a permanent resource.
3.  **Write**: detailed, atomic, and strictly following the `obsidian-markdown.md` syntax.
4.  **Cite**: If a rule from `manifesto.md` was key to a specific section's inclusion, you may internally reference it to ensure compliance, but do not clutter the final note with debug info.

## Phase 3: Validation (The Gate)

Before finalizing, verify:

1.  **Manifesto Compliance**: Did we follow the rules we identified in Step 1?
2.  **Syntax Compliance**: Is the Markdown valid according to `obsidian-markdown.md`?
3.  **Structure Compliance**: Does it match `output-structure.md`?
4.  **Hard Constraint Compliance**: Did we violate any laws in `constraints.md`?


## Output Generation

- **Emit File**: Write the final `.md` file to the directory.
- **Chat Output**: Confirm completion.
