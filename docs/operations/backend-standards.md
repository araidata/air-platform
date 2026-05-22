# Backend Standards

## Framework

- FastAPI.
- Pydantic.
- PostgreSQL.
- Redis.

## Route Design

- Thin route handlers.
- Service layer for business logic.
- Consistent response models.
- OpenAPI documentation.

## Workflow Rules

- Workflow transitions must be validated.
- Workflow transitions must create audit events.
- Blocking decisions require rationale.
- Exceptions require expiration or explicit no-expiration rationale.

## Scanner Rules

- Scanner execution belongs in scanner orchestration services.
- Scanner output must be preserved before normalization.
- Scanner failure must create visible run status.

## Security Rules

- Never log secrets.
- Treat evidence as potentially sensitive.
- Avoid exposing raw evidence publicly.
- Add authorization before production exposure.
