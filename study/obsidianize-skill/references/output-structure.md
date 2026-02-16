# Output Structure (Compressed)
# ═══════════════════════════════════════════════════════════════════════════════

**Objective:** Generate structured notes by executing the Rule Activation Plan.

## Output Objectives (References)

> **See `references/doctrine.md` for the Supreme Doctrine.**
-   **High-Signal Synthesis**: (Principle 1)
-   **Atomicity**: (Rule EXT-04)
-   **De-contextualization**: (Principle 4)
-   **10-Minute Gate**: (Principle 2)

### 2.2 OUTPUT STRUCTURE (Required Template)

Generate an Obsidian note in this order. Omit sections that lack signal or fail the Section Necessity Test.

#### Document Header

- **Title Selection:** Choose a descriptive, link-friendly title (e.g., "State Management in React" rather than "React Tutorial"). Use this title as the **filename**, not as an H1 in the body.
- **YAML Frontmatter:** YAML at the very top delimited by `---`, e.g.
  ---
  aliases: []
  tags: []
  backlinks: []
  ---
- **File Start:** After frontmatter, start immediately with the first Atomic Section (H2). No meta sections in the file.

#### Pre-Generation Artifacts (Silent Execution)

- **Strict Silence:** Do NOT emit any planning artifacts, tables, or summaries in the chat.
- **Output:** The ONLY output allowed is the final `.md` file creation.
- **Process:** Perform all Signal Gating and Budgeting internally.

### 2.0 EXAMPLES (Few-Shot)

> [!TIP] PATTERN MATCHING
> Use these examples to understand the transformation from Raw Input to Atomic Section.

**Example 1: Conceptual Extraction**
**Raw Input:**
> "So in React, you shouldn't mutate state directly. Like, don't do `state.count = 1`. Use the setter function `setState` because it triggers a re-render. If you don't, the UI won't update."

**Expected Atomic Section Output:**
```markdown
##### React State Mutation (H2)
###### Notes (H3)
- **The Immutability Rule:** Never mutate state variables directly.
  - *Why:* Direct mutation bypasses React's rendering lifecycle, causing the data to update but the UI to remain stale.
  - *When to apply:* Always use the provided setter function (e.g., `setState` or `setCount`) to guarantee UI synchronization.
```

**Example 2: Procedural Extraction**
**Raw Input:**
> "To install it, just run `npm install zod`. Then import it at the top of your schema file. You'll need to define a schema object before you can validate anything."

**Expected Atomic Section Output:**
```markdown
##### Installation & Setup (H2)
###### Configuration (H3)
1. **Install Package:**
   ```bash
   npm install zod
   ```
2. **Import:** Add `import { z } from 'zod';` to the schema file.
3. **Define Schema:** Create a schema object prior to validation.
```

#### Atomic Sections

Break the content into logical sections. Apply this structure only to concepts selected in the Activation Set and within the Budgeted Section Plan.

##### [Section Title] (H2)

###### Notes (H3)

- **Goal:** Extract the underlying **rules, patterns, frameworks, or recipes** behind what is being taught.
- **Style:** Use **Rule-Based Patterning**. Each bullet must:
  - Start with a **bolded rule/pattern name** followed by a colon.
  - Explain the **why** and **when** this rule applies, not just the **what**.
  - Be **atomic**—one rule per bullet.
- **Requirement:** For every fact, ask: _"What is the transferable principle here?"_
- **Cognitive Tooling:** Explicitly capture "Mental Models", "Common Mistakes", or "Argument Categories" if present.

###### Definitions (H3 - CONDITIONAL)

- **Trigger:** Only if the text introduces **CRITICAL** domain-specific jargon.
- **Constraint:** Do not define common words. Only define terms that would block understanding if unknown.
- **Format:** **Term:** Precise definition based on the context.

###### Distinctions & Negations (H3 - CONDITIONAL)

- **Trigger:** If the text defines what something is NOT or distinguishes between similar concepts (explicit or implied).
- **Format:** "X is NOT Y because..." or "Unlike A, B does..."
- **Goal:** Explicitly define boundaries of the concept.

###### Counter-Evidence & Disagreements (H3 - CONDITIONAL)

- **Trigger:** If the text contradicts common wisdom, previous notes, or itself (explicit or implied).
- **Goal:** Prioritize capturing contradictions ("Darwin's Golden Rule") to prevent confirmation bias.

###### Configuration (H3 - CONDITIONAL)

- _Include ONLY if the content involves setup, installation, or environment configuration._
- **MANDATORY CHECKLIST (Do not omit):**
  1.  **Terminal Commands:** specific installation/navigation commands (e.g., `cd backend`, `npm install`). **MUST be wrapped in triple backtick code blocks (```bash).**
  2.  **Packages:** List specific libraries with versions.
  3.  **Environment Variables:** ALL required env vars (Names and Values).
  4.  **Source Origin:** Where these values came from.

###### Technical Procedures & Workflows (H3 - CONDITIONAL)

- **Trigger:** If the tutorial explains _how to do something_ that isn't purely writing code (e.g., configuring a Postman environment).
- **Goal:** Capture the "Applicable" part of the text. Document exact steps.
- **Style:** Numbered lists of clear, actionable steps.
- **Balance:** Bridge the gap between "Notes" (Theory) and "Code Implementation" (Syntax).

###### Code Implementation (H3 - CONDITIONAL)

- _Include ONLY if code, scripts, or implementation logic is discussed._
- **Goal:** The FINAL, working version of the code.
- **Rules:**
  1.  **File Path Citation:** You MUST explicitly state the file path/name before the block (e.g., `**File**: src/features/auth/AuthContext.js`).
  2.  **Runnable:** Must be copy-paste ready.
  3.  **Comments:** Add educational comments explaining the _WHY_ and _HOW_.
  4.  **Integrity:** Do not truncate lines.

> [!IMPORTANT] SECTION NECESSITY TEST
> Before creating any conditional H3, ask: "Does this section add information NOT already captured in Notes H3?"
> If the answer is NO → skip the section.

#### Output Rules (References)

> **See `references/doctrine.md` for Hard Limits.**
-   **File Only**: (Constraint C-03)
-   **Structure**: (Constraint C-05)


