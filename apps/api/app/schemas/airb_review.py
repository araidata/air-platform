from datetime import date, datetime
from typing import Optional

from app.models.enums import AirbReviewStatus
from app.schemas.base import ApiModel, StrictApiModel


class AirbReviewCreate(StrictApiModel):
    system_id: str
    assessment_id: Optional[str] = None
    review_status: AirbReviewStatus = AirbReviewStatus.pending
    decision_notes: Optional[str] = None
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    exception_granted: bool = False
    expiration_date: Optional[date] = None
    civil_rights_review_status: str = "not_started"
    accessibility_review_status: str = "not_started"
    language_access_review_status: str = "not_started"
    fairness_review_status: str = "not_started"
    human_review_validated: bool = False
    appeal_path_validated: bool = False
    actor: str = "operator"


class AirbReviewUpdate(StrictApiModel):
    review_status: Optional[AirbReviewStatus] = None
    decision_notes: Optional[str] = None
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    exception_granted: Optional[bool] = None
    expiration_date: Optional[date] = None
    civil_rights_review_status: Optional[str] = None
    accessibility_review_status: Optional[str] = None
    language_access_review_status: Optional[str] = None
    fairness_review_status: Optional[str] = None
    human_review_validated: Optional[bool] = None
    appeal_path_validated: Optional[bool] = None
    actor: str = "operator"


class AirbReviewRead(ApiModel):
    id: str
    system_id: str
    assessment_id: Optional[str]
    review_status: str
    decision_notes: Optional[str]
    reviewed_by: Optional[str]
    reviewed_at: Optional[datetime]
    exception_granted: bool
    expiration_date: Optional[date]
    civil_rights_review_status: str
    accessibility_review_status: str
    language_access_review_status: str
    fairness_review_status: str
    human_review_validated: bool
    appeal_path_validated: bool
    created_at: datetime
    updated_at: datetime
