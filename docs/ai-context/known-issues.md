# Known Issues

## Current Issues

- garak is the only real external scanner adapter.
- Giskard, PyRIT, and Langfuse are not yet implemented.
- Backend tests use SQLite for fast workflow coverage; Docker smoke tests cover live PostgreSQL behavior.
- No production backup or restore automation exists yet.
- Host port conflicts can require `API_HOST_PORT`, `FRONTEND_HOST_PORT`, or `POSTGRES_PORT` overrides.
- PDF reporting and OpenControl export are not implemented.

## Documentation Issues

- Historical roadmap-slice docs have been consolidated into the current roadmap and status docs.
- Status docs are manually maintained.
- Docs outside the assessment/scanner/deployment planning set may still need future terminology cleanup when they are touched.

## Product Risks

- Adding many scanners before Giskard and PyRIT are stable would weaken evidence quality.
- Overbuilding infrastructure would make the platform harder for a small county team to operate.
- Demo data that looks operational would reduce trust in reports.

## Mitigations

- Follow the README roadmap checklist.
- Preserve raw evidence for every scanner run.
- Keep scanner integrations adapter-based.
- Keep demo metadata separate from operational records.
- Update status docs after implementation changes.
