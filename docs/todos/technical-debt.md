# Technical Debt Tracking

This file tracks known and expected technical debt. It should be updated as implementation begins.

## Current Debt

- Historical note: frontend pages previously used centralized mock data as their source of truth. Runtime pages are now API-backed or empty-state driven.
- Backend automated tests use SQLite; live PostgreSQL is covered by Docker runtime smoke testing instead of a full test suite.
- Evidence artifact storage is metadata/text only; local artifact volume workflow is deferred until file upload is implemented.
- No production backup or restore scripts exist yet.

## Expected Early Debt

- Example metadata may live in fixtures or seed scripts, but fabricated operational findings, evidence, and scanner runs should not return.
- Initial scoring weights may be hard-coded before admin configuration exists.
- Initial evidence storage may use local volumes before object storage is evaluated.
- Initial auth may be simple before role-based access is mature.

## Debt Guardrails

- Mock data debt is acceptable only if it is replaced by seed scripts.
- Hard-coded scoring weights are acceptable only if explanations are clear.
- Local evidence storage is acceptable only if hashes and metadata are preserved.
- Simple auth is acceptable only if deployment exposure is controlled.

## Debt That Should Not Be Accepted

- Scanner-specific core finding tables.
- Scores calculated only in frontend code.
- Workflow transitions without audit events.
- Evidence files without metadata or hash.
- Real scanner outputs discarded after normalization.
- OneTrust or Jira treated as source of truth for platform findings.
