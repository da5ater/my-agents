# The Ankify Manifesto

**Objective**: Generate cards by systematically applying ALL rules from the knowledge base. This document contains the consolidated, authoritative rules for the Ankify system.

## 1. The Core Pillars

1. **Context First**: No orphans. Every card must be anchored to a concept, code snippet, or scenario.
2. **Atomicity**: One card, one idea. No multi-part questions.
3. **Active Recall**: No yes/no. No recognition. Demand generation.
4. **Signal-to-Noise**: Zero filler.

## 2. Actualization Table (Machine-Checkable)

| RULE_ID | Trigger | Rule | Why | Enforcement | Repair |
|---|---|---|---|---|---|
| MC-CTX-001 | card_type == CONSTRUCTIVE | **Explicit Context Required** | Code without context is guessing. | Front must contain "Given:" or variable definitions. | Inject missing variable/state context from note. |
| MC-CTX-002 | any card | **No Orphan Pronouns** | "It" depends on context users won't have. | Front must not start with "It", "This", "They" without an antecedent. | Replace pronoun with specific noun/concept. |
| MC-ATOM-001 | any card | **Single Atomic Task** | Multi-part cards cause partial fail loops. | Front must not contain multiple distinct questions (bulleted lists of Qs). | Split into multiple cards. |
| MC-ACTIVE-001 | any card | **No Yes/No Questions** | Recognition is not recall. | Front must not start with "Is/Are/Does/Can/Should" expecting a boolean. | Rewrite as "When..." "How..." "What...". |
| MC-ACTIVE-002 | any card | **No Fill-in-the-Blank** | Cloze is for idioms, not concepts. | Front must be a complete question, not a sentence with a missing word (unless explicit Cloze type). | Convert to Q&A. |
| MC-SIGNAL-001 | any card | **No Generic "Explain"** | "Explain X" usually leads to vague, long answers. | Front must not be "Explain [Topic]". Use "Draw the model", "Trace the execution", "Contrast X and Y". | Narrow scope to specific mechanism/scenario. |
| MC-SIGNAL-002 | card_type == FAILURE_MODE | **Concrete Failure** | "What goes wrong?" is too broad. | Front must specify the scenario: "What mistake causes error X?" or "What happens if I do Y?". | Add scenario constraint. |
| MC-SIGNAL-003 | any card | **Banned Phrases** | Filler wastes time. | Back must not contain: "leads to incorrect behavior", "end-to-end", "misused". | Replace with specific error/outcome. |
| MC-ANCHOR-001 | type in [MODEL, COMPARISON] | **Anchored Prompts** | Drift leads to hallucination. | Question must contain at least one unique token (function name, specific term) from the note. | Inject code token or specific term. |
| MC-CODE-001 | card_type == CONSTRUCTIVE | **Whiteboard Rule** | Reading code is distinct from writing it. | Front asks to "Write", "Implement", "Refactor". Back contains code block. | Change verb to "Write/Implement". |
| MC-BOUND-001 | any card | **Boundary Definition** | Understanding requires limits. | Set must include at least one card asking "When does this FAIL?" or "What is NOT covered?". | Generate a Failure Mode or Negation card. |

## 3. The Mandates (Consolidated Rules)

### PR-EFFICIENCY-01
**Rule**: Spaced repetition provides 20x+ efficiency gains compared to conventional flashcards, reducing total review time from hours to minutes over multi-year periods.
- **Type**: Model
- **Directive**: Recognize the long-term time savings (4-7 minutes vs 2+ hours over 20 years) to justify the upfront effort of card creation.

### PR-0001
**Rule**: Memory is an intentional choice and behavior, not a passive event.
- **Type**: Model
- **Directive**: Treat card creation as a deliberate choice; prioritize intentional memory targets.

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

### PR-0006
**Rule**: Visual Anchoring
- **Type**: Rule
- **Directive**: Use images and diagrams to provide visual anchors for facts.

### PR-0007
**Rule**: Mnemonic Scaffolding
- **Type**: Rule
- **Directive**: Incorporate mnemonics into the answer or extra field of cards to aid initial recall.

### PR-0008
**Rule**: Graphic/Image Occlusion
- **Type**: Model
- **Directive**: Use Image Occlusion for visual-spatial knowledge.

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

### PR-0015
**Rule**: The slip-box (note system) grows in knowledge and utility (exponentially) in lockstep with the user's own competency, providing increasing connections and smart suggestions as it scales.
- **Type**: Model
- **Directive**: Scale the card collection as a reflection of deepening expertise.

