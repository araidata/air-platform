# Normalization Strategy

Scanner outputs vary by tool. The platform normalizes them into shared assessment records without losing raw evidence.

## Inputs

- Scanner reports.
- Logs.
- Prompt/output samples.
- Trace references.
- Uploaded evidence.
- Human review notes.

## Normalized Records

- Scanner Run.
- Finding.
- Evidence.
- Framework Mapping.
- Score Impact.
- Audit Event.

## Rules

- Preserve raw output before parsing.
- Keep parser failures visible.
- Never require a scanner-specific field in the core Finding model.
- Store scanner-specific details in metadata.
- Link every normalized finding to at least one evidence reference when possible.
- Map findings to NIST AI RMF, OWASP LLM Top 10, and OpenControl-ready controls where available.

## Severity and Confidence

Adapters should translate scanner-specific severity and confidence into platform values. When a scanner does not provide one, use conservative defaults and explain the source in metadata.
