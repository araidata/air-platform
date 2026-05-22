# Phase 4 AI Assessment Ecosystem Foundation

Phase 4 establishes the operational assessment ecosystem around scanners, scan controls, profiles, evidence, findings, scoring, and governance traceability.

## Implemented Components

- Scanner registry through `ScannerDefinition`.
- Scan type framework through `ScanType`.
- Assessment profile framework through `AssessmentProfile`.
- Scanner run persistence through `ScannerRun`.
- Scanner result persistence through `ScannerResult`.
- Adapter contract under `apps/api/app/scanners/adapters/base.py`.
- Deterministic mock adapter under `apps/api/app/scanners/adapters/mock_adapter.py`.
- Normalization layer under `apps/api/app/scanners/normalization/finding_normalizer.py`.
- Scanner execution service under `apps/api/app/scanners/services/scanner_execution_service.py`.
- Scanner Ecosystem frontend route under `apps/web/src/app/scanners/page.tsx`.

## Execution Flow

1. Create a scanner run.
2. Execute the selected adapter.
3. Preserve raw JSON output and execution logs.
4. Create evidence records for raw output and logs.
5. Parse scanner output.
6. Normalize scanner findings.
7. Create platform findings through the existing finding workflow.
8. Create evidence records for finding-level artifacts.
9. Record scanner audit events.
10. Trigger score recalculation through existing scoring hooks.

## Seeded Ecosystem

Phase 4 seeds:

- Mock AI Security Scanner.
- Mock Bias & Civil Rights Scanner.
- Mock Governance Evidence Scanner.
- Future-ready records for garak, AgentSeal, PyRIT, ModelScan, Fairlearn, Aequitas, IBM AI Fairness 360, Giskard, Ragas, DeepEval, and Promptfoo.
- Scan types across security, privacy, bias/civil-rights, explainability, governance, RAG integrity, agent safety, supply chain, and model integrity.
- Assessment profiles for public-facing chatbots, rights-impacting AI, law enforcement/CJIS AI, HR/employment AI, RAG applications, agentic/tool-using AI, and low-risk internal AI.
- Completed and failed mock scanner runs for seeded county systems.

## API Surface

- `GET /scanner-definitions`
- `GET /scanner-definitions/{id}`
- `POST /scanner-definitions`
- `PATCH /scanner-definitions/{id}`
- `GET /scan-types`
- `GET /scan-types/{id}`
- `POST /scan-types`
- `PATCH /scan-types/{id}`
- `GET /assessment-profiles`
- `GET /assessment-profiles/{id}`
- `POST /assessment-profiles`
- `PATCH /assessment-profiles/{id}`
- `GET /scanner-runs`
- `GET /scanner-runs/{id}`
- `POST /scanner-runs`
- `POST /scanner-runs/{id}/execute`
- `GET /scanner-results/{id}`
- `GET /scanner-adapters`
- `GET /systems/{id}/recommended-scans`
- `GET /systems/{id}/scanner-runs`

## Boundary

Phase 4 does not implement real scanner execution. Real scanner adapters begin in Phase 5 and must use this foundation rather than creating independent scanner workflows.
