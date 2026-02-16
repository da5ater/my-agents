# Depth Templates (Manifesto Aligned)

Use these patterns to generate deep cards. Do **NOT** use generic "Explain X" prompts.

## 1. The Model (Structure & Flow)
**Intent**: Visualize systems, not just lists.

*   **Pattern**: `Draw the [Diagram Name] for [Scenario].`
*   **Pattern**: `Trace the data flow of [Variable] through [Function].`
*   **Pattern**: `What are the [N, e.g. 3] stages of [Process]?`

## 2. The Failure Mode (Boundaries)
**Intent**: Define what breaks.

*   **Pattern**: `What specific error occurs if you [Action] with [Invalid Input]?`
*   **Pattern**: `Why does [Code/Pattern] fail when [Condition]?`
*   **Pattern**: `Given [Constraint], why is [Approach A] worse than [Approach B]?`

## 3. The Constructive (Whiteboard)
**Intent**: Write code, don't just read it. Context is mandatory (MC-CTX-001).

*   **Pattern**:
    *   **Front**: `Given [Context/State], write the code to [Task].`
    *   **Back**: `<pre><code>...</code></pre>`

## 4. The Distinction (Negation)
**Intent**: Define by exclusion.

*   **Pattern**: `How does [Concept A] differ from [Concept B] regarding [Dimension]?`
*   **Pattern**: `[Concept X] is NOT [Concept Y] because...?`

## 5. The Prediction
**Intent**: Test mental compiler.

*   **Pattern**: `What is the console output of the following snippet? [Code]`
*   **Pattern**: `What is the value of [Variable] after [Event]?`

## 6. The Why (Rationale)
**Intent**: Embed facts in logic (PR-0063).

*   **Pattern**: `Why is [Fact] true? (Explain the mechanism)`
*   **Pattern**: `What is the architectural reason for [Design Choice]?`

## 7. The Open List (3-Tier Strategy)
**Intent**: Handle evolving sets without rote memorization (PR-0079).

*   **Tier 1 (Anchor)**: `What category does [Instance] belong to?`
*   **Tier 2 (Pattern)**: `What are the common characteristics of [Category]?`
*   **Tier 3 (Generative)**: `Give 3 examples of [Category] (Brainstorming).`

## 8. The Connection (Synthesis)
**Intent**: Force ideas to mingle (PR-0017).

*   **Pattern**: `How does [Concept A] influence [Concept B]?`
*   **Pattern**: `What do [Concept A] and [Concept B] have in common regarding [Dimension]?`

## 9. The Sequence (Ordering)
**Intent**: Capture order without brute force (PR-0068, PR-0010).

*   **Pattern**: `In the sequence [A, B, C, D, E], what comes immediately after [B]?`
*   **Pattern**: `Arrange the following steps of [Process] in order: [Scrambled List].`

## 10. The Darwin (Disconfirmation)
**Intent**: Fight confirmation bias (PR-0038).

*   **Pattern**: `What is the strongest argument AGAINST [Concept]?`
*   **Pattern**: `Under what specific conditions does [Rule/Best Practice] become harmful?`

## 11. The Salience (Immediacy)
**Intent**: Keep ideas alive until used (PR-0081).

*   **Pattern**: `Why is [Concept] relevant to my current project [Project Name]?`
*   **Pattern**: `What is the "One Big Idea" from [Source] that I must not forget?`

## 12. The Mechanism (Deep Dive)
**Intent**: Embed facts in logic (PR-0063).

*   **Pattern**: `How does [Component] achieve [Result]? (Step-by-step mechanism)`
