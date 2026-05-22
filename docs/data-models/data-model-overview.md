# Data Model Overview

This document describes the initial conceptual model and the Phase 2 implemented database model. Future migrations should refine names and constraints while preserving these domain boundaries.

## Core Entities

### Department

- ID.
- Name.
- Executive owner.
- Operational contact.

Status: deferred. Phase 2 stores department ownership directly on AI systems and owners.

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

Status: implemented as `ai_systems`.

### Assessment

- ID.
- System ID.
- Assessment type.
- Requested by.
- Status.
- Scope.
- Created at.
- Updated at.

Status: implemented as `assessments` with status values `draft`, `running`, `under_review`, `completed`, `blocked`, and `archived`.

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

Status: deferred to the scanner adapter phase.

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

Status: implemented as `findings` with explicit workflow transitions, due dates, retest status, score impact JSON, risk acceptance flag, approval-blocking flag, and owner assignment.

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

Status: implemented as `evidence` with links to findings, assessments, and systems. Database records store metadata and references; large artifacts remain external to the database.

### Score

- ID.
- System ID.
- Score domain.
- Value.
- Explanation JSON.
- Calculated at.

Status: deferred to Phase 3.

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

Status: implemented as `airb_reviews`.

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

Status: deferred.

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

Status: implemented as `risk_acceptances` for lifecycle support.

### Audit Event

- ID.
- Actor.
- Action.
- Entity type.
- Entity ID.
- Details JSON.
- Created at.

Status: implemented as append-only `audit_events`.

### Owner

- ID.
- Display name.
- Email.
- Department.
- Role.
- Created at.
- Updated at.

Status: implemented as `owners` for assignment and accountability, not authentication.

### Retest

- ID.
- Finding ID.
- Initiated by.
- Status.
- Notes.
- Result summary.
- Started at.
- Completed at.
- Created at.
- Updated at.

Status: implemented as `retests`.

### Framework Mapping

- ID.
- Finding ID.
- Framework.
- Control.
- Description.
- Created at.

Status: implemented as `framework_mappings`.

## Relationship Notes

- A system has many findings.
- A system has many assessments.
- An assessment has many scanner runs.
- A scanner run can produce many findings.
- A finding can have many evidence records.
- Evidence can attach to findings, assessments, systems, AIRB reviews, and approvals.
- Scores are recalculated from findings, evidence completeness, and system risk properties.
