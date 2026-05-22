# Next Steps

The next development work should begin Phase 3: Scoring Engine.

## Recommended Next Task

Add explainable scoring on top of the Phase 2 backend workflow records:

1. Define domain score inputs from findings, evidence completeness, retest state, system risk flags, and risk acceptances.
2. Implement a simple, explainable scoring service.
3. Persist score snapshots and explanation JSON.
4. Add score recalculation and score read endpoints.
5. Keep the frontend usable with mock data while the score API stabilizes.

## Why This Is Next

The Phase 2 backend now makes the core assurance records durable. The next highest-value step is turning those records into explainable scores without jumping ahead to scanner integrations or OneTrust support.

The scoring layer should clarify:

- How each finding affects security, privacy, bias/civil-rights, explainability, governance, agent safety, and RAG integrity scores.
- How overdue due dates, approval-blocking findings, public-facing systems, and sensitive data flags modify risk.
- How retest outcomes and risk acceptances change score explanations.
- Which score fields the executive dashboard and system detail pages need.

## Keep From Phase 1

- Centralized mock data remains the frontend source of truth until API-backed views are intentionally wired in.
- Findings and evidence stay central.
- Review board workflow stays operational and audit-friendly.
- Scanner outputs remain mock records only.
- The Phase 2 API client layer can be used when the frontend starts moving off mock data.

## Do Not Do Next

- Do not build OneTrust integration.
- Do not add Kubernetes.
- Do not build distributed jobs.
- Do not build real scanner adapters before the adapter framework.
- Do not build a chatbot-first UI.
