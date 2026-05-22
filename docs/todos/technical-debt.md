# Technical Debt Tracking

This file tracks known and expected technical debt. It should be updated as implementation begins.

## Current Debt

- No application skeleton exists.
- No runtime exists.
- No tests exist.
- No database migrations exist.
- No seed scripts exist.

## Expected Early Debt

- Initial mock data may live in fixtures before database seed scripts are finalized.
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
