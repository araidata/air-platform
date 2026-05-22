# Codex Workflow Guide

Codex should work in this repository as a senior engineering collaborator with a strong bias toward small, useful, verifiable changes.

## Before Editing

Read:

- `AGENTS.md`
- `CODEX.md`
- `CLAUDE.md`
- `docs/ai-context/current-state.md`
- `docs/ai-context/implementation-status.md`
- `docs/ai-context/next-steps.md`

Use repository patterns before inventing new ones.

## Development Bias

Prefer:

- Mock-first implementation.
- Clear local data structures.
- API-first boundaries.
- Small modules.
- Direct workflows.
- Explicit evidence references.
- Testable functions.
- Documentation updates with each phase.

Avoid:

- Enterprise abstractions.
- Distributed orchestration.
- Generic plugin systems before one real adapter exists.
- Deep scanner rewrites.
- Chatbot-first UX.
- Decorative AI gimmicks.

## Frontend Guidance

The UI should feel like a county security and governance operations center:

- Authoritative.
- Calm.
- Trustworthy.
- Audit-friendly.
- Security-focused.
- Government-grade.

Use dense but readable dashboards, findings tables, risk heatmaps, evidence views, executive scorecards, and analyst drill-downs. Avoid neon AI styling, vague AI magic language, and toy dashboards.

## Backend Guidance

The backend should eventually expose stable APIs for:

- Systems.
- Assessments.
- Findings.
- Evidence.
- Scanner runs.
- Scoring.
- AI Review Board reviews.
- Reports.
- Integrations.

Do not build backend complexity until Phase 2 unless the current task explicitly requires it.

## Verification

For code changes, run the smallest meaningful verification available. If no tests or app code exist yet, verify file structure and documentation links.
