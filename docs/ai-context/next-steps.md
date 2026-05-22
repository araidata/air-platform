# Next Steps

The next development work should begin Phase 5: First Real Scanner Integration.

Phase 4 - AI Assessment Ecosystem Foundation is complete and verified. The Docker Compose runtime starts the frontend, backend, PostgreSQL, and scanner artifact volume together; applies the Phase 4 scanner migration; loads seeded operational scanner data; preserves scanner raw output and logs; normalizes mock scanner findings; creates evidence records; recalculates scores; and exposes the Scanner Ecosystem frontend route.

## Recommended Next Task

Integrate one real scanner without broadening the execution model:

1. Select either garak or AgentSeal as the first real scanner.
2. Add one CLI/Docker adapter that implements the Phase 4 adapter contract.
3. Keep execution synchronous and local to the backend service until real load proves a runner is needed.
4. Preserve stdout, stderr, structured output, command metadata, and logs under the scanner run artifact directory.
5. Add parser fixtures for successful output, empty output, scanner failure, malformed output, and partial output.
6. Normalize real scanner output into existing findings, evidence, audit events, and score recalculation.

## Why This Is Next

The platform now has scanner registry records, scan types, assessment profiles, mock execution, raw output preservation, evidence generation, normalized findings, score recalculation, API routes, seed data, tests, and an operator-facing scanner console. One real scanner can now be integrated without redesigning the platform.

## Keep From Phase 4

- Scanners remain external assessment tools.
- The platform remains the governance and orchestration layer.
- Raw output and logs are preserved before parser or normalization logic.
- Scanner-specific fields stay in evidence metadata or scanner results, not in the core finding schema.
- Score recalculation stays synchronous and service-layer.
- Docker Compose remains the runtime boundary.

## Do Not Do Next

- Do not integrate multiple real scanners at once.
- Do not add Kubernetes, RabbitMQ, Kafka, distributed workers, event buses, or continuous monitoring.
- Do not build scanner auto-scheduling or recurring assessments yet.
- Do not build OneTrust API integration yet.
- Do not make scanner output a substitute for evidence-backed human governance workflow.
