# Codex Workflows

Use these playbooks for common repository work.

## Starting Work

1. Read `docs/ai-engineering/project-direction.md`, `CLAUDE.md`, `AGENTS.md`, `CODEX.md`, and `docs/ai-context/current-state.md`.
2. Read `docs/ai-context/implementation-status.md` and `docs/ai-context/next-steps.md`.
3. Read only the domain docs needed for the task.
4. Keep changes narrow and verifiable.

## Documentation Update

When capability or direction changes:

1. Update `docs/ai-context/implementation-status.md`.
2. Update the relevant todo file in `docs/todos/`.
3. Update the README roadmap checklist only for implemented and verified work.
4. Keep wording assessment-first, testing-first, and evidence-first.

## Scanner Adapter Work

Use when adding or changing external testing tools.

1. Read `docs/scanners/adapter-contract.md`.
2. Reuse the existing scanner run and evidence pipeline.
3. Validate target configuration before execution.
4. Preserve raw output even when parsing fails.
5. Normalize findings into the platform schema.
6. Add tests for success, no findings, invalid target, execution failure, and parser failure.

## UI Work

1. Keep pages dense, readable, and workflow-oriented.
2. Use API-backed data or honest empty states.
3. Avoid roadmap labels and demo terminology in UI text.
4. Make evidence links and status visible.

## Commit Readiness

Before calling work complete:

- Run the smallest meaningful verification.
- Confirm terminology consistency in touched docs.
- Update status/todo docs.
- Avoid unrelated refactors.
