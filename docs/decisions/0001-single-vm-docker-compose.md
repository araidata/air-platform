# ADR 0001: Single VM And Docker Compose

## Status

Accepted.

## Context

This platform is intended for one or two county operators. It should be deployable and maintainable without a large platform engineering team.

## Decision

The initial production architecture will target one Linux VM using Docker Compose.

## Consequences

- Easier deployment.
- Easier backup and inspection.
- Lower operational burden.
- Clearer fit for a small internal tool.

## Not Chosen

- Kubernetes.
- Multi-node clusters.
- Distributed scanner workers.
- Cloud-native platform complexity before need exists.
