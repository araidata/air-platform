# Master TODO

This backlog is intentionally detailed and realistic for a single Linux VM, Docker Compose deployment, and one or two operators.

## Completed In Phase 1

- Created Next.js app under `apps/web`.
- Configured TypeScript and TailwindCSS through the Next.js scaffold.
- Created operational app shell with left navigation and top header.
- Added centralized mock data for systems, assessments, findings, evidence, scores, and AI Review Board reviews.
- Built Executive Dashboard, AI Inventory, Findings Queue, System Detail, Evidence and Audit, and AIRB Review Queue starter routes.
- Added score cards, risk heatmap, trend visualization, inventory table, findings queue table, evidence list, and governance review cards using mock data.

## Completed In Phase 2.5

- [x] Add Docker Compose runtime.
- [x] Add frontend container.
- [x] Add backend API container.
- [x] Add PostgreSQL runtime.
- [x] Add Alembic migration execution during backend startup.
- [x] Add shared environment configuration with `.env.example`.
- [x] Add frontend/backend integration through the Next.js backend proxy.
- [x] Add seed-data loading during backend startup.
- [x] Add health endpoint and database health endpoint.
- [x] Add runtime smoke testing.
- [x] Add persistent PostgreSQL volume.

## Frontend TODO

- [x] Build System Intake UI.
- [x] Build Assessment Launch UX.
- [x] Build Scanner Execution UX.
- [x] Build Findings Review UX.
- [x] Build Evidence Review UX.
- [x] Build AIRB Workflow UX.
- [x] Add guided operator workflow navigation across intake, assessment, scanning, findings, evidence, and AIRB views.
- [x] Connect frontend workflow surfaces to the existing backend APIs before adding broader new frontend pages.
- Configure shadcn/ui.
- Add user menu placeholder when authentication direction is known.
- Replace simple trend visualization with Recharts if charting needs grow.
- Replace native inventory table with TanStack Table if sorting and column controls become necessary.
- [x] Add inventory filters for department, risk tier, approval status, public-facing, rights-impacting, and data type.
- Add system detail tabs: overview, findings, evidence, scores, assessments, decisions, activity.
- [x] Add severity, status, owner, SLA, department, and domain filters.
- [x] Build Finding Detail page.
- [x] Add workflow transition dialog.
- [x] Add owner assignment dialog.
- [x] Add risk acceptance dialog.
- [x] Build Bias and Civil Rights Dashboard.
- Build Security Findings Dashboard.
- [x] Build AIRB Review Detail page.
- Build Deployment Approval page.
- Build Governance Reports page.
- Add empty states.
- Add loading states.
- Add error states.
- Add accessible labels for charts and icon controls.
- Verify responsive layouts for operator laptop and large monitor views.

## Backend TODO

- [x] Create FastAPI app under `apps/api`.
- [x] Add health endpoint.
- [x] Add database health endpoint.
- [x] Configure environment loading.
- [x] Configure database connection.
- Configure Redis connection.
- [x] Add Pydantic schemas.
- [x] Add route modules.
- [x] Add service modules.
- [x] Add audit event service.
- [x] Add finding workflow service.
- [x] Add evidence service.
- [x] Add scoring service.
- [x] Add seed command.
- Add pagination helpers.
- Add filtering helpers.
- Add structured error responses.
- [x] Add OpenAPI tags.
- [x] Add tests for health, systems, findings, evidence, and workflows.
- [x] Add tests for scoring.
- [x] Add backend Dockerfile.
- [x] Add container startup migration and seed flow.

## Database TODO

- [x] Choose SQLAlchemy or SQLModel.
- [x] Configure Alembic.
- Create departments table.
- [x] Create systems table.
- [x] Create assessments table.
- [x] Create scanner_runs table.
- [x] Create findings table.
- [x] Create evidence table.
- [x] Create scores table.
- [x] Create AIRB reviews table.
- Create deployment approvals table.
- [x] Create risk acceptances table.
- [x] Create framework mappings table.
- [x] Create audit events table.
- [x] Create language access scenarios table.
- [x] Create human appeal path checks table.
- [x] Add indexes for findings queue filters.
- [x] Add indexes for inventory filters.
- [x] Add indexes for evidence search.
- [x] Add seed data migrations or seed script.
- [x] Add test database setup.
- [x] Add PostgreSQL Docker Compose runtime.
- [x] Add persistent PostgreSQL Docker volume.
- [x] Verify Alembic migrations against live PostgreSQL.

## Dashboards TODO

- [x] Define score overview API.
- Define critical findings metric.
- Define high-risk systems metric.
- Define systems scanned metric.
- Define blocked deployments metric.
- Define live alerts query.
- Define risk trend calculation.
- Define risk heatmap query by department and domain.
- Build dashboard mock state.
- Replace mock state with API data.
- [x] Add score explanation drill-downs.

