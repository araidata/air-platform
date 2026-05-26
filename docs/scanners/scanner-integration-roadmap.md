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

## Next

### Giskard

Purpose:

- Hallucination testing.
- Bias/fairness testing.
- Prompt injection testing.
- RAG faithfulness testing.
- Business rule validation.

Acceptance criteria:

- Runs through scanner orchestration.
- Preserves raw output and reports.
- Normalizes findings.
- Links evidence.
- Maps findings to NIST AI RMF, OWASP LLM Top 10, and OpenControl-ready controls where available.

## Later

### PyRIT

Purpose:

- Jailbreak testing.
- Prompt injection attacks.
- Unsafe content testing.
- Data exfiltration testing.
- Multi-turn adversarial testing.

### Langfuse

Purpose:

- Trace capture.
- Prompt/output logging.
- Latency and cost metadata.
- Evidence references for assessment reports.

## Not Included Early

- Scanner microservices.
- Distributed scanner scheduling.
- Continuous production monitoring.
- Multiple new adapters in one implementation slice.
