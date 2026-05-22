# Next Steps

The next development work should begin Phase 6: Bias and Civil Rights Assessment Maturity.

Phase 5 - First Real Scanner Integration is complete and verified. garak now runs through the existing adapter contract in Docker, preserves native scanner artifacts and platform-normalized output as evidence, creates normalized findings from real scanner output, and triggers score recalculation through the existing service path.

## Recommended Next Task

Mature the rights-impacting assessment workflow without broadening infrastructure:

1. Add bias and civil-rights assessment templates.
2. Add language access scenarios for public-facing systems.
3. Add human appeal path checks for adverse or rights-impacting decisions.
4. Add fairness-oriented evidence expectations and finding templates.
5. Keep any future scanner work single-adapter, evidence-first, and synchronous until there is a concrete need to expand.

## Keep From Phase 5

- Scanners remain external tools.
- garak is the first proven real adapter pattern.
- Native scanner output, logs, config, and normalized artifacts are preserved as evidence.
- Scanner-specific fields stay in evidence metadata or scanner results.
- Score recalculation stays synchronous and service-layer.
- Docker Compose remains the runtime boundary.

## Do Not Do Next

- Do not integrate multiple additional scanners at once.
- Do not add Kubernetes, distributed workers, event buses, or continuous monitoring.
- Do not build scanner auto-scheduling or recurring assessments yet.
- Do not build OneTrust API integration yet.
