# Create Scanner Adapter

Before creating or modifying a scanner adapter, read:

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

Start with a mock adapter unless the adapter framework already exists and the user explicitly requested a real scanner.
