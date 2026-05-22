# Docker Architecture

The Phase 2.5 runtime target is a single Linux VM using Docker Compose. It is deliberately small and operationally boring.

## Services

- `frontend`: Next.js operational UI.
- `backend`: FastAPI API service.
- `postgres`: PostgreSQL runtime database.

Redis, scanner runners, reverse proxies, and background workers are intentionally deferred.

## Runtime Flow

```text
Browser
  -> frontend:3000
  -> /api/backend/* proxy
  -> backend:8000
  -> postgres:5432
```

The frontend defaults `NEXT_PUBLIC_API_URL` to `/api/backend`, and Next.js rewrites that path to `NEXT_INTERNAL_API_URL`, which defaults to `http://backend:8000` inside Compose.

## Volumes

- `postgres_data`: PostgreSQL data directory.
- `web_node_modules`: frontend dependency volume for bind-mounted development.
- `web_next`: frontend `.next` runtime/cache volume.

The PostgreSQL volume is the persistence boundary for Phase 2.5. `docker compose down` preserves it; `docker compose down -v` deletes it.

## Environment Variables

Backend:

- `DATABASE_URL`
- `API_HOST`
- `API_PORT`
- `API_HOST_PORT`
- `API_RELOAD`
- `ENVIRONMENT`
- `RUN_SEED`
- `ALLOWED_ORIGINS`

Frontend:

- `FRONTEND_HOST_PORT`
- `NEXT_PUBLIC_API_URL`
- `NEXT_INTERNAL_API_URL`
- `WATCHPACK_POLLING`

PostgreSQL:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_PORT`

## Health Checks

- PostgreSQL uses `pg_isready`.
- Backend checks `GET /health`.
- Frontend checks the Next.js root route.

The backend also exposes `GET /health/db` for direct database connectivity validation.

## Migration And Seed Runtime

Backend startup:

1. Waits for PostgreSQL.
2. Runs `alembic upgrade head`.
3. Runs `python -m app.seed.run_seed` when `RUN_SEED=true`.
4. Starts Uvicorn.

The seed flow is idempotent and preserves existing data when the seed systems are already present.

## What Not To Add In Phase 2.5

- Kubernetes manifests.
- Helm charts.
- Service mesh.
- RabbitMQ, Kafka, or distributed workers.
- Scanner execution containers.
- Production observability stacks.
- Cloud-specific infrastructure modules.
