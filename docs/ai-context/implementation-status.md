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
  - Added Scanner Ecosystem frontend route with registry, profile selection, recommended scans, scanner runner, scanner run table, run detail, normalized findings, and generated evidence counts.
  - Added scanner tests for adapter execution, normalization, finding creation, evidence generation, raw output persistence, scanner run persistence, score integration, API responses, invalid execution, malformed output, failed normalization, and preserved failure logs.
- Completed Phase 5 First Real Scanner Integration:
  - Selected garak as the first real scanner because it has a documented CLI, native JSONL reporting, and a deterministic local test target for Docker verification.
  - Added `GarakCliAdapter` under `apps/api/app/scanners/adapters/garak_adapter.py`.
  - Added backend Docker installation of garak through `apps/api/requirements-scanners.txt`.
  - Enabled the seeded garak scanner definition with `garak_cli_adapter`.
  - Preserved native garak JSONL report, hit log, HTML report, scanner configuration, stdout/stderr log, raw platform JSON, and normalized output artifacts as evidence.
  - Normalized garak eval records into existing findings with evidence, audit events, score impact, score recalculation, and score history.
  - Updated the Scanner Ecosystem frontend to show real scanner execution, adapter details, evidence references, normalized findings, and score change counts.
  - Added garak parser, service, failure, empty-output, partial-output, artifact preservation, and scoring tests.
- Completed Phase 6 Bias and Civil Rights Assessment Support:
  - Added `LanguageAccessScenario` and `HumanAppealPathCheck` models and migration `202605220003_phase_6_civil_rights.py`.
  - Added civil-rights assessment templates through assessment profiles.
  - Added future-ready scan types for language access, accessibility, human appeal, fairness, and civil-rights governance evidence.
  - Added fairness evidence types to the existing evidence architecture.
  - Extended AIRB reviews with civil-rights, accessibility, language-access, fairness, human-review, and appeal-path indicators.
  - Extended Bias/Civil Rights and Governance Evidence scoring with explainable Phase 6 workflow and evidence gaps.
  - Added civil-rights APIs for templates, language-access scenarios, appeal-path checks, and summary data.
  - Added seeded civil-rights findings, evidence, score impacts, language scenarios, appeal checks, AIRB records, and remediation recommendations.
  - Added Civil Rights Review frontend route.
  - Added civil-rights tests for templates, scenarios, invalid language pairs, appeal evidence validation, evidence relationships, score recalculation, and API responses.
- Repaired development bootstrap seed initialization:
  - Explicitly runs Phase 2 workflow seed data, Phase 4 scanner ecosystem seed data, and Phase 6 civil-rights seed data during development startup.
  - Logs seed phase execution, records created, and existing records skipped.
  - Recalculates scores only when seed records changed or required scores are missing.
  - Keeps bootstrap enabled by default for `ENVIRONMENT=development` and disabled by default outside development unless `RUN_SEED=true` is set.
  - Added backend regression coverage proving the full bootstrap can be rerun without duplicating seeded operational records.
- Completed Phase 7 Guided Operational UI Workflows:
  - Added `/workflows` guided operator entry point for system selection, assessment profile selection, governance domain selection, recommended scan review, scanner selection/execution, assessment creation, and AIRB routing.
  - Reworked `/inventory` into an API-backed system intake and management UI with add, edit, and archive behavior through existing system APIs.
  - Reworked `/findings` into an API-backed triage workspace with owner assignment, due dates, remediation notes, lifecycle transition controls, risk acceptance, false-positive handling, close actions, linked evidence, score impact, and retest initiation.
  - Reworked `/evidence` into an API-backed evidence review workspace with linked system, assessment, finding, scanner run, raw artifact references, and chain-of-evidence display.
  - Reworked `/review-board` into an API-backed AIRB intake and decision workspace with approval, approval with exception, blocked decisions, decision notes, exception expiration, and civil-rights review indicators.
  - Reworked `/systems/[id]` into an API-backed system detail route so newly-created systems can be inspected from the inventory table.
  - Added API client helpers for system create/update/archive-by-status, assessment creation, finding updates/transitions/retests, owners, and AIRB create/update workflows.
  - Added lightweight frontend route-contract coverage for Phase 7 workflow controls without adding new test dependencies.
