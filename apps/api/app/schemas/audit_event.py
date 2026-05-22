from datetime import datetime
from typing import Optional

from app.schemas.base import ApiModel


class AuditEventRead(ApiModel):
    id: str
    entity_type: str
    entity_id: str
    event_type: str
    actor: str
    old_value: Optional[str]
    new_value: Optional[str]
    notes: Optional[str]
    created_at: datetime
