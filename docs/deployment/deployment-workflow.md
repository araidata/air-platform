# Deployment Workflow

## Local Development

1. Copy environment template.
2. Start Docker Compose.
3. Run database migrations.
4. Seed systems and mock findings.
5. Start API and frontend.
6. Verify dashboard, inventory, findings, and evidence views.

## Single VM Production

1. Provision Linux VM.
2. Install Docker and Docker Compose.
3. Create application directory.
4. Configure environment variables.
5. Start Compose stack.
6. Run migrations.
7. Run seed only when explicitly intended.
8. Configure reverse proxy and TLS.
9. Configure backups.
10. Verify health checks.

## Backup Planning

Back up:

- PostgreSQL database.
- Evidence volume.
- Environment configuration.
- Compose files.

Backups should be tested by restoring into a non-production environment.

## Deployment Guardrails

- Do not deploy scanner integrations before evidence and finding workflows exist.
- Do not run real scanner jobs against production systems until assessment scope is approved.
- Do not expose evidence artifact storage directly to the public internet.
- Do not store model provider API keys in source control.
