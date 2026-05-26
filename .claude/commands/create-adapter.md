# Create Scanner Adapter

Before creating or modifying a scanner adapter, read:

- `docs/ai-engineering/project-direction.md`
- `docs/scanners/adapter-contract.md`
- `docs/scanners/execution-model.md`
- `docs/architecture/scanner-adapter-architecture.md`
- `docs/architecture/normalization-strategy.md`
- `docs/findings/normalized-findings-schema.md`
- `docs/evidence/evidence-model.md`

Adapter work must:

- Treat the scanner as external.
- Prefer Docker or CLI execution.
- Use isolated execution directories.
- Preserve raw logs and outputs as evidence.
- Normalize results into platform findings.
- Avoid copying scanner source into the platform.

Use a mock adapter only for development or test coverage. Real integrations must produce clearly identified scanner runs, evidence, and findings through the adapter contract.
