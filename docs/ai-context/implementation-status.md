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
- Created Phase 2 FastAPI backend under `apps/api`.
- Added SQLAlchemy 2.x models, Alembic migrations, APIs, workflow services, seed data, and tests for systems, assessments, findings, evidence, owners, retests, AIRB reviews, framework mappings, risk acceptances, and audit events.
- Completed Phase 2.5 Runtime Stabilization:
  - Docker Compose runtime with `frontend`, `backend`, and `postgres`.
  - Backend and frontend Dockerfiles.
  - Backend startup migration and seed flow.
  - PostgreSQL persistence.
  - Same-origin frontend/backend proxy.
  - Health checks and runtime smoke test.
- Completed Phase 3 Scoring Engine:
  - Score persistence models for domain scores, score history, score explanations, and score snapshots.
  - Deterministic scoring rules for security, privacy, bias/civil-rights, explainability, governance evidence, and overall governance.
  - Score explanations tied to findings, evidence gaps, workflow gaps, remediation credit, and weighted aggregation.
  - Score APIs and service-layer recalculation hooks.
  - Seed-time score recalculation and frontend score integrations.
- Completed Phase 4 AI Assessment Ecosystem Foundation:
  - Added `ScannerDefinition`, `ScanType`, `AssessmentProfile`, `ScannerRun`, and `ScannerResult` models.
  - Added Alembic migration `202605220002_phase_4_scanner_ecosystem.py`.
  - Added scanner adapter contract under `apps/api/app/scanners/adapters/base.py`.
  - Added deterministic mock scanner adapter under `apps/api/app/scanners/adapters/mock_adapter.py`.
  - Added normalization layer under `apps/api/app/scanners/normalization/finding_normalizer.py`.
  - Added `ScannerExecutionService` for run creation, mock execution, raw output and log preservation, evidence generation, finding normalization, audit events, and score recalculation.
  - Added APIs for scanner definitions, scan types, assessment profiles, scanner runs, scanner results, scanner adapters, system scan recommendations, and system scanner runs.
  - Added Docker Compose `scanner_data` volume and `SCANNER_STORAGE_ROOT`.
  - Added seeded scanner registry entries for mock scanners and future-ready garak, AgentSeal, PyRIT, ModelScan, Fairlearn, Aequitas, IBM AI Fairness 360, Giskard, Ragas, DeepEval, and Promptfoo.
  - Added seeded scan types across security, privacy, bias/civil-rights, explainability, governance, RAG integrity, agent safety, supply chain, and model integrity.
  - Added seeded assessment profiles for public-facing chatbots, rights-impacting AI, law enforcement/CJIS AI, HR/employment AI, RAG applications, agentic/tool-using AI, and low-risk internal AI.
  - Added seeded completed and failed mock scanner runs, evidence records, normalized findings, and score recalculations.
  - Added Scanner Ecosystem frontend route with registry, profile selection, recommended scans, mock assessment runner, scanner run table, run detail, normalized findings, and generated evidence counts.
  - Added scanner tests for adapter execution, normalization, finding creation, evidence generation, raw output persistence, scanner run persistence, score integration, API responses, invalid execution, malformed output, failed normalization, and preserved failure logs.

## Verification

- `py -m pytest` from `apps/api`: 18 passed.
- `py -m compileall app` from `apps/api`.
- SQLite Alembic upgrade to `202605220002`.
- `npm.cmd run lint` from `apps/web`.
- `npm.cmd run build` from `apps/web`.
- `docker compose config --quiet`.
- `docker compose up --build -d` with `API_HOST_PORT=8010`, `FRONTEND_HOST_PORT=3010`, and `POSTGRES_PORT=55432`.
- `docker compose exec -T backend alembic current`: `202605220002 (head)`.
- `py scripts/runtime-smoke-test.py --backend-url http://localhost:8010 --frontend-url http://localhost:3010`.
- Runtime scanner API checks for `/scanner-definitions`, `/scan-types`, `/assessment-profiles`, `/scanner-runs`, and `/scanner-adapters`.
- Runtime mock scanner execution through the API: completed with one normalized finding, preserved raw output, and six score records.
- Browser verification of `http://localhost:3010/scanners`: page loaded, no relevant console errors, mock run interaction completed, completed-run count increased, and run artifacts showed preserved output.

## In Progress

- No current implementation work.

## Next

- Begin Phase 5 first real scanner integration:
  - Choose garak or AgentSeal as the first real scanner.
  - Implement one CLI/Docker adapter through the Phase 4 contract.
  - Preserve raw scanner output and logs before parsing.
  - Add parser fixtures and normalization tests.
  - Keep real scanner-specific metadata in evidence or constrained result metadata, not in core finding fields.

## Blocked

- No current blockers.

## Intentionally Deferred

- Multiple real scanner integrations.
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
- Browser verification used the Node-backed Browser runtime because the direct Browser MCP tool did not lazy-load through tool discovery.
- Host ports `8000`, `3000`, and `5432` may already be allocated on the verification machine. Phase 4 runtime verification used `API_HOST_PORT=8010`, `FRONTEND_HOST_PORT=3010`, and `POSTGRES_PORT=55432`.

## Update Template

When updating this file, use:

- Completed:
- In Progress:
- Next:
- Blocked:
- Intentionally Deferred:
- Architectural Decisions:
- Current Known Issues:
