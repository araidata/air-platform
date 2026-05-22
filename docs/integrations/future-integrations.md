# Future Integrations

Future integrations should support governance operations without compromising simplicity.

## Integration Categories

- Governance platforms such as OneTrust.
- Scanner tools.
- Observability tools.
- Ticketing or work tracking.
- Identity providers.
- Reporting destinations.

## Possible Future Integrations

- OneTrust for governance records.
- Langfuse for LLM observability.
- OpenTelemetry for traces.
- MLflow for model metadata.
- ServiceNow or Jira for remediation tickets.
- Email or Teams notifications.

## Integration Principles

- Start with export/import before API sync.
- Keep the platform source of truth for findings and evidence.
- Preserve evidence references.
- Make mappings explicit.
- Avoid hidden automation for approvals.
- Avoid making operations depend on fragile external APIs.

## Not Yet

Do not build broad integration frameworks before the first few workflows prove what is needed.
