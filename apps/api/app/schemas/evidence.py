from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import Field

from app.models.enums import EvidenceType
from app.schemas.base import ApiModel, StrictApiModel


class EvidenceCreate(StrictApiModel):
    finding_id: Optional[str] = None
    assessment_id: Optional[str] = None
    system_id: Optional[str] = None
    evidence_type: EvidenceType
    title: str
    description: Optional[str] = None
    file_path: Optional[str] = None
    raw_text: Optional[str] = None
    content_type: Optional[str] = None
    created_by: str
    hash: Optional[str] = None
    metadata_json: Dict[str, Any] = Field(default_factory=dict)


class EvidenceRead(ApiModel):
    id: str
    finding_id: Optional[str]
    assessment_id: Optional[str]
    system_id: Optional[str]
    evidence_type: str
    title: str
    description: Optional[str]
    file_path: Optional[str]
    raw_text: Optional[str]
    content_type: Optional[str]
    created_by: str
    created_at: datetime
    hash: Optional[str]
    metadata_json: Dict[str, Any]
