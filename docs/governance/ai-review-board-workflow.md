# AI Review Board Workflow

The AI Review Board workflow should help reviewers make explicit, evidence-backed deployment and risk decisions.

## Review Inputs

- AI system inventory record.
- Assessment summary.
- Open findings.
- Evidence index.
- Score summary.
- Risk acceptances.
- Privacy and civil-rights notes.
- Security review notes.
- Proposed deployment decision.

## Review Queue States

- `not_ready`
- `ready_for_review`
- `in_review`
- `approved`
- `approved_with_conditions`
- `blocked`
- `returned_for_remediation`

## Decision Types

- Approve.
- Approve with conditions.
- Block deployment.
- Require remediation.
- Require retest.
- Accept risk.
- Escalate to legal, privacy, security, or civil-rights reviewer.

## Required Decision Record

Each decision should store:

- Reviewer.
- Role.
- Decision.
- Rationale.
- Date.
- Conditions.
- Evidence references.
- Expiration date for exceptions.
- Follow-up owner.

## Small-Team Reality

The workflow should support a lightweight board process. It should not assume a large approval bureaucracy. One or two operators should be able to prepare review packets and track decisions.

## What To Avoid

- Complex enterprise workflow engines.
- Hard-coded legal conclusions.
- Approval decisions without evidence references.
- Unclear risk acceptance ownership.
