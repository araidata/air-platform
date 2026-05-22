# Architecture Summary

This platform should be a modular monolith deployed on one Linux VM with Docker Compose.

## Planned Runtime Shape

- Frontend: Next.js.
- Backend: API-first service, likely FastAPI.
- Database: PostgreSQL.
- Jobs/cache: Redis only when needed.
- Scanner execution: Dockerized CLI/container adapters.
- Evidence storage: local mounted storage first; object storage later if needed.

## Core Modules

- AI systems inventory.
- Assessments.
- Scanner runs.
- Findings.
- Evidence.
- Scoring.
- AI Review Board workflow.
- Reports.
- Integrations.
- Audit events.

## Platform Responsibility

The platform owns:

- Governance records.
- Assessment workflow.
- Normalized findings.
- Evidence references.
- Audit packets.
- Risk scores.
- Review decisions.
- Reporting.

## External Tool Responsibility

External tools own:

- Attack execution.
- Model testing.
- Fairness calculations.
- RAG evaluation.
- Model file scanning.

The platform should orchestrate scanners and normalize results; it should not recreate scanner logic.

## Key Architectural Rule

Scanners are external tools. Integrate them through adapters that execute, collect output, preserve evidence, normalize findings, map frameworks, and calculate score impact.
