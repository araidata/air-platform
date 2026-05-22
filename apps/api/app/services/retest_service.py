from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.enums import AuditEventType
from app.models.finding import Finding
from app.models.retest import Retest
from app.schemas.retest import RetestCreate, RetestUpdate
from app.services.audit_event_service import AuditEventService


class RetestService:
    def __init__(self, db: Session):
        self.db = db
        self.audit = AuditEventService(db)

    def create(self, finding_id: str, payload: RetestCreate) -> Retest:
        finding = self.db.get(Finding, finding_id)
        if not finding:
            raise HTTPException(status_code=404, detail="Finding not found")
        data = payload.model_dump()
        data["status"] = payload.status.value
        retest = Retest(finding_id=finding_id, **data)
        old_finding_retest_status = finding.retest_status
        finding.retest_status = retest.status
        self.db.add(retest)
        self.db.flush()
        self.audit.record(
            entity_type="retest",
            entity_id=retest.id,
            event_type=AuditEventType.retest_created,
            actor=payload.initiated_by,
            new_value=retest.status,
            notes=payload.notes,
        )
        self.audit.record(
            entity_type="finding",
            entity_id=finding.id,
            event_type=AuditEventType.retest_status_changed,
            actor=payload.initiated_by,
            old_value=old_finding_retest_status,
            new_value=finding.retest_status,
            notes=payload.notes,
        )
        return retest

    def update(self, retest: Retest, payload: RetestUpdate) -> Retest:
        updates = payload.model_dump(exclude_unset=True, exclude={"actor"})
        if "status" in updates and updates["status"] is not None:
            updates["status"] = updates["status"].value
        old_status = retest.status
        for key, value in updates.items():
            setattr(retest, key, value)
        if "status" in updates and retest.status != old_status:
            retest.finding.retest_status = retest.status
            self.audit.record(
                entity_type="retest",
                entity_id=retest.id,
                event_type=AuditEventType.retest_status_changed,
                actor=payload.actor,
                old_value=old_status,
                new_value=retest.status,
                notes=payload.notes,
            )
            self.audit.record(
                entity_type="finding",
                entity_id=retest.finding_id,
                event_type=AuditEventType.retest_status_changed,
                actor=payload.actor,
                old_value=old_status,
                new_value=retest.status,
                notes=payload.notes,
            )
        self.db.flush()
        return retest
