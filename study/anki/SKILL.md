---
name: anki
description: >-
  Generates Anki flashcards in TSV format from source material using spaced
  repetition best practices. Supports Basic, Reversed (bidirectional), and Cloze
  card types with configurable quantity and difficulty. Use when generating
  flashcards, creating Anki cards, making study cards, converting notes to
  flashcards, turning a transcript into flashcards, or building a spaced
  repetition deck.
---

# Anki Flashcard Generator

Generate Anki flashcards from any source material. Produces TSV files ready for direct import.

## Reference Files

| File                                   | Read When                                                      |
| -------------------------------------- | -------------------------------------------------------------- |
| `references/card-design-rules.md`      | Default: card construction, anti-patterns, bidirectional rules |
| `references/tsv-format-spec.md`        | Formatting output as TSV                                       |
| `references/difficulty-calibration.md` | Applying difficulty and quantity settings                      |

## Parameters

Ask the user for these before generating. Default to Standard / Medium if not specified.

### Number of cards

| Setting  | Cards   | Strategy                                                           |
| -------- | ------- | ------------------------------------------------------------------ |
| Fewer    | 15-25   | High-priority concepts only. Every card earns its place.           |
| Standard | 30-50   | Balanced coverage. Core concepts plus important supporting detail. |
| More     | 60-100+ | Comprehensive. Includes nuance, edge cases, and worked examples.   |

### Difficulty

| Level  | Cognitive task                              | Card style                                                   |
| ------ | ------------------------------------------- | ------------------------------------------------------------ |
| Easy   | Recognition, definition, identification     | "What is X?", "Define X", single-fact cloze                  |
| Medium | Application, comparison, analysis           | "Why does X matter?", "Compare X and Y", multi-cloze         |
| Hard   | Synthesis, evaluation, multi-step reasoning | "How would you apply X to Y?", scenario-based, chained cloze |

## Workflow

```
- [ ] 1. Collect source material
- [ ] 2. Confirm parameters
- [ ] 3. Identify key concepts
- [ ] 4. Assign topics and priorities
- [ ] 5. Choose card types
- [ ] 6. Draft cards
- [ ] 7. Format as TSV
- [ ] 8. Self-review
- [ ] 9. Output
```

### 1. Collect source material

Read the provided content (transcript, document, skill, etc.). Every card must trace to the source material. Do not generate cards from general knowledge.

### 2. Confirm parameters

Ask the user for card count and difficulty if not specified. Default to Standard / Medium.

### 3. Identify key concepts

Extract core facts, definitions, relationships, formulas, benchmarks, and frameworks from the source. Group by topic.

- If the note has a “### Notes” section: treat each top-level bullet as one theory item → generate 1 theory card per bullet (sub-bullets are supporting detail only).
- Code cards do not replace theory cards.

### 4. Assign topics and priorities

Map each concept to a topic tag (kebab-case). Assign priority levels:

- `priority::high` — Core concepts that appear repeatedly or underpin other ideas
- `priority::medium` — Supporting detail that strengthens understanding
- `priority::low` — Reference knowledge, nice to have

### 5. Choose card types

Select the card type based on what is being tested:

**Basic** — Direct Q&A for explanations, reasoning, comparisons, processes.

- Front: A specific question. Never yes/no. Never vague ("Tell me about X").
- Back: Concise answer with `<b>bold</b>` on the key phrase the learner must recall.

**Reversed (bidirectional)** — For terminology, translations, concept ↔ example pairs.

- Generate two separate Basic cards: Term → Definition AND Definition → Term.
- Only reverse when both directions produce useful recall. Do NOT reverse explanatory or reasoning cards.
- Tag both cards with `reversed` modifier.

**Cloze** — For port numbers, specific values, command syntax, formulas, numeric benchmarks.

- Text: Complete sentence with `{{c1::blanks}}` replacing key values.
- Use multiple deletions (c1, c2, c3...) when values belong to one coherent fact.
- Tag with `formulas` for formulas, `benchmarks` for numeric thresholds.

