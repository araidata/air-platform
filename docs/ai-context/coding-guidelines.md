# Coding Guidelines

These guidelines apply once application code begins.

## General

- Keep the application understandable by one or two operators and one AI-assisted maintainer.
- Prefer explicit domain types over clever abstractions.
- Keep files focused on one responsibility.
- Use predictable naming for systems, assessments, findings, evidence, scanner runs, and review workflows.
- Write code that preserves audit trails and evidence references.

## Architecture

- Build a modular monolith first.
- Keep domain modules clear.
- Expose stable API boundaries.
- Avoid microservices.
- Avoid distributed job infrastructure until a real operational need appears.
- Prefer boring, inspectable execution over invisible automation.

## Bootstrap And Empty-State Rules

- Use example systems only for inventory/bootstrap metadata.
- Use honest empty states until real findings, evidence, and scanner results exist.
- Keep bootstrap metadata realistic and aligned with county use cases.

## Scanner Code Rules

- Do not embed scanner internals in the platform.
- Do not copy scanner source code.
- Treat scanner outputs as external data.
- Preserve raw logs and output.
- Normalize into the platform finding schema.
- Keep adapters small and testable.

## Testing Direction

When code exists, prioritize tests for:

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
- ADRs if a durable decision changed
