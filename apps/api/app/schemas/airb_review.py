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
    actor: str = "operator"


class AirbReviewUpdate(StrictApiModel):
    review_status: Optional[AirbReviewStatus] = None
    decision_notes: Optional[str] = None
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    exception_granted: Optional[bool] = None
    expiration_date: Optional[date] = None
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
    created_at: datetime
    updated_at: datetime
