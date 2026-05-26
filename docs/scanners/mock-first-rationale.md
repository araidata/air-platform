# Mock-First Rationale (Historical)

This document describes an earlier scaffolding phase. Runtime mock findings, mock scan results, and fabricated scanner evidence have now been removed in favor of real scanner execution or honest empty states.

## Why Mock First

Real scanners produce data. They do not define:

- How operators triage findings.
- How evidence is preserved.
- How scores are explained.
- How AIRB decisions are routed.
- How deployment approvals are blocked.
- How executives understand risk.
- How remediation ownership works.

Those operational workflows must exist first.

## Benefits

- Validates data model before external tool complexity.
- Allows UI development without scanner setup friction.
- Exercises risk scoring.
- Exercises evidence attachments.
- Creates demos for stakeholders.
- Enables AI coding assistants to understand target workflows.
- Prevents the project from becoming scanner integration glue with no governance product.

## Required Mock Systems

- Public Benefits Chatbot.
- Sheriff Incident Summary Assistant.
- Permit Review Assistant.
- HR Resume Screening AI.
- Citizen Services RAG Chatbot.

## Required Mock Findings

- Prompt injection vulnerability.
- Language disparity.
- Missing human appeal path.
- Excessive tool permissions.
- Incomplete audit logging.
- Possible data leakage.

## Exit Criteria For Mock Phase

Real scanner work should begin only when:

- Inventory pages exist.
- Findings queue exists.
- Evidence records exist.
- Score calculations exist.
- AIRB workflow exists.
- Deployment approval workflow exists.
- Normalized finding schema has been tested with mock records.
- Operators can complete an end-to-end governance workflow using seeded data.
