# Deployment Workflow

This project targets a simple Docker Compose deployment.

## Local Development Startup

1. Copy the environment template.

```powershell
Copy-Item .env.example .env
```

2. Start the stack.

```powershell
docker compose up --build
```

3. Open the application.

```text
Frontend: http://localhost:3000
Backend health: http://localhost:8000/health
API docs: http://localhost:8000/docs
```

If host ports are already allocated:

```powershell
$env:API_HOST_PORT="8010"
$env:FRONTEND_HOST_PORT="3010"
$env:POSTGRES_PORT="55432"
docker compose up --build
```

## Migration Workflow

Run migrations inside Compose:

```powershell
docker compose exec backend alembic upgrade head
docker compose exec backend alembic current
```

Create migrations from `apps/api` during backend development:

```powershell
alembic revision --autogenerate -m "description"
```

Verify migrations in Docker before marking runtime work complete.

## Seed Workflow

Development metadata loads automatically when `ENVIRONMENT=development` and `RUN_SEED` is unset or true.

Run seed manually:

```powershell
docker compose exec backend python -m app.seed.run_seed
```

Disable automatic seed loading:

```powershell
$env:RUN_SEED="false"
docker compose up
```

The seed flow should create setup metadata only. It must not create fake operational assessments, findings, evidence, scanner runs, remediation records, or scores.

## Reset

Stop containers while preserving data:

```powershell
docker compose down
```

Delete local volumes and rebuild:

```powershell
docker compose down -v
docker compose up --build
```

Use `down -v` only when intentionally deleting local runtime data.

## Smoke Testing

Run:

```powershell
py scripts/runtime-smoke-test.py --backend-url http://localhost:8000 --frontend-url http://localhost:3000
```

The smoke test should validate backend health, database health, seeded metadata endpoints, frontend load, and frontend/backend proxy connectivity.

## Single VM Production

1. Provision one Linux VM.
2. Install Docker and Docker Compose.
3. Copy the repository or release bundle.
4. Create `.env` from `.env.example`.
5. Set strong database credentials.
6. Configure scanner/evidence storage.
7. Start Compose.
8. Verify migrations and health checks.
9. Configure reverse proxy and TLS.
10. Configure backups for PostgreSQL and artifact storage.
11. Run smoke tests against production URLs.

## Troubleshooting

- Backend unhealthy: inspect `docker compose logs backend`.
- Database unavailable: inspect `docker compose logs postgres` and `DATABASE_URL`.
- Migrations failing: run `docker compose exec backend alembic current`.
- Frontend cannot reach backend: test `/api/backend/health`.
- Port conflict: override `API_HOST_PORT`, `FRONTEND_HOST_PORT`, or `POSTGRES_PORT`.

## Deployment Guardrails

- Do not add Kubernetes or Helm for the initial production target.
- Do not expose evidence artifact storage directly to the public internet.
- Do not store production secrets in source control.
- Do not run arbitrary scanner commands from user input.
