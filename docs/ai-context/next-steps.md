# Next Steps

The next development work should begin Phase 7: Governance Exports and OneTrust Workflow Support.

Phase 6 - Bias and Civil Rights Assessment Support is complete and verified. The platform now has civil-rights assessment templates, language-access scenarios, human appeal-path checks, fairness-oriented evidence, AIRB civil-rights indicators, score integration, seed data, tests, and a Civil Rights Review frontend route.

## Recommended Next Task

Add governance export support without broadening infrastructure:

1. Add CSV exports for systems, assessments, findings, evidence, and risk acceptances.
2. Add structured JSON governance exports.
3. Add audit packet export preparation.
4. Draft OneTrust field mapping.
5. Keep OneTrust upload manual until export quality is proven.

## Keep From Phase 6

- Civil-rights workflows remain evidence-backed and explainable.
- Language-access review remains scenario and reviewer driven.
- Appeal-path validation remains a governance workflow, not an automated legal conclusion.
- Scores remain deterministic explanations over findings, evidence, and workflow state.

## Do Not Do Next

- Do not integrate multiple additional scanners at once.
- Do not add Kubernetes, distributed workers, event buses, or continuous monitoring.
- Do not build scanner auto-scheduling or recurring assessments yet.
- Do not build OneTrust API integration yet.
