---
name: obsidianize
description: Convert any input (text, files, transcripts) into high-signal, atomic Obsidian notes. Use when the user wants to structure information, create technical documentation, or extract concepts into a permanent knowledge base.
---

# Obsidianize

Transform raw input into production-grade, structured technical documentation using a manifesto-first approach.

## Usage

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

## Workflow

> refrences are in the CWD of the skill itself which is in `/home/mohamed/.config/opencode/skills/obsidianize-skill/references`

1.  **Analyze Context:** Read `references/doctrine.md` for core philosophy, constraints, and process.
2.  **Plan Structure:** Use `references/output-structure.md` and `references/obsidian-markdown.md` to determine the note layout.
3.  **Execute:**
    *   Synthesize content (Cognition over Transcription).
    *   Enforce the 10-Minute Gate (High Signal).
    *   Enforce the usage of the doctrine as the main brain of the note where we write notes based on the doctrine.
    *   Write the final `.md` file to the current directory.
    *   **Silent Execution:** Do NOT output note content to chat. Only the file.

## References
> must be loaded before the skill starts
*   `references/doctrine.md`: The Mind (Philosophy), Law (Constraints), and Process.
*   `references/output-structure.md`: The Skeleton (Template).
*   `references/obsidian-markdown.md`: The Body (Syntax Reference) - 

