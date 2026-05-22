# Findings Lifecycle

Findings are the core operational unit of the platform.

## Lifecycle States

- `new`: Finding has been created and needs triage.
- `under_review`: Operator is reviewing severity, owner, and evidence.
- `in_remediation`: Fix or mitigation is underway.
- `awaiting_retest`: Remediation is complete and needs validation.
- `mitigated`: Retest or review indicates the finding is addressed.
- `risk_accepted`: Authorized reviewer accepted the risk.
- `false_positive`: Finding is not valid, with rationale preserved.
- `closed`: Finding is resolved, accepted, or otherwise complete.

## Implemented Transitions

Phase 2 enforces these transitions in `FindingWorkflowService`:

- `new` -> `under_review`
- `under_review` -> `in_remediation`
- `under_review` -> `risk_accepted`
- `under_review` -> `false_positive`
- `in_remediation` -> `awaiting_retest`
- `awaiting_retest` -> `mitigated`
- `awaiting_retest` -> `in_remediation`
- `mitigated` -> `closed`
- `risk_accepted` -> `closed`
- `false_positive` -> `closed`

## Required Transitions

Every transition should preserve:

- Actor.
- Timestamp.
- Rationale.
- Evidence references when applicable.
- Previous and new state.

Phase 2 records this through append-only audit events with `event_type=finding_status_changed`. Risk acceptance transitions also create a `risk_acceptances` record and a `risk_accepted` audit event.

## Finding Sources

Findings may come from:

- Mock seed data.
- Manual assessment.
- Scanner adapter output.
- Uploaded report.
- Governance checklist.
- Bias/civil-rights review.

## Triage Questions

Operators should answer:

- Is the finding valid?
- Which system is affected?
- Which component is affected?
- What is the severity?
- How confident is the evidence?
- Who owns the response?
- Is deployment approval blocked?
- Is retest required?

## Evidence Rule

A finding should never stand alone. It should point to evidence, even if the evidence is a manual assessment note.

## Closure Rule

Closing a finding requires one of:

- Retest evidence.
- Risk acceptance.
- False-positive rationale.
- Governance decision with evidence reference.

Phase 2 enforces transition shape but does not yet enforce closure evidence completeness. That should become part of Phase 3 scoring and later governance maturity work.
