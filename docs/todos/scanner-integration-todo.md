# Scanner Integration TODO

## Phase 4

- Implement adapter interface.
- Implement mock adapter.
- Create scanner run records.
- Create isolated execution directory structure.
- Capture raw output and logs as evidence.
- Normalize mock scanner findings.

## Phase 5

- Select first real scanner, likely garak or AgentSeal.
- Add Docker/CLI execution wrapper.
- Parse structured output.
- Preserve raw logs.
- Normalize findings.
- Add score impact.

## Planned Scanner Families

- AgentSeal.
- garak.
- PyRIT.
- ModelScan.
- Fairlearn.
- Aequitas.
- IBM AI Fairness 360.
- Giskard.
- Ragas.
- DeepEval.
- Promptfoo.

## Do Not Do Yet

- Build multiple real adapters at once.
- Create scanner microservices.
- Rewrite scanner logic.
- Add distributed execution.
