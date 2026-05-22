# Scoring Methodology

Scores must be explainable. They exist to help operators and executives prioritize work, not to create a false sense of mathematical certainty.

## Score Domains

- Security Score.
- Privacy Score.
- Bias/Civil Rights Score.
- Explainability Score.
- Governance Evidence Score.
- Overall AI Governance Score.

Each score should be 0 to 100, where higher is better.

## Initial Weighting

Phase 3 implemented overall weighting:

- Security: 30 percent.
- Privacy: 20 percent.
- Bias/Civil Rights: 25 percent.
- Explainability: 10 percent.
- Governance Evidence: 15 percent.

Weights should be configurable later, but hard-coded defaults are acceptable in the first implementation.

The Phase 3 defaults are stored centrally in `apps/api/app/scoring/scoring_rules.py`.

## Finding Severity Impact

Suggested point deductions per open finding:

- Critical: 30 points.
- High: 18 points.
- Medium: 8 points.
- Low: 3 points.
- Informational: 0 points.

Deductions should be capped per domain so a score does not become impossible to interpret.

Phase 3 also applies deterministic status modifiers:

- Closed and false-positive findings do not reduce scores.
- Mitigated findings retain a small residual impact until fully closed.
- Findings awaiting retest or in remediation have reduced active impact.
- Risk-accepted findings retain a small governance impact.
- Failed retests, overdue due dates, and approval-blocking flags increase impact.

## Modifiers

Increase risk impact when:

- System is public-facing.
- System is rights-impacting.
- System is safety-impacting.
- System uses PII.
- System uses PHI.
- System uses CJIS.
- System has no human appeal path.
- Finding is overdue.
- Finding is reopened after failed retest.

Reduce risk impact when:

- Finding is verified remediated.
- Compensating controls are documented.
- Risk acceptance is approved and unexpired.
- Evidence is complete and current.

## Score Explanation Output

Every score should show:

- Current score.
- Prior score.
- Change direction.
- Top negative contributors.
- Top positive contributors.
- Missing evidence contributors.
- Open critical/high findings.
- Expiring exceptions.

## Phase 3 Persistence

Phase 3 stores:

- `domain_scores` for current domain and overall scores.
- `score_history` for score changes over time.
- `score_explanations` for finding, evidence, workflow, remediation, and aggregation explanations.
- `score_snapshots` for audit-ready score snapshots.

Every recalculation records audit events for score recalculation and meaningful score changes.

## Example Explanation

```text
Bias/Civil Rights Score: 62
Primary contributors:
- High severity language disparity finding on Public Benefits Chatbot: -18
- Missing human appeal path: -18
- Rights-impacting system modifier: -6
- Complete review evidence for HR Resume Screening AI: +5
```

## Remediation Influence Planning

The UI should help operators understand which remediations improve scores:

- Remediating critical security findings.
- Adding human appeal path evidence.
- Completing privacy review.
- Closing overdue findings.
- Retesting remediated findings.
- Expiring or renewing risk acceptances.
