# Backend Implementation Plan

## Stack

- FastAPI.
- PostgreSQL.
- SQLAlchemy 2.x.
- Pydantic schemas.
- Alembic migrations.

## Domain Modules

- Implemented in Phase 2: `systems`, `findings`, `evidence`, `assessments`, `owners`, `retests`, `airb`, `audit`, `framework_mappings`, and `risk_acceptances`.
- Implemented in Phase 3 code: `scoring`.
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
- `GET /scores`, `GET /scores/{id}`, `GET /scores/{id}/explanations`.
- `GET /systems/{id}/scores`, `GET /systems/{id}/score-history`.
- `POST /systems/{id}/recalculate-scores`, `POST /assessments/{id}/recalculate-scores`.

## Services

- Finding workflow service.
- Assessment workflow service.
- Evidence service.
- Audit event service.
- Retest service.
- Scoring engine and deterministic domain calculators.
- Seed service.
- Scanner adapter service later.

## Migration And Seed Commands

From `apps/api`:

```powershell
py -m alembic upgrade head
py -m app.seed.run_seed
py -m pytest
```

From the repository root in the Phase 2.5 Docker runtime:

```powershell
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.seed.run_seed
docker compose exec backend alembic current
```

The current automated tests use SQLite for speed. Live PostgreSQL runtime behavior is smoke-tested through Docker Compose.

## Backend Guardrails

- Do not put workflow logic directly in route handlers.
- Do not put scanner execution in route handlers.
- Do not calculate scores in the frontend.
- Do not lose raw evidence.
- Do not let scanner-specific data define the core data model.
