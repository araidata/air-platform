# AI Assessment Scanner

AI Assessment Scanner is an internal county platform for AI risk assessment, automated testing, evidence collection, human review, and executive reporting.

It is not a chatbot platform, SOC/SIEM, generic AI governance suite, or scanner engine. The platform orchestrates assessments, preserves evidence, normalizes findings, supports review workflows, and produces reports that county leadership and security teams can use.

## Project Overview

The platform is assessment-first, testing-first, and evidence-first.

Primary goals:

- Identify and profile AI risk before and during deployment.
- Run automated tests against AI systems, prompts, models, and AI-enabled workflows.
- Preserve raw assessment evidence and scanner artifacts.
- Normalize findings into a consistent workflow.
- Support human review and remediation decisions.
- Produce executive reports and OpenControl-ready exports.

Governance exists in the platform, but it is lightweight and secondary to assessment execution, evidence quality, and operational reporting.

## Core Capabilities

- Automated risk profiling for county AI systems.
- Deterministic risk scoring with explainable factors.
- Giskard integration target for hallucination, bias/fairness, prompt injection, RAG faithfulness, and business-rule validation.
- PyRIT integration target for jailbreak, prompt injection, unsafe content, data exfiltration, and multi-turn adversarial testing.
- garak-based prompt injection testing already integrated through the scanner adapter path.
- Langfuse evidence and tracing target for prompt/output capture, trace metadata, latency, and cost signals.
- Findings management with severity, status, ownership, remediation, retest, and score impact.
- Evidence collection for raw scanner output, logs, prompts, responses, reports, uploads, and review notes.
- Human review workflows for assessment decisions, remediation, approvals, exceptions, and conditions.
- Executive reporting for risk posture, trends, heatmaps, findings summaries, and assessment outcomes.
- OpenControl / Compliance Masonry export target for control-oriented reporting.

## Architecture Overview

Runtime architecture:

- Frontend: Next.js + TypeScript operational UI.
- Backend: FastAPI API service.
- Database: PostgreSQL.
- Scanner orchestration: adapter-driven execution of external tools such as garak, Giskard, PyRIT, and future scanners.
- Evidence pipeline: raw artifacts are written to scanner/evidence storage and referenced from PostgreSQL records.
- Reporting pipeline: normalized systems, assessments, findings, evidence, scores, and workflow records feed dashboards, PDF reports, and OpenControl exports.

The platform is designed for one Linux VM with Docker Compose and one or two operators. Do not introduce Kubernetes, distributed workers, or microservices unless the project direction explicitly changes.

## Quick Start

1. Copy the environment template.

```powershell
Copy-Item .env.example .env
```

2. Start the Docker Compose stack.

```powershell
docker compose up --build
```

3. Open the application.

```text
Frontend: http://localhost:3000
Backend health: http://localhost:8000/health
API docs: http://localhost:8000/docs
```

4. If local ports are already in use, override only the host ports.

```powershell
$env:API_HOST_PORT="8010"
$env:FRONTEND_HOST_PORT="3010"
docker compose up --build
```

## Environment Variables

Use `.env.example` as the source of truth for local configuration.

Key settings:

- `DATABASE_URL`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `API_HOST_PORT`
- `FRONTEND_HOST_PORT`
- `ENVIRONMENT`
- `RUN_SEED`
- `SCANNER_STORAGE_ROOT`
- `NEXT_PUBLIC_API_URL`
- `NEXT_INTERNAL_API_URL`

Production deployments must set non-default database credentials, configure backup paths, protect scanner/evidence storage, and terminate TLS through a reverse proxy or equivalent platform control.

## Development Workflow

Standard runtime:

```powershell
docker compose up --build
```

Backend tasks:

```powershell
docker compose exec backend alembic current
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.seed.run_seed
```

Frontend changes normally hot reload through the Compose frontend service. If package dependencies or build configuration change, rebuild the frontend container:

```powershell
docker compose build frontend
docker compose up frontend
```

Backend code changes reload in development mode. If dependencies, migrations, or scanner runtime packages change, rebuild the backend container:

