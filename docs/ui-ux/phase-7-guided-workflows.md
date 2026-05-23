# Phase 7 Guided Workflows

Phase 7 adds operator-facing workflow surfaces so normal assurance work can happen from the UI instead of Swagger.

## Guided Workflow

Use `/workflows` to:

- Select an existing AI system or jump to inventory management.
- Choose an assessment profile.
- Select governance domains.
- Review required and optional recommended scans.
- Choose a compatible scanner.
- Create an assessment.
- Optionally create and execute the first scanner run.
- Route the system to AIRB review.

## System Intake

Use `/inventory` to add, edit, and archive AI systems. The form captures owner/department, risk tier, approval status, public-facing/internal posture, rights and safety impact, PII/PHI/CJIS flags, model provider/version, deployment environment, and business purpose.

Archive behavior uses the existing system update API by setting `approval_status` to `archived`.

## Findings Review

Use `/findings` to triage findings. Operators can assign owners, manage due dates, update remediation notes, move findings through the existing lifecycle, request retests, accept risk, mark false positives, close findings, and inspect linked evidence.

## Evidence Review

Use `/evidence` to review evidence records. The detail panel shows source, linked system, linked assessment, linked finding, scanner run references, raw artifact paths, raw text where available, and a chain-of-evidence summary.

## AIRB Workflow

Use `/review-board` to create AIRB intake records and record board decisions. Operators can link systems and assessments, set review routing indicators, validate human review and appeal paths, record approved / approved with exception / blocked decisions, add notes, and set exception expiration dates.

## Verification Status

Frontend lint, build, lightweight Phase 7 route-contract tests, Docker runtime smoke testing, and browser workflow verification pass. Browser verification covered system creation, assessment launch, scanner execution with preserved artifacts, findings triage save, evidence chain detail, and AIRB intake/approval.
