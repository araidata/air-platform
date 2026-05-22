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

- Begin Phase 6 bias and civil-rights workflow support.
- Add pagination and filtering once UI integration needs are clearer.

## Completed In Phase 3

- [x] Added deterministic scoring engine and domain calculators.
- [x] Added score APIs and recalculation endpoints.
- [x] Added service-layer score recalculation hooks for workflow changes.
- [x] Added backend scoring tests.

## Completed In Phase 4

- [x] Added scanner registry, scan type, assessment profile, scanner run, and scanner result models.
- [x] Added scanner ecosystem Alembic migration.
- [x] Added scanner adapter contract and deterministic mock adapter.
- [x] Added scanner execution service and normalization layer.
- [x] Added scanner APIs and recommendation endpoints.
- [x] Added raw output and log preservation as evidence.
- [x] Added score recalculation through scanner-created findings.
- [x] Added scanner tests.

## Completed In Phase 5

- [x] Added garak CLI adapter as the first real scanner integration.
- [x] Added backend Docker scanner dependency installation.
- [x] Preserved native garak artifacts and normalized output as evidence.
- [x] Normalized garak output into findings and score recalculation.
- [x] Added real scanner execution, parser, malformed output, failure, evidence, and scoring tests.

## Deferred

- Enterprise auth.
- Complex permissions.
- Distributed jobs.
- Additional real scanner execution beyond garak.
- OneTrust API calls.
