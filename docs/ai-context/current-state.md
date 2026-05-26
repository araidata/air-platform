# Current State

County AI Assurance Operations Center is a runnable Docker Compose platform with an explainable scoring engine, scanner ecosystem foundation, first real scanner integration through garak, bias/civil-rights assessment support, and guided operational workflow UX. Runtime behavior now distinguishes real operational records from placeholder metadata: bootstrap seeds example AI systems, scanner definitions, scan types, assessment profiles, language-access scenarios, and appeal-path checks, but does not seed fake findings, fake evidence, fake scanner runs, fake remediation records, or fake score impacts.

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

Phase 7 - Guided Operational UI Workflows is implemented and verified.

Development bootstrap now runs a cleanup for known seeded/mock operational records, then runs Phase 2, Phase 4, and Phase 6 metadata seed phases. It logs created and skipped record counts and remains disabled by default outside development unless `RUN_SEED=true` is set.

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
- API-backed operational pages with empty states for missing assessments, findings, evidence, scanner runs, and scores.
- FastAPI backend under `apps/api`.
- SQLAlchemy 2.x models for systems, assessments, findings, evidence, owners, retests, AIRB reviews, framework mappings, risk acceptances, audit events, and scores.
- Alembic migrations for Phase 2 workflow tables, Phase 3 scoring tables, and Phase 4 scanner ecosystem tables.
- REST endpoints for systems, assessments, findings, evidence, audit events, retests, AIRB reviews, owners, scores, scanner definitions, scan types, assessment profiles, scanner runs, scanner results, scanner adapters, system scan recommendations, and system scanner runs.
- Workflow services for finding transitions, assessment transitions, evidence creation, retest tracking, audit event creation, scoring, and scanner execution.
- Phase 2 seed data for five example county AI systems and owner metadata only.
- Phase 4 seed data for scanner definitions, scan types, and assessment profiles only.
- Backend tests covering model creation, valid and invalid finding transitions, evidence creation, audit events, retests, scoring, scanner execution, scanner APIs, raw output persistence, normalization failures, and API smoke flows.
- Lightweight frontend API client layer in `apps/web/src/lib/api-client.ts`.
- Docker Compose runtime with `postgres`, `backend`, and `frontend` services plus `scanner_data` storage.
- Backend container startup script that validates PostgreSQL, runs Alembic migrations, runs development bootstrap by default in development mode, and starts FastAPI.
- Explicit bootstrap runner for allowed metadata plus cleanup of older seeded/mock operational records.
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
- Assessment Tool frontend route under `apps/web/src/app/scanners/page.tsx` for direct garak and live HTTP endpoint testing without mock scanner choices.
- garak CLI adapter under `apps/api/app/scanners/adapters/garak_adapter.py`.
- Docker backend image installation of garak through `requirements-scanners.txt`.
- Native garak JSONL report, hit log, HTML report, scanner configuration, stdout/stderr log, raw platform JSON, and normalized output artifact preservation.
- Real garak findings normalized into existing finding, evidence, audit event, and score recalculation workflows.
- Direct Assessment Tool frontend visibility for garak and live HTTP runs, execution steps, findings, artifacts, response excerpts, and report JSON.
- Civil-rights assessment templates for rights-impacting AI, public benefits eligibility, HR/employment, law enforcement/CJIS, citizen-facing chatbots, accessibility/language access, and human review/appeals.
- Language-access scenario records for English/Spanish evidence-backed review.
- Human appeal-path check records for escalation, adverse decision review, override, and accessibility paths.
- Fairness evidence types that reuse the existing evidence architecture.
- AIRB indicators for civil-rights, accessibility, language-access, fairness, human-review, and appeal-path validation.
- Civil Rights Review frontend route under `apps/web/src/app/civil-rights/page.tsx`.
- Guided Workflow frontend route under `apps/web/src/app/workflows/page.tsx`.
- API-backed system intake and management UI under `apps/web/src/app/inventory/page.tsx`.
- API-backed findings triage workspace under `apps/web/src/app/findings/page.tsx`.
- API-backed evidence review workspace under `apps/web/src/app/evidence/page.tsx`.
- API-backed AIRB intake and decision workspace under `apps/web/src/app/review-board/page.tsx`.
- API-backed system detail route under `apps/web/src/app/systems/[id]/page.tsx`.
- Assessment Target Configuration on system records and UI workflows, including target type/location, authentication type/reference, assessment method, scanner compatibility tags, manual-review-only, and uploaded-artifact support.
- Direct assessment-tool run persistence and APIs for one-page garak and live HTTP tester execution with process steps, findings, artifacts, and report JSON.

## Does Not Exist Yet

- Multiple real scanner integrations.
- OneTrust integration.

## Highest-Value Next Step

Begin Phase 8 governance exports and OneTrust workflow support. Prioritize CSV exports, structured JSON governance exports, audit packet export, and manual OneTrust field mapping before any API integration.

## Agent Reminder

Before making changes, read:

- `CLAUDE.md`
- `AGENTS.md`
- `CODEX.md`
- `docs/ai-context/current-state.md`
- `docs/ai-context/implementation-status.md`
- `docs/ai-context/next-steps.md`
