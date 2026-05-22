# Phase 5 garak Integration

Phase 5 integrates garak as the first real scanner.

## Selection

garak was selected ahead of AgentSeal because it has a documented CLI, native JSONL reports, a hit log, an HTML report, and deterministic local test targets that run inside the existing Docker Compose backend without credentials.

## Runtime

- Adapter: `apps/api/app/scanners/adapters/garak_adapter.py`
- Scanner definition adapter name: `garak_cli_adapter`
- Execution mode: local CLI inside the backend container
- Docker dependency file: `apps/api/requirements-scanners.txt`
- Artifact root: `SCANNER_STORAGE_ROOT`, defaulting to `/data/scanner-runs`

The default Phase 5 validation run uses garak's deterministic `test.Repeat` target with `promptinject.HijackLongPrompt` so the end-to-end path produces a real garak eval finding without external model credentials.

## Evidence Preserved

Each garak run preserves:

- Native garak report JSONL.
- Native garak hit log JSONL.
- Native garak HTML report.
- Scanner configuration JSON.
- stdout/stderr execution log.
- Platform raw output JSON.
- Platform normalized output JSON.

Evidence records are created through the existing evidence service and include the scanner run ID in metadata.

## Normalization

The adapter parses garak JSONL `eval` records and converts non-zero attack success rates into normalized scanner findings. The existing normalizer then maps them into platform finding fields, evidence references, score impacts, and source metadata.

## Scoring

Findings created from garak use the existing finding workflow service. Score recalculation, score explanations, score history, and audit events are triggered by the existing services; garak does not own scoring logic.
