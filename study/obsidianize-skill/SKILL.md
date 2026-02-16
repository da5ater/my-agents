---
name: obsidianize
description: Convert any input (text, files, transcripts) into high-signal, atomic Obsidian notes. Use when the user wants to structure information, create technical documentation, or extract concepts into a permanent knowledge base.
---

# Obsidianize

Transform raw input into production-grade, structured technical documentation using a Manifesto-First approach.

## Usage

```bash
obsidianize "path/to/file.txt"
obsidianize "here is some raw text..."
```

## Workflow

> refrences are in the CWD of the skill itself which is in `/home/mohamed/.config/opencode/skills/obsidianize-skill/references`

1.  **Analyze Context:** Read `references/doctrine.md` for core philosophy, constraints, and process.
2.  **Plan Structure:** Use `references/output-structure.md` to determine the note layout.
3.  **Execute:**
    *   Synthesize content (Cognition over Transcription).
    *   Enforce the 10-Minute Gate (High Signal).
    *   Write the final `.md` file to the current directory.
    *   **Silent Execution:** Do NOT output note content to chat. Only the file.

## References

*   `references/doctrine.md`: The Mind (Philosophy), Law (Constraints), and Process.
*   `references/output-structure.md`: The Skeleton (Template).
*   `references/obsidian-markdown.md`: The Body (Syntax Reference) - Load if complex formatting is needed.
