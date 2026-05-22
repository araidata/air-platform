# OneTrust Integration Plan

OneTrust integration is planned but intentionally deferred. The platform should first prove its own assessment, findings, evidence, scoring, and governance export workflows.

## Integration Goals

The platform may eventually sync or export:

- AI assessments.
- Governance exceptions.
- Risk acceptances.
- Findings.
- Evidence.
- Control mappings.
- Approval status.
- Audit packets.

## Recommended Sequence

### 1. CSV Export First

Create operational CSV exports that map platform records into fields OneTrust or governance staff can upload manually.

Use for:

- AI system inventory.
- Findings register.
- Risk acceptances.
- Assessment summary.
- Control mappings.

### 2. Structured JSON Export Second

Create JSON packages that preserve relationships between systems, assessments, findings, evidence, approvals, and audit packets.

Use for:

- Repeatable exports.
- Future API mapping.
- Internal backups.
- Review packet generation.

### 3. Manual Upload Workflow

Document how an operator exports a packet and uploads it to OneTrust or another governance system.

This is realistic for one or two operators and avoids premature API coupling.

### 4. API Integration Later

Only build API integration after:

- Core platform workflows exist.
- OneTrust field mapping is validated.
- CSV/JSON exports are useful.
- Authentication and sync rules are understood.

## Likely Mapping Areas

- Platform system -> OneTrust AI asset or inventory item.
- Assessment -> OneTrust assessment record.
- Finding -> Issue, risk, or control gap.
- Evidence -> Attachment or evidence reference.
- Risk acceptance -> Exception or approval record.
- Framework mapping -> Control mapping.
- AI Review Board decision -> Approval status.

## Design Rules

- Do not make OneTrust the source of truth at the beginning.
- Do not block core platform workflow on OneTrust availability.
- Preserve export history.
- Keep field mappings configurable where practical.
- Support manual review before upload.

## Deferred Until Later

- Bidirectional sync.
- Automated attachment sync.
- Real-time status updates.
- Complex conflict resolution.
- Deep OneTrust API dependency.
