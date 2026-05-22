# Master TODO

This backlog is intentionally detailed and realistic for a single Linux VM, Docker Compose deployment, and one or two operators.

## Frontend TODO

- Create Next.js app under `apps/web`.
- Configure TypeScript.
- Configure TailwindCSS.
- Configure shadcn/ui.
- Create operational app shell with left navigation.
- Add top header with environment, search, and user menu placeholder.
- Build Executive Dashboard route.
- Build score card components.
- Build risk heatmap component.
- Build trend chart component with Recharts.
- Build AI Inventory table with TanStack Table.
- Add inventory filters for department, risk tier, approval status, public-facing, rights-impacting, and data type.
- Build System Detail page.
- Add system detail tabs: overview, findings, evidence, scores, assessments, decisions, activity.
- Build Findings Queue table.
- Add severity, status, owner, SLA, department, and domain filters.
- Build Finding Detail page.
- Add workflow transition dialog.
- Add owner assignment dialog.
- Add risk acceptance dialog.
- Build Bias and Civil Rights Dashboard.
- Build Security Findings Dashboard.
- Build AIRB Review Queue.
- Build AIRB Review Detail page.
- Build Evidence and Audit page.
- Build Deployment Approval page.
- Build Governance Reports page.
- Add empty states.
- Add loading states.
- Add error states.
- Add accessible labels for charts and icon controls.
- Verify responsive layouts for operator laptop and large monitor views.

## Backend TODO

- Create FastAPI app under `apps/api`.
- Add health endpoint.
- Configure environment loading.
- Configure database connection.
- Configure Redis connection.
- Add Pydantic schemas.
- Add route modules.
- Add service modules.
- Add audit event service.
- Add finding workflow service.
- Add evidence service.
- Add scoring service.
- Add seed command.
- Add pagination helpers.
- Add filtering helpers.
- Add structured error responses.
- Add OpenAPI tags.
- Add tests for health, systems, findings, evidence, scoring, and workflows.

## Database TODO

- Choose SQLAlchemy or SQLModel.
- Configure Alembic.
- Create departments table.
- Create systems table.
- Create assessments table.
- Create scanner_runs table.
- Create findings table.
- Create evidence table.
- Create scores table.
- Create AIRB reviews table.
- Create deployment approvals table.
- Create risk acceptances table.
- Create framework mappings table.
- Create audit events table.
- Add indexes for findings queue filters.
- Add indexes for inventory filters.
- Add indexes for evidence search.
- Add seed data migrations or seed script.
- Add test database setup.

## Dashboards TODO

- Define score overview API.
- Define critical findings metric.
- Define high-risk systems metric.
- Define systems scanned metric.
- Define blocked deployments metric.
- Define live alerts query.
- Define risk trend calculation.
- Define risk heatmap query by department and domain.
- Build dashboard mock state.
- Replace mock state with API data.
- Add score explanation drill-downs.

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

- Create AIRB review model.
- Implement states: Draft, Under Review, Security Review Required, Bias Review Required, Privacy Review Required, Legal Review Required, Approved, Approved with Exception, Blocked.
- Build review packet API.
- Build review queue UI.
- Build decision dialog.
- Require rationale for blocked and exception decisions.
- Add evidence references to decisions.
- Add expiration dates for exceptions.
- Add audit events for transitions.

## Evidence System TODO

- Create evidence metadata model.
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

- Implement domain score calculation.
- Implement overall AI Governance Score.
- Add severity deductions.
- Add risk modifiers for public-facing, rights-impacting, safety-impacting, PII, PHI, CJIS, overdue findings, and reopened findings.
- Add positive modifiers for verified remediation, complete evidence, compensating controls, and accepted risks.
- Store score explanations.
- Add score recalculation endpoint.
- Add score history.
- Add score trend charts.
- Add unit tests for scoring examples.

## Scanner Integration TODO

- Define adapter interface.
- Create scanner registry.
- Create mock scanner adapter.
- Create scanner run model.
- Create scanner workspace volume.
- Implement Docker execution wrapper.
- Capture stdout, stderr, exit code, and artifacts.
- Preserve raw output as evidence.
- Implement normalization pipeline.
- Add fixture tests.
- Add first security scanner adapter after workflow readiness.
- Add first bias/fairness scanner adapter after workflow readiness.
- Add first LLM/RAG evaluation adapter after workflow readiness.

## Testing TODO

- Add backend unit tests.
- Add backend integration tests with test database.
- Add frontend component tests where useful.
- Add Playwright smoke tests after UI exists.
- Test seed data integrity.
- Test workflow transitions.
- Test score calculations.
- Test evidence linking.
- Test scanner mock normalization.
- Test API pagination and filters.

## Operational Maturity TODO

- Add Docker Compose.
- Add environment templates.
- Add local startup docs.
- Add backup scripts.
- Add restore runbook.
- Add health checks.
- Add structured logging.
- Add operator runbooks.
- Add admin settings page later.
- Add role-based access later.
- Add TLS reverse proxy guidance.

## Integrations TODO

- Create integration mapping model.
- Create integration status model.
- Document OneTrust field mapping.
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
