# Scanner Adapter Contract

Every scanner integration must use the platform adapter contract. The platform owns assessment records, scanner runs, findings, evidence, scoring, and reporting. External tools own test execution.

## Required Adapter Capabilities

Adapters must:

- Declare name, version, supported targets, and supported test categories.
- Validate target configuration and scope.
- Execute the external scanner or tester.
- Collect raw output, logs, reports, prompts, responses, and configuration.
- Preserve artifacts before parsing.
- Parse scanner-specific output.
- Normalize findings into the platform Finding model.
- Create or return evidence references for raw artifacts.
- Map findings to NIST AI RMF, OWASP LLM Top 10, and OpenControl-ready controls where available.
- Return explainable score impact inputs.

## Execution Context

Adapters receive a context that includes:

- Assessment.
- Target system.
- Scanner run.
- Risk tier.
- Test category.
- Configuration.
- Storage root.

Adapters should not write directly to workflow tables. The scanner orchestration service owns persistence.

## Result Shape

Adapter results should include:

- Status.
- Started and completed timestamps.
- Scanner version.
- Exit code or execution result.
- Raw artifact metadata.
- Parsed output metadata.
- Normalized finding candidates.
- Error message when applicable.

## Error Classes

Use clear failure categories:

- Invalid target.
- Invalid configuration.
- Execution failed.
- Timeout.
- Parser failed.
- Evidence storage failed.
- No findings.
- Partial results.

Whenever possible, preserve raw evidence before returning failure.

## Target Integrations

- `garak_cli_adapter`: implemented.
- `giskard_adapter`: implemented; Docker installs Giskard in an isolated scanner runtime.
- `pyrit_adapter`: implemented; Docker installs PyRIT in the backend scanner runtime.
- Langfuse trace evidence pipeline: implemented as scanner-run evidence capture with graceful degradation when Langfuse credentials are unavailable.

## Prohibited Patterns

- Do not copy scanner source code into the platform.
- Do not reimplement scanner logic.
- Do not create scanner-specific finding tables unless a durable reporting need is proven.
- Do not bypass raw evidence preservation.
- Do not create scanner microservices for the initial deployment model.
