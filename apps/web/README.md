# County AI Assurance Operations Center Web App

Phase 1 frontend scaffold for the County AI Assurance Operations Center. Phase 2.5 adds a Docker runtime and same-origin backend proxy.

## Local Commands

```bash
npm run dev
npm run lint
npm run build
```

The app uses centralized mock data from `src/lib/mock-data.ts`. Do not add backend persistence, scanner execution, auth, OneTrust integration, Kubernetes, or distributed workers in this Phase 1 frontend.

## Docker Runtime

From the repository root:

```bash
docker compose up --build
```

The frontend container serves Next.js on port `3000` inside Docker. It proxies `/api/backend/*` to `NEXT_INTERNAL_API_URL`, which defaults to `http://backend:8000`.

Set `NEXT_PUBLIC_API_URL=/api/backend` for browser-safe API calls through the frontend origin.

## Implemented Routes

- `/` Executive Dashboard
- `/inventory` AI Inventory
- `/findings` Findings Queue
- `/systems/[id]` System Detail Page
- `/evidence` Evidence & Audit Page
- `/review-board` AI Review Board Queue
