# Normalization Strategy

Normalization turns varied scanner outputs, manual review notes, and assessment observations into a stable platform finding model.

## Why Normalize

Different tools report different shapes of data. Governance workflows need one consistent model for triage, ownership, scoring, evidence, review, and reporting.

## Inputs

- Mock findings.
- Manual findings.
- Scanner CLI output.
- Scanner JSON output.
- Uploaded reports.
- Assessment checklist results.
- Bias/civil-rights review notes.

## Normalization Output

All inputs should become normalized findings with:

- Stable IDs.
- System and assessment links.
- Scanner/source metadata.
- Domain.
- Severity.
- Confidence.
- Human-readable title and description.
- Evidence summary.
- Raw evidence references.
- Framework mappings.
- Remediation guidance.
- Owner and status.
- Retest status.
- Score impact.

## Preserve Raw Data

Normalization must not destroy scanner-specific data. Store raw output and parser metadata as evidence. Keep scanner-specific fields in constrained metadata, not in the core workflow model.

## Severity And Confidence

Severity should express impact. Confidence should express how reliable the evidence is. Do not use severity to hide uncertainty.

## Framework Mapping

Initial mapping targets:

- NIST AI RMF.
- NIST Cybersecurity Framework.
- OWASP Top 10 for LLM Applications.
- County AI policy controls.
- Civil-rights review checklist.
- Privacy review checklist.

## Failure Handling

If parsing fails:

- Preserve raw output.
- Mark scanner run as parse_failed.
- Create no finding unless a safe fallback parser can identify one.
- Surface the failure to the operator.
