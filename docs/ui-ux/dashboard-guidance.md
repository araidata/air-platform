# Dashboard Guidance

Dashboards should help operators decide what needs attention.

## Executive Dashboard

Show:

- Overall AI risk posture.
- Systems by risk tier.
- Open critical/high findings.
- Approval blockers.
- Evidence completeness.
- Review queue count.
- Recent changes.

Avoid:

- Vanity metrics.
- Large empty charts.
- Vague AI maturity scores without evidence.

## Analyst Dashboard

Show:

- Findings requiring triage.
- Findings by domain.
- Scanner or assessment coverage.
- Evidence gaps.
- Retest queue.
- Systems with missing approvals.

## Bias & Civil Rights Dashboard

Show:

- Rights-impacting systems.
- Language access findings.
- Human appeal path status.
- Protected class assessment status.
- Open bias/civil-rights findings.

## Security Findings Dashboard

Show:

- Prompt injection findings.
- Tool permission issues.
- Supply chain and model file findings.
- Sensitive data leakage concerns.
- Retest status.

## Design Rule

Every dashboard element should answer an operational question. If it does not guide a decision or reveal risk, leave it out.
