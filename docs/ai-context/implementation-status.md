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
- Giskard adapter for hallucination, fairness/bias, prompt injection, RAG faithfulness, and business-rule validation execution against configured targets, installed in an isolated Docker runtime to avoid scanner dependency conflicts.
- PyRIT adapter for jailbreak, prompt injection, unsafe content, data exfiltration, and multi-turn adversarial execution against configured targets.
- Langfuse trace evidence manifest capture for scanner runs with graceful degradation when Langfuse credentials are unavailable.
- OpenControl-ready framework mappings and assessment export API.
- Human review states, assignments, approval history, comments, conditions, remediation workflow, and retest support.
- Executive dashboard and findings summaries.
- Deployment and local development documentation.

Partially implemented:

- Risk heatmaps and residual risk trends: score data exists, executive reporting needs stronger visualization and export support.
- Production deployment docs: Docker Compose guidance exists, hardening and runbooks need expansion.

Not implemented:

- PDF report generation.
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

- Scanner dependency footprints are large; Giskard runs from `/opt/giskard-venv` in Docker because current Giskard 2.x requires NumPy 1.x while garak 0.15 requires NumPy 2.x.
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

Latest local verification after scanner integration work:

- Backend tests: `43 passed`.
- Focused scanner tests: `17 passed`.
- Frontend lint, UI route test, and production build passed.
- Alembic static SQL generation through head passed.
- `docker compose config --quiet` passed.
- Docker Compose runtime validation passed on host ports 8400 and 3400 after Docker Desktop recovery.
- Runtime validation executed Giskard against a live target with preserved output and zero findings.
- Runtime validation executed PyRIT against a deliberately vulnerable live target and produced one real critical data-exfiltration finding with linked evidence.
- Runtime OpenControl export returned OpenControl, NIST AI RMF, and OWASP LLM controls linked to preserved evidence.

## Next

Next roadmap focus: reporting polish, residual-risk visualization, and production-readiness hardening.

## Blocked

- No current blockers.

## Intentionally Deferred

- PyRIT until Giskard integration is stable.
- Langfuse until scanner evidence flow is stable with Giskard and PyRIT.
- Distributed scanner runners.
- Kubernetes.
- Broad enterprise workflow features.
- One-off integrations that bypass the adapter and evidence model.
