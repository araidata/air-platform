# Backend TODO

## Implemented

- [x] FastAPI service under `apps/api`.
- [x] Environment-driven database connection.
- [x] Health and database health endpoints.
- [x] SQLAlchemy models and Alembic migrations.
- [x] APIs for systems, assessments, findings, evidence, owners, retests, review records, scores, scanner metadata, scanner runs, and assessment-tool runs.
- [x] Service-layer workflows for assessments, findings, evidence, retests, audit events, scoring, and scanner execution.
- [x] Container startup with migration and development metadata seed.
- [x] garak adapter execution.
- [x] Live HTTP tester execution.

## Next

- [ ] Add Giskard adapter configuration and validation.
- [ ] Add Giskard execution path.
- [ ] Preserve Giskard raw output and reports as evidence.
- [ ] Normalize Giskard findings.
- [ ] Add Giskard parser and API tests.

## Later

- [ ] PyRIT adapter.
- [ ] Langfuse trace/evidence integration.
- [ ] OpenControl export APIs.
- [ ] PDF report generation.
- [ ] RBAC foundation.
- [ ] Structured logging and monitoring.
- [ ] Backup/restore support.
