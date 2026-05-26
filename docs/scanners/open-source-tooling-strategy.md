# Open Source Tooling Strategy

Use mature open source tools where they already solve assessment problems. Do not recreate them inside the platform.

## Priority Tools

### Giskard

Use for hallucination testing, bias/fairness checks, prompt injection testing, RAG faithfulness, and business-rule validation.

### PyRIT

Use for adversarial testing, jailbreaks, prompt injection attacks, unsafe content checks, data exfiltration scenarios, and multi-turn red-team workflows.

### Langfuse

Use for trace references, prompt/output evidence, latency/cost metadata, and observability support.

### garak

Keep as the existing prompt-injection-oriented scanner adapter.

### OpenControl / Compliance Masonry

Use as the export path for control-oriented reporting.

## Integration Pattern

- Adapter.
- Safe execution plan.
- Raw artifact preservation.
- Parser.
- Normalized findings.
- Evidence linkage.
- Framework/control mappings.

## Do Not Do

- Do not copy tool source into the platform.
- Do not rewrite scanner internals.
- Do not make each scanner a service.
- Do not let scanner-specific output distort the core Finding model.
