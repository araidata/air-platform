# Frontend TODO

## Completed

- Created Next.js frontend scaffold under `apps/web`.
- Added application shell and navigation.
- Added centralized mock data module.
- Built Executive Dashboard.
- Built AI Inventory.
- Built Findings Queue.
- Built System Detail Page.
- Built Evidence & Audit Page.
- Built AI Review Board Queue starter view.
- Added frontend Dockerfile for the Phase 2.5 runtime.
- Added same-origin `/api/backend/*` proxy for backend connectivity in Docker Compose.
- Updated the frontend API client to use `NEXT_PUBLIC_API_URL`.
- Added Phase 3 score integrations for dashboard, system detail, findings queue, AI Review Board queue, and governance reports.
- Added frontend API client types and helpers for score APIs.
- Verified score views in Docker Compose.
- Added Phase 4 Scanner Ecosystem route for scanner registry, scan types, assessment profiles, recommendations, scanner runs, run detail, generated evidence counts, and mock execution.
- Added frontend API client types and helpers for scanner ecosystem APIs.
- Verified Scanner Ecosystem route in Docker Compose and Browser runtime.
- Implemented Phase 7 guided workflow route for system selection, assessment profile selection, governance domains, recommended scans, scanner execution, assessment creation, and AIRB routing.
- Implemented API-backed system intake, edit, and archive controls in the AI Inventory route.
- Implemented API-backed findings triage controls for owner assignment, due dates, remediation, lifecycle transitions, retest initiation, risk acceptance, false positives, and closure.
- Implemented API-backed evidence detail review with linked system, assessment, finding, scanner run, artifact references, raw text, and chain-of-evidence display.
- Implemented API-backed AIRB intake and decision controls for approvals, exceptions, blocked decisions, review indicators, decision notes, and exception expiration.
- Implemented API-backed system detail route for systems created from the UI.
- Added assessment target configuration to system intake, guided assessment launch, scanner execution, and system detail surfaces.
- Verified Phase 7 Docker runtime and browser workflows.

## Next

- Security Findings Dashboard.
- Settings / Integrations Page.
- Continue replacing remaining mock-only surfaces with API-backed operational data where the backend contracts are stable.

## UI Requirements

- Follow `docs/ui-ux/design-system.md`.
- Use operational density.
- Make findings and evidence easy to inspect.
- Avoid chatbot-first design.
- Avoid decorative AI styling.

## Deferred

- Authentication.
- Notification UI.
- Advanced reporting.
