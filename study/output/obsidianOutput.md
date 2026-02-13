---
aliases:
  - Context Preserving Accumulator
  - skip1 accumulator pattern
backlinks:
  - "[[Accumulators]]"
  - "[[Structural Recursion]]"
  - "[[How to Design Functions]]"
---

## Context-Preserving Accumulators
### Notes
- **Context Loss in Structural Recursion**: Structural recursion gives you each element and natural recursion, but it does not retain how far down the list you are; any logic that depends on position needs extra state to avoid losing that context.
- **Context-Preserving Accumulator**: Use an accumulator to carry the missing context (e.g., position) through recursion so decisions can be made locally without re-walking the list.
- **Accumulator Invariant**: Define a stable meaning for the accumulator (e.g., "acc is the 1-based position of first lox in lox0") and preserve that meaning in every recursive call.
- **Three Accumulator Responsibilities**: Initialize the accumulator, exploit it to make decisions, and update it to preserve the invariant across recursive calls.
- **Three-Part Accumulator Template**: Start from the structural recursion template, wrap it in an outer function with a local/trampoline, then add an accumulator parameter to the inner function and all recursive calls.

## skip1 (Keep Odd Positions)
### Notes
- **Goal**: Keep elements in odd positions (1st, 3rd, 5th, ...) of a list without recomputing position each time.
- **Key Decision**: Use `odd?` on the accumulator instead of trying to infer position from the list structure.
- **Accumulator Meaning**: A natural number representing the 1-based position of `(first lox)` in the original `lox0`.

### Code Implementation
File path: `skip1-solution.rkt`

```racket
(define (skip1 lox0)
  ;; acc: Natural; 1-based position of (first lox) in lox0
  (local [(define (skip1 lox acc)
            (cond [(empty? lox) empty]
                  [else
                   (if (odd? acc)
                       (cons (first lox)
                             (skip1 (rest lox)
                                    (add1 acc)))
                       (skip1 (rest lox)
                              (add1 acc)))]))]
    (skip1 lox0 1)))
```

### Technical Procedures & Workflows
1. Start with the structural recursion template for `(listof X)`.
2. Wrap the function in an outer definition with `local` and a trampoline call.
3. Add an accumulator parameter to the inner function and all recursive calls.
4. Define the accumulator invariant (what the accumulator always represents).
5. Initialize the accumulator in the trampoline.
6. Use the accumulator for the decision (`odd? acc`) and update it each recursion (`add1 acc`).

### Definitions
- **Accumulator**: An extra parameter that carries context or partial results through recursive calls.
- **Accumulator Invariant**: The statement that remains true about the accumulator at every call, even as its value changes.
