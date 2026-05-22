# API Standards

The platform is API-first. The UI should consume the same APIs that future integrations and reports use.

## General Standards

- JSON request and response bodies.
- OpenAPI generated from FastAPI.
- Stable resource-oriented paths.
- Pagination for list endpoints.
- Filtering and sorting for operational queues.
- Explicit error responses.
- Idempotent update patterns where practical.
- Audit events for workflow transitions.

## Naming

- Use plural nouns: `/systems`, `/findings`, `/evidence`.
- Use nested paths for strong ownership only: `/systems/{system_id}/findings`.
- Use action endpoints sparingly for workflow transitions: `/findings/{finding_id}/transition`.

## Errors

Error responses should include:

- Error code.
- Human-readable message.
- Field errors where applicable.
- Request ID.

## Pagination

List endpoints should support:

- `limit`.
- `offset` or cursor later.
- `sort`.
- `filter` parameters.

## Auditability

Endpoints that change workflow state should create audit events:

- Finding transitions.
- AIRB decisions.
- Deployment approvals.
- Risk acceptances.
- Evidence links.
- Score recalculations where manually triggered.
