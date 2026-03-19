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
   - **Section 2 — Extraction Rules (The What):** EXT-01 through EXT-07 define what to capture and what to discard.
   - **Section 3 — Structural Rules (The How):** STR-01 through STR-07 shape every note's format and linking.
   - **Section 4 — Workflow Rules (The When):** WFL-01 through WFL-07 govern process discipline and scope.
   - **Section 5 — Hard Constraints (The Law):** C-01 through C-11 are non-negotiable. Violation = immediate failure.
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

## Usage

```bash
obsidianize "path/to/file.txt"       # Any text/md/pdf file
obsidianize "here is some raw text…" # Inline text
obsidianize --override "note.md"     # Reprocess existing note
obsidianize --override "folder/"     # Reprocess entire folder
```

**Override Mode:** Reads existing note(s), extracts core content, reprocesses through full pipeline, overwrites with updated version. Preserves filename and location; regenerates structure, frontmatter, and links.

---

## Phase 1: Execution

### Workflow Steps

1. **Doctrine Active (Phase 0 complete):** All rules from all 5 doctrine sections are loaded and binding.

2. **Analyze Input:** Identify signal types per EXT-01. Gate with Principle 2 (10-Minute Gate). Discard housekeeping (EXT-05 / C-10).

3. **Multi-Pass Check (EXT-06 / EXT-07):** If input is dense (>~2000 words) or multi-source (e.g., multiple transcripts + lecture notes), perform multi-pass ingestion: Scan → Map → Extract. Build an overview model before atomizing.

4. **Signal Scan (GATE):** For each signal type in EXT-01 (Models, Definitions, Procedures, Arguments, Counter-Evidence, Insights), explicitly scan the input and mark which signals are present. The result is the **Activation Set** — a list of confirmed signal types in this source. If the Activation Set is empty, the input has no signal; stop and report.

5. **Section Palette Scan (GATE):** Walk every H3 in `references/output-structure.md`. For each conditional H3, check if its **Trigger** condition is met by the input. Build a **Section Plan** — a list of which H3 sections will appear under which H2 atomic notes. Every signal in the Activation Set must map to at least one H3 section. If a signal has no section, you have a gap.

6. **Plan Atomic Notes (EXT-04):** One concept = one note. Using the Section Plan, decide how many notes the input warrants. Do not merge disparate ideas into one note.

7. **Structure Each Note:** Apply STR-01 through STR-09. Use `references/output-structure.md` as the skeleton. Populate each H2 with the H3 sections from the Section Plan.

8. **Doctrine Compliance Check (GATE — pre-write):** Before writing, verify against this checklist. **Do not write until all pass:**
   - [ ] Every signal from the Activation Set has a corresponding section in the output
   - [ ] Every section passes the Section Necessity Test (no empty filler)
   - [ ] All code blocks from input are preserved in output (C-02)
   - [ ] No H1 in note body (STR-02)
   - [ ] Backlinks in frontmatter only, never in body (C-11)
   - [ ] Every bullet uses Rule-Based Patterning: `**Name:** Explanation` (STR-04)
   - [ ] Every code block has file path context + language tag (STR-05 / C-07)
   - [ ] Content is synthesized, not transcribed (Principle 1)

9. **Silent Write + Report (C-03 / C-04):**
   - Write each note in a single atomic `write_file` operation.
   - Do NOT output note content to chat.
   - Do NOT emit any planning artifacts, tables, or summaries to chat. The ONLY output allowed is the final `.md` file creation.
   - After writing, report only: filenames created + one-line status.

---

## References

> references are in the CWD of the skill itself which is in `/home/mohamed/.agents/skills/obsidianize-skill/references`
> Must be loaded in Phase 0 before any action.

- `references/doctrine.md` — The Mind (Philosophy), Law (Constraints), and Process. **Supreme Authority — read all 5 sections.**
- `references/output-structure.md` — The Skeleton (Template).
- `references/obsidian-markdown.md` — The Body (Syntax Reference).
