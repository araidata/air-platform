# Scanner Execution Model

Scanner execution should be simple, inspectable, and evidence-preserving.

## Preferred Execution

- CLI wrappers.
- Dockerized scanner containers where practical.
- Isolated per-run directories.
- Explicit target configuration.
- Timeouts and resource limits where available.
- Structured output when the scanner supports it.

## Run Directory

Each scanner run should write artifacts under the configured scanner storage root.

```text
scanner-runs/
  <scanner-run-id>/
    input/
    output/
    logs/
    raw-output.json
    normalized-output.json
    evidence-manifest.json
    run-metadata.json
```

## Captured Artifacts

Capture:

- Scanner configuration with secrets redacted.
- Scanner version.
- Command or execution plan with secrets redacted.
- Start and end timestamps.
- stdout and stderr.
- Native JSON, JSONL, HTML, text, or report files.
- Prompt and response samples when relevant.
- Trace references when supplied by Langfuse or similar tools.

## Optional Scanner Runtimes

The Docker image installs garak and PyRIT in the backend scanner runtime. Giskard is installed in an isolated Python environment because current Giskard 2.x dependencies require NumPy 1.x while garak 0.15 requires NumPy 2.x.

Runtime files:

- `apps/api/requirements-scanners.txt`
- `apps/api/requirements-pyrit-langfuse.txt`
- `apps/api/requirements-giskard.txt`

Set `GISKARD_PYTHON` to the isolated runtime's Python executable when overriding the Docker default.

## Failure Behavior

If execution fails:

- Preserve logs and partial output.
- Mark the run status clearly.
- Show operator-readable failure reason.
- Do not create unsupported findings.
- Allow rerun after configuration correction.

## Security Notes

- Redact secrets from logs and persisted config.
- Never pass raw user input into a shell command.
- Treat scanner output as untrusted input.
- Keep scanner targets allowlisted or explicitly declared.
