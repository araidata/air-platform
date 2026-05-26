# Claude Code Operating Guide

This repository is AI Assessment Scanner. `docs/ai-engineering/project-direction.md` is the canonical AI engineering direction.

Claude Code sessions must preserve project memory, avoid overengineering, and keep documentation and implementation aligned with the assessment-first, testing-first, evidence-first direction.

## Required Reading Before Changes

Before making code or documentation changes, read:

- `docs/ai-engineering/project-direction.md`
- `CLAUDE.md`
- `AGENTS.md`
- `CODEX.md`
- `docs/ai-context/current-state.md`
- `docs/ai-context/implementation-status.md`
- `docs/ai-context/next-steps.md`

For UI work, also read:

- `docs/ai-context/ui-guidelines.md`
- `docs/ui-ux/design-system.md`
- `docs/ui-ux/page-map.md`

For scanner work, also read:

- `docs/architecture/scanner-adapter-architecture.md`
- `docs/scanners/adapter-contract.md`
- `docs/scanners/execution-model.md`

## How To Build

- Keep changes narrow and tied to the roadmap.
- Prefer explicit schemas, clear API boundaries, and audit-friendly records.
- Preserve raw scanner output as evidence.
- Use demo metadata only for local development setup.
- Do not seed fake operational findings, evidence, scanner runs, or scores.
- Do not rewrite external scanners or bypass scanner adapters.
- Update documentation when decisions or status change.

## Status Maintenance

After meaningful changes, update:

- `docs/ai-context/implementation-status.md`
- Relevant file in `docs/todos/`
- `docs/ai-context/current-state.md` if project capability or architecture changed
- `docs/decisions/` if a durable architecture decision was made

When completing a task listed in the README checklist, tick the README checkbox in the same commit as the completed work. Only tick a box after implementation, verification, and status/todo updates are complete.

## Claude Commands

Claude command templates live in `.claude/commands/`. They are prompts, not hooks. They should not auto-commit, delete files, install packages, or run privileged commands.
