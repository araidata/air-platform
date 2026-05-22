# Database TODO

## Completed In Phase 2

- [x] Configure SQLAlchemy 2.x models.
- [x] Configure Alembic.
- [x] Create `ai_systems` table.
- [x] Create `assessments` table.
- [x] Create `findings` table.
- [x] Create `evidence` table.
- [x] Create `owners` table.
- [x] Create `retests` table.
- [x] Create `airb_reviews` table.
- [x] Create `risk_acceptances` table.
- [x] Create `framework_mappings` table.
- [x] Create `audit_events` table.
- [x] Add indexes for common queue and relationship filters.
- [x] Add Phase 2 seed script.
- [x] Add SQLite-backed test database setup.

## Completed In Phase 2.5

- [x] Add PostgreSQL Docker Compose runtime.
- [x] Add persistent `postgres_data` Docker volume.
- [x] Run Alembic migrations against live PostgreSQL in the backend container.
- [x] Load seeded systems, findings, assessments, and evidence into PostgreSQL.
- [x] Verify persistence after `docker compose down` and restart without deleting volumes.
- [x] Fix seed ordering so evidence audit events receive PostgreSQL evidence IDs.

## Phase 3 Candidate Tables

- `score_snapshots`
- `score_explanations`

## Deferred Candidate Tables

- `scanner_runs`
- `departments`
- `deployment_approvals`

## Seed Data

Seed systems:

- Public Benefits Chatbot.
- Sheriff Incident Summary Assistant.
- Permit Review Assistant.
- HR Resume Screening AI.
- Citizen Services RAG Chatbot.

Seed findings:

- Prompt injection vulnerability.
- Spanish-language explanation disparity.
- Missing human appeal path.
- Excessive MCP/tool permissions.
- Incomplete audit logging.
- Possible sensitive data leakage.
- Weak governance evidence.
- Missing risk acceptance.
- Missing retest documentation.

## Deferred

- Complex tenancy.
- Enterprise RBAC.
- Data warehouse design.
- Long-term archival strategy beyond evidence references.
