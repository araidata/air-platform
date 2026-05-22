# API Surface Plan

## Systems

- `GET /systems`
- `POST /systems`
- `GET /systems/{system_id}`
- `PATCH /systems/{system_id}`
- `GET /systems/{system_id}/findings`
- `GET /systems/{system_id}/evidence`
- `GET /systems/{system_id}/scores`

## Findings

- `GET /findings`
- `POST /findings`
- `GET /findings/{finding_id}`
- `PATCH /findings/{finding_id}`
- `POST /findings/{finding_id}/transition`
- `POST /findings/{finding_id}/assign`
- `POST /findings/{finding_id}/accept-risk`
- `POST /findings/{finding_id}/retest`

## Evidence

- `GET /evidence`
- `POST /evidence`
- `GET /evidence/{evidence_id}`
- `POST /evidence/{evidence_id}/link`
- `GET /evidence/{evidence_id}/custody`

## Assessments And Scanner Runs

- `GET /assessments`
- `POST /assessments`
- `GET /assessments/{assessment_id}`
- `POST /assessments/{assessment_id}/runs`
- `GET /scanner-runs`
- `GET /scanner-runs/{scanner_run_id}`

## Scores

- `GET /scores/overview`
- `GET /scores/systems/{system_id}`
- `POST /scores/recalculate`

## AIRB

- `GET /airb/reviews`
- `POST /airb/reviews`
- `GET /airb/reviews/{review_id}`
- `POST /airb/reviews/{review_id}/transition`
- `POST /airb/reviews/{review_id}/decision`

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
