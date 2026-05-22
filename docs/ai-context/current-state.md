# Current State

County AI Assurance Operations Center has moved from mock UI and durable backend workflow implementation into a runnable Docker Compose platform with an explainable scoring engine and Phase 4 scanner ecosystem foundation. The project still preserves durable operating context for future AI-assisted development, and now has a working frontend, FastAPI backend, PostgreSQL runtime, migrations, seed data, operational smoke checks, score workflows, scanner registry, scan types, assessment profiles, mock scanner execution, raw output preservation, evidence generation, normalized findings, and score recalculation from scanner-created findings.

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

Phase 2.5 - Runtime Stabilization is implemented and verified.

Phase 3 - Scoring Engine is implemented and verified.

Phase 4 - AI Assessment Ecosystem Foundation is implemented and verified.

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
- Next.js frontend under `apps/web`.
- Centralized mock data for systems, assessments, findings, evidence, scores, and reviews.
- Mock-data-driven pages for executive dashboard, inventory, findings queue, system detail, evidence, and AI Review Board queue.
- FastAPI backend under `apps/api`.
- SQLAlchemy 2.x models for systems, assessments, findings, evidence, owners, retests, AIRB reviews, framework mappings, risk acceptances, audit events, and scores.
- Alembic migrations for Phase 2 workflow tables, Phase 3 scoring tables, and Phase 4 scanner ecosystem tables.
- REST endpoints for systems, assessments, findings, evidence, audit events, retests, AIRB reviews, owners, scores, scanner definitions, scan types, assessment profiles, scanner runs, scanner results, scanner adapters, system scan recommendations, and system scanner runs.
- Workflow services for finding transitions, assessment transitions, evidence creation, retest tracking, audit event creation, scoring, and scanner execution.
- Phase 2 seed data for the five mock county AI systems and realistic findings/evidence.
- Phase 4 seed data for scanner definitions, scan types, assessment profiles, completed and failed scanner runs, scanner evidence, normalized findings, and recalculated scores.
- Backend tests covering model creation, valid and invalid finding transitions, evidence creation, audit events, retests, scoring, scanner execution, scanner APIs, raw output persistence, normalization failures, and API smoke flows.
- Lightweight frontend API client layer in `apps/web/src/lib/api-client.ts`.
- Docker Compose runtime with `postgres`, `backend`, and `frontend` services plus `scanner_data` storage.
- Backend container startup script that validates PostgreSQL, runs Alembic migrations, optionally loads seed data, and starts FastAPI.
- Frontend container and Next.js rewrite proxy from `/api/backend/*` to the backend service.
- `.env.example` with backend, frontend, PostgreSQL, and scanner storage configuration.
- PostgreSQL named volume for persistent runtime data.
- Scanner artifact volume mounted at `/data` for raw scanner output and logs.
- Health endpoints and Compose health checks.
- Runtime smoke test script under `scripts/runtime-smoke-test.py`.
- Score persistence models for domain scores, score history, score explanations, and score snapshots.
- Deterministic scoring engine with domain calculators for security, privacy, bias/civil-rights, explainability, governance evidence, and weighted overall governance.
- Score APIs for listing scores, retrieving explanations, system score history, and recalculating system or assessment scores.
- Service-layer score recalculation hooks for findings, evidence, retests, assessments, systems, AIRB decisions, and scanner-created findings.
- Frontend score integrations for executive dashboard, system detail, findings queue, AI Review Board queue, and governance reports.
- Scanner Ecosystem frontend route under `apps/web/src/app/scanners/page.tsx`.

## Does Not Exist Yet

- Real scanner integrations.
- OneTrust integration.

## Highest-Value Next Step

Begin Phase 5 real scanner integration through the Phase 4 adapter contract. The first candidate should be garak or AgentSeal, run through a CLI/Docker adapter, with raw output and logs preserved as evidence before parser and normalization logic create findings.

Do not broaden into multiple real scanner integrations until one real adapter proves the execution, parser, evidence, finding, and scoring path.

## Agent Reminder

Before making changes, read:

- `CLAUDE.md`
- `AGENTS.md`
- `CODEX.md`
- `docs/ai-context/current-state.md`
- `docs/ai-context/implementation-status.md`
- `docs/ai-context/next-steps.md`
