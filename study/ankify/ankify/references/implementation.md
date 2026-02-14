# ANKIFY Implementation Notes (v4)

## Doctrine Precedence

Load `references/doctrine.md` before `references/schema.md`.
If any executable rule conflicts with doctrine, follow doctrine and treat the schema rule as stale.

## 5-Stage Pipeline

```
STAGE 1 - DISCOVERY
  Scope: PRE_DISCOVERY (R-PD-001 through R-PD-006)
  Input:  user invocation (file, folder, or cwd)
  Output: file_manifest with status fields
  Gate:   R-PD-006 must pass - all files accounted for

STAGE 2 - ANALYSIS
  Scope: POST_DISCOVERY (R-POD-001 through R-POD-007)
  Input:  each file from manifest
  Output: element_inventory, context_map, rule_application_plan, classification
  Gate:   R-POD-006 must pass - plan built for all Tier 1 rules

If parse_success == false and file_text_length > 0, mark file_status as PARTIAL_READ and continue best-effort.
Include PARTIAL_READ counts in the execution report.

STAGE 2.5 - CONCEPT INTERNALIZATION
  Scope: POST_DISCOVERY
  Input:  element_inventory + classification
  Output: internalization_report (summary, boundaries, misconceptions, links)
  Gate:   internalization_report must be present before STAGE 3

Produce `internalization_report` in the format specified in `references/doctrine.md`.

STAGE 2.7 - CARD BUDGET PLANNING
  Scope: POST_DISCOVERY
  Input:  element_inventory + concept_count + presence flags
  Output: card_budget_plan
  Gate:   card_budget_plan must be present before STAGE 3

STAGE 3 - GENERATION
  Scope: PRE_CARD (R-PC-001 through R-PC-006)
       + PER_CARD (R-C-001 through R-C-021)
       + POST_CARD (R-POC-001 through R-POC-006)
  Input:  rule_application_plan + extracted elements
  Output: validated card set
  Gate:   All POST_CARD rules pass - every section covered
  Loop:   If POST_CARD fails -> regenerate missing cards -> re-validate

STAGE 4 - VALIDATION
  Scope: POST_NOTE (R-PN-001 through R-PN-005)
  Input:  complete card set for note
  Output: coverage report, SDI check
  Gate:   R-PN-002 (Tier1 coverage) + R-PN-004 (SDI) must pass
  Loop:   If validation fails -> return to STAGE 3 -> regenerate -> re-validate

STAGE 5 - SERIALIZATION
  Scope: SERIALIZATION (R-S-001 through R-S-013)
       + GLOBAL (R-G-001 through R-G-004)
  Input:  validated card set
  Output: .tsv file + execution report
  Gate:   R-S-012 (awk validation) must pass with ZERO failures
  Loop:   If R-S-012 fails -> R-S-013 activates -> fix -> re-validate -> loop
```

Before STAGE 5, run the doctrine compliance checklist from `references/doctrine.md`.
If any doctrine requirement fails, return to STAGE 3 and regenerate.

Produce `doctrine_compliance_report` in the format specified in `references/doctrine.md`.

Produce `card_budget_plan` in the format specified in `references/doctrine.md`.

## Regeneration Limits

Track regeneration attempts per note and per run.
If attempts exceed 3, abort with an explicit failure and do not loop.

## Validation Script

Use `scripts/validate_tsv.sh` after serialization.

## Budget and Compliance Scripts

- Use `scripts/compute_card_budget_pre.py --note-meta <note_meta.json> --output <card_budget.json>` for pre-generation budgets.
- Use `scripts/compute_doctrine_report.py --counts <counts.json>` to build `doctrine_compliance_report`.
- Use `scripts/compute_doctrine_report.py --counts <counts.json> --require-run-stats` to enforce run-level stats in folder mode.
- Use `scripts/build_counts.py --input <raw_stats.json> --output <counts.json>` to normalize stats.
- Use `scripts/parse_note.py --input <note.md> --output <note_meta.json>` to extract structure.
- Use `scripts/validate_cards.py --tsv <output.tsv> --note-metadata <note_meta.json> --output <raw_stats.json>` to compute raw stats.
- Use `scripts/aggregate_run_stats.py --inputs <raw_stats.json>... --output <run_stats.json>` for folder mode.
- Use `scripts/run_ankify_checks.sh <note.md> <output.tsv> [run_stats.json]` for a one-shot run.
- Set `REQUIRE_RUN_STATS=1` to fail when run-level stats are missing.

## Prune Artifacts

When pruning, produce:

- prune_plan
- redundancy_report

Deprecated:
- `scripts/compute_card_budget.py` (post-generation budgets)

## Card Type Normalization

Use a canonical internal set:

