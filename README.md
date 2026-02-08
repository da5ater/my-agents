# Agents Repository

This repository serves as a central collection for custom AI agents designed to automate and enhance personal workflows. 

Currently, it hosts two specialized "study" agents that function as a pipeline for knowledge management and retention. These agents are designed to work together to transform raw information into long-term knowledge.

## Study Agents

These agents operate on a strict "Phased Execution" model to ensure high-quality, deterministic outputs. They are built with a shared knowledge base grounded in principles of effective learning, Zettelkasten, and spaced repetition.

### 1. Obsidianize (Note Architect)
**Location:** `study/obsidianize.md`

**Role:** Expert Technical Editor & Knowledge Manager.

**Purpose:** 
Transforms unstructured raw input—such as transcripts, loose notes, or tutorial text—into production-grade, meticulously structured Obsidian Markdown notes. It acts as the "intake" mechanism for your knowledge base.

**Key Features:**
- **De-contextualization:** Strips ideas of their original source context to create universal principles.
- **Atomic Structuring:** Breaks content into logical, atomic sections with clear headers (H2/H3).
- **Rule-Based Patterning:** Uses declarative statements and specific formatting to make notes machine-parsable and easy to read.
- **Automatic Metadata:** Generates descriptive filenames and YAML frontmatter.

**Input Modes:**
- Raw text/transcript
- Single file path
- Folder of files

**Output:** 
- Clean, structured `.md` files in the current working directory, ready for your Obsidian vault.

---

### 2. Ankify (Memory Engineer)
**Location:** `study/ankify.md`

**Role:** Headless Technical TSV Compiler.

**Purpose:**
Takes existing Markdown notes (like those created by Obsidianize) and converts them into high-quality Anki flashcards. It focuses on deep conceptual integration and interview readiness.

**Key Features:**
- **3-Phase Pipeline:** Analysis -> Rule-Driven Generation -> TSV Validation.
- **Interview Readiness:** Generates questions that prepare users for senior technical interviews (e.g., "Write the code," "Explain the concept").
- **Context Docking:** Ensures every card is anchored to existing knowledge.
- **Strict Validation:** Enforces a rigid TSV format (`FRONT <tab> BACK <tab> URL`) compatible with Anki.
- **Deep Linking:** Includes `obsidian://` links back to the source note for every card.

**Input Modes:**
- Single `.md` file
- Current directory (`.`)
- Specific folder

**Output:**
- `.tsv` files ready for direct import into Anki.

## Workflow Integration

These two agents form a cohesive study loop:
1. **Input:** Paste raw learning material into **Obsidianize**.
2. **Structure:** Obsidianize creates a permanent note in your vault.
3. **Retain:** Run **Ankify** on that note to generate spaced-repetition cards.
4. **Review:** Import the TSV into Anki to ensure long-term retention.
