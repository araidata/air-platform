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

## Next

- Assessment Workspace.
- Bias & Civil Rights Dashboard.
- Security Findings Dashboard.
- Settings / Integrations Page.
- Replace mock data with API-backed data after Phase 3 scoring contracts are stable enough for UI adoption.

## UI Requirements

- Follow `docs/ui-ux/design-system.md`.
- Use operational density.
- Make findings and evidence easy to inspect.
- Avoid chatbot-first design.
- Avoid decorative AI styling.

## Deferred

- Real backend integration.
- Authentication.
- Notification UI.
- Advanced reporting.