THEORY, CONSTRUCTIVE, SYNTHESIS, MODEL, FAILURE_MODE, NEGATION, COUNTER_EVIDENCE, DEFINITION, PROCEDURE

`scripts/validate_cards.py` normalizes common variants (e.g., COUNTER-EVIDENCE, FAILURE MODE) to this set.

### counts.json schema (required fields)

- concept_count
- h2_count
- total_cards
- synthesis_cards
- cross_h2_synthesis_cards
- model_cards
- failure_mode_cards
- negation_cards
- counter_evidence_cards
- connectivity_cards
- definition_cards
- procedure_cards
- mental_models_present
- failure_modes_present
- contradictions_present
- distinctions_present
- failure_mode_triggers_present
- mapping_ok
- elements_ok
- coverage_ok
- tier1_ok
- quality_ok
- output_purity_ok
- internalization_ok
- internalization_linkage_ok
- budget_ok

## Targeted Regeneration Rules

- If only one class is missing, regenerate that class only and append.
- If only caps are violated, convert excess cards according to the doctrine conversion priority.
- Do not rewrite valid cards unless TSV validation fails.
- Full rewrite allowed only when tsv_validation_failed == true.

## POST-GEN PRUNE (Required)

After validation and before TSV serialization, prune to reduce deck size while preserving minimums.

- Never delete required minimum types until all minimums pass.
- Prefer deleting: definitions -> procedures -> shallow theory -> excess constructive.
- Keep at least one definition per H2 concept.
- Keep 2-4 constructive cards per code block.

## Redundancy Detection

Use `scripts/redundancy_prune.py --cards <cards.json> --output <prune_plan.json>` to detect near-duplicate fronts.
Apply the prune plan after minimums pass and before serialization.

## Global Failure-Mode Minimum

In folder mode, enforce:

- global_failure_mode_cards >= ceil(total_cards / 25)
- minimum 1 if total_cards > 0

Only enforce per-note failure-mode minimum when the note contains mistake/pitfall/warning language.

## Artifact Requirements

Must create the following artifacts for each run:

- file_manifest
- element_inventory
- rule_application_plan
- internalization_report
- card_budget_plan
- doctrine_compliance_report

## Input Modes

| User Says | Agent Behavior |
|-----------|----------------|
| `ankify <filename>` | Process single file -> create `<filename>.tsv` |
| `ankify .` or `ankify current folder` | Process ALL `.md` files in CWD -> create unified `ankify_output.tsv` |
| `ankify <folder>` | Process ALL `.md` files in folder -> create unified `<folder>_ankify.tsv` |
| `ankify <folder> --exclude <pattern>` | Process folder, skip files matching pattern |

## Folder Processing

1. Scan target directory for all `.md` files (recursive).
2. Exclude: `node_modules`, `.git`, `.obsidian` (default), plus user exclusions.
3. Build file manifest - list ALL discovered files with status field.
4. Process each file through the 5-stage pipeline.
5. Mark each file PROCESSED on manifest after completing.
6. Append all cards to ONE unified `.tsv` file.
7. Track source file internally for Obsidian URL generation.

## Tier Classification Reference

### TIER 1: GENERATION DRIVERS

These rules directly dictate WHAT cards to create. Evaluate every Tier 1 rule during STAGE 2.

| Rule ID | Name | What It Generates |
|---------|------|-------------------|
| PR-0003 | Generation Effect | Forces paraphrasing - no copy-paste answers |
| PR-0004 | Hidden Models | MODEL cards: "Explain/visualize how X works" |
| PR-0005 | Behavior Change | FAILURE MODE cards with emotional weight |
| PR-0017 | Idea Interaction | COMPARISON/SYNTHESIS cards: "X vs Y" |
| PR-0038 | Confirmation Bias | COUNTER-EVIDENCE cards: "What contradicts X?" |
| PR-0045 | Negation/Inversion | NEGATION cards: "What is X NOT?" |
| PR-0047 | Mere-Exposure | Forces active recall format ("Write..." not "What does...") |
| EL-PR-0001 | Understanding First | No cards for material not fully understood |
| EL-PR-0003 | Basics-First | Theory/foundational cards before advanced code |
| EL-PR-0004 | Atomicity | Each card = ONE idea (max 6 lines for code) |
| EL-PR-0009 | Set Avoidance | No "list 5 things" cards - decompose into atomic cards |
| EL-PR-0015 | Emotional Salience | Use emotionally charged examples to aid retrieval |
| Orphan Rule | >=1 per element | At least 1 card per structural element |
| SDI Rule | Structural Density | cards >= structural_elements AND SDI <= 2.5 |
| 10-min Rule | Value Heuristic | Only card-ify what is worth 10 min of future time |
| Yes/No Rule | Question Smell | No yes/no questions - refactor into elaborative form |
| Chunking Rule | Pattern Cards | Experts internalize chunks (patterns), not whole files |

