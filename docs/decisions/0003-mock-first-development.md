# ADR 0003: Mock-First Development

## Status

Accepted.

## Context

The platform must first prove its operational workflow: inventory, assessments, findings, evidence, scoring, and review decisions.

Real scanners are useful only after those workflows can receive and explain results.

## Decision

Development started with mock systems and mock operational records during early scaffolding. Runtime mock findings, evidence, and scan results have since been retired in favor of real execution paths and honest empty states.

## Consequences

- Faster validation of UI and workflow.
- Better data model design.
- Reduced distraction from scanner-specific complexity.
- Easier AI-assisted development.

## Not Chosen

- Real scanner integration as first milestone.
- Backend-first implementation without UI workflow validation.
