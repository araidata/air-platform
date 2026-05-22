# GitHub Copilot Instructions

This repository is for County AI Assurance Operations Center, a small-operator county AI governance and assurance platform.

Copilot should optimize suggestions for:

- One Linux VM.
- Docker Compose.
- One or two operators.
- Mock-first development.
- API-first platform design.
- Findings, evidence, assessments, scoring, and governance workflows.
- Scanner adapters rather than embedded scanner logic.

Avoid suggestions that introduce:

- Kubernetes.
- Microservices.
- Distributed infrastructure.
- Enterprise SaaS assumptions.
- Large-team workflow complexity.
- Chatbot-first UI.

External scanners such as garak, AgentSeal, PyRIT, Fairlearn, Aequitas, Giskard, ModelScan, Ragas, DeepEval, and Promptfoo should be executed through adapters or CLI/container wrappers. Do not suggest copying or rewriting their internals.

Prefer readable, audit-friendly code and documentation. Preserve raw evidence and normalized findings as first-class concepts.
