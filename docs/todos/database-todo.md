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

## Completed In Phase 3

- [x] Create `domain_scores` table.
- [x] Create `score_history` table.
- [x] Create `score_explanations` table.
- [x] Create `score_snapshots` table.
- [x] Verify the Phase 3 scoring migration in Docker Compose.

## Completed In Phase 4

- [x] Create `scanner_definitions` table.
- [x] Create `scan_types` table.
- [x] Create `assessment_profiles` table.
- [x] Create `scanner_runs` table.
- [x] Create `scanner_results` table.
- [x] Verify the Phase 4 scanner ecosystem migration in Docker Compose.
- [x] Add seeded scanner registry, scan types, assessment profiles, scanner runs, scanner results, generated evidence, and normalized findings.

## Completed In Phase 6

- [x] Create `language_access_scenarios` table.
- [x] Create `human_appeal_path_checks` table.
- [x] Add AIRB civil-rights workflow indicator columns.
- [x] Verify the Phase 6 civil-rights migration in Docker Compose.
- [x] Add seeded civil-rights templates, scenarios, appeal checks, fairness findings, and evidence.

## Deferred Candidate Tables

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
