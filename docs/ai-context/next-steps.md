# Next Steps

The next development work should begin Phase 4: Scanner Adapter Framework.

Phase 3 — Scoring Engine is complete and verified. The Docker Compose runtime starts the frontend, backend, and PostgreSQL together; applies the Phase 3 scoring migration; loads seeded operational data; calculates score records; and passes runtime score API and frontend score-view checks.

## Recommended Next Task

Add the scanner adapter framework without integrating a real scanner yet:

1. Define the adapter interface and execution contract.
2. Add scanner run records.
3. Implement a mock scanner adapter.
4. Capture mock raw output and logs as evidence.
5. Normalize mock scanner output into findings.
6. Reuse the scoring recalculation hooks after findings are created.

## Why This Is Next

The platform now has durable findings, evidence, workflow state, audit events, and explainable scores. A mock scanner adapter is the safest next step because it proves scanner orchestration and normalization without coupling the platform to any real scanner internals.

## Keep From Phase 3

- Scores must remain deterministic, explainable, and evidence-backed.
- Scanner output should become evidence and normalized findings before affecting scores.
- Recalculation should stay service-layer and synchronous until real operational load proves otherwise.
- The frontend can remain mock-first while API contracts stabilize.

## Do Not Do Next

- Do not integrate a real scanner before the adapter contract and mock workflow exist.
- Do not add Kubernetes.
- Do not add distributed jobs.
- Do not build OneTrust API integration.
- Do not build a chatbot-first UI.
