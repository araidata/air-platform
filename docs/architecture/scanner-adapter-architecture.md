# Scanner Adapter Architecture

Scanner adapters are the boundary between the platform and external security, fairness, model scanning, and evaluation tools.

## Purpose

Adapters allow the platform to run or ingest scanner output without becoming the scanner.

The platform should:

- Validate scan targets.
- Start scanner execution.
- Capture raw output.
- Preserve logs.
- Normalize findings.
- Store evidence references.
- Map findings to frameworks.
- Calculate score impact.

The platform should not:

- Rewrite scanner logic.
- Copy scanner source code.
- Depend on private scanner internals.
- Turn every scanner into a separate API service too early.

## Adapter Lifecycle

1. Receive scan request.
2. Validate target and configuration.
3. Create isolated execution directory.
4. Execute Docker container or CLI subprocess.
5. Collect raw output and logs.
6. Parse structured output when available.
7. Normalize findings.
8. Store evidence records.
9. Map to frameworks.
10. Return scanner run summary and score impact.

## Adapter Interface

Adapters should support:

- `run_scan()`
- `validate_target()`
- `collect_raw_output()`
- `normalize_findings()`
- `store_evidence()`
- `map_to_frameworks()`
- `calculate_score_impact()`

## Adapter Types

- Mock adapter for Phase 4.
- CLI adapter for scanners with command-line runners.
- Docker adapter for scanner containers.
- Import adapter for manually uploaded scanner output.
- API adapter later only when the external tool has a stable API and operational need.

## Evidence Rule

Every scanner run must preserve raw output and logs even when parsing fails. A failed scan can still produce useful evidence.