## Governance Workflow TODO

- Define governance status enums or lookup rows.
- Implement approval status transitions.
- Implement risk tier classification fields.
- Implement human review process field.
- Implement rights-impacting and safety-impacting flags.
- Add governance evidence checklist.
- Add exception workflow.
- Add audit events for governance decisions.

## AIRB Workflow TODO

- [x] Create AIRB review model.
- Implement states: Draft, Under Review, Security Review Required, Bias Review Required, Privacy Review Required, Legal Review Required, Approved, Approved with Exception, Blocked.
- Build review packet API.
- Build review queue UI.
- Build decision dialog.
- Require rationale for blocked and exception decisions.
- Add evidence references to decisions.
- Add expiration dates for exceptions.
- Add audit events for transitions.

## Evidence System TODO

- [x] Create evidence metadata model.
- Implement local artifact storage path.
- Implement hash calculation.
- Implement evidence upload endpoint.
- Implement evidence linking endpoint.
- Implement custody event model.
- Add evidence list UI.
- Add evidence detail UI.
- Add artifact type filters.
- Add sensitivity labels.
- Add evidence completeness calculation.
- Add backup guidance for evidence volume.

## Scoring Engine TODO

- [x] Implement domain score calculation.
- [x] Implement overall AI Governance Score.
- [x] Add severity deductions.
- [x] Add risk modifiers for public-facing, rights-impacting, safety-impacting, PII, PHI, CJIS, overdue findings, retests, risk acceptance, and approval blocking.
- [x] Add positive modifiers for remediation progress and complete evidence.
- [x] Store score explanations.
- [x] Add score recalculation endpoint.
- [x] Add score history.
- [x] Add score trend charts.
- [x] Add unit tests for scoring examples.
- [x] Verify Phase 3 scoring in Docker Compose.

## Scanner Integration TODO

- [x] Define adapter interface.
- [x] Create scanner registry.
- [x] Create scan type framework.
- [x] Create assessment profiles.
- [x] Create mock scanner adapter.
- [x] Create scanner run model.
- [x] Create scanner result model.
- [x] Create scanner workspace volume.
- [x] Capture mock raw output, logs, and artifacts.
- [x] Preserve raw output as evidence.
- [x] Implement normalization pipeline.
- [x] Add fixture and API tests.
- [x] Implement Docker/CLI execution wrapper for the first real scanner.
- [x] Add first security scanner adapter after workflow readiness.
- [x] Preserve native real scanner output, logs, configuration, and normalized output as evidence.
- [x] Normalize real scanner output into findings and trigger score recalculation.
- Defer first bias/fairness scanner adapter until a concrete workflow requires real scanner execution.
- Add first LLM/RAG evaluation adapter after workflow readiness.

## Testing TODO

- [x] Add backend unit tests.
- [x] Add backend integration tests with test database.
- [x] Add frontend component tests where useful.
- Add Playwright smoke tests after UI exists.
- [x] Add runtime verification for the guided operator workflow path once the UI is API-connected.
- [x] Test seed data integrity.
- [x] Test workflow transitions.
- [x] Test score calculations.
- [x] Test evidence linking.
- [x] Test scanner mock normalization.
- [x] Test first real scanner execution, parsing, evidence preservation, failure handling, and score integration.
- Test API pagination and filters.
- [x] Add runtime smoke test for frontend, backend, database, migrations, seed data, and core API endpoints.

## Governance Export TODO

- Export system inventory CSV.
- Export findings CSV.
- Export risk acceptances CSV.
- Export JSON audit packet.
- Document OneTrust field mapping.

## Operational Maturity TODO

- [x] Add Docker Compose.
- [x] Add environment templates.
- [x] Add local startup docs.
- Add backup scripts.
- Add restore runbook.
- [x] Add health checks.
- Add structured logging.
- Add operator runbooks.
- Add admin settings page later.
- Add role-based access later.
- Add TLS reverse proxy guidance.

## Integrations TODO

- Create integration mapping model.
- Create integration status model.
- Plan Jira ticket mapping.
- Plan ServiceNow ticket mapping.
- Plan Teams notification templates.
- Plan email notification templates.
- Add outbound event model later.
- Add sync retry model later.
- Do not implement real integrations until core workflows are stable.

## Documentation TODO

- Keep README current.
- Update implementation status after each phase.
- Add ADRs for major architecture choices.
- Update API docs when endpoints are implemented.
- Update data model docs when migrations change.
- Update AI context docs when priorities change.
- Add runbooks as operations mature.
