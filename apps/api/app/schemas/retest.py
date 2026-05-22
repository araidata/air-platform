from datetime import datetime
from typing import Optional

from app.models.enums import RetestStatus
from app.schemas.base import ApiModel, StrictApiModel


class RetestCreate(StrictApiModel):
    initiated_by: str
    status: RetestStatus = RetestStatus.pending
    notes: Optional[str] = None
    result_summary: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class RetestUpdate(StrictApiModel):
    status: Optional[RetestStatus] = None
    notes: Optional[str] = None
    result_summary: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    actor: str = "operator"


class RetestRead(ApiModel):
    id: str
    finding_id: str
    initiated_by: str
    status: str
    notes: Optional[str]
    result_summary: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
