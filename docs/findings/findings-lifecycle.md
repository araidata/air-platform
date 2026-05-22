# Findings Lifecycle

Findings are the core operational unit of the platform.

## Lifecycle States

- `new`: Finding has been created and needs triage.
- `triaged`: Operator reviewed severity, owner, and evidence.
- `assigned`: Owner is responsible for remediation or response.
- `in_remediation`: Fix or mitigation is underway.
- `risk_accepted`: Authorized reviewer accepted the risk.
- `ready_for_retest`: Remediation is complete and needs validation.
- `retest_passed`: Finding has been validated as resolved.
- `retest_failed`: Finding still reproduces or evidence is insufficient.
- `closed`: Finding is resolved, accepted, or otherwise complete.
- `false_positive`: Finding is not valid, with rationale preserved.

## Required Transitions

Every transition should preserve:

- Actor.
- Timestamp.
- Rationale.
- Evidence references when applicable.
- Previous and new state.

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
