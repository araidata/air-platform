# API Surface Plan

## Health

- `GET /health`
- `GET /health/db`

## Systems

- `GET /systems`
- `POST /systems`
- `GET /systems/{system_id}`
- `PATCH /systems/{system_id}`
- Deferred: `GET /systems/{system_id}/findings`
- Deferred: `GET /systems/{system_id}/evidence`
- Phase 3: `GET /systems/{system_id}/scores`

## Findings

- `GET /findings`
- `POST /findings`
- `GET /findings/{finding_id}`
- `PATCH /findings/{finding_id}`
- `POST /findings/{finding_id}/transition`
- `POST /findings/{finding_id}/retest`
- Owner assignment and due-date changes are currently handled through `PATCH /findings/{finding_id}`.
- Risk acceptance is currently handled through `POST /findings/{finding_id}/transition` with `status=risk_accepted`.

## Evidence

- `GET /evidence`
- `POST /evidence`
- `GET /evidence/{evidence_id}`
- Deferred: `POST /evidence/{evidence_id}/link`
- Deferred: `GET /evidence/{evidence_id}/custody`

## Assessments

- `GET /assessments`
- `POST /assessments`
- `GET /assessments/{assessment_id}`
- `PATCH /assessments/{assessment_id}`

## Scanner Runs

- Deferred to Phase 4: `POST /assessments/{assessment_id}/runs`
- Deferred to Phase 4: `GET /scanner-runs`
- Deferred to Phase 4: `GET /scanner-runs/{scanner_run_id}`

## Scores

- `GET /scores/overview`
- `GET /scores/systems/{system_id}`
- `POST /scores/recalculate`

## Audit

- `GET /audit-events`

## Retests

- `POST /findings/{finding_id}/retest`
- `GET /retests/{retest_id}`
- `PATCH /retests/{retest_id}`

## Owners

- `GET /owners`
- `POST /owners`

## AIRB

- `GET /airb-reviews`
- `POST /airb-reviews`
- `PATCH /airb-reviews/{review_id}`

## Civil Rights

- `GET /civil-rights/templates`
- `GET /civil-rights/language-access-scenarios`
- `POST /civil-rights/language-access-scenarios`
- `GET /civil-rights/appeal-path-checks`
- `POST /civil-rights/appeal-path-checks`
- `GET /civil-rights/summary`

## Deployment Approvals

- `GET /deployment-approvals`
- `POST /deployment-approvals`
- `GET /deployment-approvals/{approval_id}`
- `POST /deployment-approvals/{approval_id}/decision`

## Reports

- `GET /reports`
- `POST /reports/generate`
- `GET /reports/{report_id}`

## Integrations Planning

No external integrations should be implemented initially. Later endpoints may support export packages, webhook events, or synchronization status.
