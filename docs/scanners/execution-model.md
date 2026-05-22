# Scanner Execution Model

The scanner execution model should be simple, inspectable, and safe enough for one Linux VM.

## Preferred Execution

Use:

- Dockerized scanner containers.
- CLI wrappers.
- Isolated execution directories.
- Structured JSON output where possible.
- Retained raw logs as evidence.

## Execution Directory

Each scanner run should get its own directory:

```text
scanner-runs/
  scan_2026_001/
    input/
    output/
    logs/
    evidence-manifest.json
    run-metadata.json
```

Phase 4 stores scanner artifacts in the configured `SCANNER_STORAGE_ROOT`. Docker Compose sets this to `/data/scanner-runs` and mounts the `scanner_data` volume at `/data`. Local non-Docker tests can override the storage root in `ScannerExecutionService`.

Phase 5 uses the same directory model for garak. A garak run stores the native garak artifacts under the scanner run directory and the platform also writes `raw-output.json`, `execution.log`, and `normalized-output.json`.

## Captured Artifacts

Capture:

- Command arguments, with secrets redacted.
- Scanner version.
- Container image digest if available.
- Start and end timestamps.
- stdout.
- stderr.
- JSON report.
- HTML or text report if generated.
- Prompt and output samples when relevant.

For garak, preserve:

- Native `*.report.jsonl`.
- Native `*.hitlog.jsonl`.
- Native `*.report.html`.
- Scanner configuration JSON.
- Platform raw output JSON.
- Platform normalized output JSON.
- Execution log with stdout and stderr.

## Isolation

Initial isolation should use:

- Per-run directories.
- Container execution.
- Timeouts.
- Resource limits where practical.
- Explicit allowlisted targets.

Do not build distributed orchestration until one-VM execution is insufficient.

## Failure Behavior

If a scan fails:

- Preserve logs.
- Preserve raw output when execution produced any structured output before parsing or normalization failed.
- Mark run status clearly.
- Do not create unsupported findings.
- Show operator-readable failure reason.
- Allow rerun after configuration fix.

## Security Notes

- Redact secrets from logs.
- Do not allow arbitrary shell commands from user input.
- Keep scanner configuration explicit.
- Treat scanner outputs as untrusted input.
