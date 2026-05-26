# System Overview

AI Assessment Scanner helps a county assess AI systems, run automated tests, preserve evidence, manage findings, route human review, and produce executive reports.

## System Role

The platform tracks:

- Which AI systems are being assessed.
- What risk profile applies.
- Which automated tests have run.
- What findings were produced.
- What evidence supports each finding.
- What remediation or review action is pending.
- What residual risk remains.
- What should appear in executive reporting or OpenControl export.

## Core Flow

1. Create or update an AI system record.
2. Complete assessment intake.
3. Calculate a risk profile.
4. Launch a scanner run or collect manual evidence.
5. Preserve raw artifacts.
6. Normalize findings.
7. Link evidence to findings and assessments.
8. Route human review and remediation.
9. Produce executive reporting.

## Boundary

The platform does not implement scanner logic internally. It orchestrates external tools and converts their outputs into assessment records, evidence, and findings.
