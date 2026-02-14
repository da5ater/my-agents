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
Distinction (X != Y)    -> NEGATION ("What is X NOT?" / "X vs Y")
Counter-evidence        -> COUNTER-EVIDENCE ("What contradicts X?")
Definition              -> DEFINITION ("What is [term]?")
Configuration           -> PROCEDURE ("How do you set up X?")
Mental model            -> MODEL ("Explain/visualize how X works")
Common mistake          -> FAILURE MODE ("What goes wrong if you do X?")
```

## Quality Constraints

- Keep fronts short, single-question, and plain language.
- Require active recall; avoid recognition-only prompts.
- Provide context docking and semantic anchors.
- Enforce unambiguous answers and interference prevention.
- For code cards: include variables/imports/scope/expected behavior; answers <= 6 lines.

## Coverage Expectations

- Every structural element yields at least one card.
- Every code block yields at least one constructive card.
- Every distinction/contradiction yields its matching card type.
- No section is silently skipped; skipped content must have a reason.

## Tier 1 Doctrine Coverage

Before serialization, verify these doctrine-driven intents are represented when the note contains the triggering elements:

- Hidden models present -> at least one MODEL card.
- Behavior change or failure modes present -> at least one FAILURE MODE card.
- Contradictions present -> at least one COUNTER-EVIDENCE card.
- Distinctions present -> at least one NEGATION card.
- Multi-concept notes -> at least one SYNTHESIS or comparison card.

If any required doctrine-driven card type is missing, regenerate the note before continuing.

## Doctrine Compliance Checklist

Use this checklist before TSV serialization:

- Mapping: H2/H3 structural mapping applied to all sections.
- Elements: content elements mapped to required card types.
- Coverage: every structural element yields >=1 card.
- Tier 1: MODEL, FAILURE MODE, NEGATION, COUNTER-EVIDENCE, SYNTHESIS present when triggered.
- Quality: atomic, active recall, contextualized, unambiguous.
- Output: no rule metadata leaked into card text.

## Doctrine Compliance Report Format

Provide a structured report artifact with these fields:

```
doctrine_compliance_report:
  all_checks_passed: <true|false>
  mapping_ok: <true|false>
  elements_ok: <true|false>
  coverage_ok: <true|false>
  tier1_ok: <true|false>
  quality_ok: <true|false>
  output_purity_ok: <true|false>
  failures:
    - <short_reason>
```

If any field other than `all_checks_passed` is false, set `all_checks_passed` to false and regenerate.

## Output Guardrails

- Output TSV with 3 columns: FRONT, BACK, OBSIDIAN_URL.
- Do not leak rule metadata into card fronts or backs.
- Code answers must be HTML-serialized with `<pre><code>` and no real newlines.
- Obsidian URLs must be vault `mohamed`, URL-encoded path, and no `.md` suffix.