### 6. Draft cards

Write each card following the design rules in `references/card-design-rules.md`. Apply difficulty calibration from `references/difficulty-calibration.md`.

### 7. Format as TSV

Format cards following the exact specification in `references/tsv-format-spec.md`.

### 8. Self-review

Check every card against the quality checklist below. Remove or rewrite any that fail.

### 9. Output

Present Basic cards and Cloze cards as separate TSV code blocks. Include count summary and import instructions:

1. Open Anki → File → Import
2. Select the TSV file
3. Set note type to "Basic" or "Cloze" as appropriate
4. Map fields: Field 1 → Front/Text, Field 2 → Back/Extra, Field 3 → ObsidianURL Field 4 -> Tags

## Quality Checklist

Every card must pass all of these:

- [ ] **Atomic** — Tests exactly one fact. If you need "and" to describe what it tests, split it.
- [ ] **8-second rule** — A prepared learner can answer in under 8 seconds.
- [ ] **Source-grounded** — The answer comes from the provided source material, not general knowledge.
- [ ] **Useful for recall** — Tests meaningful knowledge, not trivial facts.
- [ ] **No orphans** — The learner can understand this card without needing another card first.
- [ ] **Bold highlight** — The answer has at least one `<b>bold</b>` phrase marking the key recall target.
- [ ] **Specific question** — The front asks a precise question, not "Tell me about X".
- [ ] **No yes/no** — Never a question answerable with yes or no.
- [ ] **No shopping lists** — Never "List the 7 types of..." (break into individual cards or use cloze).
- [ ] **Tagged** — Has exactly one topic tag and one priority level.
- [ ] **Difficulty-appropriate** — Matches the requested difficulty level.
- [ ] **Front MUST NOT contain the final code lines required in Back.**
- [ ] **code blocks questions front are like leetcode questions, front is the question and back is the solution where the solution is the code block itself.**
- [ ] Theory coverage: _if “### Notes” exists, every top-level bullet produced at least 1 theory card (code cards don’t count)._

---

## Programming / Code Block Cards — Lead-Code Standard (Mandatory)

### 0) When this section applies

If a source note contains **any code block**, you MUST generate **≥ 1 constructive code-context card** for that note.
Code blocks are **not** AIUs; extract the highest-signal AIU(s) from the code and test those.

---

### 1) Definitions (use these terms consistently)

**Leet-code prompt**
A leetcode-style problem statement where the learner can answer **without seeing the note**, because the prompt contains all needed constraints/spec.

**Code witness**
A minimal runnable artifact included in the prompt: signature, data shapes, invariants, small trace/example, and the expected output shape. Coding prompts MUST include this.

**Leakage**
Any content on the Front that contains the solution (or near-solution) for what the learner must produce. This is forbidden.

---

### 2) Non-negotiable constraints (hard gates)

**Self-contained Front**
The Front MUST be understandable alone: no “in the note…”, no filename references, no “see above”.

**TSV-safe code formatting**

- No literal newlines in any field; use `<br>` for line breaks.
- Escape `< > &` as `&lt; &gt; &amp;`.
- Only allowed HTML tags: `<b>` and `<br>` (NO `<code>`).

**Output shape is mandatory**
Every code prompt must explicitly state what the output looks like (return value / mutation / printed output).

---

### 3) The “Lead-Code” card types (choose exactly one per selected code block)

#### A) Hard — Full Block Synthesis (preferred when the block is high-signal)

**Front structure (leetcode-style):**

1. **Goal**: what the function/program must do
2. **Inputs**: types + constraints
3. **Outputs**: exact shape
4. **Rules/Constraints**: invariants, time/space notes if relevant
5. **Edge cases**: at least 1–3
6. (Optional) **Example**: input → output
7. **Task**: “Write the full code block …”

**Leakage limits for Hard full-block cards**

