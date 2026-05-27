# Scanner Integration Roadmap

Scanner integrations should be added one at a time through the adapter contract.

## Implemented

### garak

Purpose:

- Prompt injection-oriented testing.
- Red-team style prompt probes.
- Native report preservation.

Status:

- CLI adapter implemented.
- Native JSONL, hit log, HTML report, configuration, stdout/stderr, raw platform JSON, and normalized output are preserved.
- Findings normalize into existing Finding and Evidence workflows.

### Live HTTP Assessment Tester

Purpose:

- Endpoint-based adversarial prompt checks.
- Quick assessment of deployed HTTP AI endpoints.

Status:

- Implemented as an assessment workbench path.
- Preserves report artifacts and redacted request metadata.

### Giskard

- Hallucination testing.
- Bias/fairness testing.
- Prompt injection testing.
- RAG faithfulness testing.
- Business rule validation.

Status:

- Adapter implemented and Docker/runtime validated.
- Preserves raw output, reports, prompt/response records, logs, and trace manifest evidence.
- Normalizes real Giskard issues into existing Finding and Evidence workflows.
- Maps findings to NIST AI RMF, OWASP LLM Top 10, and OpenControl-ready controls where available.

### PyRIT

Purpose:

- Jailbreak testing.
- Prompt injection attacks.
- Unsafe content testing.
- Data exfiltration testing.
- Multi-turn adversarial testing.

Status:

- Adapter implemented and Docker/runtime validated.
- Preserves attack prompts, responses, logs, execution metadata, and trace manifest evidence.
- Normalizes only real concerning responses into existing Finding and Evidence workflows.

### Langfuse

Purpose:

- Trace capture.
- Prompt/output logging.
- Latency and cost metadata.
- Evidence references for assessment reports.

Status:

- Evidence pipeline implemented and Docker/runtime validated.
- Captures local trace manifests when Langfuse is unavailable.
- Attempts Langfuse trace/generation capture when SDK and credentials are present.

## Later

- Additional scanner adapters only when a concrete assessment workflow requires them.

## Not Included Early

- Scanner microservices.
- Distributed scanner scheduling.
- Continuous production monitoring.
