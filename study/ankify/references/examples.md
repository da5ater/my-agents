# Examples (Manifesto Aligned)

## Good Examples

### Model
**Front**: Draw the Request Lifecycle diagram for a NestJS Middleware.
**Back**: Request -> Middleware -> Guard -> Interceptor -> Pipe -> Controller -> Interceptor -> Exception Filter -> Response

### Constructive (MC-CTX-001 Compliant)
**Front**:
Given: `const users = [{id: 1, name: 'Alice'}]`
Task: Write a `reduce` function to create a map keyed by ID.
**Back**:
```javascript
const map = users.reduce((acc, user) => {
  acc[user.id] = user;
  return acc;
}, {});
```

### Failure Mode (MC-SIGNAL-002 Compliant)
**Front**: What error is thrown if you access `this.props` before `super()` in a React Class constructor?
**Back**: `ReferenceError: Must call super constructor in derived class before accessing 'this'`

## Bad Examples (Do Not Generate)

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
*   **Why**: 50% guess chance.
*   **Fix**: "Compare the performance characteristics of `map` vs `forEach`."
