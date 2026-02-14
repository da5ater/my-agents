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

**Phase 1 Exit Criteria:** You have a complete mental model of the input, de-contextualized into universal principles. Proceed to Weight Classification.

---

# ═══════════════════════════════════════════════════════════════════════════════
# Weight Classification (W1–W4)
# ═══════════════════════════════════════════════════════════════════════════════

**Objective:** Classify the input by content weight BEFORE activating rules. Weight determines which rules fire, how many sections to create, and whether conditional H3s should trigger.

> [!IMPORTANT] WEIGHT GATES ELIGIBILITY AND CEILINGS
> Weight classification is the FIRST decision after Phase 1. It controls eligibility, section density, conditional H3 trigger thresholds, and structural complexity.
> Skipping this step or defaulting to the heaviest weight is a **guardrail violation**.

## 1.1.1 Weight Levels

| Level | Name | Criteria | Typical Input |
|-------|------|----------|---------------|
| **W1** | Lightweight | ≤20 lines content, 1-2 concepts, 0-1 code blocks, no config | Quick concept note, single API method, brief explanation |
| **W2** | Standard | 20-80 lines, 3-6 concepts, 1-3 code blocks | Focused tutorial section, single pattern with examples |
| **W3** | Heavy | 80-200 lines, 6+ concepts, 3+ code blocks, has config/setup | Full tutorial, multi-step implementation, architectural guide |
| **W4** | Reference | 200+ lines, 10+ concepts, complex multi-file code | Comprehensive reference, textbook chapter, multi-pattern guide |

## 1.1.2 How to Classify

During Phase 1 you already mapped the document structure. Now count:

1. Total content lines (exclude frontmatter, blank lines)
2. Number of distinct concepts extracted
3. Number of code blocks
4. Presence of configuration/setup content

Assign the **lowest weight level whose criteria the input meets**. When in doubt, round DOWN (lighter), not up.

The user CAN override with `--weight W3` etc. If no override, use automatic classification.

## 1.1.3 Mode System

Modes are **orthogonal to weight**. Weight measures content size. Mode measures **intent**.

| Mode | Trigger | Effect |
|------|---------|--------|
| **Deep Drill** | User says "deep", "thorough", "drill" | Expands depth within already activated categories. Does not increase rule count, bypass ceilings, or bypass signal gating. |
| **Tactical** | Default — no special trigger | Standard weight-based activation. Balanced structure. |
| **Lightweight** | User says "quick", "brief", OR auto-selected when W1 | Minimal structure. Notes H3 optional. Suppress most conditional H3s. |
| **Research** | User says "research", "explore" | Prioritize connections, mental models, counter-evidence. Suppress code sections. |

**Auto-detection:** If weight = W1 and no explicit mode → auto-select **Lightweight** mode.

> [!IMPORTANT] DEEP DRILL LIMITS
> Deep Drill expands depth within activated categories but NEVER increases rule count, bypasses ceilings, or bypasses signal gating.

## 1.1.4 Weight Impact on Structure

| Aspect | W1 | W2 | W3 | W4 |
|--------|----|----|----|----|  
| H2 sections (target range) | 1-2 | 2-4 | 3-6 | 4-8+ |
| Notes H3 | Optional (can inline) | Preferred | Preferred | Preferred |
| Conditional H3 triggers | Explicit only | Signal-driven | Signal-driven | Signal-driven |
| Wikilinks preference | 1 | 2 | 3+ | 5+ |
| Tier 1 eligibility scope | Core only (3 rules) | Partial (8 rules) | Full (all) | Full (all) |

**These are targets, not quotas.** Do NOT fabricate sections to meet minimums.

**W1 hard ceiling:** Max 2 H2 sections. Conditional H3s only when explicit signal exists. No multi-layer expansion.

**Density ratio (hard cap):** H2 count / content lines ≤ 0.2. Structural ceilings still apply.

**Phase 1.1 Exit Criteria:** Weight level and mode are determined. Proceed to Priority Hierarchy.

---

# ═══════════════════════════════════════════════════════════════════════════════
# Priority Order
# ═══════════════════════════════════════════════════════════════════════════════

**Objective:** Resolve rule conflicts and prevent structural explosion.

**Priority Order (highest → lowest):**
1. **Format & Tool Constraints** (markdown contract, write-once model)
2. **Safety/Validity Gates** (no fabrication, signal-only extraction, 10-minute gate)
3. **Weight/Mode Gating** (W1–W4 + mode limits)
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
- Weight and mode
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
