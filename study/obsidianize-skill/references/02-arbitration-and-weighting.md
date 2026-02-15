# ═══════════════════════════════════════════════════════════════════════════════
# Arbitration Engine
# ═══════════════════════════════════════════════════════════════════════════════

## Input Analysis (Phase 1)

**Objective:** Deeply understand the input before generating any structured notes.

## Phase 1 Tasks (Required - Execute Silently)

### 1.1 Complete Input Analysis
- Read the ENTIRE input from start to finish
- Do NOT begin note generation until you have processed ALL content
- Map the document structure: identify sections, code blocks, errors, iterations

### 1.2 Knowledge Element Extraction
Identify and categorize ALL of the following:
- **Definitions:** New terms and their meanings
- **Distinctions:** What X is NOT (boundary definitions)
- **Procedures:** Step-by-step processes and workflows
- **Code Examples:** Final code AND intermediate iterations/errors
- **Configurations:** Setup, env vars, packages
- **Mental Models:** Visualizations and conceptual frameworks
- **Counter-Evidence:** Contradictions to common wisdom

### 1.3 De-contextualization (PR-0037)
For EVERY extracted element:
- Strip it of its original source context
- Translate it into a universal principle
- Ask: "How would this apply to a completely different problem?"

### 1.4 Feynman Test (PR-0046)
For EVERY concept:
- Can you explain it simply in plain language?
- If not, you have NOT understood it. Research further.

**Phase 1 Exit Criteria:** You have a complete mental model of the input, de-contextualized into universal principles. Proceed to Fixed Depth Configuration.

---

# ═══════════════════════════════════════════════════════════════════════════════
# Fixed Depth Configuration (W4 + Deep Drill)
# ═══════════════════════════════════════════════════════════════════════════════

**Objective:** Run at maximum depth for every input. Weight and mode are fixed.

> [!IMPORTANT] FIXED DEPTH
> Weight is always **W4**. Mode is always **Deep Drill**.
> All Tier 1 rules are eligible; activation remains signal-driven and budgeted.

## Structural Ceilings (W4)

- **H2 sections (target range):** 4-8+
- **Notes H3:** Preferred
- **Conditional H3 triggers:** Signal-driven
- **Wikilinks preference:** 5+
- **Tier 1 eligibility scope:** Full (all)
- **Density ratio (hard cap):** H2 count / content lines ≤ 0.2

**These are targets, not quotas.** Do NOT fabricate sections to meet minimums.

**Phase 1.1 Exit Criteria:** Fixed depth confirmed (W4 + Deep Drill). Proceed to Priority Hierarchy.

---

# ═══════════════════════════════════════════════════════════════════════════════
# Priority Order
# ═══════════════════════════════════════════════════════════════════════════════

**Objective:** Resolve rule conflicts and prevent structural explosion.

**Priority Order (highest → lowest):**
1. **Format & Tool Constraints** (markdown contract, write-once model)
2. **Safety/Validity Gates** (no fabrication, signal-only extraction, 10-minute gate)
3. **Fixed Depth Gating** (W4 + Deep Drill)
4. **Signal-Driven Applicability** (rule only fires if signal exists)
5. **Structural Ceilings** (upper bounds and density ratio)
6. **Structural Preferences** (ordering, stylistic preferences)
7. **Workflow/Meta Guidance** (Tier 3)

---

# ═══════════════════════════════════════════════════════════════════════════════
# Arbitration Layer
# ═══════════════════════════════════════════════════════════════════════════════

**Objective:** Decide final scope before any planning or generation.

**Arbitration Inputs:**
- Fixed depth configuration (W4 + Deep Drill)
- Signal map from Phase 1 extraction
- Hard ceilings and density ratio
- Output budget (pre-generation)

**Arbitration Outputs (FINAL):**
- **Activation Set:** which rules are allowed to fire
- **Budgeted Section Plan:** counts and types of sections allowed

**Arbitration Doctrine:**
- Arbitration decisions are **final**.
- Downstream phases **cannot expand scope**.
- If a rule is not in the Activation Set, it cannot be activated later.
- Generation must stay within the Budgeted Section Plan.

### Depth Priority Clause
Under structural budget pressure, prioritize sections that:
- Explain mechanisms.
- Capture mental models.
- Surface failure modes.
- Clarify conceptual boundaries.

De-prioritize:
- Redundant summaries.
- Surface-level restatements.
- Excessive wikilinks.
- Stylistic expansion.

Arbitration must favor conceptual depth over coverage breadth.
No numeric scoring system is introduced.
No quotas are introduced.
No expansion beyond the locked Activation Set is allowed.
Depth prioritization operates strictly within existing ceilings and budget.

---

# ═══════════════════════════════════════════════════════════════════════════════
# Rule Classification Matrix
# ═══════════════════════════════════════════════════════════════════════════════

**Objective:** Classify rules to reduce fabrication pressure and control depth.

### HARD (must always hold)
- Markdown structural contract (H2/H3 hierarchy, no H1 in body)
- Write-once model
- No fabrication (no inferred content beyond source signal)
- Context mandate for code (include required files/imports/inputs)
- 10-minute gate
- Hard ceilings and density ratio

### SOFT (best-effort; drop under pressure)
- Diversity preference (section variety)
- Basics-first ordering
- Interview readiness emphasis (if technical)
- Wikilink density preference

### CONDITIONAL (requires explicit signal)
- Distinctions, counter-evidence, definitions, configuration, procedures
- Code implementation and decomposition depth (only when code exists and adds signal)

### SACRIFICIAL (drop first when ceilings are tight)
- Extra decomposition depth
- Extra cross-links

---
