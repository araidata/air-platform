# Audit Packet Strategy

Audit packets package the records needed to explain an AI system's governance posture.

## Purpose

Audit packets should help a county answer:

- What is this AI system?
- Who owns it?
- What risks were assessed?
- What findings exist?
- What evidence supports the decision?
- What exceptions were accepted?
- What retesting was done?
- What approvals or blocks exist?

## Packet Contents

An audit packet may include:

- System inventory summary.
- Assessment summary.
- Risk score summary.
- Open and closed findings.
- Evidence index.
- Framework mappings.
- Review decisions.
- Risk acceptances.
- Retest records.
- Export manifest.

## Export Formats

Start with:

- CSV for tabular governance upload.
- JSON for structured transfer.
- PDF-ready or HTML packet later.

Do not start with a complex document-generation engine.

## Packet Rules

- Include evidence references, not just summaries.
- Include generated timestamp.
- Include version of scoring method if scores are included.
- Include unresolved findings and accepted risks.
- Keep packet generation repeatable.

## OneTrust Relationship

Audit packets should eventually support OneTrust upload or API sync, but manual CSV/JSON export is the first practical step.
