# ADR 0002: Adapter-Based Scanner Architecture

## Status

Accepted.

## Context

The platform should support scanners such as AgentSeal, garak, PyRIT, ModelScan, Fairlearn, Aequitas, Giskard, Ragas, DeepEval, and Promptfoo.

These tools already own specialized testing logic.

## Decision

Scanner integrations will use adapters. Adapters execute or ingest external scanner output, preserve evidence, normalize findings, map frameworks, and calculate score impact.

## Consequences

- Scanner logic stays outside the platform.
- Tool-specific output becomes normalized.
- Raw evidence remains available.
- New scanners can be added without reshaping the workflow model.

## Not Chosen

- Rewriting scanner tools.
- Copying scanner source code.
- Creating scanner microservices by default.
