# Ankify Depth Templates

Use these canonical templates to satisfy doctrine requirements for deep card types.
If a card is tagged as one of these types but does not match a template, it does not count toward the minimums.

## MODEL (Mental Model)

**Intent:** Force the user to visualize the mechanism, state changes, or invisible flow.
**Trigger:** Hidden logic, lifecycles, state machines, architecture.

| Template | Example |
|----------|---------|
| `Explain/visualize how [Concept] works.` | "Explain/visualize how the Event Loop handles async callbacks." |
| `What are the stages of [Process]?` | "What are the stages of the React render lifecycle?" |
| `Trace the flow of [Data] through [System].` | "Trace the flow of a request through the Express middleware stack." |

**Forbidden (Too Shallow):**
- "What is the model for X?"
- "How does X work?" (Too vague)

## FAILURE_MODE (Pre-mortems)

**Intent:** Encode "pain avoidance" and operational boundaries.
**Trigger:** Pitfalls, common errors, edge cases, "don't do this" warnings.

| Template | Example |
|----------|---------|
| `What goes wrong if you [Concrete Misuse]?` | "What goes wrong if you mutate state with push in React?" |
| `[System] breaks if [Concrete Condition]. Explain why.` | "The build breaks if you import circularly between A and B. Explain why." |

**Must include:** a concrete incorrect action and a concrete consequence.

**Forbidden:**
- "What goes wrong if X is misused?"
- "Is X bad?"
- "Name one error."

## COUNTER_EVIDENCE (Nuance)

**Intent:** Break the "always true" heuristic. Prevent overgeneralization.
**Trigger:** Exceptions to rules, specific context constraints, trade-offs.

| Template | Example |
|----------|---------|
| `When does [Concept/Rule] NOT apply?` | "When does the Same-Origin Policy NOT apply?" |
| `Under what condition does [Assertion] fail?` | "Under what condition does `useEffect` fail to run on mount?" |

**Forbidden:**
- "What contradicts X?"
- "Is X always true?"

## NEGATION (Boundaries)

**Intent:** Define what something is *not* to sharpen the mental category.
**Trigger:** Distinctions, "X is not Y", boundaries.

| Template | Example |
|----------|---------|
| `How does [A] differ from [B]?` | "How does `map` differ from `forEach`?" |

**Must include:** two concrete tokens from the note.

## SYNTHESIS (Connections)

**Intent:** Connect two isolated concepts (H2s) to build a knowledge graph.
**Trigger:** Multi-concept notes, interactions, tradeoffs.

| Template | Example |
|----------|---------|
| `Compare [A] and [B] regarding [Dimension 1] and [Dimension 2].` | "Compare `map` and `forEach` regarding mutation and return value." |

**Must reference:** Two distinct concrete tokens and at least two dimensions.
