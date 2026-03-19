# Output Structure

**Objective:** Generate structured notes by executing the Rule Activation Plan.

> [!CAUTION] DOCTRINE ANCHORS — Do Not Skip
> These are the rules you are statistically most likely to violate. Re-read before generating.
> 1. **Atomicity (EXT-04):** One concept = one note. Do NOT merge multiple concepts into a mega-note.
> 2. **Code Preservation (C-02):** Every code block from input MUST appear in output. No exceptions.
> 3. **Signal-Based Reality (Principle 3):** Only structure what exists. Do not fabricate sections.
> Full doctrine: `references/doctrine.md`

## Note Template (Required)

Generate an Obsidian note in this order. Omit sections that lack signal or fail the Section Necessity Test.

### Document Header

- **Title Selection:** Choose a descriptive, link-friendly title (e.g., "State Management in React" rather than "React Tutorial"). Use this title as the **filename**, not as an H1 in the body.
- **YAML Frontmatter:** YAML at the very top delimited by `---`, e.g.
  ```yaml
  ---
  aliases: ["Alternative Name", "Short Name"]
  tags: ["topic", "subtopic"]
  backlinks: ["[[Related Note A]]", "[[Related Note B]]"]
  ---
  ```
- **Backlinks Rule:** The `backlinks` field is **required**. Populate it with `[[wikilinks]]` to all related notes. If no related notes exist yet, use `[]`. **This is the ONLY place backlinks or related-note links should appear — never in the note body (C-11).**
- **File Start:** After frontmatter, start immediately with the first Atomic Section (H2). No meta sections in the file.


### Examples (Few-Shot)

> [!TIP] PATTERN MATCHING
> Use these examples to understand the transformation from Raw Input to Atomic Section.

**Example 1: Conceptual Extraction**
**Raw Input:**
> "In React, you shouldn't mutate state directly. Like, don't do `state.count = 1`. Use the setter function `setState` because it triggers a re-render. If you don't, the UI won't update."

**Expected Atomic Section Output:**
```markdown
## React State Mutation
### Notes
- **The Immutability Rule:** Never mutate state variables directly.
  - *Why:* Direct mutation bypasses React's rendering lifecycle, causing the data to update but the UI to remain stale.
  - *When to apply:* Always use the provided setter function (e.g., `setState` or `setCount`) to guarantee UI synchronization.
```

**Example 2: Procedural Extraction**
**Raw Input:**
> "To install it, just run `npm install zod`. Then import it at the top of your schema file. You'll need to define a schema object before you can validate anything."

**Expected Atomic Section Output:**
```markdown
## Installation & Setup
### Configuration
1. **Install Package:**
   ```bash
   npm install zod
   ```
2. **Import:** Add `import { z } from 'zod';` to the schema file.
3. **Define Schema:** Create a schema object prior to validation.
```



### Atomic Sections

Break the content into logical sections. Apply this structure only to concepts selected in the Activation Set and within the Budgeted Section Plan.

> [!TIP] SUGGESTED PALETTE — NOT A RIGID CHECKLIST
> The H3 sections below are a **suggested palette** of section types derived from the doctrine's signal types. Use whichever sections the source signal demands — do not force sections that lack signal (Principle 3: Signal-Based Reality). Omit any that fail the Section Necessity Test.

> These sections MUST enforce `references/doctrine.md` rules:

> **In the output note, each section title below becomes an H3 under the parent H2 atomic section.**

#### Models & Mental Frameworks (H3)
> **Signal Type:** Models (EXT-01)
- **Goal:** Extract mental models, frameworks, or "ways of seeing" the domain
- **Style:** Use **Rule-Based Patterning** (STR-04). Each bullet must:
  - Start with a **bolded model name** followed by a colon
  - Explain the **why** and **when** this model applies
  - Be **atomic**—one model per bullet
- **Requirement:** Answer: _"What is the transferable principle here?"_
- **Format:** `**Model Name:** Explanation including when to apply it.`


#### Definitions (H3 - CONDITIONAL)

> **Signal Type:** Definitions (EXT-01) | Enforces: **EXT-02** (Feynman Test)

- **Trigger:** Only if the text introduces **CRITICAL** domain-specific jargon (EXT-01)
- **Constraint:** Do not define common words. Only define terms that would block understanding if unknown.
- **Format:** **Term:** Precise definition explained simply (Feynman Test)
- **Requirement:** If you cannot explain it simply, revisit the source and rewrite until it is clear.

#### Distinctions & Negations (H3 - CONDITIONAL)

