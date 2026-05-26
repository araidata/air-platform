# Known Issues

## Current Issues

- Historical docs may still reference retired mock-first runtime behavior and should continue being cleaned up when touched.
- Backend tests use SQLite for fast workflow coverage; Docker smoke tests cover live PostgreSQL runtime behavior.
- garak is the only real scanner integration; additional scanners are intentionally deferred.
- No OneTrust integration exists yet.
- No production backup or restore automation exists yet.
- Host port conflicts can require `API_HOST_PORT` or `FRONTEND_HOST_PORT` overrides on developer machines.

## Documentation Issues

- Some older documentation paths overlap with the new requested file structure.
- Future agents may consolidate or cross-link older docs after implementation begins.
- Status docs must be manually maintained until tooling exists.

## Product Risks

- Broadening into multiple real scanner integrations too early could distract from the governance workflow.
- Overbuilding infrastructure could make the project harder for one or two operators to run.
- A chatbot-first UI would misrepresent the product as a conversational tool rather than an assurance operations center.

## Mitigations

- Follow the phase plan.
- Prefer honest empty states over fabricated operational activity.
- Keep findings and evidence central.
- Update status docs after changes.
- Use adapters for scanners.
