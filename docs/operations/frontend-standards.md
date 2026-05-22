# Frontend Standards

## Framework

- Next.js App Router.
- React Server Components where useful.
- Client components for interactive tables, filters, dialogs, and charts.
- TypeScript everywhere.

## Styling

- TailwindCSS.
- shadcn/ui.
- Dark professional operational theme.
- Semantic severity colors.
- Dense but readable spacing.

## Tables

- Use TanStack Table.
- Support sorting, filtering, and pagination.
- Keep row actions compact.
- Include visible SLA and severity states.
- Avoid hiding operationally important data behind hover-only UI.

## Charts

- Use Recharts.
- Always include text summaries.
- Use charts to clarify risk posture, not decorate.

## Forms

- Use clear labels.
- Group fields by operational meaning.
- Validate required governance fields.
- Require rationale for approval, blocking, and exception actions.

## Accessibility

- Keyboard accessible queues.
- Sufficient contrast.
- Labels for controls.
- No color-only meaning.
