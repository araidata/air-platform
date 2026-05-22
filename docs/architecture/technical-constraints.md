# Technical Constraints

These constraints protect the platform from growing in the wrong direction before it has operational value.

## Must Keep

- Single Linux VM deployment for the initial platform.
- Docker Compose deployment.
- API-first backend.
- Normalized finding and evidence schemas.
- Scanner adapters with loose coupling.
- Seed data and mock findings before real scanner integrations.
- Clear domain boundaries in backend modules.
- Dense, operational frontend design.

## Must Avoid Initially

- Kubernetes.
- Distributed scanner microservices.
- Enterprise SSO as a blocker.
- Advanced CI/CD gates as a blocker.
- Complex observability stacks.
- Real-time telemetry pipelines.
- Autonomous remediation.
- Autonomous deployment approval.
- Tight dependency on scanner internals.
- Rewriting open-source scanner logic.

## Acceptable Early Simplifications

- Local username/password or simple admin bootstrap auth in development.
- Local evidence volume.
- Manual scanner execution records.
- Mock scanner output fixtures.
- Simple Redis-backed jobs.
- Manual AIRB participant assignment.
- CSV or PDF export planning before full reporting automation.

## Non-Negotiable Architecture Requirements

- Findings must map to affected systems.
- Findings must support evidence.
- Evidence must support immutable artifact references and custody events.
- Scores must be explainable.
- AIRB decisions must be auditable.
- Deployment approvals must preserve reviewer rationale.
- Scanner outputs must normalize before entering the findings workflow.