### PR-0016
**Rule**: A note system must be treated as a dynamic, interconnected structure rather than a static collection or storage space for isolated notes.
- **Type**: Constraint
- **Directive**: Design cards that refer to other cards or broader concepts to avoid isolation.

### PR-0017
**Rule**: The primary utility of a note-taking system is to provide a space for ideas to mingle and generate new insights, rather than merely retrieving specific facts.
- **Type**: Principle
- **Directive**: Create "comparison" or "synthesis" cards that force different ideas to interact.

### PR-0018
**Rule**: Effective learning requires anchoring new information to a rich, interconnected latticework of prior knowledge ("docking points") to facilitate understanding and retrieval.
- **Type**: Model
- **Directive**: Use "context" fields to explicitly name the prior knowledge that "docks" the new fact.

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

### PR-0022
**Rule**: Static questions maintain memory but don't promote progressive deepening of understanding over time.
- **Type**: Failure mode
- **Directive**: The limitation of static flashcards (maintenance without progressive deepening).

### PR-0023
**Rule**: Memory systems often fail to connect to authentic practice, making practice feel decontextualized and generic rather than project-grounded.
- **Type**: Failure mode
- **Directive**: The authentic practice disconnect in traditional spaced repetition (generic vs. context-grounded).

### PR-0024
**Rule**: Practice prompts should be synthesized from learner's own activity (highlights, questions) and grounded in their authentic project context.
- **Type**: Rule
- **Directive**: The principle of synthesizing practice from personal activity traces (not generic questions).

### PR-0025
**Rule**: Complex ideas cannot be fully structured or critiqued within working memory; externalization (writing) is a prerequisite for improvement and analysis.
- **Type**: Principle
- **Directive**: Teach that externalization allows for manipulation and critique impossible in working memory.

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

### PR-0030
**Rule**: Understanding is functionally equivalent to the density of connections between ideas; the slip-box acts as a machine for building these connections and thus understanding. Contribution types include additions, contradictions, and questions.
- **Type**: Definition
- **Directive**: Context cues retrieval; connections aid recall.

### PR-0031
**Rule**: Incomplete tasks (open loops) occupy short-term memory (Zeigarnik effect); writing them down ("closing" the task) clears cognitive load.
- **Type**: Mechanism
- **Directive**: None specific.

### PR-0032
**Rule**: Deliberately keeping questions unanswered ("open loops") allows the brain to process them in the background (diffuse mode) for creative problem solving.
- **Type**: Strategy
- **Directive**: None specific.

### PR-0033
**Rule**: The synthesis should strengthen both authentic practice (by making it more tractable) and explicit learning (by connecting it to community).
- **Type**: Principle
- **Directive**: The third design principle (strengthen both immersion and guided learning domains).

