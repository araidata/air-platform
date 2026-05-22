from datetime import date, datetime
from typing import Any, Dict, Optional

from pydantic import Field

from app.models.enums import (
    FindingConfidence,
    FindingDomain,
    FindingRetestStatus,
    FindingSeverity,
    FindingStatus,
)
from app.schemas.base import ApiModel, StrictApiModel


class FindingCreate(StrictApiModel):
    system_id: str
    assessment_id: str
    scanner_name: str = "manual"
    scanner_version: str = "0.1.0"
    domain: FindingDomain
    severity: FindingSeverity
    confidence: FindingConfidence = FindingConfidence.unknown
    title: str
    description: str
    evidence_summary: str
    remediation: str
    owner_id: Optional[str] = None
    due_date: Optional[date] = None
    retest_status: FindingRetestStatus = FindingRetestStatus.not_started
    score_impact: Dict[str, Any] = Field(default_factory=dict)
    risk_accepted: bool = False
    approval_blocking: bool = False
    actor: str = "operator"


class FindingUpdate(StrictApiModel):
    scanner_name: Optional[str] = None
    scanner_version: Optional[str] = None
    domain: Optional[FindingDomain] = None
    severity: Optional[FindingSeverity] = None
    confidence: Optional[FindingConfidence] = None
    title: Optional[str] = None
    description: Optional[str] = None
    evidence_summary: Optional[str] = None
    remediation: Optional[str] = None
    owner_id: Optional[str] = None
    due_date: Optional[date] = None
    score_impact: Optional[Dict[str, Any]] = None
    approval_blocking: Optional[bool] = None
    actor: str = "operator"
    notes: Optional[str] = None


class FindingTransition(StrictApiModel):
    status: FindingStatus
    actor: str
    notes: Optional[str] = None
    risk_acceptance_rationale: Optional[str] = None


class FindingRead(ApiModel):
    id: str
    system_id: str
    assessment_id: str
    scanner_name: str
    scanner_version: str
    domain: str
    severity: str
    confidence: str
    title: str
    description: str
    evidence_summary: str
    remediation: str
    owner_id: Optional[str]
    status: str
    due_date: Optional[date]
    retest_status: str
    score_impact: Dict[str, Any]
    risk_accepted: bool
    approval_blocking: bool
    created_at: datetime
    updated_at: datetime
