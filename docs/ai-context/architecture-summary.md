# Architecture Summary

AI Assessment Scanner is a modular monolith deployed with Docker Compose on one Linux VM.

## Runtime Shape

- Frontend: Next.js + TypeScript.
- Backend: FastAPI.
- Database: PostgreSQL.
- Scanner execution: adapter-driven CLI/container execution.
- Evidence storage: local mounted storage first.
- Reporting: API-backed dashboards, PDF/export pipeline later.

## Core Modules

- Assessment intake.
- Risk profiles.
- Scanner runs.
- Findings.
- Evidence.
- Scoring.
- Review workflows.
- Executive reports.
- Control exports.

## Platform Responsibility

The platform owns:

- Assessment records.
- Risk profile inputs and scores.
- Scanner run metadata.
- Normalized findings.
- Evidence references and custody metadata.
- Human review decisions.
- Executive reporting.
- OpenControl-ready export data.

## External Tool Responsibility

External tools own:

- Model and prompt testing.
- Adversarial probing.
- Bias/fairness evaluation.
- RAG evaluation.
- Trace and observability capture.

Integrate external tools through adapters. Do not copy scanner source code or couple to unstable internals.
