# Backend Implementation Plan

## Stack

- FastAPI.
- PostgreSQL.
- SQLAlchemy 2.x.
- Pydantic schemas.
- Alembic migrations.

## Domain Modules

- Implemented in Phase 2: `systems`, `findings`, `evidence`, `assessments`, `owners`, `retests`, `airb`, `audit`, `framework_mappings`, and `risk_acceptances`.
- Planned for Phase 3: `scoring`.
- Deferred: `scanner_runs`, `deployment_approvals`, `reports`, and `integrations`.

## First Endpoints

- `GET /health`.
- `GET /systems`, `GET /systems/{id}`, `POST /systems`, `PATCH /systems/{id}`.
- `GET /assessments`, `GET /assessments/{id}`, `POST /assessments`, `PATCH /assessments/{id}`.
- `GET /findings`, `GET /findings/{id}`, `POST /findings`, `PATCH /findings/{id}`, `POST /findings/{id}/transition`.
- `GET /evidence`, `GET /evidence/{id}`, `POST /evidence`.
- `GET /audit-events`.
- `POST /findings/{id}/retest`, `GET /retests/{id}`, `PATCH /retests/{id}`.
- `GET /airb-reviews`, `POST /airb-reviews`, `PATCH /airb-reviews/{id}`.
- `GET /owners`, `POST /owners`.

## Services

- Finding workflow service.
- Assessment workflow service.
- Evidence service.
- Audit event service.
- Retest service.
- Scoring service next.
- Seed service.
- Scanner adapter service later.

## Migration And Seed Commands

From `apps/api`:

```powershell
py -m alembic upgrade head
py -m app.seed.run_seed
py -m pytest
```

The current automated tests use SQLite for speed. Live PostgreSQL smoke testing should be added with Docker Compose when the runtime exists.

## Backend Guardrails

- Do not put workflow logic directly in route handlers.
- Do not put scanner execution in route handlers.
- Do not calculate scores in the frontend.
- Do not lose raw evidence.
- Do not let scanner-specific data define the core data model.