> **Signal Type:** Arguments (EXT-01) | Enforces: **EXT-03** (Darwin's Golden Rule)

- **Trigger:** If the text defines what something is NOT or distinguishes between similar concepts
- **Format:** "X is NOT Y because..." or "Unlike A, B does..."
- **Goal:** Explicitly define boundaries of the concept
- **Requirement:** Capture disconfirming evidence—what this concept is NOT

#### Arguments & Evidence (H3 - CONDITIONAL)

> **Signal Type:** Arguments (EXT-01)

- **Trigger:** If the text presents a claim backed by evidence, data, or logical reasoning
- **Format:** `**Claim:** [The claim] → **Evidence:** [Supporting data/logic]`
- **Goal:** Capture the argument structure — what is being claimed and *why* it should be believed
- **Distinction from Counter-Evidence:** This section captures *affirmative* arguments; Counter-Evidence captures *disconfirming* ones

#### Insights & Novel Connections (H3 - CONDITIONAL)

> **Signal Type:** Insights (EXT-01)

- **Trigger:** Novel connections, "aha" moments, or unexpected relationships
- **Format:** `**Insight:** [The connection] → [Why it matters]`
- **Goal:** Capture moments of synthesis that restructure understanding

#### Notes (H3 - CONDITIONAL)

> Enforces: **Principle 5** (Connectivity), **Principle 6** (Project-Anchored Relevance), **STR-08** (Anti-Orphan Clustering)

- **Trigger:** Observations, contextual remarks, or connections that carry signal but don't fit into any other H3 category
- **Use cases:**
  - Docking points: "This relates to [[X]] because…"
  - Project anchoring: "This is relevant to [active project] because…"
  - Caveats or scope limitations the author mentions
  - Historical context or background that aids understanding
- **Format:** Unstructured bullets — each should be a self-contained observation
- **Constraint:** Must still pass the 10-Minute Gate (Principle 2). No filler.

#### Procedures & Workflows (H3 - CONDITIONAL)

> **Signal Type:** Procedures (EXT-01)

- **Trigger:** Actionable, step-by-step "how-to" recipes
- **Style:** Numbered lists of clear, actionable steps
- **Requirement:** Include prerequisites, steps, and expected outcomes
- **Format:** 
  ```
  1. **Step Name:** Action to take
  2. **Step Name:** Action to take
  ```

#### Configuration (H3 - CONDITIONAL)

> **Signal Type:** Procedures (EXT-01) | Enforces: **STR-05** (Code Contextualization)

- _Include ONLY if the content involves setup, installation, or environment configuration._
- **MANDATORY CHECKLIST (Do not omit):**
  1.  **Terminal Commands:** specific installation/navigation commands (e.g., `cd backend`, `npm install`). **MUST be wrapped in triple backtick code blocks (```bash).**
  2.  **Packages:** List specific libraries with versions.
  3.  **Environment Variables:** ALL required env vars (Names and Values).
  4.  **Source Origin:** Where these values came from.


#### Code Implementation (H3 - CONDITIONAL)

> Enforces: **STR-05** (Code Contextualization) | **C-07** (Code Context)

- _Include ONLY if code, scripts, or implementation logic is discussed._
- **Goal:** The FINAL, working version of the code.
- **Rules:**
  1.  **File Path Citation (REQUIRED):** You MUST explicitly state the file path/name before the block (e.g., `**File**: src/features/auth/AuthContext.js`).
  2.  **Language Specification (REQUIRED):** Must specify language (e.g., ```python, ```javascript)
  3.  **Runnable:** Must be copy-paste ready.
  4.  **Comments:** Add educational comments explaining the _WHY_ and _HOW_.
  5.  **Integrity:** Do not truncate lines.
  6.  **Preservation:** **ALL code blocks from input MUST appear in output**—no exceptions

> [!CRITICAL] CODE PRESERVATION MANDATE
> **Constraint C-02 (Signal Sanctity) applies:** If code appears in the source, it MUST appear in the note.
> - Do not summarize code—include full implementation
> - Do not omit "obvious" code—if it's in the source, it's in the note
> - Every code block requires context: where it came from and what it does

> [!IMPORTANT] SECTION NECESSITY TEST
> Before creating any conditional H3, ask: "Does this section add information NOT already captured in higher-level sections?"
> If the answer is NO → skip the section.

### Code Preservation Rules (Hard Constraints)

> **Enforces:** **C-02** (Signal Sanctity), **C-07** (Code Context), **STR-05** (Code Contextualization)

**The Code Imperative:**
Every code block discussed in the input MUST be preserved in the final note. This is non-negotiable.

**Rules:**
1. **No Code Left Behind**: If the source contains code, the note contains code
2. **Full Context Required**: Every code block must have:
   - File path/origin citation
   - Language specification
   - Explanation of purpose
3. **No Summarization**: Do not replace code with "The code does X" descriptions
4. **Complete Implementation**: Include full code, not partial snippets (unless source is partial)
5. **Working State**: Code must be copy-paste ready

**Verification Checklist:**
- [ ] Count code blocks in input
- [ ] Count code blocks in output  
- [ ] Verify count matches (input count ≤ output count)
- [ ] Verify each has file path context
- [ ] Verify each has language tag

> Enforces: **C-03** (File-Only Emission), **C-05** (Template Adherence), **C-11** (Backlinks in Frontmatter Only) — see `references/doctrine.md`.
