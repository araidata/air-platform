from enum import Enum


class AssessmentStatus(str, Enum):
    draft = "draft"
    running = "running"
    under_review = "under_review"
    completed = "completed"
    blocked = "blocked"
    archived = "archived"


class FindingDomain(str, Enum):
    security = "security"
    privacy = "privacy"
    bias_civil_rights = "bias_civil_rights"
    explainability = "explainability"
    governance = "governance"
    supply_chain = "supply_chain"
    agent_safety = "agent_safety"
    rag_integrity = "rag_integrity"


class FindingSeverity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    informational = "informational"


class FindingConfidence(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"
    unknown = "unknown"


class FindingStatus(str, Enum):
    new = "new"
    under_review = "under_review"
    in_remediation = "in_remediation"
    awaiting_retest = "awaiting_retest"
    mitigated = "mitigated"
    risk_accepted = "risk_accepted"
    false_positive = "false_positive"
    closed = "closed"


class FindingRetestStatus(str, Enum):
    not_started = "not_started"
    pending = "pending"
    running = "running"
    passed = "passed"
    failed = "failed"
    inconclusive = "inconclusive"


class EvidenceType(str, Enum):
    raw_log = "raw_log"
    screenshot = "screenshot"
    uploaded_file = "uploaded_file"
    scanner_output = "scanner_output"
    prompt = "prompt"
    model_response = "model_response"
    export = "export"
    note = "note"
    reference = "reference"


class AuditEventType(str, Enum):
    system_created = "system_created"
    assessment_created = "assessment_created"
    assessment_status_changed = "assessment_status_changed"
    finding_created = "finding_created"
    finding_updated = "finding_updated"
    finding_status_changed = "finding_status_changed"
    owner_assigned = "owner_assigned"
    due_date_changed = "due_date_changed"
    evidence_created = "evidence_created"
    risk_accepted = "risk_accepted"
    retest_created = "retest_created"
    retest_status_changed = "retest_status_changed"
    airb_review_created = "airb_review_created"
    airb_decision_recorded = "airb_decision_recorded"


class RetestStatus(str, Enum):
    pending = "pending"
    running = "running"
    passed = "passed"
    failed = "failed"
    inconclusive = "inconclusive"


class AirbReviewStatus(str, Enum):
    pending = "pending"
    under_review = "under_review"
    approved = "approved"
    approved_with_exception = "approved_with_exception"
    blocked = "blocked"
