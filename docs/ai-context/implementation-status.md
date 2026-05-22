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

## In Progress

- Phase 1 UI refinement as future workflow requirements become clearer.

## Next

- Phase 2 findings, evidence, and assessment workflow:
  - Backend persistence.
  - Finding lifecycle transitions.
  - Evidence records and links.
  - Owners, due dates, retest status, risk acceptance, and audit events.

## Blocked

- No current blockers.

## Intentionally Deferred

- Real scanner integrations.
- OneTrust API integration.
- Database schema and migrations.
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
- No automated tests exist yet beyond lint, production build, and manual HTTP route smoke checks.
- Browser plugin localhost verification was blocked by the in-app browser with `ERR_BLOCKED_BY_CLIENT`; route smoke verification was used as a fallback.

## Update Template

When updating this file, use:

- Completed:
- In Progress:
- Next:
- Blocked:
- Intentionally Deferred:
- Architectural Decisions:
- Current Known Issues:
