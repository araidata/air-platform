# Operational Workflows

## AI System Intake

```mermaid
flowchart TD
    Draft["Draft system record"] --> Classify["Classify risk and data sensitivity"]
    Classify --> Evidence["Attach initial governance evidence"]
    Evidence --> ReviewNeed{"Requires AIRB review?"}
    ReviewNeed -->|Yes| AIRB["Create AIRB review"]
    ReviewNeed -->|No| Active["Mark as inventory active"]
    AIRB --> Decision{"Decision"}
    Decision --> Approved["Approved"]
    Decision --> Exception["Approved with exception"]
    Decision --> Blocked["Blocked"]
```

## Finding Lifecycle

```mermaid
flowchart TD
    New["New finding"] --> Triage["Triage"]
    Triage --> Assigned["Assigned"]
    Assigned --> InProgress["Remediation in progress"]
    InProgress --> Retest["Ready for retest"]
    Retest --> Verified["Verified remediated"]
    Retest --> Reopened["Reopened"]
    Triage --> Accepted["Risk accepted"]
    Triage --> FalsePositive["False positive"]
    Assigned --> Escalated["Escalated"]
```

## Scanner Result Flow

```mermaid
flowchart LR
    Request["Assessment request"] --> Adapter["Scanner adapter"]
    Adapter --> Container["Docker scanner execution"]
    Container --> Raw["Raw output"]
    Raw --> Evidence["Preserve raw evidence"]
    Raw --> Normalize["Normalize findings"]
    Normalize --> Queue["Findings queue"]
    Queue --> Score["Recalculate scores"]
```

## Deployment Approval Flow

```mermaid
flowchart TD
    Request["Deployment approval request"] --> Check["Evidence and finding checks"]
    Check --> Security{"Security required?"}
    Security --> Bias{"Bias/civil-rights required?"}
    Bias --> Privacy{"Privacy required?"}
    Privacy --> Legal{"Legal required?"}
    Legal --> Decision["AIRB decision"]
    Decision --> Approved["Approved"]
    Decision --> Exception["Approved with exception"]
    Decision --> Blocked["Blocked"]
```

## Daily Operator Workflow

1. Review executive dashboard for score changes and blocked deployments.
2. Open Findings Queue filtered by critical and high severity.
3. Review overdue SLAs.
4. Inspect AIRB Review Queue.
5. Check Evidence and Audit page for incomplete evidence records.
6. Update remediation status and retest records.
7. Generate or refresh governance reports as needed.

## Weekly Governance Workflow

1. Review all high-risk systems.
2. Review systems without recent assessment evidence.
3. Review accepted risks nearing expiration.
4. Review blocked deployments and unresolved blockers.
5. Prepare AIRB packet for pending decisions.
6. Export reports for leadership.
