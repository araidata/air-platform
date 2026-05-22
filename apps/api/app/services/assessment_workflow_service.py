from typing import Dict, Set

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ai_system import AISystem
from app.models.assessment import Assessment
from app.models.enums import AssessmentStatus, AuditEventType
from app.schemas.assessment import AssessmentCreate, AssessmentUpdate
from app.scoring.scoring_engine import ScoringEngine
from app.services.audit_event_service import AuditEventService


class AssessmentWorkflowService:
    valid_transitions: Dict[str, Set[str]] = {
        AssessmentStatus.draft.value: {
            AssessmentStatus.running.value,
            AssessmentStatus.under_review.value,
            AssessmentStatus.blocked.value,
            AssessmentStatus.archived.value,
        },
        AssessmentStatus.running.value: {
            AssessmentStatus.under_review.value,
            AssessmentStatus.completed.value,
            AssessmentStatus.blocked.value,
        },
        AssessmentStatus.under_review.value: {
            AssessmentStatus.completed.value,
            AssessmentStatus.blocked.value,
            AssessmentStatus.archived.value,
        },
        AssessmentStatus.blocked.value: {
            AssessmentStatus.running.value,
            AssessmentStatus.under_review.value,
            AssessmentStatus.archived.value,
        },
        AssessmentStatus.completed.value: {AssessmentStatus.archived.value},
        AssessmentStatus.archived.value: set(),
    }

    def __init__(self, db: Session):
        self.db = db
        self.audit = AuditEventService(db)

    def create(self, payload: AssessmentCreate) -> Assessment:
        if not self.db.get(AISystem, payload.system_id):
            raise HTTPException(status_code=404, detail="System not found")
        data = payload.model_dump()
        assessment = Assessment(**self._enum_values(data))
        self.db.add(assessment)
        self.db.flush()
        self.audit.record(
            entity_type="assessment",
            entity_id=assessment.id,
            event_type=AuditEventType.assessment_created,
            actor=payload.initiated_by,
            new_value=assessment.status,
        )
        ScoringEngine(self.db).recalculate_system_scores(
            assessment.system_id,
            assessment.id,
            triggered_by=payload.initiated_by,
            change_reason="assessment created",
        )
        return assessment

    def update(self, assessment: Assessment, payload: AssessmentUpdate) -> Assessment:
        updates = payload.model_dump(exclude_unset=True, exclude={"actor"})
        updates = self._enum_values(updates)
        requested_status = updates.pop("status", None)

        for key, value in updates.items():
            setattr(assessment, key, value)

        if requested_status and requested_status != assessment.status:
            allowed = self.valid_transitions.get(assessment.status, set())
            if requested_status not in allowed:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid assessment transition: {assessment.status} -> {requested_status}",
                )
            old_status = assessment.status
            assessment.status = requested_status
            self.audit.record(
                entity_type="assessment",
                entity_id=assessment.id,
                event_type=AuditEventType.assessment_status_changed,
                actor=payload.actor,
                old_value=old_status,
                new_value=requested_status,
            )
        self.db.flush()
        if updates or requested_status:
            ScoringEngine(self.db).recalculate_system_scores(
                assessment.system_id,
                assessment.id,
                triggered_by=payload.actor,
                change_reason="assessment updated",
            )
        return assessment

    def _enum_values(self, data: dict) -> dict:
        return {
            key: value.value if hasattr(value, "value") else value
            for key, value in data.items()
        }
