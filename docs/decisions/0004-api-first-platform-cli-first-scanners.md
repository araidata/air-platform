# ADR 0004: API-First Platform, CLI-First Scanners

## Status

Accepted.

## Context

The platform needs stable internal operations for systems, assessments, findings, evidence, scoring, reviews, reports, and integrations. External scanners often work best through CLIs or containers.

## Decision

The platform will be API-first. Scanner execution will initially be CLI/container-first through adapters.

## Consequences

- Core governance workflows have stable APIs.
- Scanner execution remains practical and inspectable.
- The platform can add API-based scanner integrations later when justified.

## Not Chosen

- Turning every scanner into an internal API service.
- Building scanner orchestration before workflow needs are proven.
