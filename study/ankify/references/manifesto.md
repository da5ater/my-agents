# The Ankify Manifesto

**Objective**: Generate cards by systematically applying ALL rules from the knowledge base. This document contains the consolidated, authoritative rules for the Ankify system.

## 0. Configuration & Constraints

> [!IMPORTANT]
> The following settings are the definitive source of truth for the Agent's behavior.

### Configuration & Variables
| Variable | Value | Description |
| :--- | :--- | :--- |
| `MAX_CARDS_PER_NOTE_BASE` | 5 | Base limit for cards per note. |
| `MAX_CARDS_PER_NOTE_CAP` | 10 | Absolute maximum cards per note (hard cap). |
| `MIN_CARDS_PER_NOTE` | 3 | Minimum cards where complex rules apply. |
| `CODE_BLOCK_SCALER` | 1 | Additional cards allowed per atomic code logical unit. |
| `VAULT_NAME` | mohamed | The name of the Obsidian vault for URL generation. |

### URL Format
**Rule**: All cards MUST include a valid Obsidian URL in the 3rd column.
**Format**: `obsidian://open?vault=<VAULT_NAME>&file=<relative_path_encoded>`
**Example**: `obsidian://open?vault=mohamed&file=programming%2Fjavascript%2Farrays.md`

### Triggers (Input -> Card Type)
**Rule**: If the note contains these elements, you MUST generate the corresponding card type.

| Content Element | Target Card Type | Prompt Strategy |
| :--- | :--- | :--- |
| **Code Block** (Atomic Logic) | **CONSTRUCTIVE** | "Given [Context], write the code to [Task]" |
| **Big Code Block** (>5 lines) | **CONSTRUCTIVE** (x3-5) | Decompose into multiple atomic logic cards |
| **"Bolded" Rule/Pattern** | **THEORY** | "What is the rule for..." / "Explain why..." |
| **Distinction** (X vs Y) | **NEGATION** | "How does A differ from B?" / "X is NOT Y because..." |
| **Counter-Evidence** | **COUNTER-EVIDENCE** | "When does X NOT apply?" / "What contradicts this?" |
| **Definition** | **DEFINITION** | "What is [term]?" |
| **Configuration/Steps** | **PROCEDURE** | "How do you set up X?" |
| **Mental Model** | **MODEL** | "Draw the diagram..." / "Visualize..." |
| **Common Mistake** | **FAILURE_MODE** | "What goes wrong if you do X?" |

### Quota Priorities (The Cull)
**Rule**: If `total_cards > MAX_CARDS_PER_NOTE_CAP`, keep cards in this priority order (1 = Keep, 6 = Drop first).

1.  **MODEL** (Highest Value)
2.  **CONSTRUCTIVE**
3.  **FAILURE_MODE**
4.  **COUNTER_EVIDENCE**
5.  **SYNTHESIS**
6.  **NEGATION** (Lowest Value - drop first)

### Validation Rules (The Gatekeeper)
**Rule**: Any card violating these rules is **INVALID** and must be regenerated.

1.  **NO Generic "Explain X"**: Prompt must be specific ("How does X handle Y?").
2.  **NO Yes/No Questions**: Prompt must demand production, not recognition.
3.  **NO Orphan Pronouns**: Front must not start with "It", "This", "They" (unless defined in the same card).
4.  **NO Filler Phrases**: Back must not contain "leads to incorrect behavior", "end-to-end", "misused".
5.  **NO Multi-part Questions**: One Question = One Card.
6.  **Context Required**: Constructive cards must provide "Given:" state.
7.  **NO Duplicates**: If two cards test the same target fact, keep only the strongest version.
8.  **AIU Cap**: One Atomic Information Unit (AIU) → one card by default; two cards max only if the AIU is hard.
9.  **Fragility Filter**: Avoid blank-swap or label-only cards unless tied to a concrete scenario or boundary.

---

## Operational Rule Pack (Applies to Card Generation)

These rules replace all abstract/philosophical mandates during generation. Cards must comply with TSV: `Front<TAB>Back<TAB>URL`, and **Front/Back must contain only the question and answer** (no metadata, prefixes, or labels).

### 1) Decision Framework (AIU + Hardness)
- List AIUs (Atomic Information Units) in the note.
- For each AIU, label **Easy** or **Hard**.
- **Easy AIU → 1 card**. **Hard AIU → 2 cards max**.
- If a note has **1–2 AIUs**, cap total cards at **1–2** (skip trigger expansion).
- Code blocks are not AIUs; extract the AIU(s) and keep only the highest‑signal one(s).

### 2) Card Quality Checklist (Must Pass)
- Specific target (no generic "Explain X").
- Single correct answer (univocal).
- Concrete scenario or boundary (no abstract-only prompts).
- Minimal runnable context for code prompts.
- No full lists unless ordered.
- No duplicate testing of the same AIU.
- No blank-swap prompts unless tied to a scenario or boundary.

### 3) Type Selector (Choose ONE per AIU)
- **Mechanism** → Why/How with example.
- **Distinction** → Contrast/Negation.
- **Procedure** → Constructive steps.
- **Mistake** → Failure mode.
- **Definition** → Only if paired with boundary or example (hard AIU only).

### 4) Anti-Bloat Filters
- If two cards differ only by wording, keep one.
- Do not auto-add "why" cards unless AIU is hard.
- Do not apply 5‑lens expansion unless concept is advanced + high‑leverage.

### 5) Thin-Prompt Fixer
- If a prompt is just a label swap, replace with a scenario/boundary prompt.
- If a prompt is abstract, add a concrete example.
- If a prompt is too easy, drop or merge into the strongest AIU card.

## Atomic Information Unit (AIU) Budgeting

**Rule**: An AIU is a single discrete idea (fact, mechanism, distinction, or procedure).
**Rule**: Each AIU gets one card by default.
**Rule**: A second card is allowed only if the AIU is hard (multi-step, error-prone, counter-intuitive, or frequently confused).
**Rule**: If a note contains 1–2 AIUs, cap the note at 1–2 total cards; skip trigger expansion.
**Rule**: Code blocks are not AIUs. Extract AIUs from code and keep only the highest-signal ones.
**Rule**: When two cards differ only by wording, keep one and delete the rest.

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
