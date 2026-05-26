# Docker Architecture

AI Assessment Scanner runs locally and on a small production host with Docker Compose.

## Services

- `frontend`: Next.js + TypeScript UI.
- `backend`: FastAPI API service.
- `postgres`: PostgreSQL database.

Scanner artifacts are written to the configured scanner/evidence storage path, mounted into the backend container.

## Runtime Flow

```text
Browser
  -> frontend:3000
  -> /api/backend/* proxy
  -> backend:8000
  -> postgres:5432
```

The frontend defaults `NEXT_PUBLIC_API_URL` to `/api/backend`. Next.js rewrites that path to `NEXT_INTERNAL_API_URL`, which defaults to `http://backend:8000` inside Compose.

## Volumes

- `postgres_data`: PostgreSQL data directory.
- `scanner_data`: scanner and evidence artifacts.
- `web_node_modules`: frontend dependency volume for bind-mounted development.
- `web_next`: frontend build/cache volume.

`docker compose down` preserves named volumes. `docker compose down -v` deletes them.

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
- `SCANNER_STORAGE_ROOT`

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

## Startup

Backend startup:

1. Wait for PostgreSQL.
2. Run `alembic upgrade head`.
3. Run development metadata seed when configured.
4. Start FastAPI with Uvicorn.

Development seed may create example systems and configuration metadata. It must not fabricate operational assessments, findings, evidence, scanner runs, or scores.

## Health Checks

- PostgreSQL uses `pg_isready`.
- Backend exposes `GET /health` and `GET /health/db`.
- Frontend health is checked through the root route.

## Production Notes

- Set non-default database credentials.
- Protect evidence and scanner artifact storage.
- Configure backups for PostgreSQL and artifacts.
- Add TLS through a reverse proxy or hosting platform.
- Keep scanner execution local and adapter-controlled unless operational load proves otherwise.
