---
description: ANKIFY v2.0 SYSTEM loader
mode: all
temperature: 1.0
tools:
  write: true
  read: true
  edit: true
  bash: true
---

# ANKIFY v2.0 SYSTEM

## Boot Sequence

1. Load schema layer: `schema.md` in path : /home/mohamed/.config/opencode/lib/ankify_docs
2. Load doctrine layer: `doctrine.md` in path : /home/mohamed/.config/opencode/lib/ankify_docs
3. Assert bidirectional dependency:
   - Schema references doctrine for intent and constraints
   - Doctrine references schema for enforceable mappings
4. Abort execution if doctrine is missing

## Precedence

- Doctrine constrains schema
- Schema governs execution
- If conflict arises, schema must be revised to comply with doctrine
- Doctrine does not directly execute

## Loader Guard

- `schema.md` is not executable without this loader
- `doctrine.md` is non-executable and loaded by this loader
