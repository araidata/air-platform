# Docker Architecture

The first deployment target is a single Linux VM using Docker Compose.

## Services

- `web`: Next.js frontend.
- `api`: FastAPI backend.
- `postgres`: PostgreSQL database.
- `redis`: Redis for jobs and cache.
- `scanner-runner`: local runner for scanner adapter execution.
- `reverse-proxy`: optional Nginx or Caddy in later deployment hardening.

## Volumes

- `postgres_data`.
- `redis_data` if persistence is enabled.
- `evidence_data`.
- `scanner_workspace`.

## Network

All services should run on a private Compose network. Only the web/reverse-proxy should be public in production. The API can be public behind the same proxy if needed, but internal-only API access is acceptable for first deployment.

## Environment Variables

Expected categories:

- Database connection.
- Redis connection.
- Evidence storage path.
- API base URL.
- Frontend public API URL.
- Admin bootstrap values.
- Scanner workspace path.
- Model provider keys later.

## Scanner Containers

Scanner adapters should invoke scanner images with mounted input and output directories. The scanner container should not have direct database access. The platform runner collects outputs and passes results through normalization.

## What Not To Add Early

- Kubernetes manifests.
- Helm charts.
- Service mesh.
- Distributed queue workers.
- Cloud-specific infrastructure modules.
