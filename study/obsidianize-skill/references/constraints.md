# Hard Constraints (The Law)

> **Status:** Non-Negotiable
> **Violation:** Immediate Failure

These constraints are the "physics" of the Obsidianize agent. They cannot be broken, ignored, or hallucinated away.

---

## 1. The Initiation Constraint

**Constraint [C-01]: Workflow Supremacy**
Upon activation, the **VERY FIRST** action MUST be to read `references/workflow.md`.
-   **Trace:** `SKILL.md` -> `read_file(references/workflow.md)`
-   **Violation:** Generating plans, reading input, or writing files *before* reading the workflow is a critical failure.

## 2. The Input Constraint

**Constraint [C-02]: Signal Sanctity (No Hallucination)**
You are a filter, not a generator.
-   **Rule:** If a concept is not in the source text, it DOES NOT EXIST.
-   **Ban:** Do not invent "Intro", "Conclusion", "Prerequisites", or "Next Steps" unless explicitly present in the source.
-   **Ban:** Do not infer "what the author meant" beyond logical deduction. Stick to what was said.

## 3. The Output Constraint

**Constraint [C-03]: File-Only Emission**
We are a silent engine.
-   **Rule:** The final note content must **ONLY** appear in the `write_file` tool call.
-   **Ban:** Do NOT print the note content, summary, or "draft" into the Chat.
-   **Chat:** Use Chat ONLY for:
    1.  Status updates (e.g., "Reading workflow...").
    2.  Validation reports (e.g., "Plan validated.").
    3.  Error reporting.

**Constraint [C-04]: Atomic Write**
-   **Rule:** Write the file in ONE `write_file` operation.
-   **Ban:** Do not partial-write and then append.

## 4. The Structural Constraint

**Constraint [C-05]: Template Adherence**
-   **Rule:** You MUST follow `references/output-structure.md`.
-   **Ban:** Do not use H1 (`# Title`) in the file body. The filename is the title.
-   **Ban:** Do not use arbitrary headers like `## Summary` or `## Key Takeaways` if they violate the template.

## 5. The Formatting Constraint

**Constraint [C-06]: Obsidian Syntax**
-   **Rule:** Follow `references/obsidian-markdown.md`.
-   **Requirement:** Valid Frontmatter (YAML).
-   **Requirement:** Valid internal links `[[Note Name]]`.
-   **Requirement:** Callouts `> [!INFO]`.
-   **Requirement:** Code blocks with language specification.

## 6. The Context Constraint

**Constraint [C-07]: Code Context**
-   **Rule:** Code implies context.

## 7. The Negative Constraint (Specific Bans)

**Constraint [C-08]: Content Scope**
-   **Ban:** No "Interaction Orders" (e.g., "Drink water", "Sleep well"). We are a text engine, not a coach.
-   **Ban:** No "Anki Mechanics" in the note body (e.g., card settings). The note is the source, not the card.

**Constraint [C-09]: Filename Safety**
-   **Rule:** Filename must be sanitized (no special chars).
-   **Rule:** If title is unclear, use current directory name as fallback.

**Constraint [C-10]: No Housekeeping**
-   **Ban:** Do not capture "housekeeping" chat (e.g., "Hello everyone", "Subscribe", "Sponsors").
-   **Rule:** If the input is purely housekeeping with no signal, output a trivial empty note or error.

**Constraint [C-11]: Open Loop Mandate**
-   **Rule:** If a concept is referenced but undefined/unclear in the source, DO NOT hallucinate a definition.
-   **Action:** Use an explicit callout: `> [!TODO] Research <Concept>`



# ═══════════════════════════════════════════════════════════════════════════════
# Guardrail Verification
# ═══════════════════════════════════════════════════════════════════════════════

**Objective:** Enforce format compliance and output integrity. This phase is required.

> [!IMPORTANT] OUTPUT VALIDATION
> This is the final gate. The note must pass all validation checks.
> Invalid output is a **structural breach**.

**Hard Rule Compliance Audit:**
- [ ] YAML frontmatter is present and valid
- [ ] No H1 headers in the body
- [ ] First content line after frontmatter is an H2 Atomic Section
- [ ] No process artifacts in file
- [ ] All section headings follow the hierarchy (H2 for sections, H3 for subsections)
- [ ] All code blocks have language specifiers
- [ ] All code blocks are complete (no truncation)
- [ ] File path is cited before every code block
- [ ] Conditional sections are only present when signal is explicit
- [ ] No fabrication: every section traces to explicit source signal
- [ ] Signal gating respected: sections exist only where explicit signal is present
- [ ] 10-minute gate respected (no trivial sections/bullets)
- [ ] Context mandate for code satisfied (dependencies/inputs stated)

**Failure Protocol:**
1. STOP output immediately
2. Identify the specific validation failure
3. Revise the offending section
4. Re-validate
5. Only proceed when ALL checks pass

**DO NOT OUTPUT INVALID NOTES UNDER ANY CIRCUMSTANCES.**
