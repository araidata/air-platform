# Seed Data Plan

Seed data should make the platform useful immediately for inventory, template review, workflow configuration, and development without fabricating operational activity.

## Seed AI Systems

### Public Benefits Chatbot

- Department: Health and Human Services.
- Purpose: answer benefits eligibility and application questions.
- Public-facing: yes.
- Rights-impacting: yes.
- Safety-impacting: possible.
- Uses PII: yes.
- Uses PHI: possible.
- Risk tier: high.
- Approval status: under review.

### Sheriff Incident Summary Assistant

- Department: Sheriff.
- Purpose: summarize incident narratives for internal review.
- Public-facing: no.
- Rights-impacting: yes.
- Safety-impacting: yes.
- Uses CJIS: yes.
- Risk tier: high.
- Approval status: security review required.

### Permit Review Assistant

- Department: Planning and Permitting.
- Purpose: assist staff reviewing permit applications.
- Public-facing: no.
- Rights-impacting: possible.
- Uses PII: yes.
- Risk tier: medium.
- Approval status: draft.

### HR Resume Screening AI

- Department: Human Resources.
- Purpose: assist with resume screening and job qualification summaries.
- Public-facing: no.
- Rights-impacting: yes.
- Uses PII: yes.
- Risk tier: high.
- Approval status: bias review required.

### Citizen Services RAG Chatbot

- Department: Public Information.
- Purpose: answer resident questions using county website content.
- Public-facing: yes.
- Rights-impacting: possible.
- Uses PII: possible.
- Risk tier: medium.
- Approval status: approved with exception.

## Seed Findings

### Prompt Injection Vulnerability

- System: Public Benefits Chatbot.
- Domain: Security.
- Severity: Critical.
- Evidence: prompt/output sample.
- Status: New.
- Approval impact: blocks deployment.

### Language Disparity

- System: Public Benefits Chatbot.
- Domain: Bias/Civil Rights.
- Severity: High.
- Evidence: multilingual test sample.
- Status: Triage.

### Missing Human Appeal Path

- System: HR Resume Screening AI.
- Domain: Governance Evidence.
- Severity: High.
- Evidence: policy gap note.
- Status: Assigned.

### Excessive Tool Permissions

- System: Citizen Services RAG Chatbot.
- Domain: Security.
- Severity: High.
- Evidence: tool configuration snapshot.
- Status: In Progress.

### Incomplete Audit Logging

- System: Sheriff Incident Summary Assistant.
- Domain: Governance Evidence.
- Severity: Medium.
- Evidence: logging configuration screenshot.
- Status: Triage.

### Possible Data Leakage

- System: Permit Review Assistant.
- Domain: Privacy.
- Severity: High.
- Evidence: prompt/output sample.
- Status: New.
