# ANKIFY Doctrine (Source of Truth)

Use this doctrine as the primary source of truth for card creation.
If any schema or implementation detail conflicts with this doctrine, follow doctrine and treat the other rule as stale.

## Card Intent

- Create cards that force active recall, not recognition.
- Ensure every card is intentional and worth future review time.
- Keep cards atomic: one idea per card.
- Avoid yes/no questions and list-of-things prompts.
- Provide enough context to avoid guesswork, especially for code.

## Structural Mapping

Treat H2 sections as atomic concepts. Use H3 subsections as card-type cues.

| H3 Subsection | Card Type |
|--------------|-----------|
| **Notes** | THEORY |
| **Distinctions & Negations** | NEGATION |
| **Counter-Evidence** | COUNTER-EVIDENCE |
| **Definitions** | DEFINITION |
| **Configuration** | PROCEDURE |
| **Technical Procedures** | PROCEDURE |
| **Code Implementation** | CONSTRUCTIVE |

## Content Element -> Card Type

```
Code block (<=5 lines)  -> CONSTRUCTIVE ("Write the code for...")
Code block (>5 lines)   -> Decompose into 3-5 atomic CONSTRUCTIVE cards
Bolded rule/pattern     -> THEORY ("What is the rule for..." / "Explain why...")
Distinction (X != Y)    -> NEGATION ("How does A differ from B?")
Counter-evidence        -> COUNTER-EVIDENCE ("When does X NOT apply?")
Definition              -> DEFINITION ("What is [term]?")
Configuration           -> PROCEDURE ("How do you set up X?")
Mental model            -> MODEL ("Explain/visualize how X works")
Common mistake          -> FAILURE MODE ("What goes wrong if you do X?")
```

## Canonical Card Types

Use these internal names consistently:

THEORY, CONSTRUCTIVE, SYNTHESIS, MODEL, FAILURE_MODE, NEGATION, COUNTER_EVIDENCE, DEFINITION, PROCEDURE

## Quality Constraints

- Keep fronts short, single-question, and plain language.
- Require active recall; avoid recognition-only prompts.
- Provide context docking and semantic anchors.
- Enforce unambiguous answers and interference prevention.
- For code cards: include variables/imports/scope/expected behavior; answers <= 2 lines.
- Constructive prompts must include "Given:" and "Task:" with one atomic action.

## Coverage Expectations

- Every structural element yields at least one card.
- Every code block yields at least one constructive card.
- Every distinction/contradiction yields its matching card type.
- No section is silently skipped; skipped content must have a reason.

## Concept Internalization (Required)

Before generating cards, produce a short internalization report that includes:

- A 3-6 sentence summary of the core concept in your own words.
- Explicit boundaries (what the concept is NOT or does not cover).
- At least one likely misconception.
- At least one cross-concept link within the note.

Do not proceed to card generation without this report.

### Internalization Report Format

```
internalization_report:
  summary: <3-6 sentences>
  boundaries: <1-3 bullet points>
  misconceptions:
    - <short misconception>
  links:
    - <short cross-concept link>
```

## Card Budget Plan (Required)

Create a card budget plan before generation. Use this format:

```
card_budget_plan:
  target_total_cards_min: <int>
  target_total_cards_max: <int>
  # ... other targets ...
  target_constructive_min: <int>
  target_constructive_max: <int>
```

**Feasibility Rule**:
- Ensure `target_total_cards_min` is at least equal to `target_constructive_min` + required Tier 1 cards.
- If `target_total_cards_min` exceeds `target_total_cards_max`, clamp min down to max (hard cap is absolute).

## Hard Cap (Absolute)

- Basic notes: `max_total_cards_max = 6` when anchors < 8 AND h2_count < 3 AND code_blocks <= 1.
- High complexity: `max_total_cards_max = 8` when any threshold is exceeded.

## Quantitative Minimums

When the triggering elements exist in the note, enforce minimum counts:

- concept_count >= 2 -> synthesis_cards >= 1
- concept_count >= 4 -> synthesis_cards >= 2
- h2_count >= 2 -> cross_h2_synthesis_cards >= 1
- mental_models present -> model_cards >= 1
- failure_modes present -> failure_mode_cards >= 1
- contradictions present -> counter_evidence_cards >= 1
- distinctions present -> negation_cards >= 1

Only enforce per-note failure-mode minimum when the note contains mistake/pitfall/warning language.

## Cross-H2 Synthesis Definition

A card qualifies as cross-H2 synthesis only if it:

- References **exact H2 titles** (or their canonical aliases) from the note.
- Uses a relational operator:
  compare, differ, tradeoff, impact, influence, interact, dependency, contrast, affects

Acceptable phrasing examples:

- "How does [H2: X] influence [H2: Y]?"
- "What is the tradeoff between [H2: X] and [H2: Y]?"

