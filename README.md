# County AI Assurance Operations Center

County AI Assurance Operations Center is an operational AI governance, AI security, bias/civil-rights, findings, evidence, and assessment platform for county government.

It is designed for one or two operators, not a large enterprise engineering team. The platform should help a county know which AI systems exist, what risks have been found, what evidence supports decisions, and what work still needs governance review.

This is not a chatbot product. This is the control plane for public-sector AI assurance.

## Who It Is For

- County AI assurance operators.
- Security, privacy, civil-rights, and governance reviewers.
- AI Review Board participants.
- Executives who need a trustworthy risk picture.
- Future AI coding assistants working in this repository.

## What Problem It Solves

Counties adopting AI need a practical way to inventory systems, assess them, preserve evidence, route findings, document approvals, and create audit-ready packets. Scanner tools can test pieces of the problem, but they do not create an operational governance program by themselves.

This platform owns the governance and orchestration layer:

- AI inventory.
- Assessments.
- Normalized findings.
- Evidence preservation.
- Audit packets.
- Risk scoring.
- Governance workflows.
- AI Review Board workflow.
- Dashboards and reporting.
- Future OneTrust export or integration.

External tools own specialized execution:

- Red-team probes.
- Prompt injection tests.
- Model file scanning.
- Fairness calculations.
- RAG evaluation.
- LLM evaluation.

The platform should orchestrate those tools, normalize their outputs, preserve evidence, create findings, and score risk. It should not recreate them.

## Current Status

The repository has completed Phase 7 - Guided Operational UI Workflows, with a targeted assessment-target correction for system intake and scanner launch plus a direct Garak + Live HTTP Assessment Workbench. A Next.js frontend exists under `apps/web`, and a FastAPI backend exists under `apps/api` with SQLAlchemy models, Alembic migrations, workflow services, seed data, tests for the core assurance records, an explainable scoring engine, an evidence-preserving scanner ecosystem, the first real garak CLI adapter, public-sector civil-rights review workflows, guided operator UI surfaces, and system-level target configuration for automated and manual assessments. The platform runs as a Docker Compose stack with frontend, backend, PostgreSQL, and a local scanner artifact volume.

Completed now:

- Repository context documentation.
- AI assistant rules for Claude, Codex, Cursor, Copilot, ChatGPT, and future coding agents.
- Architecture and scanner strategy docs.
- Findings, evidence, governance, integration, UI, todo, and ADR documentation.
- Claude Code command templates for future sessions.
- Next.js frontend with API-backed operational pages and honest empty states.
- FastAPI backend scaffold under `apps/api`.
- SQLAlchemy models and Alembic migration for systems, assessments, findings, evidence, owners, retests, AIRB reviews, framework mappings, risk acceptances, and audit events.
- REST endpoints for systems, assessments, findings, evidence, audit events, retests, AIRB reviews, and owners.
- Workflow services enforcing finding and assessment transitions with audit logging.
- Phase 2 seed data for example AI systems and owner metadata only.
- Basic backend tests for model creation, lifecycle transitions, evidence creation, retests, audit events, and API smoke flows.
- Docker Compose runtime with `frontend`, `backend`, and `postgres` services.
- Backend container startup flow that waits for PostgreSQL, applies Alembic migrations, loads idempotent development bootstrap metadata, and starts FastAPI.
- Development bootstrap runner that executes allowed Phase 2 inventory metadata, Phase 4 scanner registry/templates, and Phase 6 civil-rights templates/scenarios without generating findings, evidence, scanner runs, or scores.
- Frontend container with same-origin backend proxy support through `/api/backend/*`.
- PostgreSQL persistent named volume and service health checks.
- Runtime smoke test covering frontend load, backend health, DB health, seeded inventory/registry endpoints, empty operational datasets, and frontend/backend proxy connectivity.
- Phase 3 scoring models, Alembic migration, deterministic domain scoring engine, score history, score explanations, score snapshots, score APIs, recalculation workflows, and scoring tests.
- Frontend score integrations for the executive dashboard, system detail, findings queue, AI Review Board queue, and governance reports route.
- Phase 4 scanner ecosystem models for scanner definitions, scan types, assessment profiles, scanner runs, and scanner results.
- Scanner adapter contract, finding normalization layer, scanner execution service, and real adapter execution path.
- Raw scanner JSON and execution log preservation under the scanner artifact volume, with evidence records linked to systems and assessments.
- Scanner-created normalized findings that reuse the existing findings workflow, evidence architecture, audit events, and score recalculation hooks.
- Seeded scanner registry, scan types, and assessment profiles. Bootstrap intentionally does not seed scanner runs, findings, evidence, remediation records, or score impacts.
- Assessment Tool frontend route for direct garak and live HTTP endpoint testing with execution steps, findings, evidence excerpts, artifacts, and JSON report output.
- garak CLI scanner adapter for prompt-injection-oriented Phase 5 runtime validation.
- Native garak JSONL, hit log, HTML report, scanner configuration, stdout/stderr log, raw platform JSON, and normalized output preservation.
- garak findings normalized into the existing findings, evidence, audit event, and scoring workflows.
- Civil-rights assessment templates, language-access scenarios, human appeal-path checks, fairness evidence types, AIRB civil-rights indicators, and the Civil Rights Review frontend route.
- Phase 7 frontend workflow UX for system intake, assessment launch, scanner execution, findings triage, evidence review, AIRB intake/decisions, guided workflow navigation, and API-backed system detail.
- Assessment target configuration on system records: target type, target location, authentication type/reference, assessment method, compatible scanner tags, manual-review-only flag, and uploaded-artifact support.
- Direct assessment-tool APIs under `/assessment-tool/runs` so operators can run garak or live HTTP tests without pre-creating inventory records or knowing garak command-line syntax.

