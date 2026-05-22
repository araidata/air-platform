from sqlalchemy.orm import Session

from app.models.audit_event import AuditEvent
from app.models.enums import AuditEventType


class AuditEventService:
    def __init__(self, db: Session):
        self.db = db

    def record(
        self,
        *,
        entity_type: str,
        entity_id: str,
        event_type: AuditEventType,
        actor: str,
        old_value: str = None,
        new_value: str = None,
        notes: str = None,
    ) -> AuditEvent:
        event = AuditEvent(
            entity_type=entity_type,
            entity_id=entity_id,
            event_type=event_type.value,
            actor=actor,
            old_value=old_value,
            new_value=new_value,
            notes=notes,
        )
        self.db.add(event)
        return event
