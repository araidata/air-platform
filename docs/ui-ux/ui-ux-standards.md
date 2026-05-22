# UI/UX Standards

The product should feel like a government-grade security and assurance console: authoritative, calm, dense, readable, audit-friendly, and operational.

## Desired Feel

- CrowdStrike-like operational seriousness.
- Wiz-like risk visibility.
- Microsoft Defender-like security posture.
- Splunk-like investigation density.
- ServiceNow-like workflow accountability.

## Avoid

- Flashy AI gimmicks.
- Neon cyberpunk styling.
- Chatbot-first layout.
- Toy-like cards and oversized marketing sections.
- Decorative gradients as the main visual language.
- Vague "AI magic" copy.

## Use

- Dark professional dashboards.
- Dense but readable tables.
- Risk heatmaps.
- Executive scorecards.
- Drill-down investigation layouts.
- Clear evidence references.
- Workflow status badges.
- Audit trail timelines.
- Practical filters and saved views.

## Layout Standards

- Persistent left navigation.
- Top-level sections for Dashboard, Inventory, Findings, Evidence, AIRB, Approvals, Reports, and Settings.
- Dense tables with filtering, sorting, and column control.
- Detail pages with summary header, risk state, findings, evidence, activity, and decisions.
- Avoid nested cards.
- Use compact panels for operational content.
- Reserve large typography for executive dashboard headlines only.

## Component Standards

- shadcn/ui for primitives.
- Recharts for score trends and heatmaps.
- TanStack Table for operational queues.
- Icons for actions where familiar.
- Tooltips for icon-only controls.
- Badges for severity, approval state, risk tier, and SLA status.
- Tabs for detail page sections.
- Dialogs for focused workflow actions.

## Color Semantics

- Critical: strong red.
- High: red-orange.
- Medium: amber.
- Low: muted blue or neutral.
- Approved: green.
- Blocked: red.
- Under review: blue.
- Exception: amber.
- Unknown or incomplete: gray.

The palette should not become a one-note dark blue interface. Use semantic accent colors sparingly and consistently.

## Accessibility

- Ensure high contrast.
- Do not encode risk by color alone.
- Include labels and icons.
- Keyboard navigation must work for queues and dialogs.
- Tables need clear empty states.
- All charts need text summaries.
