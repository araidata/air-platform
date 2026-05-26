# Scanner Adapter Architecture

Scanners are external assessment tools. The platform integrates them through adapters so scanner-specific behavior does not leak into core assessment, finding, evidence, or reporting models.

## Plugin Model

Each adapter declares:

- Adapter name and version.
- Supported target types.
- Supported test categories.
- Required configuration.
- Execution mode.
- Output parser.
- Evidence artifact types.
- Finding normalization behavior.

Adapters are loaded by the scanner orchestration service. They do not write directly to workflow tables.

## Adapter Responsibilities

- Validate target and configuration.
- Build a safe execution plan.
- Run the scanner through CLI, container, or stable library API.
- Capture stdout, stderr, generated files, reports, prompts, and responses.
- Preserve raw artifacts.
- Parse structured output.
- Normalize findings.
- Return scanner run metadata.

## Adapter Must Not

- Reimplement scanner logic.
- Depend on unstable scanner internals.
- Bypass evidence storage.
- Bypass normalized Finding records.
- Run as a separate microservice in the initial architecture.

## Target Integrations

- Giskard for hallucination, bias/fairness, prompt injection, RAG faithfulness, and business-rule validation.
- PyRIT for jailbreak, prompt injection, unsafe content, data exfiltration, and multi-turn adversarial testing.
- Langfuse for trace and prompt/output evidence references.
- garak for prompt-injection-oriented testing already implemented.

## Failure Handling

Failures should be visible and evidence-preserving:

- Invalid target.
- Execution failed.
- Timed out.
- Parser failed.
- No findings.
- Partial results.

Failed runs should not create risk findings unless the failure itself represents an assessment issue.
