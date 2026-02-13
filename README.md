# 📘 agent_system_context.md

```markdown
# Agent System Context — Architecture & Design Doctrine

This document explains the internal mechanics, philosophy, and structural evolution of the Obsidianize and Ankify agents.

This is NOT a user-facing README.
This is a structural and architectural reference for advanced users and future agent sessions.

---

# 1. System Overview

The system consists of two primary agents:

- **Obsidianize** → Knowledge synthesis and structured note generation
- **Ankify** → Atomic flashcard generation in strict TSV format

Both agents now share a common architectural principle:

> Rules inform reasoning.  
> Arbitration controls activation.  
> Budget constrains output.  
> Guardrails enforce validity.

They are no longer template engines.
They are constrained reasoning engines.

---

# 2. The Core Design Problem (Historical Context)

Earlier versions suffered from:

- Rule coverage absolutism
- Mandatory quotas (5–20 cards, 2–3 per topic, type quotas)
- Per-rule enforcement loops
- Backfill generation (“GO BACK and generate missing”)
- Structural completionism
- Deep Drill overriding safety mechanisms

This caused:

- 8 nodes → 64 cards
- Artificial card inflation
- Template bloat
- Redundant structural sections
- Cognitive overload

The root cause:

> Philosophical rules were treated as structural obligations.

This created explosion.

---

# 3. The Architectural Solution

The system now uses a 4-layer execution model:

## Layer 1 — Signal Extraction

The agent extracts candidate elements from input:

- Definitions
- Distinctions
- Counter-evidence
- Procedures
- Code blocks
- Failure modes
- Mental models

Rules do NOT force output here.
They only identify possible candidates.

---

## Layer 2 — Arbitration & Budget

Before generation:

1. Estimate content weight.
2. Estimate output budget.
3. Rank candidates by value.
4. Apply sacrifice order if overflow.
5. Lock the Activation Set.

After this point:

> No rule may force generation outside the locked Activation Set.

This prevents backfill loops and structural explosion.

---

## Layer 3 — Controlled Generation

Only candidates in the locked Activation Set are generated.

Generation rules apply conditionally:

- Atomicity enforced.
- Code decomposition applied if selected.
- Context injection applied to generated code cards.
- No quotas.
- No rule-count enforcement.
- No mandatory type balancing.

---

## Layer 4 — Guardrail Verification

Validation checks:

- Format correctness.
- No fabrication.
- Budget adherence.
- Density guardrails.
- No structural violations.

Validation does NOT check:
- Rule coverage.
- Minimum counts.
- Quota satisfaction.

Guardrails enforce validity — not completeness.

---

# 4. Shared Architectural Pattern

Both agents follow:

```

Signal → Candidates → Budget → Lock → Generate → Validate

```

They do NOT follow:

```

Rules → Mandatory Output → Coverage Audit → Backfill

```

This distinction is critical.

---

# 5. Obsidianize — Detailed Mechanics

## Purpose

Convert source material into structured Obsidian-compatible notes.

## Phases

### Phase 1 — Extraction & Weight Classification

- Extract signal elements.
- Classify weight (W1–W4).
- Determine structural eligibility.

### Phase 2 — Arbitration Engine

- Apply signal gating.
- Allocate budget.
- Apply sacrifice order.
- Lock Activation Set.

Deep Drill:
- Expands depth within activated categories.
- NEVER expands activation count.
- NEVER bypasses ceilings.

### Phase 3 — Structured Output

Generate only budgeted sections.

Conditional sections (Distinctions, Counter-Evidence, Config, etc.) are only created if:

- Signal exists.
- Budget allows.

### Guardrails

- Hard ceilings enforced.
- Density ratio enforced.
- No backfill.
- No exhaustive reconstruction.

---

# 6. Ankify — Detailed Mechanics

## Purpose

Convert structured notes into atomic Anki cards in strict TSV format.

## Phases

### Phase 1 — Signal Extraction

Extract:

- Definitions
- Explicit distinctions
- Procedures
- Code blocks
- Failure modes
- Mental models

### Phase 2 — Arbitration & Budget

- Estimate card budget.
- Rank candidate cards.
- Apply sacrifice order.
- Lock Activation Set.

No quotas.
No per-section minimums.
No rule coverage enforcement.

### Phase 3 — Generation

For candidates in locked set:

- Enforce atomicity.
- Enforce no yes/no.
- Enforce no copy-paste.
- Apply decomposition if code > threshold.
- Inject full context into code card FRONT.

### Phase 4 — Validation

- TSV strict formatting.
- Exactly 3 columns.
- No raw newlines.
- Correct Obsidian URL.
- Post-generation validation script.

No coverage audits.
No type balancing quotas.

---

# 7. Sacrifice Order (System-Level)

If budget overflow occurs, drop in this order:

1. Redundant reformulations
2. Low-value comparisons
3. Secondary distinctions
4. Optional mental model expansions

Never drop:

- Core definitions
- Major failure modes
- Selected code coverage
- Primary conceptual anchors

---

# 8. Non-Negotiable Invariants

These rules are hard:

- Atomic cards (one idea per card)
- Code answers ≤6 lines
- Context injection for generated code cards
- Strict TSV formatting
- No fabrication
- Activation set lock
- No post-generation expansion
- No quotas
- No backfill

---

# 9. What The System Is NOT

It is not:

- A coverage engine
- A completeness machine
- A template expander
- A quota-driven generator
- A rule-count satisfier

It is:

> A constrained reasoning system.

---

# 10. Why Arbitration Is Central

Without arbitration:

Rules become structural mandates.

With arbitration:

Rules become candidate intelligence.

This is the foundational design shift.

---

# 11. Stability Guarantees

The system is stable because:

- No rule can force output.
- No section is mandatory without signal.
- Deep Drill cannot increase activation count.
- Budget is estimated before generation.
- Activation Set is locked.
- Guardrails enforce boundaries.
- Validation does not enforce coverage.

---

# 12. Future Extension Policy

When modifying agents:

1. Never reintroduce quotas.
2. Never reintroduce rule-count audits.
3. Never allow backfill loops.
4. Never allow Deep Drill to expand activation count.
5. Never bypass Activation Set lock.
6. Never move guardrails below generation.
7. Never treat rules as structural obligations.

If a rule appears to require mandatory output:

It must go through arbitration first.

---

# 13. System Philosophy (Concise)

Rules define how the agent reasons.
Arbitration defines what gets activated.
Budget defines how much is produced.
Guardrails define what is allowed.
Validation defines what is acceptable.

That is the architecture.

---

End of Document.
```

---

If you want next:

* I can create a shorter **User Mental Model Guide**
* Or a visual diagram version
* Or a simplified explanation for collaborators
* Or the formal README

You’ve now built something structurally serious.
