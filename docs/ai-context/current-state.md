# Current State

County AI Assurance Operations Center has moved from mock UI into the first durable backend workflow implementation. The project still preserves durable operating context for future AI-assisted development, and now has both a working frontend scaffold and a FastAPI backend for the Phase 2 assurance records.

## Product Definition

This is an operational AI governance, AI security, AI bias/civil-rights, findings, evidence, and assessment platform for county government.

It is intended for one or two operators who need to manage:

- AI inventory.
- Assessments.
- Findings.
- Evidence.
- Audit packets.
- Risk scoring.
- Governance workflows.
- AI Review Board decisions.
- Reports.
- Future OneTrust export or integration.

## Current Phase

Phase 2: Findings, Evidence, and Assessment Workflow is implemented and verified.

The current work is ready to move toward Phase 3 scoring while keeping the frontend mock data in place until the API contract is wired into UI workflows.

## Exists Now

- AI assistant operating files.
- Architecture documentation.
- Scanner strategy documentation.
- Findings and evidence documentation.
- Governance documentation.
- UI/UX guidance.
- Integration planning.
- Roadmap and todo files.
- ADRs for core architectural constraints.
- Next.js frontend scaffold under `apps/web`.
- Centralized mock data for systems, assessments, findings, evidence, scores, and reviews.
- Mock-data-driven pages for executive dashboard, inventory, findings queue, system detail, evidence, and AI Review Board queue.
- FastAPI backend under `apps/api`.
- SQLAlchemy 2.x models for systems, assessments, findings, evidence, owners, retests, AIRB reviews, framework mappings, risk acceptances, and audit events.
- Alembic initial migration for Phase 2 workflow tables.
- REST endpoints for systems, assessments, findings, evidence, audit events, retests, AIRB reviews, and owners.
- Workflow services for finding transitions, assessment transitions, evidence creation, retest tracking, and audit event creation.
- Phase 2 seed script with the five mock county AI systems and realistic findings/evidence.
- Backend tests covering model creation, valid and invalid finding transitions, evidence creation, audit events, retests, and API smoke flows.
- Lightweight frontend API client layer in `apps/web/src/lib/api-client.ts`.

## Does Not Exist Yet

- Docker Compose runtime.
- Scanner adapter code.
- Real scanner integrations.
- OneTrust integration.

## Highest-Value Next Step

Begin Phase 3 scoring: explainable domain scoring, overall system score calculation, score history, and score explanations tied to findings, evidence, retests, and risk acceptance state.

Do not start with scanner integrations.

## Agent Reminder

Before making changes, read:

- `CLAUDE.md`
- `AGENTS.md`
- `CODEX.md`
- `docs/ai-context/current-state.md`
- `docs/ai-context/implementation-status.md`
- `docs/ai-context/next-steps.md`
