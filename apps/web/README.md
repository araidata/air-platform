# County AI Assurance Operations Center Web App

Phase 1 frontend scaffold for the County AI Assurance Operations Center.

## Local Commands

```bash
npm run dev
npm run lint
npm run build
```

The app uses centralized mock data from `src/lib/mock-data.ts`. Do not add backend persistence, scanner execution, auth, OneTrust integration, Kubernetes, or distributed workers in this Phase 1 frontend.

## Implemented Routes

- `/` Executive Dashboard
- `/inventory` AI Inventory
- `/findings` Findings Queue
- `/systems/[id]` System Detail Page
- `/evidence` Evidence & Audit Page
- `/review-board` AI Review Board Queue
