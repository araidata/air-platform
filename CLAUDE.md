# Claude Code Operating Guide

This repository is the County AI Assurance Operations Center: an operational AI governance and assurance platform for county government.

Claude Code sessions must treat this repo as a long-term AI-assisted development project. The main job is to preserve project memory, avoid overengineering, and build the application in realistic phases.

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

- Operational simplicity.
- Governance-first design.
- Findings and evidence as the priority.
- One or two operators.
- One Linux VM.
- Docker Compose first.
- Mock-first development.
- API-first platform.
- CLI/container-first scanner execution.

## Hard Constraints

Do not add:

- Kubernetes.
- Microservices.
- Distributed workers.
- Enterprise auth.
- Multi-tenant SaaS assumptions.
- Real scanner integrations before the adapter contract exists.
- OneTrust implementation before export planning and core workflows exist.

Do not rewrite external scanners such as garak, AgentSeal, PyRIT, Fairlearn, Aequitas, Giskard, ModelScan, Ragas, DeepEval, or Promptfoo.

## How To Build

- Start with mock systems, mock findings, mock evidence, and mock scan results.
- Keep changes narrow and tied to the roadmap.
- Prefer explicit schemas, clear API boundaries, and audit-friendly records.
- Preserve raw scanner output as evidence when scanner work begins.
- Update documentation when decisions or status change.

## Status Maintenance

After meaningful changes, update:

- `docs/ai-context/implementation-status.md`
- Relevant file in `docs/todos/`
- `docs/ai-context/current-state.md` if the project phase or architecture changed
- `docs/decisions/` if a durable architecture decision was made

## Claude Commands

Claude command templates live in `.claude/commands/`:

- `/next-task`
- `/review-architecture`
- `/update-status`
- `/build-ui-page`
- `/create-adapter`

These are prompts, not dangerous hooks. They should not auto-commit, delete files, install packages, or run privileged commands.
