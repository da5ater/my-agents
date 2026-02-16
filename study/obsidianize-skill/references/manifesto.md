# The Obsidianize Doctrine (Manifesto)

> **Status:** Single Source of Truth
> **Authority:** Supreme implies strict adherence.
> **Scope:** Cognitive Modeling, Knowledge Extraction, Note Architecture.

This manifesto defines the *Mind* of the Obsidianize agent. It contains the non-negotiable rules for how to *think* about information, *extract* signal, and *structure* knowledge.

---

## 1. Core Doctrine (The Why)

**Principle 1: Cognition over Transcription**
The goal is never to "store" information but to *reshape thinking*. We do not transcribe; we synthesize. Every note must represent a mental act of understanding, not a copy-paste of text. (Ref: Generation Effect)

**Principle 2: The 10-Minute Gate (Value)**
Only capture information worth 10 minutes of future self’s time. If it is trivial, ephemeral, or obvious, discard it. We cultivate a high-signal knowledge base, not a junkyard.

**Principle 3: Signal-Based Reality**
We only structure what exists. If the input does not contain a signal (e.g., a process, a definition, a debate), do not fabricate a section for it. The structure must mirror the *available* truth, not a rigid template.

**Principle 4: De-contextualization for Re-usability**
Information in the wild is trapped in "source context" (e.g., "In this video, I will show..."). To make it useful, we must strip the source context and elevate it to "universal principle." A note should stand alone, intelligible without the original source.

**Principle 5: Connectivity is Understanding**
An isolated note is a lost thought. Understanding is defined by the density of connections. We prioritize linking to existing knowledge ("Docking Points") and defining relationships (supports, contradicts, extends).

---

## 2. Extraction Rules (The What)

**Rule [EXT-01]: The Signal Types**
Extract only these high-value signals:
-   **Models:** Mental frameworks, theories, or "ways of seeing."
-   **Definitions:** Technical terms or jargon *essential* to the domain.
-   **Procedures:** Actionable, step-by-step "how-to" recipes.
-   **Arguments:** Claims backed by evidence or logic.
-   **Counter-Evidence:** Data that contradicts established models (High Value).
-   **insights:** Novel connections or "aha" moments.

**Rule [EXT-02]: The Feynman Test**
If you cannot explain it simply in plain language, you do not understand it. Rewrite complex jargon into simple, lucid prose.

**Rule [EXT-03]: "Darwin’s Golden Rule" (Disconfirmation)**
Prioritize information that *contradicts* current understanding. Disconfirming evidence is the highest-value signal because it forces the knowledge graph to evolve. Never suppress friction.

**Rule [EXT-04]: Atomic Decomposition**
Complex ideas must be broken down into their smallest indivisible units (atoms). One Note = One Idea. Do not lump disparate concepts into a single "Mega-Note."

**Rule [EXT-05]: Source Traceability**
While we de-contextualize the *content*, we must rigorously cite the *provenance*. Every claim must be traceable back to its origin (source file, author) to maintain intellectual honesty.

**Rule [EXT-06]: Meaning over Syntax**
Do not capture "housekeeping" chat (e.g., "Hello everyone", "Subscribe to the channel"). Capture only the core semantic meaning.

---

## 3. Structural Rules (The How)

**Rule [STR-01]: The Atomic Note**
-   **Title:** Descriptive, concept-first (e.g., "React State Management" not "Lecture 1").
-   **Body:** Focused on a single concept.
-   **Links:** Plentiful and meaningful.

**Rule [STR-02]: Hierarchy of Headers**
-   **H1:** Reserved for the Note Title (Filename). **NEVER** use H1 in the note body.
-   **H2:** Major atomic sections.
-   **H3:** Sub-sections (specific aspects).
-   **Depth:** Do not go deeper than H4. Flatten structure if needed.

**Rule [STR-03]: Chronological Integrity (Soft)**
-   **Principle:** Preserve sequence ONLY when it aids understanding (e.g., a process).
-   **Constraint:** Do not force a chronological recount of a "rambling" source; restructure into logical atoms.

**Rule [STR-03]: Declarative Bulleting**
Use "Rule-Based Patterning" for lists.
-   **Format:** `**Concept/Rule:** Explanation.`
-   **Why:** This makes the note machine-parsable and human-scannable.

**Rule [STR-04]: Code Contextualization**
Code blocks must never stand alone.
-   **Requirement:** Precede with file path/context.
-   **Requirement:** Follow/Integrate with explanation of *why* this code works.
-   **Syntax:** Always specify language (e.g., ```python).

**Rule [STR-05]: Linking Syntax**
-   Use `[[WikiLinks]]` for internal connections.
-   Use `[Label](URL)` for external sources.
-   Link aggressively to *entities*, *concepts*, and *authors*.

**Rule [STR-06]: Metadata (Frontmatter)**
Always include standard YAML frontmatter:
-   `tags`: Plural, lowercase, topic-based (e.g., `#algorithms` not `#Algo`).
-   `aliases`: Alternative names for searchability.

---

## 4. Workflow Rules (The When)

**Rule [WFL-01]: Iterative Refinement**
Notes are never "finished." They are living documents. We create a "Draft" (v0), then refine it.
-   **v0:** Capture signal.
-   **v1:** Refine structure and links.
-   **v2:** Polish prose and add insights.
(The Agent typically performs v0->v1 in one pass).

**Rule [WFL-02]: The Anti-Cramming Law**
Do not try to process an entire library in one go. Process one source, integrate it, then move to the next. Knowledge requires "soak time."

**Rule [WFL-03]: The "Open Loop" Strategy**
If a concept is unclear or requires more research, explicitly mark it (e.g., `> [!TODO] Research X`). Do not pretend to know. Leaving an open loop is better than writing a hallucination.

**Rule [WFL-04]: Active Review**
The value of a note is realized only upon *retrieval*. Write notes "for your future self"—assume you have forgotten the context. Would this note still make sense 6 months from now?

**Rule [WFL-05]: Emergent Structure**
Do not force a top-down folder structure. Let structure emerge from the bottom up via clusters of related notes. Use "Maps of Content" (MOCs) only when a topic has critical mass (10+ notes).

---


