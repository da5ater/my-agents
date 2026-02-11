---
description: how to run the study pipeline (Obsidianize → AnkiFi)
---

# Study Pipeline Workflow

This workflow documents the correct way to use the Obsidianize and AnkiFi agents.

> **IMPORTANT:** Never use these agents as sub-agents (calling one agent from another).
> The sub-agent architecture summarizes input before passing it, which destroys the
> original content. Always invoke them directly.

## Step 1: Obsidianize (Raw → Obsidian Note)

**Purpose:** Transform raw input (transcript, notes, tutorial text) into a structured Obsidian markdown note.

1. Open OpenCode in your vault directory:
   ```bash
   cd /mnt/data/obsidian/gems
   opencode .
   ```
2. Activate the Obsidianize agent (it uses `mode: all`, so just mention it)
3. Provide the raw input in one of these ways:
   - **Paste directly:** Type `obsidianize` then paste your transcript/text
   - **File path:** Type `obsidianize /path/to/raw_input.txt`
   - **Folder:** Type `obsidianize ./folder_of_files`
4. The agent will create a `.md` file in the current directory

## Step 2: Move the Note (Optional)

Move the generated `.md` file to the correct location in your Obsidian vault:
```bash
mv generated_note.md /mnt/data/obsidian/gems/programming/topic/
```

## Step 3: AnkiFi (Obsidian Note → Anki Cards)

**Purpose:** Convert structured markdown notes into Anki flashcard TSV files.

// turbo
1. Navigate to the folder containing your notes:
   ```bash
   cd /mnt/data/obsidian/gems/programming/topic/
   opencode .
   ```
2. Invoke AnkiFi directly:
   - **Single file:** `ankify filename.md`
   - **Current folder:** `ankify .` or `ankify current folder`
   - **Folder with exclusions:** `ankify . --exclude templates`
3. The agent will:
   - Process all `.md` files
   - Generate a unified `.tsv` file
   - Run post-generation validation
   - Report results

## Step 4: Validate & Import

// turbo
1. Validate the output:
   ```bash
   awk -F'\t' '{if (NF != 3) print "FAIL line " NR ": " NF " columns"}' output.tsv
   ```
2. Open Anki → File → Import → Select the `.tsv` file
3. Map columns: Field 1 = Front, Field 2 = Back, Field 3 = obsidian link

## Common Mistakes to Avoid

- ❌ **Don't use as sub-agent** — Input gets summarized
- ❌ **Don't paste transcript into AnkiFi** — It expects structured markdown, not raw text
- ❌ **Don't skip Obsidianize** — The pipeline is: Raw → Obsidianize → AnkiFi
- ✅ **Do open OpenCode in the correct directory** before running
- ✅ **Do check the TSV output** before importing into Anki
