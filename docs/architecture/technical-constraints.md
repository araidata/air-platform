# Technical Constraints

## Runtime

- One Linux VM.
- Docker Compose.
- PostgreSQL.
- Local mounted evidence/scanner storage.
- Optional reverse proxy and TLS for production.

## Do Not Add Early

- Kubernetes.
- Helm.
- Service mesh.
- Distributed worker fleet.
- Scanner microservices.
- Multi-tenant SaaS architecture.
- Enterprise workflow platform assumptions.

## Data Constraints

- Preserve raw evidence.
- Keep operational records separate from development metadata.
- Do not fabricate assessments, findings, evidence, scanner runs, or scores.
- Store scanner output references and metadata in PostgreSQL.
- Treat scanner output as untrusted input.

## Integration Constraints

- Scanners integrate through adapters.
- Prefer CLI/container execution first.
- Use stable APIs only when the tool provides them.
- Do not copy scanner source into the platform.
- Do not let scanner-specific output reshape the core Finding model.
