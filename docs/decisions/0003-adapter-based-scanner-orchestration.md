# ADR 0003 - Adapter-Based Scanner Orchestration

## Status

Accepted.

## Context

The platform should orchestrate open-source scanners without reimplementing them or binding to unstable internals.

## Decision

Use scanner adapters that execute external scanners through Docker containers, subprocess wrappers, and CLI-first orchestration. Normalize all outputs into common finding and evidence schemas.

## Consequences

- Scanner integrations remain loosely coupled.
- Tool output changes are contained in adapters.
- Raw evidence can be preserved.
- Real integrations can wait until workflows are stable.
