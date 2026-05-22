# County AI Assurance API

FastAPI backend for Phase 2 findings, evidence, and assessment workflow.

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

## Seed Data

```powershell
py -m app.seed.run_seed
```

## Tests

```powershell
pytest
```
