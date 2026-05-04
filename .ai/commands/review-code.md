# Command — Review Code

## Task

Review code for open-noc-ai compliance.

## Review Areas

Check:

- AGENTS.md compliance
- architecture consistency
- model/schema/crud/endpoint pattern
- multi-tenant isolation
- soft delete
- naming
- imports
- unnecessary complexity
- Swagger visibility
- testability

## Forbidden Patterns

Flag:

- direct database logic in endpoints
- queries without tenant_id
- hard deletes
- unrelated refactors
- hidden behavior
- ambiguous naming
- new architecture without approval

## Output Format

Return:

## Summary

Short summary.

## Issues

List issues by severity.

## Required Fixes

List mandatory fixes.

## Recommended Improvements

List optional improvements.

## Final Decision

Approved / Approved with fixes / Rejected