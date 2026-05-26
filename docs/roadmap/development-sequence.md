# Development Sequence

Use this sequence when choosing the next implementation task.

## Current Order

1. Keep the Docker Compose runtime stable.
2. Maintain core assessment, finding, evidence, and scanner run APIs.
3. Add Giskard through the existing scanner adapter contract.
4. Add PyRIT after Giskard is stable.
5. Add Langfuse trace/evidence ingestion.
6. Improve human review workflow only where assessment decisions require it.
7. Build executive reporting, PDF output, and OpenControl export.
8. Add production readiness features.

## Sequencing Rule

If two tasks compete, choose the one that improves assessment execution, evidence quality, finding normalization, or executive reporting from real records.

## Do Not Prioritize

- Distributed infrastructure.
- Scanner microservices.
- Broad integrations before Giskard, PyRIT, and Langfuse.
- Demo-only dashboards.
- Workflow features that do not improve assessment decisions or reporting.
