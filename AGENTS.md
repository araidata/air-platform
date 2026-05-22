# AI Agent Operating Rules

This file applies to Claude, Codex, Cursor, ChatGPT, Copilot, and future AI coding agents working in this repository.

## Mission

Build and maintain the County AI Assurance Operations Center as a practical internal platform for county AI governance, security, bias/civil-rights review, findings, evidence, assessments, reporting, and AI Review Board workflow.

The project is not a scanner engine and not a chatbot. It is the governance and orchestration layer around AI assurance work.

## Required Startup Routine

Every coding agent must read these files before making changes:

- `CLAUDE.md`
- `AGENTS.md`
- `CODEX.md`
- `docs/ai-context/current-state.md`

Then read the relevant domain docs for the task.

## Non-Negotiable Constraints

- Keep the system realistic for one Linux VM and Docker Compose.
- Assume one or two operators.
- Build mock-first.
- Keep findings and evidence central.
- Keep the platform API-first.
- Treat scanners as external tools.
- Use adapters for scanner integration.
- Preserve raw evidence.
- Avoid premature infrastructure.

Do not introduce Kubernetes, distributed systems, complex queues, microservices, or enterprise-scale team processes unless the user explicitly changes the project direction.

## Scanner Rules

Real scanner integrations must happen through adapters that can:

- Validate targets.
- Execute a scanner.
- Collect raw output.
- Normalize findings.
- Store evidence references.
- Map findings to frameworks.
- Calculate score impact.

Scanners are external executables, containers, or libraries. The platform should not copy scanner source code or tightly couple to scanner internals.

## Product Priorities

Build in this order:

1. Operational UI with mock data.
2. Findings, evidence, and assessment workflow.
3. Scoring.
4. Adapter framework.
5. First real scanner.
6. Bias and civil-rights workflow.
7. Governance exports and OneTrust support.
8. Operational maturity.

## Documentation Discipline

When implementing a change, keep the repo memory current. Update status docs and todos when the implementation state changes.

If a future agent is unsure whether to build infrastructure or workflow, choose workflow.
