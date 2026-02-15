# Activation Logic & Budget Plan
# ═══════════════════════════════════════════════════════════════════════════════

**Objective:** Select signal-present rules and set a budgeted plan BEFORE generating any note content.

> [!IMPORTANT] RULES ARE CANDIDATES
> The knowledge base rules provide **candidates** for structure.
> Only **signal + budget + arbitration** determine what is activated.
> Skipping this phase is a **guardrail violation**.

## 1.5.1 Rule Tier System

The knowledge base rules are organized into 3 tiers:

### TIER 1: NOTE STRUCTURING DRIVERS (~20 rules)
These rules directly dictate WHAT sections and content to create. **All Tier 1 rules are eligible in fixed W4.**

| Rule ID | Name | What It Drives | Active (W4) |
|---------|------|----------------|----------|
| PR-0003 | Generation Effect | Forces active synthesis — no transcription | W4 |
| PR-0004 | Hidden Models | MENTAL MODEL sections: capture visualizations | W4 |
| PR-0007 | Stable Structure | Mandatory template compliance — H2/H3 hierarchy | W4 |
| PR-0016 | Dynamic Interconnection | WIKILINK density (soft, signal-driven) | W4 |
| PR-0018 | Docking Points | BACKLINKS — anchor new ideas to existing knowledge | W4 |
| PR-0022 | Atomicity | ATOMIC SECTIONS — one core idea per H2 | W4 |
| PR-0030 | Connection Density | Understanding = connections | W4 |
| PR-0037 | De-contextualization | Universal principles — strip source context | W4 |
| PR-0038 | Confirmation Bias | COUNTER-EVIDENCE sections | W4 |
| PR-0043 | Cognitive Tooling | Mental models, error patterns, argument categories | W4 |
| PR-0045 | Negation/Inversion | DISTINCTIONS sections — define what X is NOT | W4 |
| PR-0046 | Feynman Test | Plain language — if you can't explain it simply, research more | W4 |
| EL-PR-0004 | Atomicity (Extraction-Ready) | Declarative statements — bold key concept → detail | W4 |
| Code Integrity | Runnable Code | Code blocks: file path, copy-paste ready, WHY/HOW comments | W4 (only if code) |
| Chronological Rule | Linear Processing (soft) | Preserve sequence when it adds understanding | W4 |
| Reconstruction Rule | High-Signal Synthesis | Capture essential logic without fabrication | W4 |

> [!IMPORTANT] DEEP DRILL CLARITY
> Deep Drill expands **depth within already activated categories**.
> It does **NOT** increase rule count, bypass ceilings, or bypass signal gating.

### TIER 2: NOTE QUALITY CONSTRAINTS (~25 rules)
These rules constrain HOW sections should look. Apply during generation.

| Rule ID | Constraint |
|---------|------------|
| PR-0001 | Intentionality — every section is a deliberate choice |
| PR-0002 | Cognitive Internalization — notes reshape thinking patterns |
| PR-0005 | Behavior Change — connect notes to desired behavioral outcomes |
| PR-0011 | Feedback Loops — embed feedback triggers in note creation |
| PR-0014 | Weakness Focus — prioritize areas of least understanding |
| PR-0021 | Writing Sub-tasks — separate reading, reflecting, drafting, proofreading |
| PR-0025 | Externalization — writing is prerequisite for analysis |
| PR-0041 | Relevance-Dependent — accept any topic that connects to existing notes |
| PR-0042 | Relevance Filtering — extract only the gist, practiced through note-taking |
| Rule-Based Patterning | Notes H3 — bolded rule name + why/when explanation |
| Declarative Statements | Machine-parsable — bold concept → detail format |
| YAML Frontmatter | Header — YAML at top (aliases/tags/related links when used) |

### TIER 3: WORKFLOW/META (~50+ rules)
These rules are about study habits, motivation, note systems, and attention. They inform your understanding but do NOT directly affect note structure.

Examples: PR-0006 (emerging interests), PR-0008 (virtuous loops), PR-0009 (draining workflows), PR-0010 (intrinsic motivation), PR-0012 (improvement as motivation), PR-0013 (fixed mindsets), PR-0019 (attention fragility), PR-0020 (multitasking), PR-0023 (attention training), PR-0024 (flow states), PR-0027 (creativity oscillation), PR-0031 (Zeigarnik), PR-0033 (willpower), PR-0035 (writing assembly), PR-0036 (slip-box as partner).

## 1.5.2 Pre-Generation Budget Algorithm

Apply this algorithm BEFORE any section planning:

1. **Count signals** by type: code, config, procedures, definitions, distinctions, counter-evidence.
2. **Establish structural budget** from W4 ceilings (H2 cap, H3 cap, density ratio).
3. **Reserve mandatory structure (W4)**:
   - Notes H3 for each H2 when signal supports it.
4. **Allocate remaining budget by signal priority**:
   - Code Implementation
   - Procedures
   - Distinctions
   - Counter-Evidence
   - Definitions
   - Links/Backlinks
5. **Apply Sacrifice Order if overflow**:
   - Drop optional H3s, extra links, stylistic preferences.
   - Drop low-signal conditional H3s.
   - Reduce Deep Drill depth.
   - Drop soft rules.
6. **Lock the Activation Set** and **Budgeted Section Plan**.
7. **Generation must never exceed this plan**.

