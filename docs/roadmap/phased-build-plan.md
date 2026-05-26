# Phased Build Plan

This is the canonical roadmap for AI Assessment Scanner. The phase checklist in `README.md` is the implementation tracking surface; this file adds intent and acceptance criteria.

## Phase 1 - Core Platform Foundation

Goal: provide a runnable local platform with stable API, database, and frontend foundations.

Scope:

- Docker Compose runtime.
- FastAPI backend.
- PostgreSQL schema and migrations.
- Next.js + TypeScript frontend.
- OpenAPI documentation.
- Core models for systems, assessments, findings, evidence, scanner runs, scores, and reviews.

Acceptance criteria:

- Stack starts with `docker compose up --build`.
- Migrations run cleanly.
- Frontend can reach backend through the configured proxy.
- Smoke test validates backend, database, frontend, and seed metadata.

## Phase 2 - AI Risk Profiling

Goal: produce deterministic, explainable risk profiles from assessment intake, system attributes, findings, and framework mappings.

Scope:

- Assessment intake workflow.
- Risk tier calculation.
- Deterministic score rules.
- NIST AI RMF mappings.
- OWASP LLM Top 10 mappings.
- OpenControl-ready mapping structure.

Acceptance criteria:

- Risk profile can be calculated and explained for an AI system.
- Score changes can be traced to findings, evidence gaps, or workflow status.
- Framework mappings can be attached to findings and reports.

## Phase 3 - Scanner Orchestration

Goal: run external scanners through a safe adapter model and preserve results as evidence.

Scope:

- Scanner adapter contract.
- Scanner plugin architecture.
- Scanner run tracking.
- Assessment execution workflow.
- Raw artifact capture.
- Findings normalization.
- Evidence linkage.

Acceptance criteria:

- Scanner runs have status, timestamps, adapter metadata, raw artifacts, and linked results.
- Parser failures preserve evidence and produce visible run failures.
- Normalized findings use the shared Finding model.

## Phase 4 - Giskard Integration

Goal: add Giskard as the first broad AI evaluation adapter.

Scope:

- Giskard adapter.
- Hallucination testing.
- Bias/fairness testing.
- Prompt injection testing.
- RAG faithfulness testing.
- Business rule validation.

Acceptance criteria:

- Giskard execution runs through the scanner orchestration service.
- Raw Giskard outputs are preserved.
- Findings map to existing risk profile and evidence workflows.
- Tests cover success, no-finding, invalid target, execution failure, and parser failure.

## Phase 5 - PyRIT Integration

Goal: add adversarial testing for deeper red-team scenarios.

Scope:

- PyRIT adapter.
- Jailbreak testing.
- Prompt injection attacks.
- Unsafe content testing.
- Data exfiltration testing.
- Multi-turn adversarial testing.

Acceptance criteria:

- PyRIT runs produce preserved evidence and normalized findings.
- Multi-turn test evidence is linked to scanner runs and findings.
- Safety-sensitive outputs are handled with appropriate sensitivity metadata.

## Phase 6 - Langfuse Evidence Pipeline

Goal: connect traces and observability data to assessment evidence.

Scope:

- Langfuse integration.
- Trace capture.
- Prompt/output logging.
- Latency/cost metrics.
- Evidence pipeline.
- Observability support.

Acceptance criteria:

- Trace references can be linked to assessments, findings, and reports.
- Prompt/output evidence is retained with sensitivity metadata.
- Latency and cost metrics can support executive reporting.

## Phase 7 - Human Review Workflows

Goal: support human decisions after automated testing.

Scope:

- Workflow states.
- Reviewer assignments.
- Approval history.
- Remediation workflow.
- Review comments.
- Conditions tracking.

Acceptance criteria:

- Review decisions are auditable.
- Conditions and exceptions have owners, notes, and dates.
- Findings can move through remediation and retest workflows.

## Phase 8 - Executive Reporting

Goal: convert assessment records into leadership-ready reporting.

Scope:

- Executive dashboard.
- Risk heatmaps.
- Findings summaries.
- Residual risk trends.
- PDF report generation.
- OpenControl export.

Acceptance criteria:

- Reports draw from real assessment, finding, evidence, and score records.
- Export output is reproducible.
- Executive views avoid fabricated demo metrics.

## Phase 9 - Production Readiness

Goal: prepare the platform for county production operation.

Scope:

- RBAC foundation.
- Production deployment docs.
- Logging/monitoring.
- Backup/recovery guidance.
- Security hardening.
- Performance optimization.

Acceptance criteria:

- Operators have deployment and recovery runbooks.
- Access control is sufficient for internal production use.
- Logs and health checks support troubleshooting.
- Backup and restore paths are documented and tested.