Not built yet:

- Multiple real scanner integrations.
- OneTrust integration.

## Runtime Data Behavior

The platform now prefers honest empty states over fabricated operational activity. Bootstrap may create example inventory and governance metadata, but it must not create fake assessments, findings, evidence, scanner runs, remediation records, or score impacts.

Seeded example systems:

- Public Benefits Chatbot.
- Sheriff Incident Summary Assistant.
- Permit Review Assistant.
- HR Resume Screening AI.
- Citizen Services RAG Chatbot.

Operational pages show "No assessments executed", "No findings generated", "No scanner runs available", and "No evidence collected" until real workflow activity exists.

## Tech Stack Direction

The planned stack is intentionally boring and maintainable:

- Frontend: Next.js, TypeScript, accessible dashboard UI.
- Backend: FastAPI or equivalent API-first service.
- Database: PostgreSQL.
- Jobs/cache: Redis only when needed.
- Deployment: one Linux VM using Docker Compose.
- Scanner execution: Dockerized CLI/container adapters.
- Storage: local or mounted evidence storage first; object storage can be added later.

## Deployment Model

The initial deployment target is:

- One Linux VM.
- Docker Compose.
- One database.
- One backend service.
- One frontend service.
- Local scanner execution directories.
- Retained raw outputs and logs as evidence.

Do not introduce Kubernetes, distributed workers, multi-region infrastructure, or microservice sprawl unless explicitly requested later.

## Development Bootstrap And Seed Behavior

In development mode, Docker Compose starts a usable platform automatically:

1. The backend waits for PostgreSQL.
2. Alembic migrations run to the latest schema.
3. Bootstrap removes known seeded/mock operational records from older development volumes.
4. Bootstrap runs Phase 2, Phase 4, and Phase 6 metadata seed phases.
5. FastAPI starts after inventory, scanner registry, assessment templates, language scenarios, and appeal-path checks are ready.

The seed runner is idempotent and safe to rerun with:

```powershell
docker compose exec backend python -m app.seed.run_seed
```

Startup logs show cleanup, each seed phase, records created, and existing records skipped. The seeded dataset includes AI systems, owners, audit events, scanner definitions, scan types, assessment profiles, language-access scenarios, and appeal-path checks.

Production-safe behavior is conservative by default. If `RUN_SEED` is unset, seed bootstrap runs only when `ENVIRONMENT=development`. Set `RUN_SEED=true` to intentionally load metadata in another environment, or `RUN_SEED=false` to disable bootstrap in development.

## Phase Plan

See [Phased Build Plan](docs/roadmap/phased-build-plan.md) for details.

- Phase 0: Repository and AI Context Foundation.
- Phase 1: Operational UI.
- Phase 2: Findings, Evidence, and Assessment Workflow.
- Phase 2.5 — Runtime Stabilization.
- Phase 3: Scoring Engine.
- Phase 4: AI Assessment Ecosystem Foundation.
- Phase 5: First Real Scanner Integration.
- Phase 6: Bias and Civil Rights Assessment Maturity.
- Phase 7: Guided Operational UI Workflows.
- Phase 8: Governance Exports and OneTrust Workflow Support.
- Phase 9: Operational Maturity.

## Build Checklist

This checklist is maintained by AI agents and human operators. It is not GitHub automation. When an AI agent completes a task, it should tick the checkbox in the same commit as the completed and verified work.

AI completion rule:

- Only mark a box complete after the work is implemented, verified, and reflected in the relevant status or todo docs.
- Do not mark future work complete just because planning documentation exists.
- If a task is partially done, leave it unchecked and update `docs/ai-context/implementation-status.md`.

### Phase 0 — Repository and AI Context Foundation

- [x] Create repository AI assistant files: `CLAUDE.md`, `AGENTS.md`, and `CODEX.md`.
- [x] Add Cursor and GitHub Copilot rules.
- [x] Add Claude Code command prompts.
- [x] Add Codex workflow playbooks.
- [x] Document project philosophy, constraints, and current state.
- [x] Document roadmap, architecture, scanner strategy, findings, evidence, governance, integrations, UI guidance, todos, and ADRs.
- [x] Add README AI-updated build checklist.

### Phase 1 — Operational UI

- [x] Create the frontend application scaffold.
- [x] Retire centralized mock operational data from runtime pages.
- [x] Build the Executive Dashboard.
- [x] Build the AI Inventory page.
- [x] Build the Findings Queue.
- [x] Build the System Detail Page.
- [x] Build the Evidence & Audit Page.
- [x] Build the AI Review Board Queue starter view.

### Phase 2 — Findings, Evidence, and Assessment Workflow

- [x] Create backend persistence.
- [x] Create database models and migrations.
- [x] Implement assessment workflow mechanics.
- [x] Implement finding lifecycle status transitions.
- [x] Implement evidence records and evidence-to-finding links.
- [x] Implement owners, due dates, retest status, and audit events.

### Phase 2.5 — Runtime Stabilization

Objective:
Make the disconnected frontend, backend, migration, seed, and database components run as one local operational platform.

Rationale:
The project needs a repeatable one-VM Docker Compose runtime before scoring or scanner-adapter work adds more moving pieces.

Deliverables and operational outcomes:

- [x] Add Docker Compose runtime.
- [x] Add frontend container.
- [x] Add backend API container.
- [x] Add PostgreSQL runtime.
- [x] Add persistent PostgreSQL volume.
- [x] Add shared environment configuration with `.env.example`.
- [x] Execute Alembic migrations during backend startup.
- [x] Load idempotent seed data during backend startup.
- [x] Add backend startup validation and health checks.
- [x] Add frontend/backend integration through a same-origin proxy.
- [x] Add runtime smoke testing.
- [x] Document developer startup, migration, seed, reset, and troubleshooting workflows.

Intentionally deferred:

- Scanner execution containers.
- Redis or background job systems.
- Kubernetes, Helm, or distributed infrastructure.
- Production reverse proxy and TLS hardening.
- Enterprise authentication.

### Phase 3 — Scoring Engine

- [x] Implement explainable domain scoring.
- [x] Calculate score impact from findings.
- [x] Show score history and score explanations.
- [x] Connect scoring to system, assessment, finding, and governance views.

### Phase 4 — AI Assessment Ecosystem Foundation

- [x] Implement scanner adapter interface.
- [x] Create scanner run records.
- [x] Capture raw output and logs as evidence.
- [x] Normalize real scanner output into findings.
- [x] Add scanner registry, scan types, assessment profiles, and scan recommendation APIs.
- [x] Add direct Assessment Tool frontend route for garak and live HTTP testing with findings, artifacts, and report output.

### Phase 5 — First Real Scanner Integration

- [x] Select first real scanner, likely garak or AgentSeal.
- [x] Run the scanner through Docker or CLI adapter execution.
- [x] Parse scanner output.
- [x] Preserve raw scanner evidence.
- [x] Create normalized findings from scanner results.

### Phase 6 — Bias and Civil Rights Assessment Support

- [x] Add bias and civil-rights assessment templates.
- [x] Add language access scenarios.
- [x] Add human appeal path checks.
- [x] Add civil-rights templates, language scenarios, appeal checks, and empty-state evidence/finding views.

### Phase 7 — Guided Operational UI Workflows

- [x] Build System Intake UI.
- [x] Build Assessment Launch UX.
- [x] Build Scanner Execution UX.
- [x] Build Findings Review UX.
- [x] Build Evidence Review UX.
- [x] Build AIRB Workflow UX.
- [x] Add guided operator workflow navigation.
- [x] Connect UI workflows to existing backend APIs.
- [x] Add minimal backend API additions only when required to complete the workflows.
- [x] Verify the runtime end to end after the workflow UX is connected.
- [x] Update documentation and implementation status for the workflow phase.

### Phase 8 — OneTrust and Governance Export Support

- [ ] Add CSV exports for inventory, findings, assessments, and risk acceptances.
- [ ] Add structured JSON governance exports.
- [ ] Add audit packet export.
- [ ] Draft OneTrust field mapping.
- [ ] Support manual OneTrust upload workflow.

### Phase 9 — Operational Maturity

- [ ] Add retest scheduling.
- [ ] Add improved reporting.
- [ ] Add optional notifications.
- [ ] Add better operator filters and saved views.
- [ ] Add operational health checks.

## Development Workflow

Future AI agents should:

1. Read `CLAUDE.md`, `AGENTS.md`, `CODEX.md`, and `docs/ai-context/current-state.md`.
2. Check `docs/ai-context/implementation-status.md` and `docs/ai-context/next-steps.md`.
3. Preserve the small-operator, single-VM, workflow-first philosophy.
4. Implement one narrow workflow at a time.
5. Update implementation status, todos, and README checklist boxes after completed verified work.
6. Avoid building additional real scanner integrations until the adapter framework and garak workflow remain stable.

## What To Build Next

The recommended next development task is Phase 8: governance exports and OneTrust workflow support.

## What Not To Build Yet

Do not build yet:

- Multiple real scanner integrations.
- OneTrust API integration.
- Kubernetes.
- Microservices.
- Enterprise SSO.
- Multi-tenant SaaS features.
- Complex distributed orchestration.
- A chatbot-first experience.

The strongest version of this project is operational, calm, audit-friendly, and simple enough to run.
