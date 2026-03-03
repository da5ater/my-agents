---
name: obsidianize
description: Convert any input (text, files, transcripts) into high-signal, atomic Obsidian notes. Use when the user wants to structure information, create technical documentation, or extract concepts into a permanent knowledge base.
---

# Obsidianize

Transform raw input into production-grade, structured technical documentation using a manifesto-first approach.

## Phase 0: Initialization (Bland Mode — Always Runs First)

> **This phase fires automatically on EVERY invocation, before any processing — with or without a target.**

When the skill is activated, the **very first action** is to load and fully internalize all three references:

1. Read `references/doctrine.md` — internalize ALL five sections as active rules:
   - **Section 1 — Core Doctrine (The Mind):** The 5 Principles govern every synthesis decision. Apply them all.
   - **Section 2 — Extraction Rules (The What):** EXT-01 through EXT-05 define what to capture and what to discard.
   - **Section 3 — Structural Rules (The How):** STR-01 through STR-07 shape every note's format and linking.
   - **Section 4 — Workflow Rules (The When):** WFL-01 through WFL-05 govern process discipline and scope.
   - **Section 5 — Hard Constraints (The Law):** C-01 through C-12 are non-negotiable. Violation = immediate failure.
2. Read `references/output-structure.md` — internalize the note template and atomic section pattern.
3. Read `references/obsidian-markdown.md` — internalize all valid Obsidian syntax.

> **Doctrine Priority:** The doctrine is the supreme authority. ALL 5 sections are mandatory and equally binding. The Hard Constraints (Section 5) are the floor — not the ceiling. Sections 1–4 are not optional background reading; they are active rules applied to every decision.

**If invoked with no target** (e.g., `/obsidianize` alone):
- Complete the three reads above silently.
- Respond in chat only: **"Ready. Give me your source."**
- Do nothing else. Wait for input.

**If invoked with a target** (e.g., `/obsidianize "some text"`):
- Complete the three reads silently, then proceed immediately to Phase 1.

---

## Phase 1: Execution

### Create New Notes
```bash
obsidianize "path/to/file.txt"
obsidianize "path/to/file.md"
obsidianize "path/to/file.pdf"
obsidianize "here is some raw text..."
```

### Reprocess Existing Notes (Override Mode)
```bash
obsidianize --override "path/to/existing/note.md"
obsidianize --override "path/to/existing/folder/"
```

**Override Mode Behavior:**
- **Single file**: Read the existing note, extract its core content, reprocess through the workflow, overwrite with updated version
- **Folder**: Recursively process all `.md` files, apply doctrine rules, overwrite each note
- **Preserves**: Original filename, location in vault
- **Regenerates**: Content structure per current doctrine, frontmatter, links, formatting

### Workflow Steps

1. **Doctrine Active (Phase 0 complete):** All rules from all 5 doctrine sections are loaded and binding.
2. **Analyze Input:** Identify signal types per EXT-01. Gate with Principle 2 (10-Minute Gate). Discard housekeeping (EXT-05 / C-10).
3. **Plan Atomic Notes (EXT-04):** One concept = one note. Decide how many notes the input warrants and what atomic section each covers. Do not merge disparate ideas into one note.
4. **Structure Each Note:** Apply STR-01 through STR-07. Use `references/output-structure.md` as the skeleton.
5. **Silent Write (C-03 / C-04):**
   - Synthesize content — never transcribe (Principle 1).
   - Write each note in a single atomic `write_file` operation.
   - Do NOT output note content to chat. Only write the file.
6. **Report:** After writing, report only: filenames created + one-line status. Nothing else in chat.

---

## References

> references are in the CWD of the skill itself which is in `/home/mohamed/.config/opencode/skills/obsidianize-skill/references`
> Must be loaded in Phase 0 before any action.

- `references/doctrine.md` — The Mind (Philosophy), Law (Constraints), and Process. **Supreme Authority — read all 5 sections.**
- `references/output-structure.md` — The Skeleton (Template).
- `references/obsidian-markdown.md` — The Body (Syntax Reference).
