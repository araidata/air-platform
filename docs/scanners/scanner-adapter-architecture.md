# Scanner Adapter Architecture

Scanner adapters let the platform execute external tools while keeping the core assessment model stable.

## Current Architecture

```text
Assessment Target
  -> Scanner Orchestration Service
  -> Adapter
  -> External Tool
  -> Raw Artifacts
  -> Evidence Records
  -> Normalized Findings
  -> Risk Profile / Reports
```

## Adapter Lifecycle

1. Register adapter name, version, and capabilities.
2. Validate target and configuration.
3. Create scanner run.
4. Execute external tool.
5. Preserve artifacts.
6. Parse output.
7. Normalize findings.
8. Link evidence.
9. Update risk profile.

## Plugin Rules

- Keep adapter-specific fields in metadata.
- Keep Findings and Evidence scanner-neutral.
- Add one integration at a time.
- Prefer fixture-based parser tests before broad UI work.
- Keep execution local until operational load requires a different model.
