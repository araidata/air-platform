# API-First Platform Strategy

The platform should be API-first even when the first UI uses mock data.

## Meaning Of API-First

Core platform actions should map to stable API operations:

- Create and update AI systems.
- Start assessments.
- Record findings.
- Attach evidence.
- Update status and owner.
- Record review decisions.
- Generate reports.
- Export governance packets.

The UI should be a client of these concepts, not the only place they exist.

## Why API-First

- Makes scanner adapters easier to integrate.
- Supports future CLI tools.
- Makes exports and automation cleaner.
- Keeps workflows testable.
- Avoids burying governance logic in UI components.

## Initial API Domains

- `/systems`
- `/assessments`
- `/findings`
- `/evidence`
- `/scanner-runs`
- `/scores`
- `/reviews`
- `/reports`
- `/integrations`

## Scanner Boundary

External scanners should initially be CLI/container-first. The platform API should orchestrate scan requests and persist results, not require scanners to become first-class web services.

## Do Not Overbuild

API-first does not mean enterprise API gateway, distributed services, or complex service mesh. It means clean backend contracts inside a simple deployable system.

## Phase 3 Score APIs

Phase 3 adds deterministic score APIs:

- `GET /scores`
- `GET /scores/{id}`
- `GET /scores/{id}/explanations`
- `GET /systems/{id}/scores`
- `GET /systems/{id}/score-history`
- `POST /systems/{id}/recalculate-scores`
- `POST /assessments/{id}/recalculate-scores`

The recalculation endpoints run synchronously in the FastAPI service layer and reuse the existing database and audit-event architecture.

## Phase 4 Scanner Ecosystem APIs

Phase 4 adds scanner ecosystem APIs:

- `GET /scanner-definitions`
- `GET /scanner-definitions/{id}`
- `POST /scanner-definitions`
- `PATCH /scanner-definitions/{id}`
- `GET /scan-types`
- `GET /scan-types/{id}`
- `POST /scan-types`
- `PATCH /scan-types/{id}`
- `GET /assessment-profiles`
- `GET /assessment-profiles/{id}`
- `POST /assessment-profiles`
- `PATCH /assessment-profiles/{id}`
- `GET /scanner-runs`
- `GET /scanner-runs/{id}`
- `POST /scanner-runs`
- `POST /scanner-runs/{id}/execute`
- `GET /scanner-results/{id}`
- `GET /scanner-adapters`
- `GET /systems/{id}/recommended-scans`
- `GET /systems/{id}/scanner-runs`

Scanner execution remains synchronous and local in Phase 4. The API starts mock adapter execution, preserves artifacts, creates evidence, normalizes findings, and recalculates scores through the existing service layer.
