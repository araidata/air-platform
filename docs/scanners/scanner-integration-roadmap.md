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

Candidate: garak or PyRIT.

Phase 5 should choose one first real scanner, with garak or AgentSeal as the current preferred candidates.

Goals:

- Prompt injection tests.
- Unsafe behavior tests.
- Red-team output capture.
- Normalized security findings.

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
