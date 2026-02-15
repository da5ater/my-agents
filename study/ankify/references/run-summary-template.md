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
| MODEL | <int> | >0 | <✅/❌> |
| FAILURE_MODE | <int> | >Total/25 | <✅/❌> |
| COUNTER_EVIDENCE | <int> | >0 if trig | <✅/❌> |
| NEGATION | <int> | >0 if trig | <✅/❌> |
| SYNTHESIS | <int> | >0 if trig | <✅/❌> |
| CONSTRUCTIVE | <int> | Cap | - |
| PROCEDURE | <int> | <50% | - |
| DEFINITION | <int> | <35% | - |

### Note Status Table

| Note | Cards | Compliance | Failure Reason (if any) |
|------|-------|------------|-------------------------|
| `basics/arrays.md` | 12 | ✅ PASS | - |
| `oop/classes.md` | 0 | ❌ FAIL | Missing FAILURE_MODE |
| `config/setup.md` | - | ⏭️ SKIP | No content |

### Top 5 Largest Notes

| Note | Cards | Compliance |
|------|-------|------------|
| `path/to/note.md` | 10 | ✅ PASS |
| `path/to/note.md` | 9 | ✅ PASS |
| `path/to/note.md` | 9 | ❌ FAIL |

### Execution Artifacts
- TSV Output: `<path>`
- Manifest: `<path>`
- Run Stats: `<path>`
