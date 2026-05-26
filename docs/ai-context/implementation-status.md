# Implementation Status

Update this file whenever repository capability meaningfully changes.

## Capability Summary

Implemented:

- Docker Compose runtime for frontend, backend, and PostgreSQL.
- FastAPI backend with migration startup and health checks.
- PostgreSQL schema for core assessment records.
- Next.js frontend with API-backed operational workflows.
- Core assessment, finding, evidence, scanner run, score, and review models.
- OpenAPI documentation through FastAPI.
- Deterministic risk scoring and risk tier calculation.
- NIST AI RMF and OWASP LLM-oriented framework mapping records.
- Scanner orchestration framework and adapter contract.
- Scanner run tracking, artifact capture, finding normalization, and evidence linkage.
- garak CLI adapter and Live HTTP assessment tester.
- Human review states, assignments, approval history, comments, conditions, remediation workflow, and retest support.
- Executive dashboard and findings summaries.
- Deployment and local development documentation.

Partially implemented:

- OpenControl mappings: data model support exists, export is not implemented.
- Risk heatmaps and residual risk trends: score data exists, executive reporting needs stronger visualization and export support.
- Production deployment docs: Docker Compose guidance exists, hardening and runbooks need expansion.

Not implemented:

- Giskard adapter.
- PyRIT adapter.
- Langfuse integration.
- PDF report generation.
- OpenControl / Compliance Masonry export.
- RBAC foundation.
- Logging/monitoring package.
- Backup/recovery automation.
- Production security hardening checklist.

## Operational Maturity

Current maturity:

- Local and single-VM runtime: usable.
- Assessment intake: usable.
- Automated testing: usable for garak and live HTTP tester only.
- Evidence preservation: implemented for scanner artifacts and workflow-linked records.
- Findings workflow: usable.
- Review workflow: usable.
- Executive reporting: basic dashboard and summaries only.
- Production readiness: incomplete.

## Known Limitations

- garak is the only external scanner adapter currently implemented.
- Giskard, PyRIT, and Langfuse are roadmap targets, not active integrations.
- Scanner execution is local and synchronous.
- No production RBAC or enterprise SSO.
- No backup/restore automation.
- No OpenControl export yet.
- No generated PDF executive report yet.

## Verification Snapshot

Most recent documented verification includes:

- Backend pytest suite passing after garak/live HTTP assessment workbench changes.
- Frontend tests, lint, and build passing after assessment workbench changes.
- `docker compose config --quiet`.
- Docker Compose runtime smoke test passing with backend, frontend, PostgreSQL, migrations, seed metadata, and API proxy checks.
- Runtime live HTTP tester execution producing a real finding with report artifact and redacted authorization metadata.
- Runtime garak execution producing native artifacts and assessment report artifact.

Run current verification again before marking new implementation work complete.

## Next

Begin Giskard integration.

Initial scope:

- Add Giskard adapter configuration and validation.
- Execute a minimal local Giskard test path through the existing scanner run service.
- Preserve raw Giskard output as evidence.
- Normalize results into the existing Finding model.
- Add fixture and API coverage for success and failure paths.

## Blocked

- No current blockers.

## Intentionally Deferred

- PyRIT until Giskard integration is stable.
- Langfuse until scanner evidence flow is stable with Giskard and PyRIT.
- Distributed scanner runners.
- Kubernetes.
- Broad enterprise workflow features.
- One-off integrations that bypass the adapter and evidence model.
