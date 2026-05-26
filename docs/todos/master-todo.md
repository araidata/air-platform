# Master TODO

This backlog tracks capability work for AI Assessment Scanner.

## Core Platform Foundation

- [x] Docker runtime.
- [x] FastAPI backend.
- [x] PostgreSQL schema and migrations.
- [x] Next.js frontend.
- [x] OpenAPI documentation.
- [x] Core assessment, finding, evidence, scanner run, score, and review models.

## AI Risk Profiling

- [x] Assessment intake workflow.
- [x] Deterministic risk scoring.
- [x] Risk tier calculation.
- [x] NIST AI RMF mapping records.
- [x] OWASP LLM Top 10 mapping records.
- [ ] OpenControl-ready export mappings.

## Scanner Orchestration

- [x] Scanner adapter contract.
- [x] Scanner plugin architecture.
- [x] Assessment execution workflow.
- [x] Scanner run tracking.
- [x] Findings normalization.
- [x] Evidence linkage.
- [x] garak adapter.
- [x] Live HTTP assessment tester.

## Giskard Integration

- [ ] Giskard adapter.
- [ ] Hallucination testing.
- [ ] Bias/fairness testing.
- [ ] Prompt injection testing.
- [ ] RAG faithfulness testing.
- [ ] Business rule validation.

## PyRIT Integration

- [ ] PyRIT adapter.
- [ ] Jailbreak testing.
- [ ] Prompt injection attacks.
- [ ] Unsafe content testing.
- [ ] Data exfiltration testing.
- [ ] Multi-turn adversarial testing.

## Langfuse Evidence Pipeline

- [ ] Langfuse integration.
- [ ] Trace capture.
- [ ] Prompt/output logging.
- [ ] Latency/cost metrics.
- [ ] Evidence pipeline.
- [ ] Observability support.

## Human Review Workflows

- [x] Workflow states.
- [x] Reviewer assignments.
- [x] Approval history.
- [x] Remediation workflow.
- [x] Review comments.
- [x] Conditions tracking.

## Executive Reporting

- [x] Executive dashboard.
- [ ] Risk heatmaps.
- [x] Findings summaries.
- [ ] Residual risk trends.
- [ ] PDF report generation.
- [ ] OpenControl export.

## Production Readiness

- [ ] RBAC foundation.
- [x] Production deployment docs.
- [ ] Logging/monitoring.
- [ ] Backup/recovery guidance.
- [ ] Security hardening.
- [ ] Performance optimization.

## Documentation

- [x] Refactor docs to the AI Assessment Scanner direction.
- [x] Remove obsolete implementation-history scanner docs.
- [x] Consolidate roadmap around the current phase structure.
- [ ] Add production backup/restore runbook.
- [ ] Add OpenControl export field mapping once implemented.
