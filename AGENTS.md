# AI Agent Operating Rules

This file applies to Claude, Codex, Cursor, ChatGPT, Copilot, and future AI coding agents working in this repository.

## Mission

Build and maintain AI Assessment Scanner: an internal county platform for AI risk profiling, automated testing, evidence collection, human review workflows, and executive reporting.

The project is not a chatbot, SOC/SIEM, enterprise governance suite, or scanner engine. It is the assessment and evidence layer around external AI testing tools.

## Required Startup Routine

Before making changes, read:

- `CLAUDE.md`
- `AGENTS.md`
- `CODEX.md`
- `docs/ai-context/current-state.md`

Then read only the domain docs relevant to the task.

## Non-Negotiable Constraints

- Keep the system realistic for one Linux VM and Docker Compose.
- Assume one or two operators.
- Keep findings and evidence central.
- Keep the platform API-first.
- Treat scanners as external tools.
- Use adapters for scanner integration.
- Preserve raw evidence.
- Keep demo metadata separate from operational records.
- Avoid premature infrastructure.

Do not introduce Kubernetes, distributed systems, complex queues, microservices, or enterprise-scale team processes unless the user explicitly changes the project direction.

## Scanner Rules

Real scanner integrations must happen through adapters that can:

- Validate targets.
- Execute a scanner or tester.
- Collect raw output.
- Normalize findings.
- Store evidence references.
- Map findings to frameworks.
- Calculate score impact.

Scanners are external executables, containers, or libraries. The platform should not copy scanner source code or tightly couple to scanner internals.

## Product Priorities

Build in this order:

1. Core platform foundation.
2. AI risk profiling.
3. Scanner orchestration.
4. Giskard integration.
5. PyRIT integration.
6. Langfuse evidence pipeline.
7. Human review workflows.
8. Executive reporting and OpenControl export.
9. Production readiness.

## Documentation Discipline

When implementation state changes, update `docs/ai-context/implementation-status.md`, the relevant todo file, and the README checklist when applicable.

Only mark a README checklist item complete after the work is implemented, verified, and reflected in status/todo documentation.

If a future agent is unsure whether to build infrastructure or assessment workflow, choose assessment workflow.
