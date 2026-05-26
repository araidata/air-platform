# API-First Platform Strategy

The backend API is the contract between the UI, scanner orchestration, reporting, and future integrations.

## API Domains

- Systems.
- Assessments.
- Risk profiles.
- Scanner runs.
- Findings.
- Evidence.
- Review workflow.
- Reports.
- Exports.
- Framework mappings.

## Rules

- Keep workflows available through APIs before relying on UI-only behavior.
- Preserve raw evidence references in API responses where relevant.
- Keep scanner execution state explicit.
- Avoid scanner-specific response shapes in shared endpoints.
- Prefer additive changes to existing contracts.

## Future Integrations

Future integrations should consume stable assessment, finding, evidence, score, and report/export APIs. They should not become the source of truth for platform records.
