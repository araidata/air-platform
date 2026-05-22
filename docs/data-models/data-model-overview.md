# Data Model Overview

This document describes the initial conceptual model. Actual database migrations should refine names and constraints while preserving these domain boundaries.

## Core Entities

### Department

- ID.
- Name.
- Executive owner.
- Operational contact.

### AI System

- ID.
- Name.
- Department ID.
- Business purpose.
- Public-facing flag.
- Internal flag.
- Rights-impacting flag.
- Safety-impacting flag.
- Uses PII flag.
- Uses PHI flag.
- Uses CJIS flag.
- Model provider.
- Model version.
- APIs.
- Tools.
- MCP servers.
- Deployment environment.
- Human review process.
- Risk tier.
- Approval status.
- Created at.
- Updated at.

### Assessment

- ID.
- System ID.
- Assessment type.
- Requested by.
- Status.
- Scope.
- Created at.
- Updated at.

### Scanner Run

- ID.
- Assessment ID.
- Adapter name.
- Adapter version.
- Command or image reference.
- Status.
- Started at.
- Completed at.
- Exit code.
- Raw output evidence ID.
- Error summary.

### Finding

- ID.
- System ID.
- Assessment ID.
- Scanner Run ID.
- Title.
- Description.
- Severity.
- Domain.
- Status.
- Owner.
- SLA due date.
- Remediation guidance.
- Approval blocking flag.
- Created at.
- Updated at.

### Evidence

- ID.
- System ID.
- Finding ID.
- Assessment ID.
- AIRB Review ID.
- Artifact type.
- Source.
- Storage URI.
- Hash.
- Sensitivity.
- Created by.
- Created at.

### Score

- ID.
- System ID.
- Score domain.
- Value.
- Explanation JSON.
- Calculated at.

### AIRB Review

- ID.
- System ID.
- Status.
- Requested by.
- Required review domains.
- Decision.
- Rationale.
- Created at.
- Updated at.

### Deployment Approval

- ID.
- System ID.
- Status.
- Decision.
- Reviewer.
- Rationale.
- Conditions.
- Expiration date.
- Created at.
- Updated at.

### Risk Acceptance

- ID.
- Finding ID.
- System ID.
- Approver.
- Rationale.
- Conditions.
- Expiration date.
- Evidence ID.
- Created at.

### Audit Event

- ID.
- Actor.
- Action.
- Entity type.
- Entity ID.
- Details JSON.
- Created at.

## Relationship Notes

- A system has many findings.
- A system has many assessments.
- An assessment has many scanner runs.
- A scanner run can produce many findings.
- A finding can have many evidence records.
- Evidence can attach to findings, assessments, systems, AIRB reviews, and approvals.
- Scores are recalculated from findings, evidence completeness, and system risk properties.
