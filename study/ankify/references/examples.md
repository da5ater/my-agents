# Examples & Templates (Manifesto Aligned)

## 0. The Bad (Validation Failures)
*Avoid these patterns at all costs. They violate the input filter.*

### Generic "Explain" (Violates MC-SIGNAL-001)
*   **Front**: Explain Closures.
*   **Why**: Too broad. No success criteria.
*   **Fix**: "What happens to the scope chain when a function returns another function?"

### Orphan Pronoun (Violates MC-CTX-002)
*   **Front**: usage: How does it handle nulls?
*   **Why**: "It" is ambiguous.
*   **Fix**: "How does `JSON.parse` handle null inputs?"

### Yes/No (Violates MC-ACTIVE-001)
*   **Front**: Is `map` faster than `forEach`?
*   **Why**: Recognition is not recall. 50% guess chance.
*   **Fix**: "Compare the performance characteristics of `map` vs `forEach`."

### The "List" (Violates PR-0009)
*   **Front**: What are the 5 principles of SOLID?
*   **Why**: Rote memorization of sets is fragile.
*   **Fix**: "What is the 'L' in SOLID and how is it violated?" (Atomic)

---

## 1. The Triggers (Canonical Types)
*These strictly map to the "Triggers" table in `manifesto.md`. If you see the input, generate this card.*

### 1.1 THEORY (Rule/Pattern)
**Input**: Bolded rules, axioms, or best practices.
*   **Pattern**: `What is the [Rule Name] regarding [Topic]?`
*   **Pattern**: `Why is [Practice] preferred over [Alternative]? (The Principle)`
*   **Example**:
    *   **Front**: According to the "Prop Drilling" rule, why should you avoid passing data through 3+ layers?
    *   **Back**: It couples intermediate components to data they don't use, making refactoring brittle.

### 1.2 CONSTRUCTIVE (Code/Implementation)
**Input**: Code blocks.
**Constraint**: Context is mandatory (MC-CTX-001).
*   **Pattern**: `Given [Context/State], write the code to [Task].`
*   **Example**:
    *   **Front**:
        Given: `const users = [{id: 1}, {id: 2}]`
        Task: Write a `reduce` function to map these by ID.
    *   **Back**:
        ```javascript
        users.reduce((acc, u) => ({...acc, [u.id]: u}), {})
        ```

### 1.3 NEGATION (Distinction)
**Input**: "X is not Y", "Unlike A...", "Difference between...".
*   **Pattern**: `How does [Concept A] differ from [Concept B] regarding [Dimension]?`
*   **Pattern**: `[Concept X] is NOT [Concept Y] because...?`
*   **Example**:
    *   **Front**: How does `Subject` differ from `BehaviorSubject` regarding initial value?
    *   **Back**: `BehaviorSubject` requires an initial value and emits it to new subscribers; `Subject` does not.

### 1.4 COUNTER-EVIDENCE (Darwin)
**Input**: "However...", "Exceptions...", "Critics argue...".
*   **Pattern**: `When does [Rule/Pattern] fail or apply poorly?`
*   **Pattern**: `What is the strongest argument AGAINST [Concept]?`
*   **Example**:
    *   **Front**: When is "Don't Repeat Yourself" (DRY) a bad practice?
    *   **Back**: When the repetition is coincidental (accidental duplication) rather than structural, leading to wrong abstractions.

### 1.5 DEFINITION (Deep)
**Input**: "X is...", Definitions.
**Constraint**: No tautologies. Must connect to use/nature.
*   **Pattern**: `What is [Term] in the context of [System]?`
*   **Pattern**: `Define [Term] by its function, not just its form.`
*   **Example**:
    *   **Front**: What is a "High Order Function"?
    *   **Back**: A function that takes another function as an argument OR returns a function.

### 1.6 PROCEDURE (Configuration/Steps)
**Input**: Steps, CLI commands, Config settings.
*   **Pattern**: `What are the steps to [Task]?` (Use Cloze for ordering)
*   **Pattern**: `How do you configure [System] to [Result]?`
*   **Example**:
    *   **Front**: How do you enable strict mode in `tsconfig.json`?
    *   **Back**: Set `"strict": true` in the `compilerOptions` block.

### 1.7 MODEL (Mental Model)
**Input**: Diagrams, "Imagine...", "Structure of...".
*   **Pattern**: `Draw/Visualize the [System] architecture.`
*   **Pattern**: `Trace the flow of [Data] through [Components].`
*   **Example**:
    *   **Front**: visual: Draw the flexbox alignment matrix (Justify vs Align).
    *   **Back**: Justify = Main Axis; Align = Cross Axis.

### 1.8 FAILURE MODE (Mistake)
**Input**: "Common error", "Warning", "Crash".
*   **Pattern**: `What specific error occurs if you [Action]?`
*   **Pattern**: `What is the root cause of [Error Message]?`
*   **Example**:
    *   **Front**: What happens if you modify a state variable directly in React?
    *   **Back**: The component will not re-render because React/Fiber relies on immutable setters to detect change.

---

## 2. The Enhancers (Depth & Context)
*Use these templates to add depth when quotas allow or for specific constraints.*

### 2.1 The Prediction
**Input**: Complex logic flow.
*   **Pattern**: `What is the console output of: [Code Snippet]`

### 2.2 The Why (Mechanism)
**Input**: "Because...", "Due to...".
*   **Pattern**: `Why does [Mechanism] work this way? (Under the hood)`

### 2.3 The Connection (Synthesis)
**Input**: Multiple related concepts.
*   **Pattern**: `How does [Concept A] enable/constrain [Concept B]?`

### 2.4 The Open List (3-Tier)
**Input**: Unordered lists / sets of examples.
1.  **Anchor**: `What category does [Instance] belong to?`
2.  **Pattern**: `What characterizes [Category]?`
3.  **Generative**: `Give 3 examples of [Category].`

### 2.5 The Salience (Immediacy)
**Input**: "Important", "Key takeaway".
*   **Pattern**: `Why is [Concept] critical for [Project/Goal]?`

### 2.6 Mnemonic Scaffolding
**Input**: Hard-to-remember ordered lists.
*   **Pattern**: `What are the [N] stages? (Mnemonic: [Phrase])`

