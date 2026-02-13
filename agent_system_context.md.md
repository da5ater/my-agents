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

