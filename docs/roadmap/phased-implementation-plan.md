# Phased Implementation Plan

This roadmap uses implementation phases, not calendar dates. The platform should advance when the prior phase has enough operational value and validation.

## Phase 0 - Infrastructure Foundation

### Objectives

- Establish repository layout.
- Create Docker Compose baseline.
- Create FastAPI service skeleton.
- Create Next.js service skeleton.
- Create PostgreSQL and Redis containers.
- Create seed data framework.
- Define core database migrations.

### Rationale

The first goal is a running platform that future work can extend consistently.

### Dependencies

- Approved technology stack.
- Initial data model.
- Local development workflow.

### Deliverables

- `apps/web` skeleton.
- `apps/api` skeleton.
- Docker Compose file.
- Database migration setup.
- Seed command.
- Health check endpoints.
- Environment variable template.

### Operational Outcomes

- A developer can boot the platform locally.
- Operators can see seeded data once UI exists.

### Implementation Risks

- Overbuilding infrastructure before workflows exist.
- Letting deployment decisions drive product design too early.

### Intentionally Waits Until Later

- Real scanner execution.
- Enterprise authentication.
- Production reporting.
- Integrations.

### Should Not Yet Be Built

- Kubernetes.
- Distributed workers.
- Complex CI/CD.
- Cloud deployment abstraction.

## Phase 1 - Operational UI And Inventory

### Objectives

- Build AI inventory.
- Build executive dashboard shell.
- Build system detail page.
- Seed initial county AI systems.
- Capture risk tier and approval status.

### Rationale

Inventory is the foundation of governance. No assurance workflow can work without knowing what systems exist and who owns them.

### Dependencies

- Phase 0 foundation.
- System data model.
- Seed data plan.

### Deliverables

- AI Inventory page.
- System Detail page.
- Executive Dashboard with seeded metrics.
- System create/edit forms.
- Department owner tracking.
- Risk tier labels.
- Approval status labels.

### Operational Outcomes

- Operators can maintain an authoritative AI inventory.
- Executives can see a basic governance posture.

### Implementation Risks

- Treating inventory as a generic asset list instead of a governance record.
- Under-modeling rights-impacting and safety-impacting properties.

### Intentionally Waits Until Later

- Scanner runs.
- Evidence upload sophistication.
- Advanced scoring.

### Should Not Yet Be Built

- Live telemetry.
- Automatic system discovery.
- External CMDB synchronization.

## Phase 2 - Findings And Governance Workflows

### Objectives

- Build normalized findings model.
- Build Findings Queue.
- Build finding detail and workflow transitions.
- Seed mock findings.
- Add remediation ownership and SLA fields.
- Add framework mapping fields.

### Rationale

Findings are the operational center of the platform. Scanner integrations are not useful until findings can be triaged, assigned, remediated, retested, accepted, or escalated.

### Dependencies

- System inventory.
- Normalized findings schema.
- Workflow status model.

### Deliverables

- Findings Queue.
- Finding Detail page.
- Status transitions.
- Owner assignment.
- Remediation text fields.
- SLA due dates.
- Retest history shell.
- Mock findings for security, bias, privacy, and governance.

### Operational Outcomes

- Operators can run realistic governance drills using mock data.
- Departments can understand assigned remediation work.

### Implementation Risks

- Allowing scanner-specific fields to leak into core finding models.
- Creating too many statuses before real operations validate them.

### Intentionally Waits Until Later

- Real scanner adapters.
- Automated retesting.
- ServiceNow or Jira synchronization.

### Should Not Yet Be Built

- Autonomous remediation.
- Complex escalation automation.

## Phase 2.5 — Runtime Stabilization

### Objectives

- Add the Docker Compose runtime that matches the single-VM deployment model.
- Containerize the FastAPI backend and Next.js frontend.
- Run PostgreSQL as the primary runtime database with persistent storage.
- Execute Alembic migrations and seed data during backend startup.
- Validate frontend, backend, database, migration, seed, and API connectivity.

### Rationale

The workflow backend and mock frontend need to run as one platform before scoring, scanner adapters, or export workflows are added.

### Dependencies

- Phase 2 backend models, migrations, routes, and seed data.
- Existing Next.js frontend scaffold.
- Docker and Docker Compose on the operator machine or VM.

### Deliverables

- `docker-compose.yml`.
- Backend and frontend Dockerfiles.
- `.env.example`.
- PostgreSQL named volume.
- Health endpoints and practical container health checks.
- Runtime smoke test.
- Updated deployment and startup documentation.

### Operational Outcomes

- A new developer can copy `.env.example` to `.env`, run `docker compose up`, and access the seeded platform.
- Backend startup waits for PostgreSQL, runs migrations, loads seed data, and starts FastAPI.
- Frontend reaches the backend through a same-origin proxy.
- PostgreSQL data persists across container restart when volumes are preserved.

