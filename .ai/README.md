# .ai — open-noc-ai AI Development Framework

This folder contains operational instructions for AI-assisted development using GPT, Codex and other coding agents.

## Purpose

Optimize development by enforcing:

- predictable code
- architecture consistency
- multi-tenant safety
- small incremental changes
- better documentation
- easier code review
- agent-friendly engineering workflow

## Source of Truth

- AGENTS.md = main project constitution
- .ai/rules/ = mandatory technical rules
- .ai/commands/ = reusable task prompts
- .ai/agents/ = role definitions for AI agents
- Notion = planning, backlog and documentation
- GitHub = source of truth for code

## Mandatory Flow

Before coding:

1. Read AGENTS.md
2. Read relevant .ai/rules/
3. Read the target file
4. Read similar existing entities
5. Identify the existing pattern
6. Implement only the requested change
7. Validate before finishing

## Development Principle

Agents must not be creative.

Agents must be:

- precise
- safe
- consistent
- minimal
- auditable