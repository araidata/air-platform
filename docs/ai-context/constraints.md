# Constraints

These constraints keep the project realistic for a county team.

## Operational Constraints

- One or two primary operators.
- One Linux VM target.
- Docker Compose runtime.
- Limited engineering capacity.
- Production handoff should be understandable without specialized platform engineering.

## Technical Constraints

- No Kubernetes.
- No microservices by default.
- No distributed worker fleet.
- No multi-tenant SaaS assumptions.
- No scanner integration outside the adapter contract.
- No fabricated operational records in runtime data.

## Scanner Constraints

- Scanners remain external tools.
- Prefer Dockerized scanner containers or CLI wrappers.
- Use isolated execution directories.
- Capture raw logs, reports, prompts, outputs, and configuration.
- Normalize findings into the platform schema.
- Treat scanner output as untrusted input.
- Avoid tight coupling to scanner internals.

## UX Constraints

- Do not build a chatbot-first interface.
- Do not use toy AI branding.
- Do not hide evidence behind vague scores.
- Keep dense pages readable for operators.
- Make assessment status, finding status, and evidence availability visible.

## Scope Rule

When uncertain, build the smallest assessment workflow that improves testing, evidence, findings, or reporting.