## 1.5.3 Build the Rule Activation & Budget Plan

> [!IMPORTANT] PREDICTIVE, NOT CONTRACTUAL
> The Rule Activation & Budget Plan is a predictive estimate, not a coverage contract.
> Estimated outputs must fit within structural ceilings BEFORE generation.
> Never generate beyond ceilings or use post-generation trimming.

After de-contextualizing the input (Phase 1) and understanding the Tier system:

1. **List all Tier 1 rules (W4)**
2. **For each rule, decide:** SIGNAL-PRESENT or NO-SIGNAL
   - Example: "PR-0038 (Counter-Evidence) → SIGNAL-PRESENT: Source contradicts common wisdom about X"
   - Example: "Code Integrity → NO-SIGNAL: No code in this source"
3. **For each SIGNAL-PRESENT rule, write a specific plan:**
   - Which content element(s) from Phase 1 extraction will it structure?
   - What section type will it produce (Notes H3, Distinctions H3, Code H3, etc.)?
   - How many sections (estimate)?
4. **Check against structural ceilings** (W4 ceilings)
   - Targets are guidance only; do NOT fabricate to hit minimums
5. **Ensure estimates fit within ceilings BEFORE generation**
   - If estimates exceed ceilings:
     1. Drop SACRIFICIAL rules
     2. Drop SOFT rules
     3. Reduce CONDITIONAL rule depth (narrow scope)
   - **Do NOT generate then trim or backfill**


## Doctrine-Depth Mode (Required Pre-Generation Artifacts)

Add these blocks as mandatory pre-generation artifacts. Do NOT generate the final output until they exist. Emit a summarized view in chat using a table.

Output contract: chat contains process artifacts (summary table + compliance). File contains only the final note.

Note: extraction_budget_plan is a planning artifact for downstream use. This skill outputs Obsidian notes only.

summary_artifacts (table format):

| Section | Summary |
|---|---|
| Element Inventory | H2: <list>; Per H2: <h2 -> h3 sections -> extracted elements (short labels)> |
| Classification | Type: PURE_THEORY | PURE_CODE | MIXED |
| Tier-1 Plan | PR-0003: <APPLICABLE/NOT> (<count>); PR-0004: <...> |
| Internalization | Summary: <3-6 sentences>; Boundaries: <1-3 bullets>; Misconceptions: <1-3 bullets>; Links: <1-3 bullets> |
| Extraction Budget | Total: <int>; Synthesis: <int>; Cross-H2: <int>; Model: <int>; Failure: <int>; Negation: <int>; Counter: <int>; Constructive: <min-max>; Theory: <int>; Def Max: <int>; Proc Max: <int> |
| Compliance | All checks passed: <true|false>; Failures: <short list> |

stage2_analysis_artifacts:
  element_inventory:
    h2_concepts: [...]
    per_h2:
      - h2: "<title>"
        h3_sections_present: [...]
        extracted_elements:
          bold_rules: [...]
          definitions: [...]
          distinctions: [...]
          contradictions: [...]
          failure_triggers: [...]
          mental_models: [...]
          procedures: [...]
          code_blocks:
            - lines: <int>
              key_context_needed: [imports, variables, state_shapes, external_deps]
  classification:
    type: PURE_THEORY | PURE_CODE | MIXED
  tier1_rule_application_plan:
    - rule_id: PR-0003
      verdict: APPLICABLE|NOT_APPLICABLE
      target_content: "<what triggers it>"
      unit_type: "<THEORY/MODEL/etc>"
      estimated_count: <int>
    - rule_id: PR-0004 ...
    - rule_id: PR-0005 ...
    - rule_id: PR-0017 ...
    - rule_id: PR-0038 ...
    - rule_id: PR-0045 ...
    - rule_id: PR-0047 ...

internalization_report:
  summary: <3-6 sentences in your own words>
  boundaries:
    - <what it is NOT / does NOT cover>
  misconceptions:
    - <likely misconception>
  links:
    - <cross-concept link within the note>

extraction_budget_plan:
  target_total_units: <int>
  target_synthesis: <int>
  target_cross_h2_synthesis: <int>
  target_model: <int>
  target_failure_mode: <int>
  target_negation: <int>
  target_counter_evidence: <int>
  target_constructive_min: <int>
  target_constructive_max: <int>
  target_theory: <int>
  target_definition_max: <int>
  target_procedure_max: <int>

doctrine_compliance_report:
  all_checks_passed: <true|false>
  internalization_ok: <true|false>
  internalization_linkage_ok: <true|false>
  mapping_ok: <true|false>
  elements_ok: <true|false>
  coverage_ok: <true|false>
  tier1_ok: <true|false>
  minimums_ok: <true|false>
  connectivity_ok: <true|false>
  caps_ok: <true|false>
  global_failure_mode_ok: <true|false>
  budget_ok: <true|false>
  quality_ok: <true|false>
  output_purity_ok: <true|false>
  failures:
    - <short_reason>

If any doctrine check fails, regenerate missing classes only, max 3 attempts. Do not full-rewrite unless TSV validation fails.

**Phase 1.5 Exit Criteria:** Activation Set and Budgeted Section Plan are locked. Eligible Tier 1 rules were evaluated for signal presence. Estimated structure does not exceed ceilings (after reductions). Required pre-generation artifacts are complete. Proceed to Phase 2.

---
