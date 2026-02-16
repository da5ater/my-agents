# ═══════════════════════════════════════════════════════════════════════════════
# Output Structure
# ═══════════════════════════════════════════════════════════════════════════════

**Objective:** Generate structured notes by executing the Rule Activation & Budget Plan from Phase 1.5.

## Output Objectives (References)

> **See `references/manifesto.md` for the Supreme Doctrine.**
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
  ---
- **File Start:** After frontmatter, start immediately with the first Atomic Section (H2). No meta sections in the file.

#### Pre-Generation Artifacts (Chat Only)

- Emit the **summary_artifacts** table in chat only, exactly as specified in `03-activation-and-budget.md`.
- Do NOT include any planning artifacts in the file.

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
- **Signal Gate:** For thin signal, inline or omit Notes H3. Do not fabricate to satisfy structure.
- **Cognitive Tooling:** Explicitly capture "Mental Models", "Common Mistakes", or "Argument Categories" if present. (Source: PR-0004, PR-0043)

###### Distinctions & Negations (H3 - CONDITIONAL) (Source: PR-0045)

- **Trigger:** If the text defines what something is NOT or distinguishes between similar concepts (explicit or implied).
- **Format:** "X is NOT Y because..." or "Unlike A, B does..."
- **Goal:** Explicitly define boundaries of the concept.

###### Counter-Evidence & Disagreements (H3 - CONDITIONAL) (Source: PR-0038)

- **Trigger:** If the text contradicts common wisdom, previous notes, or itself (explicit or implied).
- **Goal:** Prioritize capturing contradictions ("Darwin's Golden Rule") to prevent confirmation bias.

###### Definitions (H3 - CONDITIONAL)

- **Trigger:** Only if the text introduces **CRITICAL** domain-specific jargon.
- **Constraint:** Do not define common words. Only define terms that would block understanding if unknown.
- **Format:** **Term:** Precise definition based on the context.

###### Configuration (H3 - CONDITIONAL)

- _Include ONLY if the content involves setup, installation, or environment configuration._
- **Required Checklist:**
  1.  **Terminal Commands:** Wrapped in ```bash code blocks.
  2.  **Packages:** List with versions.
  3.  **Environment Variables:** ALL required env vars.
  4.  **Source Origin:** Where these values came from.

###### Technical Procedures & Workflows (H3 - CONDITIONAL)

- **Trigger:** If the tutorial explains _how to do something_ (not purely code).
- **Goal:** Document the exact steps as numbered lists.
- **Style:** Clear, actionable steps with inline snippets if needed.

###### Code Implementation (H3 - CONDITIONAL)

- _Include ONLY if code, scripts, or implementation logic is discussed._
- **Goal:** The FINAL, working version of the code.
- **Rules:**
  1.  **File Path Citation:** State the file path before the block.
  2.  **Runnable:** Must be copy-paste ready.
  3.  **Comments:** Add educational WHY and HOW comments.
  4.  **Integrity:** Do not truncate lines.
  5.  **Context Mandate:** Include required inputs, dependencies, and assumptions in nearby text so code is not guesswork.

> [!IMPORTANT] SECTION NECESSITY TEST
> Before creating any conditional H3, ask: "Does this section add information NOT already captured in Notes H3?"
> If the answer is NO → skip the section.

#### Output Rules (References)

> **See `references/constraints.md` for Hard Limits.**
-   **File Only**: (Constraint C-03)
-   **Structure**: (Constraint C-05)



# ═══════════════════════════════════════════════════════════════════════════════
# Guardrail Verification
# ═══════════════════════════════════════════════════════════════════════════════

**Objective:** Enforce format compliance and output integrity. This phase is required.

> [!IMPORTANT] OUTPUT VALIDATION
> This is the final gate. The note must pass all validation checks.
> Invalid output is a **structural breach**.

**Hard Rule Compliance Audit:**
- [ ] YAML frontmatter is present and valid
- [ ] Validator script passed
- [ ] No H1 headers in the body
- [ ] First content line after frontmatter is an H2 Atomic Section
- [ ] No process artifacts in file
- [ ] All section headings follow the hierarchy (H2 for sections, H3 for subsections)
- [ ] All code blocks have language specifiers
- [ ] All code blocks are complete (no truncation)
- [ ] File path is cited before every code block
- [ ] Conditional sections are only present when signal is explicit
- [ ] H2 count does not exceed W4 ceilings
- [ ] No fabrication: every section traces to explicit source signal
- [ ] Signal gating respected: sections exist only where explicit signal is present
- [ ] 10-minute gate respected (no trivial sections/bullets)
- [ ] Context mandate for code satisfied (dependencies/inputs stated)
- [ ] Budgeted Section Plan respected (no generation outside budget)
- [ ] Structural ceilings and density ratio respected

**Guardrail Exit Criteria:** Guardrails satisfied and signal gating respected. Proceed to finalization.

## Failure Protocol

**If any validation fails:**

1. STOP output immediately
2. Identify the specific validation failure
3. Revise the offending section
4. Re-validate
5. Only proceed when ALL checks pass

If any doctrine_compliance_report check is false, regenerate missing classes only (no full rewrite), max 3 attempts. Do not full-rewrite unless TSV validation fails.

**DO NOT OUTPUT INVALID NOTES UNDER ANY CIRCUMSTANCES.**