- Completed targeted Assessment Target Configuration correction:
  - Added lightweight system fields for target type, target location, authentication type/reference, assessment method, compatible scanner tags, manual-review-only, and uploaded-artifact support.
  - Added Alembic migration `202605220004_assessment_target_config.py`.
  - Updated system intake/edit UI, guided assessment launch, scanner execution UI, and system detail to expose target configuration.
  - Passed target metadata into scanner execution context, preserved scanner output metadata, and filtered scanner recommendations/runs by system compatibility.
  - Updated seeded demo systems with realistic chatbot, internal RAG, HR/vendor, policy document, and agent target configurations.

## Verification

- `py -m pytest` from `apps/api`: 24 passed.
- `py -m pytest` from `apps/api`: 30 passed after Phase 6.
- `py -m pytest` from `apps/api`: 31 passed after bootstrap seed initialization repair.
- `py -m compileall app` from `apps/api`.
- `docker compose config --quiet`.
- `docker compose up --build -d` with `COMPOSE_PROJECT_NAME=air_bootstrap_verify`, `API_HOST_PORT=8011`, `FRONTEND_HOST_PORT=3011`, and `POSTGRES_PORT=55433`.
- Backend startup logs showed Phase 2, Phase 4, Phase 6, and score recalculation execution with created and skipped-existing record counts.
- `docker compose exec -T backend alembic current`: `202605220003 (head)`.
- Runtime API counts after startup: 5 systems, 5 assessments, 17 findings, 31 evidence records, 178 audit events, 30 score records, 14 scanner definitions, 2 scanner adapters, 40 scan types, 11 assessment profiles, and 6 scanner runs.
- Runtime civil-rights summary after startup: 7 templates, 3 language-access scenarios, 4 appeal-path checks, 7 fairness findings, and 10 fairness evidence records.
- Runtime seed rerun in the backend container created 0 records and skipped existing records without changing key API counts.
- `py scripts/runtime-smoke-test.py --backend-url http://localhost:8011 --frontend-url http://localhost:3011`.
- Browser verification of `http://localhost:3011`: dashboard, Scanner Ecosystem, Civil Rights Review, Findings Queue, and Evidence & Audit pages loaded with meaningful data and no relevant console errors.
- `py -m compileall app` from `apps/api`.
- SQLite Alembic upgrade to `202605220002`.
- SQLite Alembic upgrade to `202605220003`.
- `npm.cmd run lint` from `apps/web`.
- `npm.cmd run build` from `apps/web`.
- `docker compose config --quiet`.
- `docker compose up --build -d` with `API_HOST_PORT=8010`, `FRONTEND_HOST_PORT=3010`, and `POSTGRES_PORT=55432` after Phase 6.
- `docker compose exec -T backend alembic current`: `202605220003 (head)`.
- `py scripts/runtime-smoke-test.py --backend-url http://localhost:8010 --frontend-url http://localhost:3010`.
- Runtime check for `/civil-rights/summary`: 7 templates, 3 scenarios, 4 appeal-path checks, 7 fairness findings, and 9 fairness evidence records.
- Browser verification of `http://localhost:3010/civil-rights`: page loaded, no relevant console errors, summary cards rendered, templates/language-access/appeal checks/fairness findings visible, and scrolling exposed the findings table.
- `docker compose up --build -d` with `API_HOST_PORT=8010`, `FRONTEND_HOST_PORT=3010`, and `POSTGRES_PORT=55432`.
- `docker compose exec -T backend alembic current`: `202605220002 (head)`.
- `py scripts/runtime-smoke-test.py --backend-url http://localhost:8010 --frontend-url http://localhost:3010`.
- Runtime scanner API checks for `/scanner-definitions`, `/scan-types`, `/assessment-profiles`, `/scanner-runs`, and `/scanner-adapters`.
- Runtime mock scanner execution through the API: completed with one normalized finding, preserved raw output, and six score records.
- Browser verification of `http://localhost:3010/scanners`: page loaded, no relevant console errors, mock run interaction completed, completed-run count increased, and run artifacts showed preserved output.
- Docker Compose backend image build installed garak 0.15.0.
- Runtime garak scanner execution through the API: completed with one normalized finding, eight linked evidence records, raw output path, log path, scanner result normalization version `phase5_scanner_v1`, six score records, and score history entries.
- Browser verification of `http://localhost:3010/scanners`: page loaded, no console errors, garak visible, real completed garak run visible with one finding, preserved artifacts, and score changes.
- `npm.cmd run lint` from `apps/web` after Phase 7 UI implementation.
- `npm.cmd test` from `apps/web` after Phase 7 UI implementation.
- `npm.cmd run build` from `apps/web` after Phase 7 UI implementation.
- `docker compose config --quiet` after Phase 7 UI implementation.
- `docker compose up --build -d` with `COMPOSE_PROJECT_NAME=air_phase7_verify`, `API_HOST_PORT=8012`, `FRONTEND_HOST_PORT=3500`, and `POSTGRES_PORT=55434` after Phase 7.
- `py scripts/runtime-smoke-test.py --backend-url http://localhost:8012 --frontend-url http://localhost:3500`.
- `docker compose exec -T backend alembic current`: `202605220003 (head)`.
- Browser verification of `http://localhost:3500/workflows`, `/inventory`, `/findings`, `/evidence`, `/review-board`, `/scanners`, and `/civil-rights`: key Phase 7 markers rendered and console checks had no relevant errors.
- Browser-created system through `/inventory`; the new system appeared in the inventory table.
- Browser-created assessment through `/workflows`; the guided workflow showed the created assessment outcome.
- Browser-executed scanner run through `/scanners`; completed run detail showed preserved artifacts.
- Browser-created and approved AIRB intake through `/review-board`.
- Browser-saved finding triage through `/findings` and verified evidence chain detail through `/evidence`.
- `py -m compileall app` from `apps/api` after Assessment Target Configuration correction.
- `py -m pytest` from `apps/api`: 33 passed after Assessment Target Configuration correction.
- `npm.cmd test` from `apps/web` after Assessment Target Configuration correction.
- `npm.cmd run lint` from `apps/web` after Assessment Target Configuration correction.
- `npm.cmd run build` from `apps/web` after Assessment Target Configuration correction.
- `docker compose config --quiet` after Assessment Target Configuration correction.
- `docker compose up --build -d` with `COMPOSE_PROJECT_NAME=air_target_verify`, `API_HOST_PORT=8014`, `FRONTEND_HOST_PORT=3514`, and `POSTGRES_PORT=55444`.
- `docker compose exec -T backend alembic current`: `202605220004 (head)`.
- `py scripts/runtime-smoke-test.py --backend-url http://localhost:8014 --frontend-url http://localhost:3514`: passed.
- Runtime seeded system target check confirmed chatbot, RAG endpoint, vendor AI, agent, and manual uploaded-document target configurations.
- Browser verification of `http://localhost:3514/inventory`, `/workflows`, and `/scanners`: assessment target markers rendered and no console errors.

