# Database TODO

## Implemented

- [x] PostgreSQL Docker Compose runtime.
- [x] SQLAlchemy model layer.
- [x] Alembic migration workflow.
- [x] Systems table.
- [x] Assessments table.
- [x] Scanner runs and scanner results tables.
- [x] Findings table.
- [x] Evidence table.
- [x] Scores, score history, explanations, and snapshots.
- [x] Review workflow records.
- [x] Risk acceptances.
- [x] Framework mappings.
- [x] Audit events.
- [x] Language access scenarios.
- [x] Human appeal path checks.
- [x] Development metadata seed.
- [x] Persistent PostgreSQL volume.

## Next

- [ ] Add tables or columns required for Giskard result metadata only if existing scanner result metadata is insufficient.
- [ ] Add OpenControl export metadata if needed.

## Later

- [ ] RBAC tables.
- [ ] Report generation metadata.
- [ ] Backup/restore verification notes.
- [ ] Additional indexes driven by production query patterns.
