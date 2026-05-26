# Coding Guidelines

These guidelines apply to application and documentation changes.

## General

- Keep the application understandable by one or two operators and a small county development team.
- Prefer explicit domain types over clever abstractions.
- Keep files focused on one responsibility.
- Use predictable naming for systems, assessments, scanner runs, findings, evidence, risk profiles, and review workflows.
- Write code that preserves evidence references and audit trails.

## Architecture

- Keep the modular monolith.
- Keep domain modules clear.
- Expose stable API boundaries.
- Avoid microservices.
- Avoid distributed job infrastructure until a real operational need appears.
- Prefer boring, inspectable execution over invisible automation.

## Runtime Data Rules

- Use example systems only as development metadata.
- Use honest empty states until real assessments, findings, evidence, scanner runs, and scores exist.
- Keep development metadata realistic and clearly separate from operational records.

## Scanner Code Rules

- Do not embed scanner internals in the platform.
- Do not copy scanner source code.
- Treat scanner outputs as external data.
- Preserve raw logs and output.
- Normalize into the platform Finding schema.
- Keep adapters small and testable.

## Testing Direction

Prioritize tests for:

- Finding normalization.
- Evidence preservation.
- Score calculations.
- Status transitions.
- Scanner adapter parsing.
- API contract behavior.

## Documentation Updates

After meaningful changes, update:

- `docs/ai-context/implementation-status.md`
- The relevant `docs/todos/*.md`
- The README checklist when implementation work is completed and verified
- ADRs if a durable decision changed
