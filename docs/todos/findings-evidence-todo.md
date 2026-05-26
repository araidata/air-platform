# Findings And Evidence TODO

## Phase 1

- [x] Retired frontend mock findings and evidence runtime data.
- [x] Link findings to evidence.
- [x] Show finding status, owner, severity, confidence, domain, and score impact.

## Phase 2

- [x] Add persisted finding records.
- [x] Add evidence records.
- [x] Implement finding lifecycle transitions.
- [x] Add retest status.
- [x] Add risk acceptance reference.
- [x] Add audit events for status changes.
- [x] Add evidence-to-finding and evidence-to-assessment links.
- [x] Add basic tests for evidence creation and lifecycle audit events.

## Phase 3

- [x] Connect findings to scoring through deterministic impact calculations and recalculation hooks.
- [x] Persist score impact explanations in the backend.
- [x] Render score impact explanations in API-backed or empty-state frontend views.

## Phase 4

- [x] Generate evidence records from scanner raw output and execution logs.
- [x] Generate finding-level evidence records only from real scanner output.
- [x] Normalize scanner findings into the existing finding workflow.
- [x] Preserve scanner run metadata in evidence metadata.
- [x] Recalculate scores when scanner-created findings and evidence are created.

## Phase 6

- [x] Add fairness-oriented findings using the existing findings workflow.
- [x] Add fairness evidence types using the existing evidence architecture.
- [x] Recalculate scores when civil-rights evidence is linked.

## Deferred

- Complex chain-of-custody workflow.
- Advanced retention policy automation.
- Full document-generation engine.
