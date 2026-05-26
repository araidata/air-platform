# Deployment Workflow

Phase 2.5 stabilizes the local and single-VM runtime around Docker Compose. The runtime is intentionally small:

```text
Browser
  -> frontend container (Next.js)
  -> backend container (FastAPI)
  -> postgres container (PostgreSQL)
```

## Local Development Startup

1. Copy the environment template:

```powershell
Copy-Item .env.example .env
```

2. Start the stack:

```powershell
docker compose up --build
```

3. Open the frontend:

```text
http://localhost:3000
```

4. Open the API:

```text
http://localhost:8000/health
http://localhost:8000/docs
```

If host ports are already in use, override only the published ports:

```powershell
$env:API_HOST_PORT="8010"
$env:FRONTEND_HOST_PORT="3010"
docker compose up --build
```

The backend still listens on `8000` inside Docker, and the frontend still listens on `3000` inside Docker.

## Startup Process

The backend container runs `apps/api/scripts/start.sh`:

1. Validate PostgreSQL connectivity.
2. Run `alembic upgrade head`.
3. Run the development bootstrap when `RUN_SEED=true`, or when `RUN_SEED` is unset and `ENVIRONMENT=development`.
4. Start FastAPI with Uvicorn.

The seed script is idempotent across Phase 2 inventory metadata, Phase 4 scanner ecosystem metadata, and Phase 6 civil-rights templates/checks. It also removes older seeded mock operational records. Startup logs identify each phase, records created, removed, and existing records skipped. If `RUN_SEED` is unset and `ENVIRONMENT` is not `development`, the bootstrap is skipped by default.

## Migration Workflow

Run migrations manually when needed:

```powershell
docker compose exec backend alembic upgrade head
docker compose exec backend alembic current
```

Create new migrations from `apps/api` during backend development:

```powershell
alembic revision --autogenerate -m "description"
```

Then verify the migration inside Docker before marking runtime work complete.

## Seed Workflow

Seed data loads automatically on backend startup in development mode. The bootstrap populates systems, owners, audit events, scanner definitions, scan types, assessment profiles, language-access scenarios, and appeal-path checks. It does not create assessments, findings, evidence, scanner runs, remediation records, or scores.

Run it manually:

```powershell
docker compose exec backend python -m app.seed.run_seed
```

Disable automatic seed loading:

```powershell
$env:RUN_SEED="false"
docker compose up
```

Intentionally seed outside development:

```powershell
$env:ENVIRONMENT="production"
$env:RUN_SEED="true"
docker compose up
```

## Reset And Reseed

Stop containers while preserving data:

```powershell
docker compose down
```

Reset the database volume and reload from migrations and seed:

```powershell
docker compose down -v
docker compose up --build
```

Only use `down -v` when intentionally deleting local runtime data.

## Smoke Testing

Run the smoke test from a Python container on the Compose network:

```powershell
docker run --rm --network air-platform_default -v "${PWD}:/work" -w /work python:3.12-slim python scripts/runtime-smoke-test.py --frontend-url http://frontend:3000 --backend-url http://backend:8000 --skip-docker
```

The smoke test verifies:

- Backend `/health`.
- Backend `/health/db`.
- Seeded `/systems`.
- Seeded `/findings`.
- Seeded `/evidence`.
- Seeded `/assessments`.
- Frontend dashboard load.
- Frontend/backend proxy through `/api/backend/health`.

## Single VM Production

1. Provision one Linux VM.
2. Install Docker and Docker Compose.
3. Copy the repository or release bundle.
4. Create `.env` from `.env.example`.
5. Set a non-default `POSTGRES_PASSWORD` and matching `DATABASE_URL`.
6. Start Compose.
7. Run migrations and seed only when intended.
8. Configure a reverse proxy and TLS later during deployment hardening.
9. Configure backups for PostgreSQL and evidence storage when evidence artifacts are added.
10. Verify health checks and smoke tests.

## Troubleshooting

- If `8000` or `3000` is already allocated, set `API_HOST_PORT` or `FRONTEND_HOST_PORT`.
- If the backend is unhealthy, inspect `docker compose logs backend`.
- If migrations fail, run `docker compose exec backend alembic current` and inspect the migration error.
- If seed data fails, run `docker compose exec backend python -m app.seed.run_seed` and inspect the traceback.
- If the frontend cannot reach the backend, check `NEXT_INTERNAL_API_URL` and test `/api/backend/health` from the frontend host.

## Deployment Guardrails

- Do not add Kubernetes, Helm, service mesh, or distributed workers for this phase.
- Do not add scanner execution containers until the adapter framework phase.
- Do not expose evidence artifact storage directly to the public internet.
- Do not store model provider API keys or production secrets in source control.
