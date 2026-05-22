# Backend Implementation Plan

## Stack

- FastAPI.
- PostgreSQL.
- Redis.
- Pydantic models.
- Alembic migrations.

## Domain Modules

- `systems`.
- `findings`.
- `evidence`.
- `assessments`.
- `scanner_runs`.
- `scoring`.
- `airb`.
- `deployment_approvals`.
- `reports`.
- `audit`.
- `integrations`.

## First Endpoints

- Health check.
- Systems list.
- System detail.
- Findings list.
- Finding detail.
- Evidence list.
- Score overview.

## Services

- Finding workflow service.
- Evidence service.
- Scoring service.
- Audit event service.
- Seed service.
- Scanner adapter service later.

## Backend Guardrails

- Do not put workflow logic directly in route handlers.
- Do not put scanner execution in route handlers.
- Do not calculate scores in the frontend.
- Do not lose raw evidence.
- Do not let scanner-specific data define the core data model.
