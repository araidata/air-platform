# Current State

County AI Assurance Operations Center has moved from mock UI and durable backend workflow implementation into a runnable Docker Compose platform with an explainable scoring engine. The project still preserves durable operating context for future AI-assisted development, and now has a working frontend scaffold, FastAPI backend, PostgreSQL runtime, migrations, seed data, operational smoke checks, and Phase 3 score workflows.

## Product Definition

This is an operational AI governance, AI security, AI bias/civil-rights, findings, evidence, and assessment platform for county government.

It is intended for one or two operators who need to manage:

- AI inventory.
- Assessments.
- Findings.
- Evidence.
- Audit packets.
- Risk scoring.
- Governance workflows.
- AI Review Board decisions.
- Reports.
- Future OneTrust export or integration.

## Current Phase

Phase 2.5 — Runtime Stabilization is implemented and verified.

Phase 3 â€” Scoring Engine is implemented and verified.

## Exists Now

- AI assistant operating files.
- Architecture documentation.
- Scanner strategy documentation.
- Findings and evidence documentation.
- Governance documentation.
- UI/UX guidance.
- Integration planning.
- Roadmap and todo files.
- ADRs for core architectural constraints.
- Next.js frontend scaffold under `apps/web`.
- Centralized mock data for systems, assessments, findings, evidence, scores, and reviews.
- Mock-data-driven pages for executive dashboard, inventory, findings queue, system detail, evidence, and AI Review Board queue.
- FastAPI backend under `apps/api`.
- SQLAlchemy 2.x models for systems, assessments, findings, evidence, owners, retests, AIRB reviews, framework mappings, risk acceptances, and audit events.
- Alembic initial migration for Phase 2 workflow tables.
- REST endpoints for systems, assessments, findings, evidence, audit events, retests, AIRB reviews, and owners.
- Workflow services for finding transitions, assessment transitions, evidence creation, retest tracking, and audit event creation.
- Phase 2 seed script with the five mock county AI systems and realistic findings/evidence.
- Backend tests covering model creation, valid and invalid finding transitions, evidence creation, audit events, retests, and API smoke flows.
- Lightweight frontend API client layer in `apps/web/src/lib/api-client.ts`.
- Docker Compose runtime with `postgres`, `backend`, and `frontend` services.
- Backend container startup script that validates PostgreSQL, runs Alembic migrations, optionally loads seed data, and starts FastAPI.
- Frontend container and Next.js rewrite proxy from `/api/backend/*` to the backend service.
- `.env.example` with backend, frontend, and PostgreSQL configuration.
- PostgreSQL named volume for persistent runtime data.
- Health endpoints and Compose health checks.
- Runtime smoke test script under `scripts/runtime-smoke-test.py`.
- Score persistence models for domain scores, score history, score explanations, and score snapshots.
- Alembic migration for Phase 3 scoring tables.
- Deterministic scoring engine with domain calculators for security, privacy, bias/civil-rights, explainability, governance evidence, and weighted overall governance.
- Score APIs for listing scores, retrieving explanations, system score history, and recalculating system or assessment scores.
- Service-layer score recalculation hooks for findings, evidence, retests, assessments, systems, and AIRB decisions.
- Seed-time score recalculation for the five mock county AI systems.
- Frontend score integrations for executive dashboard, system detail, findings queue, AI Review Board queue, and governance reports.

## Does Not Exist Yet

- Scanner adapter code.
- Real scanner integrations.
- OneTrust integration.

## Highest-Value Next Step

Begin Phase 4 scanner adapter framework: define the adapter contract, create a mock scanner adapter, preserve raw output as evidence, and normalize mock scanner output into findings.

Do not start with scanner integrations.

## Agent Reminder

Before making changes, read:

- `CLAUDE.md`
- `AGENTS.md`
- `CODEX.md`
- `docs/ai-context/current-state.md`
- `docs/ai-context/implementation-status.md`
- `docs/ai-context/next-steps.md`
