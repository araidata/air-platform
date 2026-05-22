# AI Review Board Workflow

The AI Review Board, abbreviated AIRB, provides structured review for higher-risk AI systems and deployment decisions.

## Workflow States

- Draft.
- Under Review.
- Security Review Required.
- Bias Review Required.
- Privacy Review Required.
- Legal Review Required.
- Approved.
- Approved with Exception.
- Blocked.

## State Guidance

### Draft

The review exists but is incomplete.

### Under Review

The review packet is ready for AIRB inspection.

### Security Review Required

Security findings, tool permissions, prompt injection, data leakage, or model supply chain concerns require security review.

### Bias Review Required

Rights-impacting or protected-class concerns require bias and civil-rights review.

### Privacy Review Required

PII, PHI, CJIS, or sensitive data use requires privacy review.

### Legal Review Required

Legal interpretation, appeal rights, public records, procurement, or statutory concerns require legal review.

### Approved

Deployment or operation is approved based on current evidence.

### Approved With Exception

Approved with documented conditions, compensating controls, and expiration.

### Blocked

System may not deploy or continue operation until blockers are resolved.

## Review Packet

Each AIRB review should include:

- System summary.
- Risk tier.
- Business purpose.
- Data classification.
- Current scores.
- Open critical and high findings.
- Evidence checklist.
- Human review process.
- Appeal path where applicable.
- Review notes.
- Proposed decision.

## Decision Record

Each decision should capture:

- Decision.
- Reviewer or board actor.
- Rationale.
- Evidence references.
- Conditions.
- Expiration date for exceptions.
- Follow-up tasks.

## Blocking Criteria

Examples:

- Open critical security finding.
- Missing human appeal path for rights-impacting use.
- High-confidence language disparity in public benefits workflow.
- Missing privacy review for sensitive data use.
- Excessive tool permissions in public-facing AI system.
- Incomplete audit logging for high-risk system.
