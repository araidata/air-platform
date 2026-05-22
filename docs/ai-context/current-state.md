# Current State

County AI Assurance Operations Center has moved from a documentation-first repository into the first mock UI implementation. The project still preserves durable operating context for future AI-assisted development, but there is now a working frontend scaffold to validate the operational workflow.

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

Phase 1: Operational UI and Mock Data.

The current work is to validate navigation, information density, risk presentation, findings triage, evidence visibility, and AI Review Board workflow before backend persistence exists.

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

## Does Not Exist Yet

- Backend API.
- Database migrations.
- Docker Compose runtime.
- Scanner adapter code.
- Real scanner integrations.
- OneTrust integration.

## Highest-Value Next Step

Begin Phase 2 workflow mechanics behind the UI: persisted findings and evidence records, assessment workflow transitions, retest and risk acceptance lifecycle, and audit events.

Do not start with scanner integrations.

## Agent Reminder

Before making changes, read:

- `CLAUDE.md`
- `AGENTS.md`
- `CODEX.md`
- `docs/ai-context/current-state.md`
- `docs/ai-context/implementation-status.md`
- `docs/ai-context/next-steps.md`