### TIER 2: CARD QUALITY CONSTRAINTS

These rules constrain HOW cards should look. Apply during generation.

| Rule ID | Constraint |
|---------|------------|
| PR-0001 | Intentionality - every card is a deliberate choice |
| PR-0018 | Context Docking - anchor to prior knowledge |
| PR-0022 | Signal-to-Noise - high-signal, low-noise prompts |
| PR-0046 | Feynman Test - plain language only |
| PR-0016 | Connectivity - cards reference broader concepts |
| EL-PR-0002 | Contextual Scaffolding - derived from structured understanding |
| EL-PR-0011 | Interference Prevention - unambiguous items |
| EL-PR-0012 | Word Choice - fewer words, no trailing messages |
| EL-PR-0013 | Semantic Anchoring - familiar words in questions |
| EL-PR-0016 | Domain Context Cues - prefix with context label |
| EL-PR-0018 | Source Traceability - include source reference |
| Context Mandate | NEVER force guessing of variables/imports/state |
| Whiteboard Rule | Code cards demand creation, not recognition |
| Decomposition Rule | Code blocks >5 lines -> decompose into 3-5 atomic cards |

## Obsidianize Note Structure Map

Input notes follow the Obsidianize structure. H2 sections = atomic concepts. H3 subsections map to card types:

| H3 Subsection | -> Card Type |
|---------------|-------------|
| **Notes** | Theory Cards. Each bolded rule = 1 card. |
| **Distinctions & Negations** | Negation Cards. Each distinction = 1 card. |
| **Counter-Evidence** | Counter-Evidence Cards. Each contradiction = 1 card. |
| **Definitions** | Definition Cards. Each term = 1 card. |
| **Configuration** | Procedure Cards. Setup steps = 1 card. |
| **Technical Procedures** | Procedure Cards. Each workflow = 1 card. |
| **Code Implementation** | Constructive Cards. <=5 lines = 1 card. >5 lines = decompose. |

## Card Type -> Content Element Mapping

```
Code block (<=5 lines)  -> 1 CONSTRUCTIVE card ("Write the code for...")
Code block (>5 lines)   -> DECOMPOSE into 3-5 atomic cards (2-6 lines each per answer)
Bolded rule/pattern     -> THEORY card ("What is the rule for..." / "Explain why...")
Distinction (X != Y)    -> NEGATION card ("What is X NOT?" / "X vs Y")
Counter-evidence        -> COUNTER-EVIDENCE card ("What contradicts X?")
Definition              -> DEFINITION card ("What is [term]?")
Configuration           -> PROCEDURE card ("How do you set up X?")
Mental model            -> MODEL card ("Explain/visualize how X works")
Common mistake          -> FAILURE MODE card ("What goes wrong if you do X?")
```

## TSV Format Specification

Every output line: `FRONT<TAB>BACK<TAB>OBSIDIAN_URL`

| Column | Content | Format |
|--------|---------|--------|
| FRONT | Question only | `<strong>[Topic]</strong><br>Question?` |
| BACK | Answer only | Plain text OR `<pre style='text-align:left; font-family:monospace;'><code>...</code></pre>` |
| URL | Obsidian deep link | `obsidian://open?vault=mohamed&file=<urlencoded_path>` |

### Code Block Serialization (for EVERY code answer)

1. Replace every `\n` with `<br>`
2. Replace every space (indentation) with `&nbsp;`
3. Replace every tab with `&nbsp;&nbsp;&nbsp;&nbsp;`
4. Wrap in `<pre style='text-align:left; font-family:monospace;'><code>...</code></pre>`
5. Verify: ZERO real newlines in final line

### Obsidian URL Construction

1. Vault is ALWAYS `mohamed`
2. Extract path relative to vault root
3. URL-encode: `/` -> `%2F`, spaces -> `%20`
4. Remove `.md` extension
5. Result: `obsidian://open?vault=mohamed&file=programming%2Fnode%2Fandrew%2Fmongodb`

### Output File Rules

- Single file: `<input_filename>.tsv`
- Folder mode: `ankify_output.tsv`
- Custom: `--output <filename>` override

### Post-Generation Validation Script

```bash
awk -F'\t' '{
  if (NF != 3) print "FAIL line " NR ": " NF " columns (expected 3)"
  if ($1 ~ /\[Source:/) print "FAIL line " NR ": [Source:] in FRONT column"
}' "$OUTPUT_FILE"
```

If ANY line fails -> fix -> rewrite -> re-run -> only report success at ZERO failures.
