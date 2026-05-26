# Claude Code Operating Guide

This repository is AI Assessment Scanner: an internal county platform for AI risk profiling, automated testing, evidence collection, human review workflows, and executive reporting.

Claude Code sessions must preserve project memory, avoid overengineering, and keep the documentation and implementation aligned with the assessment-first direction.

## Required Reading Before Changes

Before making code or documentation changes, read:

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

## Project Philosophy

Preserve these principles:

- Assessment-first.
- Testing-first.
- Evidence-first.
- Findings remain central.
- One or two operators.
- One Linux VM.
- Docker Compose first.
- API-first platform.
- CLI/container-first scanner execution.

## Hard Constraints

Do not add:

- Kubernetes.
- Microservices.
- Distributed workers.
- Enterprise auth before production readiness work.
- Multi-tenant SaaS assumptions.
- Scanner integrations outside the adapter model.
- Reporting integrations before export formats are stable.

Do not rewrite external scanners such as garak, Giskard, PyRIT, Langfuse, Fairlearn, Aequitas, ModelScan, Ragas, DeepEval, or Promptfoo.

## How To Build

- Keep changes narrow and tied to the roadmap.
- Prefer explicit schemas, clear API boundaries, and audit-friendly records.
- Preserve raw scanner output as evidence.
- Use demo metadata only for local development setup.
- Do not seed fake operational findings, evidence, scanner runs, or scores.
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
