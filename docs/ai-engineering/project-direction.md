# AI Engineering Project Direction

This is the authoritative AI engineering direction for AI Assessment Scanner. Agent-specific files may add workflow details, but they must not override this document.

## Product Purpose

AI Assessment Scanner is an internal county platform for assessing AI systems, testing them, collecting evidence, generating findings, supporting human review, and producing executive risk reporting.

The platform is assessment-first, testing-first, and evidence-first.

It is not:

- A broad governance suite.
- A review-board workflow platform.
- A specialized civil-rights platform.
- A chatbot platform.
- A SOC/SIEM.
- A multi-tenant SaaS platform.
- A scanner engine.

The platform orchestrates and records assessment work around external testing tools.

## Core Technical Stack

- FastAPI.
- PostgreSQL.
- Next.js + TypeScript.
- Docker Compose.
- Giskard.
- PyRIT.
- Langfuse.
- OpenControl / Compliance Masonry.

## Implementation Priorities

Prioritize:

1. Scanner execution.
2. Assessment workflows.
3. Evidence collection.
4. Findings generation.
5. Traceability.
6. Executive reporting.
7. Operational usability.

Current product priority order:

1. Core platform foundation.
2. AI risk profiling.
3. Scanner orchestration.
4. Giskard integration.
5. PyRIT integration.
6. Langfuse evidence pipeline.
7. Human review workflows.
8. Executive reporting and OpenControl export.
9. Production readiness.

Do not prioritize:

- Governance theater.
- Enterprise abstraction.
- Kubernetes.
- Distributed scaling.
- Complex RBAC before production readiness.
- Committee-style review workflows.
- Scanner integrations that bypass adapters.

## Terminology Standards

Preferred terms:

- Assessment.
- Scanner Run.
- Evidence.
- Finding.
- Risk Profile.
- Executive Report.
- Review Workflow.

Avoid or remove:

- Ecosystem language for scanners.
- Roadmap labels in UI copy.
- Governance as primary product framing.
- Specialized review-board language.
- Ambiguous generic platform language.
- Specialized civil-rights positioning.

Governance terms may appear only when they describe concrete review decisions, evidence, reports, or control mappings.

## Scanner Integration Rules

Scanners are external executables, containers, or libraries. The platform must not copy scanner source code or tightly couple to scanner internals.

Real scanner integrations must use adapters that can:

- Validate targets.
- Execute a scanner or tester.
- Collect raw output.
- Preserve evidence references.
- Normalize findings.
- Map findings to frameworks.
- Calculate score impact.

## Mock And Demo Policy

Mock or demo behavior is allowed only for development and testing.

Mock/demo records must:

- Never appear operationally real.
- Never fabricate findings in production mode.
- Always be clearly identified.
- Stay separate from operational assessment records.

Prefer honest empty states over fake operational activity.

## Operational Philosophy

Optimize for:

- Operational truth.
- Evidence integrity.
- Realistic assessment workflows.
- Scanner validation.
- Maintainability.
- County operational use.
- One Linux VM.
- Docker Compose.
- One or two operators.

Avoid premature infrastructure and broad platform abstractions.

## AI Coding Expectations

Future AI-assisted development must:

- Read this document before making direction-sensitive changes.
- Preserve the modular monolith architecture.
- Keep changes narrow and verifiable.
- Avoid unnecessary rewrites.
- Avoid broad repository scans unless the task requires them.
- Avoid duplicate direction documents.
- Avoid architecture drift.
- Avoid reintroducing governance-heavy concepts.
- Keep findings, evidence, assessments, scanner runs, risk profiles, review workflows, and reports consistent across UI, API, data models, and docs.
- Update status documentation when implementation state changes.

When unsure whether to build infrastructure or improve the assessment workflow, improve the assessment workflow.
