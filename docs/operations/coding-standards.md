# Coding Standards

## General

- Prefer clear domain modules over clever abstraction.
- Keep public schemas stable.
- Use typed models for request and response bodies.
- Keep scanner-specific logic behind adapters.
- Add tests for workflow transitions and score calculations.
- Preserve audit events for meaningful state changes.

## Frontend

- TypeScript only.
- Use shadcn/ui primitives.
- Use TanStack Table for queues.
- Use Recharts for operational charts.
- Keep pages dense and readable.
- Avoid marketing layouts.
- Avoid chat-first UI patterns.
- Use route-level loading and error states.
- Keep component props explicit and typed.

## Backend

- FastAPI with Pydantic models.
- SQLAlchemy or SQLModel acceptable, but choose one and stay consistent.
- Alembic migrations.
- Service layer for business rules.
- Repository/data access layer where it reduces repetition.
- Do not put scoring logic inside route handlers.
- Do not put scanner execution logic inside route handlers.
- Write audit events through a shared service.

## Database

- Use UUIDs or stable string IDs consistently.
- Use enums carefully; prefer lookup tables if workflow states are expected to evolve often.
- Add indexes for operational queues.
- Preserve created and updated timestamps.
- Avoid JSON blobs for fields that need filtering.
- JSON is acceptable for score explanations, scanner raw metadata references, and controlled integration metadata.

## Documentation

- Update AI context docs when current state changes.
- Update ADRs when architecture direction changes.
- Update TODO status when meaningful work lands.
