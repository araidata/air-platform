# Initial Product Pages

These are the first ten product pages. They define the operational shape of the platform before scanner integrations are implemented.

## 1. Executive Dashboard

Purpose: give leadership an immediate view of county AI assurance posture.

Required elements:

- AI Governance Score.
- Security Score.
- Bias/Civil Rights Score.
- Privacy Score.
- Explainability Score.
- Governance Evidence Score.
- Critical Findings count.
- High Risk Systems count.
- Systems Scanned count.
- Blocked Deployments count.
- Live Alerts list.
- Risk trend charts.
- Risk heatmap by department and domain.
- Top overdue remediation items.
- Systems pending AIRB review.

## 2. AI Inventory

Purpose: authoritative list of AI systems and their governance classifications.

Fields:

- System name.
- Department owner.
- Business purpose.
- Public-facing or internal.
- Rights-impacting.
- Safety-impacting.
- Uses PII.
- Uses PHI.
- Uses CJIS.
- Model provider.
- Model version.
- APIs.
- Tools.
- MCP servers.
- Deployment environment.
- Human review process.
- Risk tier.
- Approval status.

Core interactions:

- Filter by department, risk tier, approval status, data class, and public-facing status.
- Create and edit system records.
- Open system detail.
- Export inventory.

## 3. Findings Queue

Purpose: operational work queue for risk remediation and review.

Required columns:

- Severity.
- Finding title.
- Affected system.
- Domain.
- Owner.
- Workflow status.
- SLA due date.
- Evidence count.
- Framework mappings.
- Last updated.

Required filters:

- Severity.
- Domain.
- Owner.
- SLA status.
- Approval impact.
- System.
- Department.

## 4. System Detail Page

Purpose: single operational record for a governed AI system.

Sections:

- System overview.
- Risk classification.
- Model and tool dependencies.
- Data sensitivity.
- Human review process.
- Findings.
- Evidence.
- Assessment runs.
- Score history.
- AIRB decisions.
- Deployment approval history.
- Activity timeline.

## 5. Bias And Civil Rights Dashboard

Purpose: focus on protected-class, language access, and civil-rights risk.

Coverage:

- Race.
- Sex.
- Age.
- Disability.
- Religion.
- National origin.
- Language access.
- Veteran status.
- Socioeconomic proxy risk.

County use-case views:

- Public benefits.
- Permitting.
- Housing.
- HR screening.
- Law enforcement summaries.
- Emergency services.
- Citizen service chatbots.

## 6. Security Findings Dashboard

Purpose: focus on AI security and misuse risks.

Sections:

- Prompt injection.
- Data exfiltration.
- Excessive tool permissions.
- Model supply chain.
- RAG poisoning.
- Unsafe function/tool execution.
- Audit logging gaps.
- Sensitive data exposure.

## 7. AIRB Review Queue

Purpose: manage AI Review Board workflow.

States:

- Draft.
- Under Review.
- Security Review Required.
- Bias Review Required.
- Privacy Review Required.
- Legal Review Required.
- Approved.
- Approved with Exception.
- Blocked.

## 8. Evidence And Audit Page

Purpose: searchable evidence repository and chain-of-custody view.

Artifact types:

- Scanner output.
- Prompt sample.
- Model output.
- Screenshot.
- Configuration snapshot.
- Human review policy.
- AIRB decision.
- Report.
- Remediation proof.

## 9. Deployment Approval Page

Purpose: approve or block deployment based on current risk and evidence.

Required content:

- System summary.
- Current scores.
- Open critical/high findings.
- Required review states.
- Evidence checklist.
- Reviewer rationale.
- Exception conditions.
- Approval expiration if applicable.

## 10. Governance Reports Page

Purpose: generate repeatable reports for leadership and audit needs.

Initial reports:

- AI inventory report.
- High-risk systems report.
- Open findings report.
- Blocked deployments report.
- AIRB decision report.
- Evidence completeness report.
- Bias and civil-rights risk report.
- Scanner assessment summary report.
