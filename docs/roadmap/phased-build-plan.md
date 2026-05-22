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

## Phase 1 — Operational UI and Mock Data

Purpose:
Build dashboard, inventory, findings queue, and system detail pages using mock data.

Build:

- Executive Dashboard.
- AI Inventory.
- Findings Queue.
- System Detail Page.
- Evidence & Audit Page.
- AI Review Board Queue starter view.
- Centralized mock systems, findings, evidence, assessments, and reviews.

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

## Phase 4 — Scanner Adapter Framework

Purpose:
Build the scanner adapter interface and mock adapter implementation.

Build:

- Adapter contract.
- Mock scanner adapter.
- Scanner run records.
- Raw output and log capture.
- Normalization path into findings.

Do not build:

- Multiple real scanner integrations.
- API services per scanner.
- Distributed orchestration.

## Phase 5 — First Real Scanner Integration

Purpose:
Integrate one scanner first, likely garak or AgentSeal, through Docker/CLI adapter execution.

Build:

- One real adapter.
- Container/CLI execution path.
- Parser for structured output.
- Evidence storage for raw output.
- Normalized findings from scanner results.

Do not build:

- Broad scanner marketplace.
- Tight scanner internals coupling.
- Custom reimplementation of scanner logic.

## Phase 6 — Bias and Civil Rights Assessment Support

Purpose:
Add structured bias scenario testing and fairness-oriented findings.

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

## Phase 7 — OneTrust and Governance Export Support

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

## Phase 8 — Operational Maturity

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