- Front MAY include: signature + data types + a skeleton with `TODO` placeholders.
- Front MUST NOT include any finished helper logic, loop bodies, condition bodies, recursion bodies, or the key algorithmic lines that appear in the Back.
- If Back is the entire code block, the Front must contain **0 solution lines** beyond the signature / placeholder skeleton.

This aligns with the “answer is the actual code block” contract.

#### B) Medium — Patch / Fill / Debug (preferred when full synthesis is too big)

Use a **small code witness** and force one precise production action:

- “Write the missing line(s) that update X”
- “Complete the base case”
- “Add the accumulator update”
- “Fix the bug and name one concrete failure mode if unfixed”

(Keep it atomic: one action + one expected output or failure).

---

### 4) Mechanical procedure (apply to ANY note; no creativity needed)

For each note that contains code blocks:

**Step 1 — Pick target**

- all of the code blocks in the note

**Step 2 — Choose card type**

- leetcode style question for each code block in given note

**Step 3 — Build the code witness (Front)**
Include only:

- Language + function signature
- Data shapes (e.g., “list of ints”, “tree node has left/right”)
- Invariants / rules
- 1 short example or trace (optional but strongly recommended)
- Explicit output shape

**Step 4 — Write the Task line**

- Hard: “Write the full code block that satisfies the spec.”
- Medium: “Write the missing line(s) and state one concrete failure if done incorrectly.”

**Step 5 — Write the Back**

- Hard: include the full final code block (TSV-safe: `<br>` lines, escaped chars).
- Medium: include only the exact line(s) + 1–2 sentence explanation with `<b>` on the recall target.

**Step 6 — Run the leakage test (must pass)**
Fail the card and rewrite if any of these are true:

- The Front contains the same non-trivial solution lines that appear in the Back (beyond signature/skeleton).
- The Front includes complete algorithmic bodies (loop/recursion/condition bodies) for a “write full code” task.
- The prompt says “refer to the note / file / above”.

**Step 7 — Final quality gates**

- Front is unambiguous + single-target; Back is univocal.
- TSV rules enforced: no tabs/newlines, `<br>` for line breaks, escape entities, only `<b>`/`<br>`.

---

### 5) Templates (copy/paste and fill)

#### Hard Template — Full Block (Front)

Use TSV-safe formatting (`<br>`). Do NOT include final logic.

```text
[Language: ____]<br>
Implement: ____ (function name)<br>
Description: ____<br>
Signature: ____<br>
Inputs: ____ (types + constraints)<br>
Output: ____ (exact shape)<br>
Rules / invariants:<br>
- ____<br>
- ____<br>
Edge cases:<br>
- ____<br>
Example:<br>
Input: ____ → Output: ____<br>
Task: Write the full code block that satisfies the spec.
```

#### Medium Template — Patch/Debug (Front)

```text
[Language: ____]<br>
You are given this partial code skeleton:<br>
____ (signature)<br>
____ (2–6 lines of non-solution scaffolding / TODO placeholders)<br>
Constraints / expected output shape: ____<br>
Task: Write the missing line(s) marked TODO, and name one concrete failure mode if the TODO is implemented incorrectly.
```

## Tag Syntax

Tags are space-separated within the Tags field. Order: topic tag, then priority, then modifiers.

```
topic-name priority::high
topic-name priority::medium formulas
topic-name priority::low reversed
```

- Topic tags: kebab-case (`python-basics`, `web-security`)
- Hierarchical topics: use `::` separator (`networking::protocols`)
- Priority: `priority::high`, `priority::medium`, `priority::low`
- Modifiers: `formulas`, `benchmarks`, `reversed`

## Output Format

**Basic cards:**

```
Question text here	Answer with <b>bold</b> key terms	topic-tag priority::level
```

**Cloze cards:**

```
Text with {{c1::blanks}} for key values		topic-tag priority::level formulas
```

Note: Cloze cards have an empty second field (two consecutive tabs).
