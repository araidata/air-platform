# Frontend Implementation Plan

## Stack

- Next.js.
- React.
- TypeScript.
- TailwindCSS.
- shadcn/ui.
- Recharts.
- TanStack Table.

## App Sections

- Dashboard.
- Inventory.
- Findings.
- System detail.
- Bias and Civil Rights.
- Security Findings.
- AIRB Reviews.
- Evidence and Audit.
- Deployment Approvals.
- Governance Reports.

## Component Groups

- Layout shell.
- Navigation.
- Score cards.
- Risk heatmap.
- Trend charts.
- Operational tables.
- Filter bars.
- Detail headers.
- Evidence list.
- Audit timeline.
- Workflow transition dialogs.
- Report panels.

## First Implementation Order

1. App shell and navigation.
2. Dashboard with seeded metrics.
3. Inventory table.
4. System detail.
5. Findings queue.
6. Finding detail.
7. Evidence page.
8. AIRB queue.
9. Deployment approval page.
10. Reports page.

## Frontend Data Strategy

Use API calls even for seeded data once the backend exists. Before the backend exists, temporary fixtures are acceptable but must be easy to replace.
