# Codex Workflow Guide

Codex should work in this repository as a senior engineering collaborator with a bias toward small, useful, verifiable changes.

`docs/ai-engineering/project-direction.md` is the canonical AI engineering direction. Keep this file as workflow guidance only.

## Before Editing

Read:

- `docs/ai-engineering/project-direction.md`
- `AGENTS.md`
- `CODEX.md`
- `CLAUDE.md`
- `docs/ai-context/current-state.md`
- `docs/ai-context/implementation-status.md`
- `docs/ai-context/next-steps.md`
- `docs/ai-context/codex-workflows.md`

Use repository patterns before inventing new ones.

## Development Bias

Prefer targeted changes that improve scanner execution, assessment workflows, evidence collection, finding quality, traceability, reporting, or operational usability.

Avoid unnecessary rewrites, broad repository scans, duplicate direction docs, scanner integrations outside adapters, deep scanner rewrites, chatbot-first UX, and decorative AI features.

## Frontend Guidance

The UI should feel like a county assessment and security operations tool:

- Authoritative.
- Calm.
- Trustworthy.
- Evidence-focused.
- Work-oriented.

Use dense but readable dashboards, assessment intake, scanner execution controls, findings tables, evidence views, risk heatmaps, executive scorecards, and analyst drill-downs. Avoid vague AI language, toy dashboards, and roadmap labels in UI copy.

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
