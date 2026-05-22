# Implementation Status

Update this file whenever the repository meaningfully changes.

## Completed

- Created repository-level AI assistant guidance:
  - `CLAUDE.md`
  - `AGENTS.md`
  - `CODEX.md`
  - `.cursor/rules/project-rules.mdc`
  - `.github/copilot-instructions.md`
- Created Claude Code command templates under `.claude/commands/`.
- Added Codex workflow playbooks in `docs/ai-context/codex-workflows.md`.
- Added README Build Checklist and AI-maintained completion rules.
- Documented project philosophy, constraints, roadmap, architecture, scanner strategy, findings, evidence, governance, integrations, UI guidance, todos, and ADRs.
- Confirmed project direction:
  - Single Linux VM.
  - Docker Compose first.
  - Mock-first development.
  - API-first platform.
  - CLI/container-first scanners through adapters.
- Created Phase 1 Next.js frontend scaffold under `apps/web`.
- Added centralized mock data for systems, assessments, findings, evidence, scores, and AI Review Board reviews.
- Built mock-data-driven Phase 1 pages:
  - Executive Dashboard.
  - AI Inventory.
  - Findings Queue.
  - System Detail Page.
  - Evidence & Audit Page.
  - AI Review Board Queue.
- Verified the frontend with `npm run lint`, `npm run build`, and HTTP route smoke checks for all Phase 1 pages.
- Created Phase 2 FastAPI backend under `apps/api`.
- Added SQLAlchemy 2.x models for:
  - AI systems.
  - Assessments.
  - Findings.
  - Evidence.
  - Owners.
  - Retests.
  - AIRB reviews.
  - Framework mappings.
  - Risk acceptances.
  - Audit events.
- Added Alembic configuration and initial Phase 2 workflow migration.
- Added REST endpoints for systems, assessments, findings, evidence, audit events, retests, AIRB reviews, and owners.
- Added workflow services for finding transitions, assessment status changes, evidence creation, retest tracking, and audit logging.
- Added Phase 2 seed data for the five mock systems, realistic findings, evidence, framework mappings, AIRB reviews, and audit records.
- Added backend tests covering model creation, valid and invalid finding transitions, evidence creation, audit event creation, retest creation/update, and API route smoke flows.
- Added lightweight frontend API client layer while preserving mock data as the frontend source of truth.
- Verified Phase 2 with `py -m pytest`, `py -m compileall app`, in-memory Alembic migration upgrade, and `npm.cmd run build`.
- Completed Phase 2.5 — Runtime Stabilization:
  - Added Docker Compose runtime with `frontend`, `backend`, and `postgres` services.
  - Added backend Dockerfile and startup script.
  - Added frontend Dockerfile and same-origin `/api/backend/*` proxy.
  - Added `.env.example` for backend, frontend, and PostgreSQL configuration.
  - Added PostgreSQL named volume persistence and container health checks.
  - Added `/health/db` for database connectivity validation.
  - Backend startup now waits for PostgreSQL, runs Alembic migrations, and loads idempotent seed data when `RUN_SEED=true`.
  - Added `scripts/runtime-smoke-test.py`.
  - Fixed PostgreSQL seed startup by flushing evidence records before creating evidence audit events.
- Verified Phase 2.5 with:
  - `docker compose config`.
  - `docker compose up --build -d`.
  - `docker compose exec -T backend alembic current`.
  - `docker compose exec -T backend python -m compileall app`.
  - `docker run --rm -v "${PWD}\apps\api:/app" -w /app python:3.12-slim sh -c "pip install -q -r requirements-dev.txt && pytest"`.
  - `npm.cmd run build`.
  - `docker run --rm --network air-platform_default ... scripts/runtime-smoke-test.py`.
  - `docker compose down` followed by `docker compose up -d` without removing volumes.
  - Host-facing checks for backend health, systems API, frontend load, and frontend/backend proxy.
- Completed Phase 3 â€” Scoring Engine:
  - Added score persistence models for domain scores, score history, score explanations, and score snapshots.
  - Added Alembic scoring migration.
  - Added deterministic scoring rules for security, privacy, bias/civil-rights, explainability, governance evidence, and overall governance.
  - Added score explanations tied to findings, evidence gaps, workflow gaps, remediation credit, and weighted aggregation.
  - Added score recalculation APIs and service-layer recalculation hooks for finding, evidence, retest, assessment, system, and AIRB workflow changes.
  - Added seed-time score recalculation for all seeded systems.
  - Added frontend score cards, domain breakdowns, score history, explanation panels, AIRB score context, findings impact summaries, and a governance reports route.
  - Verified with local backend tests, backend compile, frontend lint, frontend production build, Alembic migration test, Docker Compose runtime startup, score API checks, recalculation checks, frontend score-view checks, and disposable-container backend tests.

## In Progress

- No current implementation work.

## Next

- Begin Phase 4 scanner adapter framework:
  - Adapter contract.
  - Mock scanner adapter.
  - Scanner run records.
  - Raw output and log preservation as evidence.
  - Normalization into findings.

## Blocked

- No current blockers.

## Intentionally Deferred

- Real scanner integrations.
- OneTrust API integration.
- Background job execution.
- Authentication and authorization.
- Production hardening beyond the local Docker Compose runtime.
- Kubernetes or distributed orchestration.

## Architectural Decisions

- ADR 0001: Single VM and Docker Compose.
- ADR 0002: Adapter-based scanner architecture.
- ADR 0003: Mock-first development.
- ADR 0004: API-first platform and CLI-first scanners.

## Current Known Issues

- Documentation exists in both new and earlier paths; future cleanup may consolidate older docs after implementation stabilizes.
- Docker Desktop initially was not running in the current session, but it was started and Phase 3 Docker Compose runtime verification completed successfully.
- Host ports `8000` and `3000` were already allocated on the verification machine. Runtime verification used `API_HOST_PORT=8010` and `FRONTEND_HOST_PORT=3010`; the default `.env.example` remains `8000` and `3000`.
- Browser plugin localhost verification was previously blocked by the in-app browser with `ERR_BLOCKED_BY_CLIENT`; route smoke verification was used as a fallback for Phase 1.

## Update Template

When updating this file, use:

- Completed:
- In Progress:
- Next:
- Blocked:
- Intentionally Deferred:
- Architectural Decisions:
- Current Known Issues:
