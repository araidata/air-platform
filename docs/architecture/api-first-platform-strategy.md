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
