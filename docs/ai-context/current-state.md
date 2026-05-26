# Current State

Canonical AI engineering direction: `docs/ai-engineering/project-direction.md`.

AI Assessment Scanner is a runnable Docker Compose platform for county AI risk profiling, automated testing, evidence collection, human review, and executive reporting.

The product direction is assessment-first, testing-first, and evidence-first. Governance language should remain lightweight and tied to review decisions, evidence, reports, and control mappings.

## Exists Now

- Next.js + TypeScript frontend under `apps/web`.
- FastAPI backend under `apps/api`.
- PostgreSQL runtime through Docker Compose.
- SQLAlchemy models and Alembic migrations for systems, assessments, scanner runs, findings, evidence, owners, retests, review records, framework mappings, risk acceptances, audit events, and scores.
- API endpoints for systems, assessments, findings, evidence, audit events, retests, owners, scores, scanner definitions, scan types, assessment profiles, scanner runs, scanner results, scanner adapters, recommendations, and direct assessment-tool runs.
- Deterministic scoring with score history, explanations, snapshots, and service-layer recalculation hooks.
- Scanner orchestration framework with adapter contract, scanner run records, artifact preservation, evidence linkage, finding normalization, and score impact.
- garak CLI adapter for real prompt-injection-oriented testing.
- Live HTTP assessment tester for endpoint-based adversarial prompts and report artifacts.
- Assessment Tool UI for garak and live HTTP testing.
- API-backed intake, assessment launch, findings triage, evidence review, review workflow, and system detail surfaces.
- Development bootstrap for example systems, owners, scanner definitions, scan types, assessment profiles, language-access scenarios, and appeal-path checks.
- Honest empty-state behavior for operational records that have not been created by real workflow activity.

## Not Built Yet

- Giskard adapter.
- PyRIT adapter.
- Langfuse trace/evidence integration.
- OpenControl / Compliance Masonry export.
- PDF executive reports.
- Production RBAC.
- Backup/restore automation.
- Production logging and monitoring.

## Runtime Data Behavior

Development bootstrap may seed metadata and example systems. It must not seed fabricated assessments, findings, evidence, scanner runs, remediation records, or score impacts.

Production records should come from:

- Assessment intake.
- Real scanner execution.
- Uploaded or captured evidence.
- Human review actions.
- Reporting/export generation.

## Highest-Value Next Step

Begin Giskard integration.

Recommended first implementation slice:

- Add a Giskard adapter skeleton behind the existing scanner adapter contract.
- Support hallucination and prompt-injection test configuration first.
- Preserve raw Giskard outputs as evidence.
- Normalize initial Giskard results into existing findings.
- Keep execution local and Docker/CLI friendly.

## Agent Reminder

Before making changes, read:

- `docs/ai-engineering/project-direction.md`
- `CLAUDE.md`
- `AGENTS.md`
- `CODEX.md`
- `docs/ai-context/current-state.md`
- `docs/ai-context/implementation-status.md`
- `docs/ai-context/next-steps.md`
