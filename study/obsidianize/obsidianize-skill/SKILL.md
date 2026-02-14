---
name: obsidianize
description: Turn any input into an Obsidian note using the obsidianize rule system. Trigger when the user says `obsidianize [input]` or provides `obsidianize [path/to/input]`, or asks to obsidianize a file/folder or raw transcript into a structured .md note.
---

# Obsidianize

## Rule Source

- Read the canonical rules from `obsidianize.md` in the working directory if it exists.
- Focus on the "Rule Library / Knowledge Base" and "Output Structure" sections.
- If the file is missing, follow the condensed workflow below.

## Core Workflow (Condensed)

0. Detect input mode:
   - Raw text/transcript
   - File path (read file)
   - `obsidianize <folder>` (process each file)
1. Read the full input before writing anything.
2. Classify weight (W1–W4) and mode; round down when unsure.
3. Build an activation set: only rules with explicit signal may fire.
4. Plan a budgeted section plan within structural ceilings.
5. Generate the note using the Output Structure template.
6. Write the final note in a single file creation operation.
7. Respond only with: `Created <filename>.md`.

## Output Contract

- Write a single `.md` file in the current working directory.
- Filename derives from the main topic; sanitize unsafe characters.
- Do not include an H1 in the body.
- Use YAML frontmatter (aliases/backlinks) at top.
- Use H2 for atomic sections, H3 for conditional subsections.
- Only create conditional sections when explicit signal exists.
- Apply the 10-minute gate: exclude trivial content.
- No fabrication. Rephrase in plain language.

## Conditional Sections (Only When Signal Exists)

- Distinctions & Negations
- Counter-Evidence & Disagreements
- Definitions (only critical jargon)
- Configuration (setup/install/env)
- Procedures & Workflows
- Code Implementation (file path + runnable code + context)

## Tooling Constraints

- Use the file creation tool to write the full note in one operation.
- Do not edit after writing; no incremental writes.
- Do not output the note content in chat.