## In Progress

- No current implementation work.

## Next

- Begin Phase 8 governance exports and OneTrust workflow support:
  - Add CSV exports for inventory, findings, assessments, and risk acceptances.
  - Add structured JSON governance exports.
  - Add audit packet export.
  - Draft OneTrust field mapping.
  - Support manual OneTrust upload workflow before any API integration.

## Blocked

- No current blockers.

## Intentionally Deferred

- Additional real scanner integrations beyond garak.
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
- Browser verification used the Node-backed Browser runtime.
- Host ports `8000`, `3000`, and `5432` may already be allocated on the verification machine. Phase 4 runtime verification used `API_HOST_PORT=8010`, `FRONTEND_HOST_PORT=3010`, and `POSTGRES_PORT=55432`.
- Windows excluded port ranges can block some frontend verification ports. Phase 7 verification used `FRONTEND_HOST_PORT=3500` after `3012` was refused.
- garak 0.15.0 brings a large dependency set into the backend image. Keep it as the only real scanner dependency until a second integration is explicitly prioritized.
- Local direct `alembic upgrade head` may hang if PostgreSQL is not running on the configured default URL. Use Docker Compose or set `DATABASE_URL` for a SQLite migration check.

## Update Template

When updating this file, use:

- Completed:
- In Progress:
- Next:
- Blocked:
- Intentionally Deferred:
- Architectural Decisions:
- Current Known Issues:
