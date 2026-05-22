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

The repository has completed Phase 2: Findings, Evidence, and Assessment Workflow. A Next.js frontend scaffold exists under `apps/web`, and a FastAPI backend now exists under `apps/api` with SQLAlchemy models, Alembic migrations, workflow services, seed data, and tests for the core assurance records.

Completed now:

- Repository context documentation.
- AI assistant rules for Claude, Codex, Cursor, Copilot, ChatGPT, and future coding agents.
- Architecture and scanner strategy docs.
- Findings, evidence, governance, integration, UI, todo, and ADR documentation.
- Claude Code command templates for future sessions.
- Next.js frontend scaffold and mock operations-center pages.
- FastAPI backend scaffold under `apps/api`.
- SQLAlchemy models and Alembic migration for systems, assessments, findings, evidence, owners, retests, AIRB reviews, framework mappings, risk acceptances, and audit events.
- REST endpoints for systems, assessments, findings, evidence, audit events, retests, AIRB reviews, and owners.
- Workflow services enforcing finding and assessment transitions with audit logging.
- Phase 2 seed data matching the mock county AI systems.
- Basic backend tests for model creation, lifecycle transitions, evidence creation, retests, audit events, and API smoke flows.

Not built yet:

- Docker Compose runtime.
- Scanner adapter code.
- Real scanner integrations.
- OneTrust integration.

## Why Mock-First

The platform must prove that it can receive, explain, route, score, and preserve findings before real scanners are integrated. Mock systems, mock findings, mock evidence, and mock scan results allow the operating workflow to stabilize first.

Start with seeded data for:

- Public Benefits Chatbot.
- Sheriff Incident Summary Assistant.
- Permit Review Assistant.
- HR Resume Screening AI.
- Citizen Services RAG Chatbot.

Start with mock findings such as:

- Prompt injection vulnerability.
- Spanish-language explanation disparity.
- Missing human appeal path.
- Excessive MCP/tool permissions.
- Incomplete audit logging.
- Possible sensitive data leakage.
- Weak governance evidence.
- Missing risk acceptance.
- Missing retest documentation.

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

## Phase Plan

See [Phased Build Plan](docs/roadmap/phased-build-plan.md) for details.

- Phase 0: Repository and AI Context Foundation.
- Phase 1: Operational UI and Mock Data.
- Phase 2: Findings, Evidence, and Assessment Workflow.
- Phase 3: Scoring Engine.
- Phase 4: Scanner Adapter Framework.
- Phase 5: First Real Scanner Integration.
- Phase 6: Bias and Civil Rights Assessment Support.
- Phase 7: OneTrust and Governance Export Support.
- Phase 8: Operational Maturity.

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

### Phase 1 — Operational UI and Mock Data

- [x] Create the frontend application scaffold.
- [x] Add centralized mock data for systems, assessments, findings, evidence, scores, and reviews.
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

### Phase 3 — Scoring Engine

- [ ] Implement explainable domain scoring.
- [ ] Calculate score impact from findings.
- [ ] Show score history and score explanations.
- [ ] Connect scoring to system, assessment, finding, and governance views.

### Phase 4 — Scanner Adapter Framework

- [ ] Implement scanner adapter interface.
- [ ] Implement mock scanner adapter.
- [ ] Create scanner run records.
- [ ] Capture raw output and logs as evidence.
- [ ] Normalize mock scanner output into findings.

### Phase 5 — First Real Scanner Integration

- [ ] Select first real scanner, likely garak or AgentSeal.
- [ ] Run the scanner through Docker or CLI adapter execution.
- [ ] Parse scanner output.
- [ ] Preserve raw scanner evidence.
- [ ] Create normalized findings from scanner results.

### Phase 6 — Bias and Civil Rights Assessment Support

- [ ] Add bias and civil-rights assessment templates.
- [ ] Add language access scenarios.
- [ ] Add human appeal path checks.
- [ ] Add fairness-oriented findings and evidence views.

### Phase 7 — OneTrust and Governance Export Support

- [ ] Add CSV exports for inventory, findings, assessments, and risk acceptances.
- [ ] Add structured JSON governance exports.
- [ ] Add audit packet export.
- [ ] Draft OneTrust field mapping.
- [ ] Support manual OneTrust upload workflow.

### Phase 8 — Operational Maturity

- [ ] Add retest scheduling.
- [ ] Add improved reporting.
- [ ] Add optional notifications.
- [ ] Add better operator filters and saved views.
- [ ] Add operational health checks.

## Development Workflow

Future AI agents should:

1. Read `CLAUDE.md`, `AGENTS.md`, `CODEX.md`, and `docs/ai-context/current-state.md`.
2. Check `docs/ai-context/implementation-status.md` and `docs/ai-context/next-steps.md`.
3. Preserve the small-operator, single-VM, mock-first philosophy.
4. Implement one narrow workflow at a time.
5. Update implementation status, todos, and README checklist boxes after completed verified work.
6. Avoid building real scanner integrations until the adapter framework and mock workflow are stable.

## What To Build Next

The recommended next development task is Phase 3: implement the explainable scoring engine that derives domain and overall scores from systems, assessments, findings, evidence completeness, retest outcomes, and risk acceptances.

## What Not To Build Yet

Do not build yet:

- Real scanner integrations.
- OneTrust API integration.
- Kubernetes.
- Microservices.
- Enterprise SSO.
- Multi-tenant SaaS features.
- Complex distributed orchestration.
- A chatbot-first experience.

The strongest version of this project is operational, calm, audit-friendly, and simple enough to run.
