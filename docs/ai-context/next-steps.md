# Next Steps

The next implementation focus should be Giskard integration.

## Recommended Next Task

Implement the first Giskard adapter slice through the existing scanner orchestration framework.

Target scope:

1. Add `giskard_adapter` configuration and target validation.
2. Support hallucination and prompt-injection checks first.
3. Execute through a local CLI/container-friendly path.
4. Preserve raw output, logs, configuration, and reports as evidence.
5. Normalize Giskard results into Findings.
6. Map findings to NIST AI RMF, OWASP LLM Top 10, and OpenControl-ready controls where available.
7. Add fixture coverage for success, no-finding, invalid-target, and parser-failure paths.

## Keep

- Assessment-first workflow.
- Raw evidence preservation.
- Existing scanner adapter contract.
- Existing Finding and Evidence models.
- Synchronous local execution until operational need proves otherwise.
- Clear separation between development metadata and operational records.

## Do Not Do Next

- Do not add PyRIT before Giskard has a stable adapter path.
- Do not add Langfuse before scanner evidence capture remains stable.
- Do not create scanner microservices.
- Do not add Kubernetes or distributed queues.
- Do not create fabricated scanner runs, findings, evidence, or scores for demos.
