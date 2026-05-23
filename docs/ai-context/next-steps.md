# Next Steps

The next development work should begin Phase 7: Guided Operational UI Workflows.

Phase 6 - Bias and Civil Rights Assessment Support is complete and verified. The platform now has civil-rights assessment templates, language-access scenarios, human appeal-path checks, fairness-oriented evidence, AIRB civil-rights indicators, score integration, seed data, tests, and a Civil Rights Review frontend route.

## Recommended Next Task

Implement guided operational UI workflows without broadening infrastructure:

1. Build System Intake UI.
2. Build Assessment Launch UX.
3. Build Scanner Execution UX.
4. Build Findings Review UX.
5. Build Evidence Review UX.
6. Build AIRB Workflow UX.
7. Add guided operator workflow navigation.
8. Connect the UI to the existing backend APIs.
9. Add minimal backend API additions only if a workflow truly needs them.
10. Verify the runtime end to end.
11. Update documentation and implementation status.

## Keep From Phase 6

- Civil-rights workflows remain evidence-backed and explainable.
- Language-access review remains scenario and reviewer driven.
- Appeal-path validation remains a governance workflow, not an automated legal conclusion.
- Scores remain deterministic explanations over findings, evidence, and workflow state.
- Keep backend additions minimal and driven by operator workflow gaps, not architecture expansion.

## Do Not Do Next

- Do not integrate multiple additional scanners at once.
- Do not add Kubernetes, distributed workers, event buses, or continuous monitoring.
- Do not build scanner auto-scheduling or recurring assessments yet.
- Do not build OneTrust API integration yet.
- Do not jump ahead to export-heavy work before the operator workflows are connected and usable.
