# Next Steps

The next development work should begin Phase 1: Operational UI and Mock Data.

## Recommended Next Task

Create the first frontend scaffold and mock-data-driven operational pages:

1. Executive Dashboard.
2. AI Inventory.
3. Findings Queue.
4. System Detail Page.
5. Evidence & Audit Page.

This should validate navigation, information density, risk presentation, findings triage, and evidence visibility before backend persistence exists.

## Why This Is Next

The project needs an operational surface before real integrations. If scanner work starts too early, the repo risks becoming a scanner experiment collection instead of a governance platform.

The UI will clarify:

- What data needs to exist.
- How findings should be triaged.
- How evidence should be displayed.
- How risk scoring should be explained.
- What backend APIs are actually needed.

## Mock Data To Include

Seed systems:

- Public Benefits Chatbot.
- Sheriff Incident Summary Assistant.
- Permit Review Assistant.
- HR Resume Screening AI.
- Citizen Services RAG Chatbot.

Seed findings:

- Prompt injection vulnerability.
- Spanish-language explanation disparity.
- Missing human appeal path.
- Excessive MCP/tool permissions.
- Incomplete audit logging.
- Possible sensitive data leakage.
- Weak governance evidence.
- Missing risk acceptance.
- Missing retest documentation.

## Definition Of Done For Phase 1 Start

- App scaffold exists.
- Mock data is centralized.
- Initial pages render from mock data.
- No real scanner integration is attempted.
- UI follows `docs/ui-ux/design-system.md`.
- Status docs are updated.

## Do Not Do Next

- Do not build OneTrust integration.
- Do not add Kubernetes.
- Do not build distributed jobs.
- Do not build real scanner adapters before the adapter framework.
- Do not build a chatbot-first UI.
