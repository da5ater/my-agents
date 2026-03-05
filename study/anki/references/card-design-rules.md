# Card Design Rules

## Contents

- [Core principles](#core-principles)
- [Minimum information principle](#minimum-information-principle)
- [8-second rule](#8-second-rule)
- [Bidirectional cards](#bidirectional-cards)
- [Card construction patterns](#card-construction-patterns)
- [Cloze-specific rules](#cloze-specific-rules)
- [Anti-patterns](#anti-patterns)
- [Progressive difficulty](#progressive-difficulty)
- [Phylosofical madates](#phylosofical-madates)
- [how to ask about a code block](#how-to-ask-about-a-code-block)

## Core principles

Every card must be:

- **Atomic** — Tests exactly one fact. One card, one recall target.
- **Source-grounded** — Traces directly to the provided source material. Never generate from general knowledge.
- **Recall-oriented** — Requires active retrieval, not passive recognition. The learner must produce the answer, not just recognize it.
- **Useful** — Tests meaningful knowledge the learner will actually need. Skip trivial facts, obvious definitions, and filler.

## Minimum information principle

One card = one fact. If you can split a card into two independent questions, you must.

**Bad — tests a set:**

```
Q: What are the four HTTP request methods used in REST APIs?
A: GET, POST, PUT, DELETE
```

**Good — one card per item:**

```
Q: Which HTTP method is used to retrieve a resource without modifying it?
A: <b>GET</b>
```

The exception: when the set itself is the atomic fact (e.g., a formula with named variables). In that case, use cloze deletion to test each variable individually.

## 8-second rule

A learner who knows the material should produce the answer in under 8 seconds. If the answer requires more than 2-3 sentences of recall, the card is too big. Break it down or convert to cloze.

Signs a card violates this rule:

- Answer is longer than 3 sentences
- Learner needs to mentally enumerate items
- Answer requires chaining multiple reasoning steps

## Bidirectional cards

Create reversed pairs for:

- **Terminology** — Term → Definition AND Definition → Term
- **Translations** — Source language → Target language AND back
- **Concept ↔ Example** — Concept → Concrete example AND Example → Concept name

Generate as two separate Basic cards. Tag both with the `reversed` modifier.

**Do NOT reverse:**

- Explanatory cards ("Why does X matter?")
- Reasoning cards ("How does X work?")
- Comparison cards ("How does X differ from Y?")
- Application cards ("When would you use X?")

Reversing these produces vague, unanswerable prompts.

**Example — good bidirectional pair:**

```
Forward: What is the term for a function passed as an argument to another function?
Back: <b>Callback</b>

Backward: What does a callback do?
Back: A function <b>passed as an argument</b> to another function, invoked after an operation completes
```

## Card construction patterns

| Pattern      | Front template                                                     | Back template                                   |
| ------------ | ------------------------------------------------------------------ | ----------------------------------------------- |
| Definition   | "What is X?" / "What does X mean?"                                 | "X is `<b>`key definition`</b>`"                |
| Comparison   | "How does X differ from Y?"                                        | "X does `<b>`A`</b>` while Y does `<b>`B`</b>`" |
| Application  | "When would you use X instead of Y?"                               | "Use X when `<b>`condition`</b>`"               |
| Cause-effect | "Why does X lead to Y?"                                            | "Because `<b>`mechanism/reason`</b>`"           |
| Context cue  | Prefix with topic area when ambiguous: "In [domain], what does..." | Same rules apply                                |

**Bold highlighting:**

- Always bold the exact phrase the learner must recall
- Bold 1-3 key phrases per answer, not entire sentences
- Use `<b>bold</b>` HTML tags (not Markdown)

**HTML rules:**

- `<b>` for bold key terms
- `<br>` for line breaks within a field
- No other HTML tags (`<i>`, `<ul>`, `<p>`, etc.)

## Cloze-specific rules

Use cloze deletion for:

- **Port numbers** — `SSH runs on port {{c1::22}}`
- **Specific values** — `TCP/IP has {{c1::4}} layers`
- **Command syntax** — `To stage all changes: {{c1::git add .}}`
- **Formulas** — `BMI = {{c1::weight (kg)}} / {{c2::height (m)}}²`
- **Numeric benchmarks** — `HTTP status {{c1::404}} means resource not found`

Rules:

- Multiple deletions (c1, c2, c3...) are fine when values belong to one coherent fact
- Each deletion generates a separate review card in Anki
- Never blank more than 30% of the text — the surrounding context must provide enough cue
- The blank must have exactly one correct answer. If multiple answers could fit, cloze is the wrong format.
- Keep the surrounding sentence specific enough to prime recall

**Bad cloze — too much blanked:**

```
The {{c1::___}} enzyme catalyzes the conversion of {{c2::___}} to {{c3::___}}
```

**Good cloze — enough context remains:**

```
BMI = {{c1::weight (kg)}} / {{c2::height (m)}}²
```

## Anti-patterns

| Anti-pattern       | Problem                                         | Fix                                                        |
| ------------------ | ----------------------------------------------- | ---------------------------------------------------------- |
| Kiddie card        | Trivially easy, zero learning value             | Skip it entirely — not everything deserves a card          |
| Midterm essay      | Answer is 5+ sentences, takes 30s+ to recall    | Split into 2-3 atomic cards                                |
| Shopping list      | "List the 7 types of..." tests rote sequence    | One card per item, or use overlapping cloze                |
| Yes/no question    | Binary answer, tests recognition not recall     | Reframe: "Is X a debt?" → "How is X classified?"           |
| Life hack card     | Generic advice, not testable knowledge          | Only create cards for testable, specific facts             |
| Vague prompt       | "Tell me about DNS" — no specific recall target | Ask a precise question with one expected answer            |
| Trivial fact       | Tests something obvious or self-evident         | Focus on knowledge that requires effort to retain          |
| Overly long answer | Buries the key point in paragraphs              | Trim to 1-3 sentences with bold on the key phrase          |
| Example trap       | "Give an example of X" — which example?         | Pin down the specific example: "What is X's example of Y?" |

## Progressive difficulty

Cards exist on a spectrum from recognition (easier) to free recall (harder):

1. **Recognition** — Multiple choice, true/false (avoid in Anki — too easy)
2. **Cued recall** — Cloze deletion with rich surrounding context (moderate)
3. **Free recall** — Open-ended question with minimal cues (hardest, most effective)

The target is "recalled with effort" — slightly challenging but achievable. If trivially easy every time, the card wastes review time. If impossibly hard, it builds frustration.

Easy cards lean toward cued recall. Hard cards lean toward free recall. Medium cards mix both.

## Philosophical mandates

## Operational Rule Pack (Applies to Card Generation)

These rules replace all abstract/philosophical mandates during generation. Cards must comply with TSV: `Front<TAB>Back<TAB>URL`, and **Front/Back must contain only the question and answer** (no metadata, prefixes, or labels).

### 1) Card Quality Checklist (Must Pass)

- Specific target (no generic "Explain X").
- Single correct answer (univocal).
- Concrete scenario or boundary (no abstract-only prompts).
- Minimal runnable context for code prompts.
- No full lists unless ordered.
- No duplicate testing of the same AIU.
- No blank-swap prompts unless tied to a scenario or boundary.
- No metadata-only answers (`source:`, `title:`, bare wikilinks).
- Procedure/constructive prompts include concrete state + explicit action task.
- Coding prompts must include code witness and output shape.
- Refactor prompts include before/after anchors.
- Task verbs are strong production verbs; avoid weak recognition verbs.
- Back should be canonical/univocal (avoid `or`, `e.g.`, `like`, `implementation-specific`) unless the card explicitly asks for alternatives.
- Front must be self-contained (no undeclared local symbols).
- If front claims context, include explicit snippet/state content.

### 2) Anti-Bloat Filters

- If two cards differ only by wording, keep one.
- Do not auto-add "why" cards unless AIU is hard.
- Do not apply 5‑lens expansion unless concept is advanced + high‑leverage.

### 3) Thin-Prompt Fixer

- If a prompt is just a label swap, replace with a scenario/boundary prompt.
- If a prompt is abstract, add a concrete example.
- If a prompt is too easy, drop or merge into the strongest AIU card.
- If a coding prompt lacks runnable artifacts, inject snippet/trace and output shape.
- If task asks two actions, split into separate cards.
- If prompt is source-bound ("book/note said"), rewrite to concept-use framing.
- Never use heuristic code-generation scripts to author cards; generation must be doctrine-driven from note understanding.


## 1. The Mandates (The Core Philosophy)

### PR-0002

**Rule**: Contextual Scaffolding

- **Type**: Rule
- **Directive**: Cards should be derived from a structured understanding, not loosely related facts.

### PR-0003

**Rule**: Passive consumption (reading/delegation/lectures) fails; learning requires active engagement and rephrasing (Generation Effect). Always read with a pen in hand.

- **Type**: Failure mode
- **Directive**: Disallow copy-paste or auto-generated cards without processing; require user authorship; personalize cues; use paraphrased prompts.

### PR-0004

**Rule**: Expertise relies on hidden internal models that must be made explicit for effective learning.

- **Type**: Model
- **Directive**: Create cards that ask for the visualization/model, anchored by a minimal example.

### PR-0005

**Rule**: Cloze Deletion Efficiency

- **Type**: Model
- **Directive**: Use cloze deletion as a primary card type for rapid content creation.

### PR-0007

**Rule**: Mnemonic Scaffolding

- **Type**: Rule
- **Directive**: Incorporate mnemonics into the answer or extra field of cards to aid initial recall.

### PR-0009

**Rule**: Set Avoidance

- **Type**: Failure Mode
- **Directive**: Avoid cards that ask for a list of items unless they are ordered (enumerations).

### PR-0010

**Rule**: Enumeration Decomposition

- **Type**: Rule
- **Directive**: Use overlapping cloze deletions for sequences (e.g., A [B C D] E, B [C D E] F).

### PR-0011

**Rule**: Feedback loops are foundational for growth and learning.

- **Type**: Rule
- **Directive**: Use immediate review results as the core learning feedback loop.

### PR-0012

**Rule**: Word Choice Optimization

- **Type**: Rule
- **Directive**: Use fewer words to speed up learning. Avoid trailing messages or side information in the main question/answer.

### PR-0013

**Rule**: Semantic Anchoring

- **Type**: Rule
- **Directive**: Use specific, familiar words in the question to ground the answer in a known semantic web.

### PR-0014

**Rule**: Personalization Principle

- **Type**: Rule
- **Directive**: Add parenthetical personal references or specific examples to questions (e.g., 'like the one at [Person]'s house').

### PR-0016

**Rule**: A note system must be treated as a dynamic, interconnected structure rather than a static collection or storage space for isolated notes.

- **Type**: Constraint
- **Directive**: Design cards that refer to other cards or broader concepts to avoid isolation.

### PR-0018

**Rule**: Effective learning requires anchoring new information to a rich, interconnected latticework of prior knowledge ("docking points") to facilitate understanding and retrieval.

- **Type**: Model
- **Directive**: Include minimal context in the question that names the prior knowledge that "docks" the new fact.

### PR-0019

**Rule**: Temporal Stamping

- **Type**: Constraint
- **Directive**: Include a year or version in the question for volatile knowledge (e.g., 'GNP in 2024').

### PR-0020

**Rule**: Dynamic Prioritization

- **Type**: Rule
- **Directive**: Use SuperMemo/Anki priority tools (forgetting index, pending queue) to manage the flow of material.

### PR-0021

**Rule**: Writing is a composite process of distinct sub-tasks (reading, reflecting, drafting, proofreading) that require fundamentally different attention modes; these must be separated consciously to prevent cognitive interference.

- **Type**: Rule
- **Directive**: Create cards that distinguish between different writing sub-tasks and their specific cognitive requirements.

### PR-0024

**Rule**: Practice prompts should be synthesized from learner's own activity (highlights, questions) and grounded in their authentic project context.

- **Type**: Rule
- **Directive**: The principle of synthesizing practice from personal activity traces (not generic questions).

### PR-0026

**Rule**: Expertise is the result of sedimented experience and feedback loops, allowing for intuitive action ("gut feeling") that transcends explicit rule-following.

- **Type**: Definition
- **Directive**: Immediate feedback in reviews builds the "gut feeling" of knowing.

### PR-0027

**Rule**: Learners should be able to provide feedback on practice questions to steer future question synthesis toward their needs.

- **Type**: Rule
- **Directive**: The importance of learner feedback in adaptive question generation (steering the system).

### PR-0028

**Rule**: Active, slow processing (pen in hand) is the engine of production.

- **Type**: Rule
- **Directive**: Beware of 'one-click' card creation; the effort of manual card drafting is a learning feature. Who "does the learning" in an educational context?

### PR-0029

**Rule**: Working memory is severely limited (7+/-2 items) and volatile; information must be offloaded to external storage to free up cognitive resources.

- **Type**: Constraint
- **Directive**: None specific.

### PR-0031

**Rule**: Incomplete tasks (open loops) occupy short-term memory (Zeigarnik effect); writing them down ("closing" the task) clears cognitive load.

- **Type**: Mechanism
- **Directive**: None specific.

### PR-0032

**Rule**: Deliberately keeping questions unanswered ("open loops") allows the brain to process them in the background (diffuse mode) for creative problem solving.

- **Type**: Strategy
- **Directive**: None specific.

### PR-0038

**Rule**: Confirmation bias is the primary enemy of research; the system must actively prioritize capturing contradictory/disconfirming evidence ("Darwin's Golden Rule") because it generates the most valuable connections and prevents echo chambers.

- **Type**: Principle
- **Directive**: Create cards that ask "What contradicts this?" or "What is the opposing view?"

### PR-0039

**Rule**: Linear processes that start with a fixed hypothesis encourage confirmation bias; the workflow must separate accurate understanding from hypothesizing and prioritize insight over adherence to the original plan.

- **Type**: Principle
- **Directive**: Why avoid linear processes? (To reduce confirmation bias).

### PR-0042

**Rule**: Decontextualized information prevents true understanding.

- **Type**: Failure mode
- **Directive**: Avoid "orphan" cards that test facts without reference to their theoretical or narrative context.

### PR-0045

**Rule**: True understanding of a claim requires explicitly defining its boundaries and what it excludes (Negation/Inversion).

- **Type**: Mental Model
- **Directive**: Create 'X is NOT Y' cards.

### PR-0046

**Rule**: Understanding is validated only by the ability to explain ideas simply in plain language (The Feynman Test).

- **Type**: Validation
- **Directive**: Simple Q&A only.

### PR-0047

**Rule**: Familiarity (often from rereading) creates a dangerous illusion of competence (Mere-Exposure Effect); only active testing or writing prevents self-deception.

- **Type**: Failure Mode
- **Directive**: Testing beats review.

### PR-0048

**Rule**: Using SRS allows an individual to decide what they will remember long-term rather than leaving it to chance.

- **Type**: Model
- **Directive**: Create cards that reinforce the agency of the user in determining their memory contents.

### PR-0051

**Rule**: A prompt is essentially an instruction for a future mental action.

- **Type**: Model
- **Directive**: Ensure prompts are actionable and clear tasks for the future self.

### PR-0054

**Rule**: Meta-cognitive awareness is required to change thinking patterns.

- **Type**: Rule
- **Directive**: Include cards about cognitive biases and thinking patterns to build meta-awareness.

### PR-0056

**Rule**: Opportunistic flexibility beats rigid planning in intellectual work.

- **Type**: Rule
- **Directive**: Be willing to delete or modify cards as your understanding evolves.

### PR-0057

**Rule**: Ambiguity in the question leads to low-quality recall.

- **Type**: Rule
- **Directive**: Ensure every prompt has a clear, unambiguous target answer.

### PR-0058

**Rule**: Knowledge is not monolithic; different types (facts, procedures, concepts) require different SRS strategies.

- **Type**: Model (Taxonomy)
- **Directive**: Use specific card templates/strategies based on the knowledge type.

### PR-0060

**Rule**: Trying to be 100% exhaustive is counterproductive and leads to burnout; prioritize high-value information.

- **Type**: Failure mode / Rule
- **Directive**: Do not create cards for every trivial detail; select for value.

### PR-0065

**Rule**: Grouping items by their role or function makes a list easier to remember.

- **Type**: Model (Strategy)
- **Directive**: Prompt for the "category" or "functional group" before prompting for members.

### PR-0068

**Rule**: Sequence learning from atomic components to integrative holistic understanding.

- **Type**: Rule (Sequencing)
- **Directive**: Sequence card creation from atomic to integrative.

### PR-0069

**Rule**: Cues should narrow the search space without removing the 'desirable difficulty' of retrieval.

- **Type**: Rule (Constraint)
- **Directive**: Use cues sparingly and only to resolve ambiguity; avoid trivializing the prompt.

### PR-0078

**Rule**: Identify "open lists" (evolving sets of examples) and treat them differently than "closed lists" (fixed factual sets); avoid closed-list techniques like clozes for open lists.

- **Type**: Model
- **Directive**: Avoid closed-list techniques (like clozes) for open lists.

### PR-0079

**Rule**: Apply a three-tier strategy for open lists: link instances to the category, analyze the category's patterns, and fuzzily link the category back to instances by asking for examples.

- **Type**: Rule
- **Directive**: Use the three-tier approach (Instance->Tag, Tag Pattern, Tag->Instance) for open lists.

### PR-0082

**Rule**: Prompt writing and note-taking must be an iterative process that deepens and refines as the user's subject-matter mastery matures over time.

- **Type**: Rule
- **Directive**: Regularly refine and update prompts as conceptual understanding improves.

### PR-0083

**Rule**: Rote memorization of terminology or definitions is a shallow substitute for conceptual understanding.

- **Type**: Failure mode
- **Directive**: Avoid simple 'Term/Definition' pairs for complex concepts; use multi-perspective prompts instead.

### PR-0084

**Rule**: Bridge the theory-practice gap by anchoring salience prompts in specific, real-world contexts.

- **Type**: Rule
- **Directive**: Personalize prompts by framing them in the context of the user's specific life situations.


# how-to-ask-about-a-code-block

