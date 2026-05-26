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

- [ ] Add Giskard adapter.
- [ ] Validate target configuration.
- [ ] Support hallucination testing.
- [ ] Support prompt injection testing.
- [ ] Preserve Giskard artifacts.
- [ ] Normalize Giskard findings.
- [ ] Add framework/control mappings.
- [ ] Add tests for success, no findings, invalid target, execution failure, and parser failure.

## Later

- [ ] PyRIT adapter.
- [ ] Langfuse trace/evidence adapter.
- [ ] Additional scanner adapters only when a concrete assessment workflow requires them.

## Do Not Do

- [ ] Do not build scanner microservices.
- [ ] Do not bypass the adapter contract.
- [ ] Do not seed fake scanner runs or findings.
