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

The backend container waits for PostgreSQL, runs `alembic upgrade head`, runs `python -m app.seed.run_seed` when `RUN_SEED=true`, and starts Uvicorn.

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

## Tests

```powershell
pytest
```
