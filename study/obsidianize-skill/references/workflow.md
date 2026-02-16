# Workflow: The Obsidianize Doctrine (v3)

This workflow defines the **strict execution path** for transforming raw input into high-signal Obsidian notes. It enforces the `manifesto.md` as the supreme authority on rules and `obsidian-markdown.md` as the authority on syntax.

> [!IMPORTANT] DOCTRINE HIERARCHY
> 1.  **Manifesto (`manifesto.md`)**: The "Mind" - Contains ALL rules for thinking, extraction, and synthesis.
> 2.  **Constraints (`obsidian-markdown.md`)**: The "Body" - Contains ALL rules for formatting and syntax.
> 3.  **Template (`output-structure.md`)**: The "Skeleton" - Contains the required output structure.

## Phase 1: BOOT (Kernel Load)
1.  **Load Process**: Read `references/workflow.md`.
2.  **Load Logic**: Read `references/manifesto.md`.
3.  **Load Safety**: Read `references/constraints.md`.

## Phase 2: INTERNALIZE (Input Analysis)

1.  Read the Raw Input.
2.  **Signal Check**: Verify that the input actually contains the signal required to trigger these rules. Do not hallucinate signal.

## Phase 3: PLAN (Structure Mapping)

1.  **Manifesto Scan**: Scan `manifesto.md` for rules applicable to this specific content.
2.  **Template Select**: Select sections from `output-structure.md` that match the signal.
3.  **Constraint Check**: Ensure the plan adheres to `obsidian-markdown.md`.

## Phase 4: GENERATE (The Synthesis)
**Goal**: Write the note.

1.  **De-contextualize**: Strip original context (e.g., "In this video...", "The speaker says...").
2.  **Re-contextualize**: Apply the "Identity" (Senior Engineering Mentor) to rewrite the content as a permanent resource.
3.  **Write**: detailed, atomic, and strictly following the `obsidian-markdown.md` syntax.
4.  **Cite**: If a rule from `manifesto.md` was key to a specific section's inclusion, you may internally reference it to ensure compliance, but do not clutter the final note with debug info.

## Phase 5: VALIDATE (The Gate)

Before finalizing, verify:

1.  **Manifesto Compliance**: Did we follow the rules we identified in Step 1?
2.  **Syntax Compliance**: Is the Markdown valid according to `obsidian-markdown.md`?
3.  **Structure Compliance**: Does it match `output-structure.md`?
4.  **Hard Constraint Compliance**: Did we violate any laws in `constraints.md`?


## Output Generation

- **Emit File**: Write the final `.md` file to the directory.
- **Chat Output**: Confirm completion.
