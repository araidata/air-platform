# Development Sequence

This sequence turns the phase plan into a practical build order for future agents.

## 1. Establish Frontend Shell

- Create the app scaffold.
- Add navigation for initial pages.
- Add mock data.
- Build layout and design tokens.
- Render executive dashboard first.

## 2. Build Mock Operational Pages

- AI Inventory.
- Findings Queue.
- System Detail Page.
- Evidence & Audit Page.
- AI Review Board Queue.
- Reports Page.
- Settings / Integrations Page.

Each page should render realistic county data and expose the fields future APIs must provide.

## 3. Define Backend API Contracts

- Systems API.
- Assessments API.
- Findings API.
- Evidence API.
- Scanner Runs API.
- Reviews API.
- Reports API.

Start from the UI data needs. Avoid backend-first guessing.

## 4. Add Persistence

- PostgreSQL schema.
- Seed data.
- Basic CRUD APIs.
- Status transitions.
- Audit events.

## 5. Stabilize Runtime

- Docker Compose startup.
- Frontend container.
- Backend API container.
- PostgreSQL container and named volume.
- Container migration and seed startup flow.
- Runtime smoke tests.

## 6. Add Scoring

- Domain score inputs.
- Finding severity and confidence impact.
- Governance evidence completeness.
- Score history.
- Explanation text.

## 7. Add Adapter Framework

- Adapter interface.
- Mock adapter.
- Scanner run directory structure.
- Evidence capture.
- Normalization path.

## 8. Add One Real Scanner

Pick one scanner. Prefer garak or AgentSeal. Integrate through Docker/CLI execution and normalize results.

## 9. Add Governance Exports

- CSV first.
- JSON second.
- Audit packet packaging.
- OneTrust field mapping.

## Sequencing Rule

If two tasks compete, choose the task that improves findings, evidence, assessment workflow, or auditability.
