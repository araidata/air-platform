# Scanner Adapter Contract

This contract defines what every scanner adapter should provide. The base contract lives in `apps/api/app/scanners/adapters/base.py`, and the current real executable adapter is `apps/api/app/scanners/adapters/garak_adapter.py`.

## Phase 4 Implemented Contract

The implemented adapter protocol supports:

- `get_name()`
- `get_version()`
- `validate_configuration()`
- `execute()`
- `parse_output()`
- `normalize_findings()`
- `generate_evidence()`

Adapters receive a `ScannerExecutionContext` with the scanner run, system, risk tier, scan type, scan domain, and optional assessment profile. They return a `ScannerExecutionResult` containing execution status, raw structured output, execution logs, optional error message, and optional artifact metadata.

The `ScannerExecutionService` owns persistence, evidence generation, audit events, finding creation, and score recalculation. Adapters do not write directly to database workflow tables.

## Required Methods

### `validate_target()`

Confirms the target can be scanned safely and with enough configuration.

Should check:

- Target type.
- Required credentials or test endpoint.
- Allowed execution mode.
- Scope boundaries.
- Safety flags.

### `run_scan()`

Runs the scanner through Docker, CLI, or a controlled subprocess.

Should produce:

- Exit status.
- Start and end timestamps.
- Execution directory.
- Raw output references.
- Structured output references when available.

### `collect_raw_output()`

Collects stdout, stderr, generated files, logs, reports, and metadata.

Raw output must be preserved even when parsing fails.

### `normalize_findings()`

Converts scanner-specific output into normalized platform findings.

Should populate:

- Scanner name and version.
- Domain.
- Severity.
- Confidence.
- Title and description.
- Evidence summary.
- Raw evidence references.
- Affected component.
- Remediation.

### `store_evidence()`

Creates evidence records for raw output, logs, prompts, responses, uploaded artifacts, and generated reports.

### `map_to_frameworks()`

Maps findings to relevant frameworks such as NIST AI RMF, OWASP LLM, county policy controls, privacy checklist, or civil-rights review checklist.

### `calculate_score_impact()`

Returns explainable score impact by domain.

## Adapter Result Shape

```json
{
  "scanner_run_id": "scan_001",
  "scanner_name": "garak",
  "scanner_version": "example",
  "status": "completed",
  "raw_evidence_refs": ["evidence_raw_log_001"],
  "normalized_finding_ids": ["finding_001"],
  "score_impact": {
    "security": -8,
    "governance": -2
  }
}
```

## Error Handling

Adapters should distinguish:

- Target validation failure.
- Scanner execution failure.
- Timeout.
- Parser failure.
- Evidence storage failure.
- Normalization failure.

Whenever possible, preserve evidence before returning failure.

## Phase 5 Implementation

The first real scanner adapter is `garak_cli_adapter`. It adds only garak-specific CLI execution and JSONL parser logic. Persistence, evidence creation, finding creation, audit events, and score recalculation remain owned by `ScannerExecutionService` and the existing workflow services.
