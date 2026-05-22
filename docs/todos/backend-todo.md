# Backend TODO

## Completed In Phase 2

- [x] Create FastAPI backend service under `apps/api`.
- [x] Add environment-driven database connection.
- [x] Implement systems API.
- [x] Implement findings API.
- [x] Implement evidence API.
- [x] Implement assessment API.
- [x] Implement AIRB review API.
- [x] Implement owners API.
- [x] Implement retest API.
- [x] Add audit event recording.
- [x] Add workflow services for findings, assessments, evidence, retests, and audit events.
- [x] Add seed command and backend tests.

## Completed In Phase 2.5

- [x] Add backend API container.
- [x] Add backend startup script.
- [x] Validate database connectivity before startup.
- [x] Run Alembic migrations during container startup.
- [x] Run idempotent seed data during container startup.
- [x] Add `/health/db` database health endpoint.
- [x] Add CORS environment configuration for local frontend access.

## Next

- Implement Phase 3 scoring service and score endpoints.
- Add pagination and filtering once UI integration needs are clearer.

## Deferred

- Enterprise auth.
- Complex permissions.
- Distributed jobs.
- Real scanner execution.
- OneTrust API calls.
