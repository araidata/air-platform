# County AI Assurance API

FastAPI backend for Phase 2 findings, evidence, and assessment workflow plus the Phase 2.5 Docker runtime.

## Local Setup

```powershell
cd apps/api
py -m pip install -r requirements-dev.txt
```

Set `DATABASE_URL` for PostgreSQL:

```powershell
$env:DATABASE_URL="postgresql+psycopg://air_platform:air_platform@localhost:5432/air_platform"
```

## Migrations

```powershell
py -m alembic revision --autogenerate -m "phase 2 workflow tables"
py -m alembic upgrade head
```

The checked-in initial migration creates all Phase 2 workflow tables.

## Run

```powershell
uvicorn app.main:app --reload
```

## Docker Runtime

From the repository root:

```powershell
docker compose up --build
```

The backend container waits for PostgreSQL, runs `alembic upgrade head`, runs `python -m app.seed.run_seed` when `RUN_SEED=true` or when `RUN_SEED` is unset and `ENVIRONMENT=development`, and starts Uvicorn.

Useful runtime commands:

```powershell
docker compose exec backend alembic current
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.seed.run_seed
```

Health endpoints:

```text
GET /health
GET /health/db
```

## Seed Data

```powershell
py -m app.seed.run_seed
```

The seed command explicitly runs Phase 2 workflow data, Phase 4 scanner ecosystem data, and Phase 6 civil-rights data. It logs created and skipped existing record counts, is safe to rerun, and recalculates scores only when seeded records changed or required scores are missing.

## Tests

```powershell
pytest
```
