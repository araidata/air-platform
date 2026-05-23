# Next Steps

The next development work should begin Phase 8: Governance Exports and OneTrust Workflow Support.

Phase 7 - Guided Operational UI Workflows is complete and verified. Operators can now use the UI for system intake, assessment launch, scanner execution, findings triage, evidence review, AIRB intake, and AIRB decisions without relying on Swagger for normal operations.

## Recommended Next Task

Implement governance exports without broadening infrastructure:

1. Add CSV exports for inventory, findings, assessments, and risk acceptances.
2. Add structured JSON governance exports.
3. Add audit packet export.
4. Draft OneTrust field mapping.
5. Support a manual OneTrust upload workflow before any API integration.

## Keep From Phase 7

- Keep workflows API-backed and operator-facing.
- Keep findings and evidence central.
- Keep scanner execution evidence-preserving and adapter-based.
- Keep AIRB decisions audit-friendly and linked to systems, assessments, findings, and evidence.

## Do Not Do Next

- Do not build a OneTrust API integration before export fields and manual workflow are stable.
- Do not integrate multiple additional scanners at once.
- Do not add Kubernetes, distributed workers, event buses, or continuous monitoring.
- Do not build scanner auto-scheduling or recurring assessments yet.