```powershell
docker compose build backend
docker compose up backend
```

Run the runtime smoke test after meaningful integration changes:

```powershell
py scripts/runtime-smoke-test.py --backend-url http://localhost:8000 --frontend-url http://localhost:3000
```

## Real vs Demo Mode

Real scanner execution means an adapter validates a target, invokes an external scanner or tester, preserves raw artifacts, normalizes findings, links evidence, and updates assessment records.

Current real execution:

- garak CLI adapter.
- Live HTTP assessment tester.
- Raw artifact preservation under the configured scanner storage root.
- Normalized findings, evidence records, audit events, and score recalculation.

Optional demo/testing mode means development metadata can be seeded so the UI has systems, scanner definitions, assessment profiles, and review templates. Demo metadata must not fabricate completed assessments, findings, evidence, scanner runs, remediation records, or score impacts.

Operational expectation: production records should come from real intake, real scanner runs, uploaded evidence, or human review actions.

## Roadmap Checklist

This checklist is maintained manually. Mark a task complete only after implementation is verified and reflected in `docs/ai-context/implementation-status.md` plus the relevant todo file.

### Core Platform Foundation

- [x] Docker runtime
- [x] FastAPI backend
- [x] PostgreSQL schema
- [x] Next.js frontend
- [x] API documentation
- [x] Core assessment models

### AI Risk Profiling

- [x] Assessment intake workflow
- [x] Deterministic risk scoring
- [x] NIST AI RMF mapping
- [x] OWASP LLM Top 10 mapping
- [ ] OpenControl mappings
- [x] Risk tier calculation

### Scanner Orchestration

- [x] Scanner orchestration framework
- [x] Scanner plugin architecture
- [x] Assessment execution workflow
- [x] Scanner run tracking
- [x] Findings normalization
- [x] Evidence linkage

### Giskard Integration

- [ ] Giskard adapter
- [ ] Hallucination testing
- [ ] Bias/fairness testing
- [ ] Prompt injection testing
- [ ] RAG faithfulness testing
- [ ] Business rule validation

### PyRIT Integration

- [ ] PyRIT adapter
- [ ] Jailbreak testing
- [ ] Prompt injection attacks
- [ ] Unsafe content testing
- [ ] Data exfiltration testing
- [ ] Multi-turn adversarial testing

### Langfuse Evidence Pipeline

- [ ] Langfuse integration
- [ ] Trace capture
- [ ] Prompt/output logging
- [ ] Latency/cost metrics
- [ ] Evidence pipeline
- [ ] Observability support

### Human Review Workflows

- [x] Workflow states
- [x] Reviewer assignments
- [x] Approval history
- [x] Remediation workflow
- [x] Review comments
- [x] Conditions tracking

### Executive Reporting

- [x] Executive dashboard
- [ ] Risk heatmaps
- [x] Findings summaries
- [ ] Residual risk trends
- [ ] PDF report generation
- [ ] OpenControl export

### Production Readiness

- [ ] RBAC foundation
- [x] Production deployment docs
- [ ] Logging/monitoring
- [ ] Backup/recovery guidance
- [ ] Security hardening
- [ ] Performance optimization

## Documentation Map

- Current state: `docs/ai-context/current-state.md`
- AI engineering direction: `docs/ai-engineering/project-direction.md`
- Implementation status: `docs/ai-context/implementation-status.md`
- Next steps: `docs/ai-context/next-steps.md`
- Architecture: `docs/architecture/architecture-overview.md`
- Deployment: `docs/deployment/deployment-workflow.md`
- Scanner adapters: `docs/scanners/adapter-contract.md`
- Roadmap: README roadmap checklist and `docs/ai-context/next-steps.md`

## Build Guardrails

- Keep the system realistic for one Linux VM and Docker Compose.
- Keep findings and evidence central.
- Treat scanners as external tools.
- Preserve raw scanner output and logs.
- Prefer adapters over direct scanner coupling.
- Keep demo data clearly separate from operational records.
- Avoid Kubernetes, distributed queues, scanner microservices, and enterprise-scale workflow assumptions until production needs justify them.
