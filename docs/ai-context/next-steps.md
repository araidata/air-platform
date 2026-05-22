# Next Steps

The next development work should begin Phase 2: Findings, Evidence, and Assessment Workflow.

## Recommended Next Task

Add the first backend persistence and workflow mechanics behind the Phase 1 mock UI:

1. Define persisted records for systems, assessments, findings, evidence, and AI Review Board reviews.
2. Implement finding lifecycle status transitions.
3. Implement evidence records and evidence-to-finding links.
4. Track owners, due dates, retest status, risk acceptance references, and audit events.
5. Keep the frontend usable with mock data until the API contract is stable enough to replace it.

## Why This Is Next

The Phase 1 UI now shows the operating model. The next highest-value step is making the core assurance records durable without jumping ahead to scanner integrations or OneTrust support.

The workflow layer should clarify:

- Which fields are required for findings and evidence.
- How status changes are audited.
- How evidence supports closure, retest, and risk acceptance.
- Which API boundaries the frontend actually needs.
- How board decisions depend on evidence completeness.

## Keep From Phase 1

- Centralized mock data remains the frontend source of truth until APIs exist.
- Findings and evidence stay central.
- Review board workflow stays operational and audit-friendly.
- Scanner outputs remain mock records only.

## Do Not Do Next

- Do not build OneTrust integration.
- Do not add Kubernetes.
- Do not build distributed jobs.
- Do not build real scanner adapters before the adapter framework.
- Do not build a chatbot-first UI.
