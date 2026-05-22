# Scanner Integration Roadmap

Scanner integrations should begin after workflows, evidence, and scoring exist.

## Integration Sequence

### Step 1 - Mock Adapter

- Produces deterministic mock scanner output.
- Exercises raw evidence capture.
- Exercises normalization pipeline.
- Creates findings from fixtures.

Status: implemented and verified in Phase 4.

### Step 2 - Security Scanner

Selected first: garak.

Status: implemented and verified in Phase 5.

Goals:

- Prompt injection tests.
- Unsafe behavior tests.
- Red-team output capture.
- Normalized security findings.

Implemented Phase 5 scope:

- `garak_cli_adapter` executes garak through the backend Docker runtime.
- Native garak JSONL report, hit log, HTML report, scanner configuration, stdout/stderr log, raw platform JSON, and normalized output are preserved.
- garak eval records normalize into existing findings, evidence, audit events, and score recalculation.

### Step 3 - Bias/Fairness Scanner

Candidate: Fairlearn or Aequitas.

Goals:

- Protected-class disparity metrics.
- Language access risk records.
- Civil-rights finding normalization.

### Step 4 - LLM/RAG Evaluation

Candidate: Promptfoo, Ragas, or DeepEval.

Goals:

- RAG answer quality.
- Faithfulness.
- Retrieval quality.
- Prompt regression tests.

### Step 5 - Model Artifact Scanner

Candidate: ModelScan.

Goals:

- Model artifact supply-chain checks.
- Unsafe serialization detection where applicable.

## Integration Acceptance Criteria

Each integration must:

- Run through adapter interface.
- Preserve raw output evidence.
- Normalize findings.
- Record scanner run metadata.
- Handle failures visibly.
- Include fixture-based tests.

## Not Included Initially

- Scheduled recurring scanner fleet.
- Scanner microservices.
- Continuous production monitoring.
- Autonomous red-team campaigns.
- Multiple real scanner integrations in the same phase.
