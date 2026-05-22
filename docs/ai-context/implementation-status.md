# Implementation Status

Update this file whenever the repository meaningfully changes.

## Completed

- Created repository-level AI assistant guidance:
  - `CLAUDE.md`
  - `AGENTS.md`
  - `CODEX.md`
  - `.cursor/rules/project-rules.mdc`
  - `.github/copilot-instructions.md`
- Created Claude Code command templates under `.claude/commands/`.
- Added Codex workflow playbooks in `docs/ai-context/codex-workflows.md`.
- Added README Build Checklist and AI-maintained completion rules.
- Documented project philosophy, constraints, roadmap, architecture, scanner strategy, findings, evidence, governance, integrations, UI guidance, todos, and ADRs.
- Confirmed project direction:
  - Single Linux VM.
  - Docker Compose first.
  - Mock-first development.
  - API-first platform.
  - CLI/container-first scanners through adapters.
- Created Phase 1 Next.js frontend scaffold under `apps/web`.
- Added centralized mock data for systems, assessments, findings, evidence, scores, and AI Review Board reviews.
- Built mock-data-driven Phase 1 pages:
  - Executive Dashboard.
  - AI Inventory.
  - Findings Queue.
  - System Detail Page.
  - Evidence & Audit Page.
  - AI Review Board Queue.
- Verified the frontend with `npm run lint`, `npm run build`, and HTTP route smoke checks for all Phase 1 pages.
- Created Phase 2 FastAPI backend under `apps/api`.
- Added SQLAlchemy 2.x models for:
  - AI systems.
  - Assessments.
  - Findings.
  - Evidence.
  - Owners.
  - Retests.
  - AIRB reviews.
  - Framework mappings.
  - Risk acceptances.
  - Audit events.
- Added Alembic configuration and initial Phase 2 workflow migration.
- Added REST endpoints for systems, assessments, findings, evidence, audit events, retests, AIRB reviews, and owners.
- Added workflow services for finding transitions, assessment status changes, evidence creation, retest tracking, and audit logging.
- Added Phase 2 seed data for the five mock systems, realistic findings, evidence, framework mappings, AIRB reviews, and audit records.
- Added backend tests covering model creation, valid and invalid finding transitions, evidence creation, audit event creation, retest creation/update, and API route smoke flows.
- Added lightweight frontend API client layer while preserving mock data as the frontend source of truth.
- Verified Phase 2 with `py -m pytest`, `py -m compileall app`, in-memory Alembic migration upgrade, and `npm.cmd run build`.

## In Progress

- Phase 3 scoring design and implementation planning.

## Next

- Phase 3 scoring engine:
  - Explainable domain scoring.
  - Score impact calculation from findings.
  - Score history and score explanations.
  - API surfaces that the frontend can adopt without removing mock data abruptly.

## Blocked

- No current blockers.

## Intentionally Deferred

- Real scanner integrations.
- OneTrust API integration.
- Background job execution.
- Authentication and authorization.
- Docker Compose runtime.
- Production deployment.
- Kubernetes or distributed orchestration.

## Architectural Decisions

- ADR 0001: Single VM and Docker Compose.
- ADR 0002: Adapter-based scanner architecture.
- ADR 0003: Mock-first development.
- ADR 0004: API-first platform and CLI-first scanners.

## Current Known Issues

- Documentation exists in both new and earlier paths; future cleanup may consolidate older docs after implementation stabilizes.
- No Docker Compose runtime exists yet, so PostgreSQL was not live-smoke-tested. The initial Alembic migration was sanity-checked against SQLite, and backend workflow tests use SQLite.
- Browser plugin localhost verification was previously blocked by the in-app browser with `ERR_BLOCKED_BY_CLIENT`; route smoke verification was used as a fallback for Phase 1.

## Update Template

When updating this file, use:

- Completed:
- In Progress:
- Next:
- Blocked:
- Intentionally Deferred:
- Architectural Decisions:
- Current Known Issues:
