# Backend Plan

The backend is a FastAPI service with PostgreSQL persistence.

## Domain Modules

- Systems.
- Assessments.
- Risk profiles and scoring.
- Scanner runs.
- Findings.
- Evidence.
- Review workflows.
- Reports and exports.
- Framework mappings.
- Audit events.

## API Expectations

- Stable OpenAPI documentation.
- Explicit schemas.
- Clear error responses.
- Pagination and filtering where list sizes require it.
- Service-layer business logic rather than route-level orchestration.

## Scanner Execution

Scanner execution should remain behind the scanner orchestration service. Adapters validate targets, execute external tools, preserve artifacts, and return normalized results for persistence by shared services.

## Reporting

Reporting APIs should read from assessment records, findings, evidence, score history, and review decisions. Export generation should not rely on hand-written summaries.
