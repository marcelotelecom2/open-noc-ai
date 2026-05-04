# Command — Validate Module

## Task

Validate a completed module or entity.

## Validation Checklist

Check:

- model exists
- schema exists
- crud exists
- endpoint exists
- route registered
- Swagger visible
- create works
- list works
- get works
- update works
- soft delete works
- tenant isolation works
- imports work
- no unrelated changes

## Risk Classification

Classify issues as:

- LOW: naming or minor consistency issue
- MEDIUM: missing validation or incomplete pattern
- HIGH: broken endpoint, broken import or persistence issue
- CRITICAL: multi-tenant leak or security issue

## Output

Return:

- summary
- checklist result
- issues found
- risk level
- recommended fixes