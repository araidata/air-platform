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

The repository is currently in Phase 0: documentation and AI-assistant operating structure. Application code has not been built yet.

Completed now:

- Repository context documentation.
- AI assistant rules for Claude, Codex, Cursor, Copilot, ChatGPT, and future coding agents.
- Architecture and scanner strategy docs.
- Findings, evidence, governance, integration, UI, todo, and ADR documentation.
- Claude Code command templates for future sessions.

Not built yet:

- Next.js application.
- Backend API.
- Database schema.
- Docker Compose runtime.
- Mock data seed scripts.
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

## Development Workflow

Future AI agents should:

1. Read `CLAUDE.md`, `AGENTS.md`, `CODEX.md`, and `docs/ai-context/current-state.md`.
2. Check `docs/ai-context/implementation-status.md` and `docs/ai-context/next-steps.md`.
3. Preserve the small-operator, single-VM, mock-first philosophy.
4. Implement one narrow workflow at a time.
5. Update implementation status and todos after meaningful changes.
6. Avoid building real scanner integrations until the adapter framework and mock workflow are stable.

## What To Build Next

The recommended next development task is Phase 1: create the first operational UI using mock data:

- Executive Dashboard.
- AI Inventory.
- Findings Queue.
- System Detail Page.
- Evidence & Audit Page.

This should be a usable front end with seeded mock data before backend persistence is introduced.

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
