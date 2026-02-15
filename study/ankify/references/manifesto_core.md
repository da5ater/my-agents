# Manifesto Core (Runtime Rules)

Derived from `references/manifisto.md`. This file is the runtime rule-set.
If any rule fails validation, the run must fail (quality_ok=false).

## Immutable Core Mandates

### Context Mandate (PR-0018)

Never force the user to guess variable names, imports, state shapes, or schema rules.

### Interview Readiness

Prepare for senior technical interview tasks by requiring active recall prompts
and avoiding yes/no or recognition-only questions.

### Whiteboard Rule

Focus on technical/code concepts. Demand creation, not recognition.

## Signal-to-Noise (PR-0022)

Minimize cognitive tax with high-signal, low-noise prompts.

## Actualization Table (Machine-Checkable)

| RULE_ID | Trigger | Enforce | Measure | Repair |
|---|---|---|---|---|
| MC-CTX-001 | card_type == CONSTRUCTIVE | Include explicit context and anchors | Front contains "Given:" and "Task:" and references >=1 anchor token | Rewrite front/back using code snippet and anchors, or convert to deep type |
| MC-WHITEBOARD-001 | card_type == CONSTRUCTIVE | Demand a single atomic creation task | Task contains a single action; code answer <= 2 lines | Rewrite to a closed one-line task, or convert to deep type |
| MC-INTERVIEW-001 | any card | Active recall only, no yes/no prompts | Front does not start with yes/no prefixes; uses active recall form or Given/Task | Rewrite prompt to active recall form |
| MC-SIGNAL-001 | any card | No filler or generic answers | Back does not match banned filler patterns; deep cards are anchored | Rewrite answer with anchored specifics |
