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
- [x] Filter scanner launch workflows by system target configuration and compatible scanner tags.

## Phase 5

- [x] Select first real scanner, likely garak or AgentSeal.
- [x] Add Docker/CLI execution wrapper.
- [x] Parse structured output.
- [x] Preserve raw logs and raw output.
- [x] Normalize findings.
- [x] Add parser fixtures for success, empty, failed, malformed, and partial outputs.
- [x] Add score impact.

## Phase 6

- [x] Add bias and civil-rights assessment templates.
- [x] Add language access scenario workflows.
- [x] Add human appeal path checks.
- [x] Add fairness-oriented evidence expectations.
- [x] Defer additional real scanner integrations until one Phase 6 workflow needs them.

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
