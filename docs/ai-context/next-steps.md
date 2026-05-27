# Next Steps

The next implementation focus should be reporting polish and production-readiness hardening.

## Recommended Next Task

Improve report outputs and operational hardening without expanding governance workflow scope.

Target scope:

1. Add residual-risk visualization and report export polish.
2. Improve production logging and monitoring guidance.
3. Add backup/recovery runbook details.
4. Keep scanner execution evidence-first and avoid new workflow abstractions.

## Keep

- Assessment-first workflow.
- Raw evidence preservation.
- Existing scanner adapter contract.
- Existing Finding and Evidence models.
- Synchronous local execution until operational need proves otherwise.
- Clear separation between development metadata and operational records.

## Do Not Do Next

- Do not create scanner microservices.
- Do not add Kubernetes or distributed queues.
- Do not create fabricated scanner runs, findings, evidence, or scores for demos.
