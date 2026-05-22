# Scanner Integration TODO

## Phase 4

- [x] Implement adapter interface.
- [x] Implement mock adapter.
- [x] Create scanner registry records.
- [x] Create scan type records.
- [x] Create assessment profile records.
- [x] Create scanner run records.
- [x] Create scanner result records.
- [x] Create isolated execution directory structure.
- [x] Capture raw output and logs as evidence.
- [x] Normalize mock scanner findings.
- [x] Trigger score recalculation from scanner findings.
- [x] Add scanner recommendation APIs and Scanner Ecosystem UI.

## Phase 5

- [ ] Select first real scanner, likely garak or AgentSeal.
- [ ] Add Docker/CLI execution wrapper.
- [ ] Parse structured output.
- [ ] Preserve raw logs and raw output.
- [ ] Normalize findings.
- [ ] Add parser fixtures for success, empty, failed, malformed, and partial outputs.
- [ ] Add score impact.

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
