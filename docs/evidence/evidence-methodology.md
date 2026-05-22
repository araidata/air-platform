# Evidence Methodology

Evidence is the basis for defensible governance. The platform should treat evidence as durable, searchable, and auditable.

## Evidence Types

- Raw scanner output.
- Normalized scanner finding.
- Prompt sample.
- Model output sample.
- Screenshot.
- Configuration snapshot.
- Model card or vendor documentation.
- Data handling documentation.
- Human review policy.
- Remediation proof.
- Retest output.
- AIRB decision record.
- Risk acceptance record.
- Generated report.

## Evidence Metadata

Every evidence record should include:

- Evidence ID.
- Artifact type.
- Related system.
- Related finding, assessment, or decision.
- Created by.
- Created at.
- Source.
- Storage URI.
- Hash.
- Size.
- MIME type where applicable.
- Sensitivity label.
- Retention category.
- Chain-of-custody events.

## Chain Of Custody

Custody events should capture:

- Created.
- Uploaded.
- Linked.
- Viewed.
- Exported.
- Superseded.
- Archived.

Each event should include actor, timestamp, action, and context.

## Local Storage First

Initial evidence storage can use a Docker volume mounted to the API service. PostgreSQL stores metadata and hashes. Later phases may move artifacts to object storage, but the database metadata model should not depend on the storage backend.

## Evidence Completeness

Evidence completeness should influence Governance Evidence Score. A system with critical decisions but missing supporting evidence should score lower even if findings are remediated.

## Sensitive Evidence

Evidence may contain PII, PHI, CJIS-related content, prompts, outputs, and screenshots. The first implementation should mark sensitivity and avoid casual broad export. Later phases should add stronger access controls.
