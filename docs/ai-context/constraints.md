# Constraints

These constraints keep the project realistic.

## Operational Constraints

- One or two operators.
- Small internal county tool.
- One Linux VM.
- Docker Compose.
- Limited engineering capacity.
- AI-assisted development over time.

## Technical Constraints

- No Kubernetes.
- No microservices by default.
- No distributed worker fleet.
- No enterprise auth at the beginning.
- No multi-tenant SaaS assumptions.
- No real scanner integrations before adapter framework.
- No OneTrust API implementation before export workflow.

## Scanner Constraints

- Scanners remain external tools.
- Prefer Dockerized scanner containers.
- Prefer CLI wrappers at first.
- Use isolated execution directories.
- Capture raw logs and outputs.
- Normalize findings into the platform schema.
- Avoid tight coupling to scanner internals.

## UX Constraints

- Do not build a chatbot-first interface.
- Do not use toy AI branding.
- Do not hide evidence behind vague scores.
- Keep density readable for operators.
- Make audit status and finding status visible.

## Scope Constraint

When uncertain, build the smallest workflow that improves operational assurance.
