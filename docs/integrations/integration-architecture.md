# Integration Architecture

Integrations should be planned carefully and implemented only after core workflows are stable.

## Planned Integrations

- OneTrust.
- Jira.
- ServiceNow.
- Microsoft Teams.
- Email notifications.
- Azure OpenAI.
- OpenAI APIs.
- Anthropic APIs.

## Integration Principles

- Core platform remains source of truth for AI assurance findings and evidence metadata.
- External systems receive synchronized workflow artifacts, not control of core logic.
- Integrations must preserve auditability.
- Integration failures must be visible.
- Synchronization should be idempotent where possible.
- External identifiers should be stored in integration mapping tables.

## Initial Integration Pattern

Later phases should use:

- Outbound events.
- Pullable reports.
- Export packages.
- Integration mapping records.
- Retryable sync jobs.
- Sync status UI.

Do not implement integrations during foundational workflow phases.

## Jira And ServiceNow Planning

Use cases:

- Create remediation tickets from findings.
- Sync status changes back to findings.
- Link evidence and retest records.
- Escalate overdue findings.

The platform should keep the finding as authoritative and treat external tickets as execution work items.

## Teams And Email Planning

Use cases:

- Notify owners of assigned findings.
- Notify AIRB participants of review packets.
- Notify executives of blocked deployments.
- Remind operators about overdue SLAs.

Notifications should not replace in-platform queues.

## Model Provider API Planning

Azure OpenAI, OpenAI APIs, and Anthropic APIs may be used later for:

- Model metadata capture.
- Controlled test prompts.
- Evaluation execution.
- Report summarization with strict evidence references.

They should not become the primary user experience or governance authority.