### PR-0034
**Rule**: Explicit learning must include dynamic, varied reinforcement that ensures transfer and progressively deepens understanding over time.
- **Type**: Principle
- **Directive**: The fourth design principle (learning that works

### PR-0035
**Rule**: Writing should be the assembly of existing notes into a draft, rather than a linear process of facing a blank page; the goal is the note series, not the draft itself.
- **Type**: Process
- **Directive**: None specific.

### PR-0036
**Rule**: The slip-box acts as a semi-autonomous dialogue partner that generates surprise and feedback, rather than just a passive storage device.
- **Type**: Metaphor
- **Directive**: None specific.

### PR-0037
**Rule**: Notes must strip ideas of their original source context (de-contextualization) and translate them into the user's own language to allow them to be re-embedded into new contexts; copying quotes without this process destroys meaning.
- **Type**: Mechanism
- **Directive**: None specific.

### PR-0038
**Rule**: Confirmation bias is the primary enemy of research; the system must actively prioritize capturing contradictory/disconfirming evidence ("Darwin's Golden Rule") because it generates the most valuable connections and prevents echo chambers.
- **Type**: Principle
- **Directive**: Create cards that ask "What contradicts this?" or "What is the opposing view?"

### PR-0039
**Rule**: Linear processes that start with a fixed hypothesis encourage confirmation bias; the workflow must separate accurate understanding from hypothesizing and prioritize insight over adherence to the original plan.
- **Type**: Principle
- **Directive**: Why avoid linear processes? (To reduce confirmation bias).

### PR-0040
**Rule**: Literature notes are a transient tool for understanding and preparing ideas for the slip-box; they should not be polished as final products but used to capture the essence and 'practice' understanding.
- **Type**: Principle
- **Directive**: None specific.

### PR-0041
**Rule**: The note system is content-agnostic but relevance-dependent; it accepts any topic provided it connects to existing notes.
- **Type**: System Property
- **Directive**: None.

### PR-0042
**Rule**: Decontextualized information prevents true understanding.
- **Type**: Failure mode
- **Directive**: Avoid "orphan" cards that test facts without reference to their theoretical or narrative context.

### PR-0043
**Rule**: Mental models, error patterns, and categories act as navigation aids for understanding texts.
- **Type**: Cognitive Tooling
- **Directive**: None.

### PR-0044
**Rule**: Intellectual maturity requires the courage to use one's own understanding rather than relying on guidance (Sapere aude).
- **Type**: Core Value
- **Directive**: None.

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

### PR-0049
**Rule**: Prompt engineering is a skill that can be analyzed and taught through principles, not just an art.
- **Type**: Rule
- **Directive**: Test the specific criteria for "effective" prompts.

### PR-0050
**Rule**: The goal of SRS is both retention of external info and development of personal insight.
- **Type**: Goal
- **Directive**: Include prompts that ask for personal applications or connections between ideas.

### PR-0051
**Rule**: A prompt is essentially an instruction for a future mental action.
- **Type**: Model
- **Directive**: Ensure prompts are actionable and clear tasks for the future self.

### PR-0052
**Rule**: The effort of pulling information from the brain is what strengthens the memory trace.
- **Type**: Model (Mechanism)
- **Directive**: Prioritize active recall over recognition or passive reading.

### PR-0053
**Rule**: Memory and understanding are deeply linked; being able to recall details makes it easier to think with them.
- **Type**: Model
- **Directive**: Use recall tasks to build the foundation for complex problem-solving.

### PR-0054
**Rule**: Meta-cognitive awareness is required to change thinking patterns.
- **Type**: Rule
- **Directive**: Include cards about cognitive biases and thinking patterns to build meta-awareness.

### PR-0055
**Rule**: The "test" is the learning event itself, not just a measurement of previous learning.
- **Type**: Model
- **Directive**: Emphasize the learning aspect of the review session.

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

### PR-0059
**Rule**: True understanding comes from linking external information to personal experience and existing knowledge.
- **Type**: Model
- **Directive**: Write personalized prompts that ask for connections to the user's own life/projects.

### PR-0060
**Rule**: Trying to be 100% exhaustive is counterproductive and leads to burnout; prioritize high-value information.
- **Type**: Failure mode / Rule
- **Directive**: Do not create cards for every trivial detail; select for value.

### PR-0062
**Rule**: Effective prompts are atomic (one detail), precise, consistent, and tractable (easy to attempt).
- **Type**: Rule (Criteria)
- **Directive**: Audit cards against these four criteria.

### PR-0063
**Rule**: Asking "why" helps embed facts, list items, and procedural steps into a larger conceptual network, making them easier to retain and apply.
- **Type**: Rule / Strategy
- **Directive**: Supplement factual cards with "Why" (explanation) cards; create rationale-based prompts for list members.

### PR-0064
**Rule**: A prompt must lead to exactly one correct answer to be effective for retrieval practice.
- **Type**: Rule (Constraint)
- **Directive**: Refine prompts until the intended answer is the only logical response.

### PR-0065
**Rule**: Grouping items by their role or function makes a list easier to remember.
- **Type**: Model (Strategy)
- **Directive**: Prompt for the "category" or "functional group" before prompting for members.

### PR-0066
**Rule**: Raw lists are hard for memory because they lack internal structure or sequence.
- **Type**: Failure mode / Constraint
- **Directive**: Avoid asking for an entire list at once.

### PR-0067
**Rule**: Using cloze deletions in a fixed-order list leverages visual memory (shape) to support recall.
- **Type**: Model (Strategy)
- **Directive**: Use fixed-order lists with cloze deletions for list items.

### PR-0068
**Rule**: Sequence learning from atomic components to integrative holistic understanding.
- **Type**: Rule (Sequencing)
- **Directive**: Sequence card creation from atomic to integrative.

### PR-0069
**Rule**: Cues should narrow the search space without removing the 'desirable difficulty' of retrieval.
- **Type**: Rule (Constraint)
- **Directive**: Use cues sparingly and only to resolve ambiguity; avoid trivializing the prompt.

### PR-0070
**Rule**: Standardize placement of mnemonics in the answer field (e.g., in parentheses) to preserve retrieval effort.
- **Type**: Rule
- **Directive**: Place mnemonics in the "Extra" or "Answer" field, parenthesized.

### PR-0071
**Rule**: Use high-valence, vivid, or personal associations (visuals, humor, disgust) for maximum mnemonic efficiency.
- **Type**: Rule
- **Directive**: Suggest vivid/emotional imagery for difficult prompts to aid recall.

### PR-0072
**Rule**: Create auxiliary cards for difficult mnemonics to reinforce the 'memory hook' itself.
- **Type**: Failure mode fix
- **Directive**: Add auxiliary cards to practice difficult mnemonics for "leech" cards.

### PR-0076
**Rule**: Use metadata and external links to maintain context and provenance without cluttering the prompt text itself.
- **Type**: Rule/Constraint
- **Directive**: Use the 'Source' field or a metadata footer for context instead of the question field.

### PR-0077
**Rule**: Triangulate a concept by applying five specific lenses: Attributes/tendencies, Similarities/differences, Parts/wholes, Causes/effects, Significance/implications.
- **Type**: Model/Rule
- **Directive**: Generate a suite of cards for each concept, covering all five lenses.

### PR-0078
**Rule**: Identify "open lists" (evolving sets of examples) and treat them differently than "closed lists" (fixed factual sets); avoid closed-list techniques like clozes for open lists.
- **Type**: Model
- **Directive**: Avoid closed-list techniques (like clozes) for open lists.

### PR-0079
**Rule**: Apply a three-tier strategy for open lists: link instances to the category, analyze the category's patterns, and fuzzily link the category back to instances by asking for examples.
- **Type**: Rule
- **Directive**: Use the three-tier approach (Instance->Tag, Tag Pattern, Tag->Instance) for open lists.

### PR-0081
**Rule**: Spaced repetition can be used to artificially extend the Baader-Meinhof phenomenon, keeping ideas salient ("top of mind") until they connect to life experiences.
- **Type**: Model
- **Directive**: Use salience prompts to keep important but not-yet-applied ideas top-of-mind.

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

## 4. Operational Doctrine (Procedures & Quotas)

### Structural Mapping
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

### Content Element -> Card Type
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

### Canonical Card Types
Use these internal names consistently:
THEORY, CONSTRUCTIVE, SYNTHESIS, MODEL, FAILURE_MODE, NEGATION, COUNTER_EVIDENCE, DEFINITION, PROCEDURE

### Quantitative Minimums
When the triggering elements exist in the note, enforce minimum counts:
- concept_count >= 2 -> synthesis_cards >= 1
- concept_count >= 4 -> synthesis_cards >= 2
- h2_count >= 2 -> cross_h2_synthesis_cards >= 1
- mental_models present -> model_cards >= 1
- failure_modes present -> failure_mode_cards >= 1
- contradictions present -> counter_evidence_cards >= 1
- distinctions present -> negation_cards >= 1

### Hard Cap (Absolute)
- Basic notes: `max_total_cards_max = 6` when anchors < 8 AND h2_count < 3 AND code_blocks <= 1.
- High complexity: `max_total_cards_max = 8` when any threshold is exceeded.

### Conversion Quota (Depth Without Growth)
For every 5 PROCEDURE cards in a note, convert 1 into a deeper doctrine type by replacement.
Priority order:
1. MODEL
2. FAILURE_MODE
3. COUNTER_EVIDENCE
4. SYNTHESIS
5. NEGATION


### Manifesto Compliance Checklist
Use this checklist before TSV serialization:
- Mapping: H2/H3 structural mapping applied to all sections.
- Elements: content elements mapped to required card types.
- Coverage: every structural element yields >=1 card.
- Tier 1: MODEL, FAILURE MODE, NEGATION, COUNTER-EVIDENCE, SYNTHESIS present when triggered.
- Minimums: quantitative minimums satisfied when triggered.
- Connectivity: connectivity minimums satisfied when triggered.
- Internalization linkage: boundary, misconception, link reflected in cards.
- Budget: card counts aligned with card_budget_plan.
- Conversion quota: procedure-to-deep conversion quota satisfied.
- Quality: atomic, active recall, contextualized, unambiguous.
- Output: no rule metadata leaked into card text.
