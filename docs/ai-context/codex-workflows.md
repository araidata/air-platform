# Codex Workflows

This file gives Codex a practical operating playbook for this repository. It is intentionally lightweight. Do not add auto-running hooks, privileged commands, or hidden automation here.

## Startup Workflow

Before editing, Codex should read:

- `AGENTS.md`
- `CODEX.md`
- `CLAUDE.md`
- `docs/ai-context/current-state.md`
- `docs/ai-context/implementation-status.md`
- `docs/ai-context/next-steps.md`
- `docs/ai-context/constraints.md`

Then read the task-specific docs:

- UI work: `docs/ui-ux/design-system.md`, `docs/ui-ux/page-map.md`, `docs/ai-context/ui-guidelines.md`
- Scanner work: `docs/scanners/adapter-contract.md`, `docs/scanners/execution-model.md`
- Findings work: `docs/findings/findings-lifecycle.md`, `docs/findings/normalized-findings-schema.md`
- Evidence work: `docs/evidence/evidence-model.md`, `docs/evidence/audit-packet-strategy.md`
- Integration work: `docs/integrations/onetrust-integration-plan.md`, `docs/integrations/future-integrations.md`

## Next Task Workflow

Use when the user asks what to do next or asks Codex to continue.

1. Read current state, implementation status, priorities, and next steps.
2. Choose the smallest task that advances the current phase.
3. Prefer API-backed UI work with honest empty states unless the user explicitly asks for exploratory scaffolding.
4. Name affected files before editing.
5. Implement the task.
6. Verify with the smallest meaningful check.
7. Update implementation status and relevant todo files.

Default next task:

- Build operational UI pages against real APIs or honest empty states.

## Build UI Page Workflow

Use when building a dashboard, queue, table, detail page, or settings page.

1. Read the UI guidance and page map.
2. Use backend persistence when it exists; otherwise show explicit empty states instead of fabricated operational records.
3. Keep the page operational, dense, and audit-friendly.
4. Show findings, evidence, approval state, and risk clearly.
5. Avoid chatbot-first layout, neon AI styling, and marketing copy.
6. Verify the page renders and text fits.
7. Update frontend todo and implementation status.

## Update Status Workflow

Use after meaningful changes.

Update:

- `docs/ai-context/implementation-status.md`
- `docs/ai-context/current-state.md` if the phase or architecture changed
- Relevant file under `docs/todos/`
- `docs/ai-context/known-issues.md` if a blocker or risk changed
- `docs/decisions/` if a durable architectural decision was made

Keep status factual. Do not turn status docs into a changelog of every small edit.

## Create Scanner Adapter Workflow

Use only when the project reaches Phase 4 or the user explicitly asks for adapter work.

1. Read the scanner adapter contract and execution model.
2. Start with the real adapter framework and return a clear unsupported-adapter state when no executable scanner is available.
3. Treat scanners as external tools.
4. Prefer Docker or CLI execution.
5. Use isolated execution directories.
6. Preserve raw output and logs as evidence.
7. Normalize findings into the platform schema.
8. Do not copy or rewrite scanner internals.

## Review Architecture Workflow

Use before large changes.

Check whether the proposed work:

- Preserves one-VM Docker Compose simplicity.
- Supports one or two operators.
- Keeps findings and evidence central.
- Uses adapters for scanners.
- Avoids microservices, Kubernetes, and distributed orchestration.
- Keeps OneTrust integration deferred until export workflows exist.

If the work violates these rules, stop and explain the safer path.

## Commit And Push Workflow

Only commit or push when the user asks.

Before committing:

- Check `git status -sb`.
- Review the staged scope.
- Stage only intended files.
- Use a terse commit message.
- Push to the configured remote only after the user requested it.

Do not auto-commit, auto-push, delete files, or install packages from this workflow.

## Future Codex Skill

A reusable Codex skill may be useful later if this county AI assurance pattern is reused across multiple repositories. For this repo, `AGENTS.md`, `CODEX.md`, and this workflow file are enough.
