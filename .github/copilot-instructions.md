# GitHub Copilot Instructions

This repository is AI Assessment Scanner.

`docs/ai-engineering/project-direction.md` is the canonical AI engineering direction. Follow it for product purpose, terminology, priorities, technical stack, mock/demo policy, and operational boundaries.

Copilot should optimize suggestions for:

- Assessment workflows.
- Scanner runs through adapters.
- Findings and evidence integrity.
- Risk profiles and executive reports.
- FastAPI, PostgreSQL, Next.js + TypeScript, and Docker Compose.
- Small-operator county use.

Avoid suggestions that introduce unnecessary rewrites, fake operational records, Kubernetes, microservices, distributed infrastructure, multi-tenant SaaS assumptions, large-team workflow complexity, chatbot-first UI, governance-heavy language, or scanner internals.

External scanners such as garak, Giskard, PyRIT, Langfuse, Fairlearn, Aequitas, ModelScan, Ragas, DeepEval, and Promptfoo should be executed through adapters or CLI/container wrappers. Do not suggest copying or rewriting their internals.

Prefer readable, audit-friendly code and documentation. Preserve raw evidence and normalized findings as first-class concepts.