## Required Phrasing Patterns

**Definitions**:
- Preferred: "Define [Term]." or "Explain what [Term] is."
- Allowed: "What is [Term]?" (only if answer is a definition, not a fact/property).

Negation cards must be phrased as: "How does A differ from B?" with concrete tokens.

Counter-evidence cards must be phrased as: "When does X NOT apply?"

## Tier 1 Doctrine Coverage

Before serialization, verify these doctrine-driven intents are represented when the note contains the triggering elements:

- Hidden models present -> at least one MODEL card.
- Behavior change or failure modes present -> at least one FAILURE MODE card.
- Contradictions present -> at least one COUNTER-EVIDENCE card.
- Distinctions present -> at least one NEGATION card.
- Multi-concept notes -> at least one SYNTHESIS or comparison card.

If any required doctrine-driven card type is missing, regenerate the note before continuing.

## Internalization Linkage Requirements

Internalization must affect generation:

- At least 1 card reflects a boundary (negation/boundary framing).
- At least 1 card reflects a misconception (failure-mode framing).
- At least 1 card reflects a link (connectivity or synthesis framing).

If internalization exists but none of these appear, regenerate missing classes only.

## Connectivity Requirements

Connectivity cards must explicitly reference another H2 concept when the note contains multiple concepts.

## Conversion Quota (Depth Without Growth)

For every 5 PROCEDURE cards in a note, convert 1 into a deeper doctrine type by replacement.

Priority order:

1. MODEL
2. FAILURE_MODE
3. COUNTER_EVIDENCE
4. SYNTHESIS
5. NEGATION

Prefer conversion over append unless a required class is missing.

## Constructive Card Compression

For each code block:

- If block <= 5 lines -> 1 atomic card ("Write the code for...")
- If block > 5 lines -> decompose into 3-5 atomic cards.
- **Variant Rule**: Multiple cards for the same block must test materially different things (e.g., "Basic Usage" vs "Edge Case" vs "Error Handling"). Do not generate identical code snippets with slightly different questions.

## Per-Note Card Cap

max_cards_per_note = clamp(10 + code_blocks*2, 12, 18)

If code_blocks == 0, max_cards_per_note = 12

If exceeded, convert excess into deeper variants using the priority order below.

### Conversion Priority

When definition_cards > cap:

1. SYNTHESIS
2. MODEL
3. FAILURE_MODE
4. NEGATION

When procedure_cards > cap:

1. MODEL
2. FAILURE_MODE
3. SYNTHESIS
4. NEGATION

Never convert into more definitions or procedures.

## Doctrine Compliance Checklist

Use this checklist before TSV serialization:

- Mapping: H2/H3 structural mapping applied to all sections.
- Elements: content elements mapped to required card types.
- Coverage: every structural element yields >=1 card.
- Tier 1: MODEL, FAILURE MODE, NEGATION, COUNTER-EVIDENCE, SYNTHESIS present when triggered.
- Minimums: quantitative minimums satisfied when triggered.
- Connectivity: connectivity minimums satisfied when triggered.
- Internalization linkage: boundary, misconception, link reflected in cards.
- Internalization: internalization report present and complete.
- Budget: card counts aligned with card_budget_plan.
- Conversion quota: procedure-to-deep conversion quota satisfied.
- Quality: atomic, active recall, contextualized, unambiguous.
- Output: no rule metadata leaked into card text.

## Doctrine Compliance Report Format

Provide a structured report artifact with these fields:

```
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
  conversion_quota_ok: <true|false>
  quality_ok: <true|false>
  output_purity_ok: <true|false>
  failures:
    - <short_reason>
```

If any field other than `all_checks_passed` is false, set `all_checks_passed` to false and regenerate.

## Redundancy and Uniqueness (Strict)

- **Uniqueness**: No two cards may cover the same question-answer pair.
- **Deduplication**: If two cards share >80% front or back similarity, keep only the one with higher Tier 1 alignment.
- **Cross-Note Check**: In folder mode, ensure questions are unique across the entire corpus.

## Output Guardrails

- Output TSV with 3 columns: FRONT, BACK, OBSIDIAN_URL.
- **Content Purity**: 
  - Strip all Obsidian callout syntax (e.g., `[!danger]`, `[!info]`) from card backs.
  - Do not include "Rule:", "Evidence:", or metadata labels in card text.
- Code answers must be HTML-serialized with `<pre><code>` and no real newlines.
- Obsidian URLs must be vault `mohamed`, URL-encoded path, and no `.md` suffix.

## Stop and Fail Protocol (Strict)

If doctrine compliance (Tier 1 coverage, minimums, or internalization linkage) fails after 3 regeneration attempts:
- Abort the process for that note.
- Do NOT output a non-compliant TSV.
- Report the failure clearly in the final summary.
- It is better to output nothing than to output a shallow, non-compliant deck.
