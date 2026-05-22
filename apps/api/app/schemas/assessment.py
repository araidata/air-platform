from datetime import datetime
from typing import Optional

from app.models.enums import AssessmentStatus
from app.schemas.base import ApiModel, StrictApiModel


class AssessmentCreate(StrictApiModel):
    system_id: str
    assessment_type: str
    initiated_by: str
    status: AssessmentStatus = AssessmentStatus.draft
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    summary: Optional[str] = None
    overall_score: Optional[float] = None
    notes: Optional[str] = None


class AssessmentUpdate(StrictApiModel):
    assessment_type: Optional[str] = None
    status: Optional[AssessmentStatus] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    summary: Optional[str] = None
    overall_score: Optional[float] = None
    notes: Optional[str] = None
    actor: str = "operator"


class AssessmentRead(ApiModel):
    id: str
    system_id: str
    assessment_type: str
    initiated_by: str
    status: str
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    summary: Optional[str]
    overall_score: Optional[float]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
