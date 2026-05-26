# Phased Build Plan

This plan has no dates. Move forward only when the current phase has enough working value to support the next phase.

## Phase 0 — Repository and AI Context Foundation

Purpose:
Create documentation, AI assistant files, roadmap, and architecture context.

Build:

- Assistant rules for Claude, Codex, Cursor, Copilot, and future agents.
- Architecture, scanner, findings, evidence, governance, integration, UI, and todo docs.
- ADRs for core constraints.

Do not build:

- Application code.
- Real scanner integrations.
- OneTrust integration.

## Phase 1 — Operational UI Foundation

Purpose:
Build dashboard, inventory, findings queue, and system detail pages. Historical scaffolding used mock data, but runtime mock operational behavior is now retired.

Build:

- Executive Dashboard.
- AI Inventory.
- Findings Queue.
- System Detail Page.
- Evidence & Audit Page.
- AI Review Board Queue starter view.
- Initial page shells that later bind to real APIs or explicit empty states.

Do not build:

- Backend persistence.
- Real scanners.
- Authentication.
- Complex reporting engine.

## Phase 2 — Findings, Evidence, and Assessment Workflow

Purpose:
Build real data models and workflow mechanics for assessments, findings, evidence, status, owners, and retesting.

Build:

- Database schema.
- API endpoints.
- Finding lifecycle.
- Evidence records.
- Assessment status transitions.
- Owners and due dates.
- Retest status.

Do not build:

- Real scanner breadth.
- OneTrust API integration.
- Distributed workers.

## Phase 2.5 — Runtime Stabilization

Objectives:

- Make the platform runnable with Docker Compose.
- Run frontend, backend, and PostgreSQL together on one host.
- Apply Alembic migrations inside the backend container.
- Load idempotent seed data into PostgreSQL.
- Validate frontend/backend connectivity and API persistence.

Rationale:

Phase 2 created the backend workflow records, but the repository still needed an operational runtime. This phase turns the code into a reproducible one-VM platform before Phase 3 scoring adds more business logic.

Deliverables:

- `docker-compose.yml` with `frontend`, `backend`, and `postgres` services.
- Backend Dockerfile and startup script.
- Frontend Dockerfile and same-origin backend proxy.
- `.env.example` for runtime configuration.
- PostgreSQL named volume.
- Health checks for practical startup validation.
- Runtime smoke test script.
- Deployment documentation for startup, migrations, seed, reset, and troubleshooting.

Operational outcomes:

- A developer can copy `.env.example` to `.env`, run `docker compose up`, and use seeded data.
- Backend startup validates PostgreSQL, applies migrations, seeds data, and exposes FastAPI.
- The frontend can reach the backend through `/api/backend/*`.
- PostgreSQL data survives container restart when volumes are preserved.

What intentionally remains deferred:

- Scanner execution containers.
- Redis, queues, and background job systems.
- Production reverse proxy, TLS, and backup automation.
- Kubernetes, Helm, service mesh, or distributed infrastructure.
- Enterprise authentication and authorization.

## Phase 3 — Scoring Engine

Purpose:
Implement explainable scoring for security, privacy, bias/civil rights, explainability, and governance evidence.

Built:

- Score inputs.
- Domain scores.
- Overall system risk score.
- Score impact from findings.
- Explanation text and score history.
- Score snapshots.
- Score APIs and recalculation endpoints.
- Service-layer recalculation hooks.
- Frontend score displays and governance reports.

Do not build:

- Opaque ML scoring.
- Unexplainable risk formulas.
- Executive-only scores without evidence drill-down.

## Phase 4 — AI Assessment Ecosystem Foundation

Purpose:
Build the scanner and assessment ecosystem foundation around the existing findings, evidence, scoring, and governance workflows.

Built:

- Adapter contract.
- Base scanner adapter abstraction.
- Real adapter framework with graceful unsupported-adapter handling.
- Scanner registry.
- Scan type framework.
- Assessment profiles.
- Lightweight scan recommendation logic.
- Scanner run records.
- Scanner result records.
- Raw output and log capture.
- Evidence generation from scanner output.
- Normalization path into findings.
- Score recalculation from scanner-created findings.
- Scanner execution APIs.
- Scanner Ecosystem frontend route.
- Seeded scanner definitions, scan types, profiles, completed runs, failed runs, findings, evidence, and score recalculations.

Do not build:

- Multiple real scanner integrations.
- API services per scanner.
- Distributed orchestration.
- Auto-scheduling or continuous scanner monitoring.

## Phase 5 — First Real Scanner Integration

Purpose:
Integrate one scanner first through the Phase 4 adapter contract and Docker/CLI execution.

Built:

- garak CLI adapter.
- Docker backend runtime installation for garak.
- Parser for garak JSONL eval output.
- Evidence storage for native garak report JSONL, hit log JSONL, HTML report, scanner configuration, stdout/stderr logs, platform raw output, and normalized output.
- Normalized findings from garak scanner results.
- Score recalculation through the existing findings workflow.
- Fixture coverage for successful, empty, failed, malformed, and partial scanner outputs.

Do not build:

- Broad scanner marketplace.
- Tight scanner internals coupling.
- Custom reimplementation of scanner logic.

## Phase 6 — Bias and Civil Rights Assessment Support

Purpose:
Add structured bias scenario testing and fairness-oriented findings now that the first real scanner path is proven.

Build:

- Bias/civil-rights assessment templates.
- Language access scenarios.
- Human appeal path checks.
- Fairness finding categories.
- Protected class impact documentation.

Do not build:

- Automated legal conclusions.
- Claims that scanner output alone proves compliance.
- Full statistical fairness platform before workflow needs are known.

## Phase 7 — Guided Operational UI Workflows

Purpose:
Turn the existing pages and APIs into guided operator workflows that make intake, assessment launch, scanner execution, findings review, evidence review, and AIRB progression usable end to end.

Build:

- System Intake UI.
- Assessment Launch UX.
- Scanner Execution UX.
- Findings Review UX.
- Evidence Review UX.
- AIRB Workflow UX.
- Guided operator workflow navigation.
- UI connection to the existing backend APIs.
- Minimal backend API additions only when a workflow requires them.
- Runtime verification and documentation/status updates.

Do not build:

- Large frontend rewrites disconnected from the existing operations-center structure.
- Broad new backend abstractions before workflow gaps are proven.
- Export-heavy work before the operator workflows are connected.

## Phase 8 — OneTrust and Governance Export Support

Purpose:
Add export packages for OneTrust or governance review, starting with CSV/JSON/PDF-ready packets.

Build:

- CSV exports.
- Structured JSON exports.
- Audit packet export.
- Control mapping export.
- Manual upload workflow.

Do not build:

- OneTrust API integration first.
- Deep bidirectional sync before field mapping is validated.

## Phase 9 — Operational Maturity

Purpose:
Add scheduling, retesting, improved reporting, optional notifications, and better operator workflow.

Build:

- Retest scheduling.
- Notification hooks if needed.
- Better reports.
- Improved filters and saved views.
- Operational health checks.

Do not build:

- Enterprise workflow suites.
- Distributed scanner farms unless real load requires it.
- Multi-tenant SaaS layers.

