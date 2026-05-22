# Scanner Adapter Architecture

Scanners are external assessment engines. The platform orchestrates and governs them without tightly coupling to their internals.

## Planned Scanner Categories

Security and red teaming:

- AgentSeal.
- garak.
- PyRIT.
- ModelScan.

Bias and fairness:

- Fairlearn.
- Aequitas.
- IBM AI Fairness 360.
- Giskard.

LLM and RAG evaluation:

- Ragas.
- DeepEval.
- Promptfoo.

Observability and future:

- Langfuse.
- OpenTelemetry.
- MLflow.

## Adapter Responsibilities

Adapters should:

- Declare scanner name and version.
- Declare supported assessment types.
- Validate required inputs.
- Build CLI/container execution command.
- Execute scanner through Docker or subprocess wrapper.
- Capture stdout, stderr, exit code, and generated artifacts.
- Persist raw output as evidence.
- Normalize outputs into platform findings.
- Return scanner run metadata.

## Adapter Must Not

- Reimplement scanner logic.
- Depend on unstable scanner internals.
- Transform the platform into a scanner-specific application.
- Require scanner APIs before CLI execution is proven.
- Run as a distributed microservice in the initial architecture.

## Conceptual Interface

```text
ScannerAdapter
  name
  version
  capabilities
  validate(input)
  build_execution_plan(input)
  execute(plan)
  collect_artifacts(result)
  normalize(result, artifacts)
```

## Execution Model

Initial execution should support:

- Docker containers.
- CLI arguments.
- Mounted input/output directories.
- Timeouts.
- Exit code capture.
- Raw artifact preservation.

## Scanner Run Record

Scanner runs should capture:

- Scanner run ID.
- System ID.
- Assessment ID.
- Adapter name.
- Adapter version.
- Scanner image or command.
- Started at.
- Completed at.
- Status.
- Exit code.
- Raw output evidence ID.
- Normalized finding IDs.
- Error summary.

## Failure Handling

Failures should be operationally visible:

- Failed execution.
- Timed out.
- Invalid configuration.
- No findings.
- Partial results.
- Normalization failed.

Failures should create assessment run records but should not automatically create risk findings unless the failure itself indicates a governance gap.
