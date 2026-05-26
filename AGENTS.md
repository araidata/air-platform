# AI Agent Operating Rules

This file applies to Claude, Codex, Cursor, ChatGPT, Copilot, and future AI coding agents working in this repository.

## Canonical Direction

`docs/ai-engineering/project-direction.md` is the source of truth for product purpose, terminology, technical stack, implementation priorities, mock/demo policy, and AI coding expectations.

Do not duplicate or override that direction here.

## Required Startup Routine

Before making changes, read:

- `docs/ai-engineering/project-direction.md`
- `CLAUDE.md`
- `AGENTS.md`
- `CODEX.md`
- `docs/ai-context/current-state.md`

Then read only the domain docs relevant to the task.

## Working Rules

- Keep changes narrow, verifiable, and consistent with the existing architecture.
- Preserve assessment, scanner run, finding, evidence, risk profile, review workflow, and report terminology.
- Treat scanners as external tools integrated through adapters.
- Preserve raw evidence and clear evidence references.
- Keep demo metadata separate from operational records.
- Avoid unnecessary rewrites, broad repo scans, duplicate docs, and premature infrastructure.

## Documentation Discipline

When implementation state changes, update `docs/ai-context/implementation-status.md`, the relevant todo file, and the README checklist when applicable.

Only mark a README checklist item complete after the work is implemented, verified, and reflected in status/todo documentation.
