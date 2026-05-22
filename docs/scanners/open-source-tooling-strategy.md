# Open Source Tooling Strategy

The platform should use strong open source tools where they already exist. It should not recreate them.

## Security / Red Teaming

Planned support:

- AgentSeal.
- garak.
- PyRIT.
- ModelScan.

Use these tools for attack simulation, prompt injection testing, red-team probes, and model artifact scanning.

## Bias / Fairness

Planned support:

- Fairlearn.
- Aequitas.
- IBM AI Fairness 360.
- Giskard.

Use these tools to support fairness calculations, bias testing, dataset checks, and civil-rights-oriented assessment evidence.

## LLM / RAG Evaluation

Planned support:

- Ragas.
- DeepEval.
- Promptfoo.

Use these tools for RAG quality checks, regression tests, prompt evaluations, hallucination checks, and answer quality testing.

## Observability / Future

Future support:

- Langfuse.
- OpenTelemetry.
- MLflow.

Use these later for traces, evaluation history, model run metadata, and operational telemetry.

## Integration Pattern

Tools should eventually integrate through:

- Scanner adapters.
- Docker execution.
- CLI wrappers.
- Result parsers.
- Normalized findings.
- Evidence storage.

## Do Not Do

- Do not copy scanner source into the platform.
- Do not rewrite scanner internals.
- Do not make each scanner a microservice early.
- Do not let scanner-specific fields distort the core findings model.

The platform is the governance layer. The tools perform specialized testing.
