# Scanner Integration TODO

## Implemented

- [x] Adapter interface.
- [x] Scanner registry records.
- [x] Scan type records.
- [x] Assessment profile records.
- [x] Scanner run records.
- [x] Scanner result records.
- [x] Isolated execution directory structure.
- [x] Raw output and log capture.
- [x] Finding normalization.
- [x] Evidence linkage.
- [x] Score recalculation from scanner findings.
- [x] garak adapter.
- [x] Live HTTP assessment tester.

## Next: Giskard

- [x] Add Giskard adapter.
- [x] Validate target configuration.
- [x] Support hallucination testing.
- [x] Support prompt injection testing.
- [x] Preserve Giskard artifacts.
- [x] Normalize Giskard findings.
- [x] Add framework/control mappings.
- [x] Add tests for execution, graceful failure, evidence, normalization, and OpenControl export.

## PyRIT and Langfuse

- [x] PyRIT adapter.
- [x] Langfuse trace/evidence adapter.
- [x] Docker runtime validation after Docker Desktop recovery.
- [x] Operational test target execution with installed Giskard/PyRIT SDKs.

## Later

- [ ] Additional scanner adapters only when a concrete assessment workflow requires them.

## Do Not Do

- [ ] Do not build scanner microservices.
- [ ] Do not bypass the adapter contract.
- [ ] Do not seed fake scanner runs or findings.
