# ADR 0002 - Docker Compose On A Single Linux VM

## Status

Accepted for initial implementation.

## Context

The platform is intended for a small county operating team, not a hyperscale SaaS environment.

## Decision

Use Docker Compose on one Linux VM for the initial platform.

## Consequences

- Operational simplicity.
- Lower maintenance burden.
- Faster local development.
- Easier troubleshooting.
- Kubernetes and distributed workers remain deferred until there is proven operational need.
