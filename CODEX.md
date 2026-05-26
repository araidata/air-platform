# Codex Workflow Guide

Codex should work in this repository as a senior engineering collaborator with a bias toward small, useful, verifiable changes.

## Before Editing

Read:

- `AGENTS.md`
- `CODEX.md`
- `CLAUDE.md`
- `docs/ai-context/current-state.md`
- `docs/ai-context/implementation-status.md`
- `docs/ai-context/next-steps.md`
- `docs/ai-context/codex-workflows.md`

Use repository patterns before inventing new ones.

## Development Bias

Prefer:

- Assessment-first implementation.
- API-first boundaries.
- Clear local data structures.
- Small modules.
- Direct workflows.
- Explicit evidence references.
- Testable functions.
- Documentation updates with each capability.

Avoid:

- Enterprise abstractions.
- Distributed orchestration.
- Scanner integrations outside adapters.
- Deep scanner rewrites.
- Chatbot-first UX.
- Decorative AI features.

## Frontend Guidance

The UI should feel like a county assessment and security operations tool:

- Authoritative.
- Calm.
- Trustworthy.
- Evidence-focused.
- Work-oriented.

Use dense but readable dashboards, assessment intake, scanner execution controls, findings tables, evidence views, risk heatmaps, executive scorecards, and analyst drill-downs. Avoid vague AI language and toy dashboards.

## Backend Guidance

The backend should expose stable APIs for:

- Systems.
- Assessments.
- Scanner runs.
- Findings.
- Evidence.
- Risk profiles.
- Review workflows.
- Reports.
- Integrations.

Do not build backend complexity until a workflow or integration requires it.

## Verification

For code changes, run the smallest meaningful verification available. For documentation-only changes, verify the edited docs for terminology consistency and broken roadmap references.

## README Checklist

When Codex completes a task listed in the README checklist, update the checkbox in the same commit as the completed work. Only tick a box after implementation, verification, and status/todo documentation updates are done.

## Workflow Playbooks

Detailed Codex playbooks live in `docs/ai-context/codex-workflows.md`.
