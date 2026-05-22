# Development Workflow

## First Development Loop

1. Read AI context documents.
2. Check implementation status.
3. Pick next item from TODO.
4. Keep changes small and vertical.
5. Update docs when architecture or workflow behavior changes.
6. Run tests.
7. Seed data and verify operational UI behavior.

## Development Priorities

- Build inventory before scanner integrations.
- Build findings before scanner integrations.
- Build evidence before scanner integrations.
- Build scoring after findings and evidence exist.
- Build AIRB workflow before integrations.

## Seed Data

Seed data must include:

- Public Benefits Chatbot.
- Sheriff Incident Summary Assistant.
- Permit Review Assistant.
- HR Resume Screening AI.
- Citizen Services RAG Chatbot.

Mock findings must include:

- Prompt injection vulnerability.
- Language disparity.
- Missing human appeal path.
- Excessive tool permissions.
- Incomplete audit logging.
- Possible data leakage.

## Pull Request Expectations

When this becomes a Git repository, PRs should explain:

- User-facing change.
- Data model changes.
- Workflow changes.
- Evidence or scoring impact.
- Tests run.
- Docs updated.

## Testing Expectations

Initial tests should cover:

- API validation.
- Finding workflow transitions.
- Score calculations.
- Evidence linking.
- Seed data integrity.
- UI rendering for queues and dashboard cards.