### Implementation Risks

- Host port conflicts on developer machines.
- Treating this phase as production hardening instead of runtime stabilization.

### Intentionally Waits Until Later

- Scanner execution containers.
- Redis and background jobs.
- Production TLS/reverse proxy hardening.
- Backup automation.
- Enterprise authentication.

### Should Not Yet Be Built

- Kubernetes.
- Helm.
- Service mesh.
- Distributed workers.
- Cloud infrastructure modules.

## Phase 3 - Scoring And Evidence System

### Objectives

- Build evidence metadata model.
- Build Evidence and Audit page.
- Implement score calculation for security, privacy, bias/civil rights, explainability, and governance evidence.
- Add score explanations.
- Attach evidence to findings and AIRB decisions.

### Rationale

County leadership needs defensible scores and preserved evidence, not opaque AI ratings.

### Dependencies

- Findings workflow.
- Evidence model.
- Scoring methodology.

### Deliverables

- Evidence artifact records.
- Evidence custody events.
- Evidence page.
- Initial scoring service.
- Score contribution breakdowns.
- Score trend storage.
- Governance evidence score.

### Operational Outcomes

- Operators can explain why a score changed.
- Reviewers can inspect evidence behind a decision.

### Implementation Risks

- Building scores that appear precise but are not explainable.
- Treating evidence as casual file attachments.

### Intentionally Waits Until Later

- Object storage.
- External evidence synchronization.
- Advanced analytics.

### Should Not Yet Be Built

- Black-box machine learning risk scoring.
- Real-time scoring streams.

## Phase 4 - Scanner Integration Framework

### Objectives

- Build scanner adapter interface.
- Build scanner run records.
- Build Dockerized scanner execution model.
- Build raw result storage.
- Build normalization pipeline.
- Build mock adapter fixtures.

### Rationale

The platform must orchestrate scanners without becoming dependent on scanner internals.

### Dependencies

- Findings schema.
- Evidence system.
- Assessment run model.
- Docker execution baseline.

### Deliverables

- Adapter contract.
- Scanner registry.
- Execution wrapper.
- Result normalizer interface.
- Raw output evidence capture.
- Mock scanner adapter.
- CLI-first execution documentation.

### Operational Outcomes

- Developers can add scanner integrations consistently.
- Operators can see assessment run history even before production scanner tools are enabled.

### Implementation Risks

- Binding too tightly to scanner-specific Python APIs.
- Treating scanner containers as independent production services.

### Intentionally Waits Until Later

- Real scanners.
- Scheduled scans.
- Parallel execution tuning.

### Should Not Yet Be Built

- Scanner microservices.
- Kubernetes job controller.
- Long-running distributed worker fleet.

## Phase 5 - Real Scanner Integrations

### Objectives

- Integrate first security scanner.
- Integrate first bias/fairness scanner.
- Integrate first LLM/RAG evaluation scanner.
- Normalize real outputs.
- Validate evidence capture.

### Rationale

Once workflows, evidence, and scoring exist, real scanner data can enter a governed operating model.

### Dependencies

- Adapter framework.
- Test fixtures.
- Normalization schema.
- Evidence preservation.

### Deliverables

- Initial garak or PyRIT adapter.
- Initial Fairlearn or Aequitas adapter.
- Initial Promptfoo, Ragas, or DeepEval adapter.
- Scanner run UI.
- Scanner result import tests.
- Failure handling.

### Operational Outcomes

- Operators can execute real assessments and manage resulting findings.

### Implementation Risks

- Tool output instability.
- Environment drift in scanner containers.
- False positives without review context.

### Intentionally Waits Until Later

- Broad scanner catalog.
- Automatic scheduling.
- Model provider deep integrations.

### Should Not Yet Be Built

- Autonomous red teaming.
- Continuous production monitoring.

## Phase 6 - Operational Maturity And Automation

### Objectives

- Add reporting workflows.
- Add scheduled assessment plans.
- Add integration readiness for Jira, ServiceNow, OneTrust, Teams, and email.
- Add operational metrics.
- Mature access control.
- Harden deployment.

### Rationale

Automation should follow a stable operational model, not define it prematurely.

### Dependencies

- Proven manual workflows.
- Evidence and scoring stability.
- Initial scanner integrations.

### Deliverables

- Governance reports.
- Scheduled assessment plans.
- Notification rules.
- External workflow export or sync.
- Role-based access model.
- Backup and restore guide.
- Production runbooks.

### Operational Outcomes

- The county can operate AI assurance as a repeatable governance function.

### Implementation Risks

- Automating poor workflows.
- Creating fragile external dependencies.

### Intentionally Waits Until Later

- Advanced observability.
- MLflow or Langfuse integration.
- OpenTelemetry pipeline.

### Should Not Yet Be Built

- Multi-tenant SaaS capabilities.
- Hyperscale analytics platform.
- Fully autonomous approval decisions.
