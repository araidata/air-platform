# Current State

County AI Assurance Operations Center has moved from mock UI and durable backend workflow implementation into a runnable Docker Compose platform with an explainable scoring engine, Phase 4 scanner ecosystem foundation, Phase 5 first real scanner integration, and Phase 6 bias/civil-rights assessment support. The project still preserves durable operating context for future AI-assisted development, and now has a working frontend, FastAPI backend, PostgreSQL runtime, migrations, seed data, operational smoke checks, score workflows, scanner registry, scan types, assessment profiles, mock scanner execution, real garak CLI execution, raw output preservation, evidence generation, normalized findings, score recalculation from scanner-created findings, civil-rights templates, language-access scenarios, appeal-path checks, AIRB civil-rights indicators, and fairness evidence views.

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

Phase 5 - First Real Scanner Integration is implemented and verified with garak.

Phase 6 - Bias and Civil Rights Assessment Support is implemented and verified.

Development bootstrap now explicitly runs Phase 2, Phase 4, and Phase 6 seed phases during development startup, logs created and skipped record counts, and remains disabled by default outside development unless `RUN_SEED=true` is set.

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
- Backend container startup script that validates PostgreSQL, runs Alembic migrations, runs development/demo bootstrap by default in development mode, and starts FastAPI.
- Explicit bootstrap runner for Phase 2 workflow data, Phase 4 scanner ecosystem data, Phase 6 civil-rights data, and score recalculation when seed records changed.
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
- garak CLI adapter under `apps/api/app/scanners/adapters/garak_adapter.py`.
- Docker backend image installation of garak through `requirements-scanners.txt`.
- Native garak JSONL report, hit log, HTML report, scanner configuration, stdout/stderr log, raw platform JSON, and normalized output artifact preservation.
- Real garak findings normalized into existing finding, evidence, audit event, and score recalculation workflows.
- Scanner Ecosystem frontend visibility for real scanner runs, adapters, evidence counts, normalized findings, and score change history.
- Civil-rights assessment templates for rights-impacting AI, public benefits eligibility, HR/employment, law enforcement/CJIS, citizen-facing chatbots, accessibility/language access, and human review/appeals.
- Language-access scenario records for English/Spanish evidence-backed review.
- Human appeal-path check records for escalation, adverse decision review, override, and accessibility paths.
- Fairness evidence types that reuse the existing evidence architecture.
- AIRB indicators for civil-rights, accessibility, language-access, fairness, human-review, and appeal-path validation.
- Civil Rights Review frontend route under `apps/web/src/app/civil-rights/page.tsx`.

## Does Not Exist Yet

- Multiple real scanner integrations.
- OneTrust integration.

## Highest-Value Next Step

Begin Phase 7 guided operational UI workflows. Prioritize operator-facing system intake, assessment launch, scanner execution, findings review, evidence review, AIRB workflow guidance, and connection to the existing backend APIs before expanding exports or new backend surface area.

## Agent Reminder

Before making changes, read:

- `CLAUDE.md`
- `AGENTS.md`
- `CODEX.md`
- `docs/ai-context/current-state.md`
- `docs/ai-context/implementation-status.md`
- `docs/ai-context/next-steps.md`
