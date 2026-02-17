# Ankify Run Summary Template

At the end of every run, you MUST output a summary in this exact format.
Do not wrap this in a code block; render it as Markdown.

## Run Summary

| Metric | Value |
|--------|-------|
| Total Notes Discovered | <int> |
| Notes Processed | <int> |
| Notes Skipped | <int> |
| **Total Cards Generated** | **<int>** |
| **Doctrine Compliance** | <PASS/FAIL> |

### Card Type Distribution

| Type | Count | Target | Status |
|------|-------|--------|--------|


### Note Status Table

| Note | Cards | Compliance | Failure Reason (if any) |
|------|-------|------------|-------------------------|
| `basics/arrays.md` | 12 | ✅ PASS | - |
| `oop/classes.md` | 0 | ❌ FAIL | Missing FAILURE_MODE |
| `config/setup.md` | - | ⏭️ SKIP | No content |


### Execution Artifacts
- TSV Output: `<path>`
- Manifest: `<path>`

