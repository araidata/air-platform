from typing import Dict, Set

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.assessment import Assessment
from app.models.enums import AuditEventType, FindingStatus
from app.models.finding import Finding
from app.models.owner import Owner
from app.models.risk_acceptance import RiskAcceptance
from app.models.ai_system import AISystem
from app.schemas.finding import FindingCreate, FindingTransition, FindingUpdate
from app.scoring.scoring_engine import ScoringEngine
from app.services.audit_event_service import AuditEventService


class FindingWorkflowService:
    valid_transitions: Dict[str, Set[str]] = {
        FindingStatus.new.value: {FindingStatus.under_review.value},
        FindingStatus.under_review.value: {
            FindingStatus.in_remediation.value,
            FindingStatus.risk_accepted.value,
            FindingStatus.false_positive.value,
        },
        FindingStatus.in_remediation.value: {FindingStatus.awaiting_retest.value},
        FindingStatus.awaiting_retest.value: {
            FindingStatus.mitigated.value,
            FindingStatus.in_remediation.value,
        },
        FindingStatus.mitigated.value: {FindingStatus.closed.value},
        FindingStatus.risk_accepted.value: {FindingStatus.closed.value},
        FindingStatus.false_positive.value: {FindingStatus.closed.value},
        FindingStatus.closed.value: set(),
    }

    def __init__(self, db: Session):
        self.db = db
        self.audit = AuditEventService(db)

    def create(self, payload: FindingCreate) -> Finding:
        self._require_system(payload.system_id)
        assessment = self._require_assessment(payload.assessment_id)
        if assessment.system_id != payload.system_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="assessment_id does not belong to system_id",
            )
        if payload.owner_id:
            self._require_owner(payload.owner_id)

        data = payload.model_dump(exclude={"actor"})
        finding = Finding(**self._enum_values(data))
        self.db.add(finding)
        self.db.flush()
        self.audit.record(
            entity_type="finding",
            entity_id=finding.id,
            event_type=AuditEventType.finding_created,
            actor=payload.actor,
            new_value=finding.status,
            notes=finding.title,
        )
        ScoringEngine(self.db).recalculate_system_scores(
            finding.system_id,
            finding.assessment_id,
            triggered_by=payload.actor,
            change_reason="finding created",
        )
        return finding

    def update(self, finding: Finding, payload: FindingUpdate) -> Finding:
        updates = payload.model_dump(exclude_unset=True, exclude={"actor", "notes"})
        updates = self._enum_values(updates)
        old_owner_id = finding.owner_id
        old_due_date = str(finding.due_date) if finding.due_date else None

        if "owner_id" in updates and updates["owner_id"]:
            self._require_owner(updates["owner_id"])

        for key, value in updates.items():
            setattr(finding, key, value)
        self.db.flush()

        if "owner_id" in updates and updates["owner_id"] != old_owner_id:
            self.audit.record(
                entity_type="finding",
                entity_id=finding.id,
                event_type=AuditEventType.owner_assigned,
                actor=payload.actor,
                old_value=old_owner_id,
                new_value=updates["owner_id"],
                notes=payload.notes,
            )
        if "due_date" in updates:
            new_due_date = str(finding.due_date) if finding.due_date else None
            if new_due_date != old_due_date:
                self.audit.record(
                    entity_type="finding",
                    entity_id=finding.id,
                    event_type=AuditEventType.due_date_changed,
                    actor=payload.actor,
                    old_value=old_due_date,
                    new_value=new_due_date,
                    notes=payload.notes,
                )
        if updates:
            self.audit.record(
                entity_type="finding",
                entity_id=finding.id,
                event_type=AuditEventType.finding_updated,
                actor=payload.actor,
                notes=payload.notes,
            )
            ScoringEngine(self.db).recalculate_system_scores(
                finding.system_id,
                finding.assessment_id,
                triggered_by=payload.actor,
                change_reason="finding updated",
            )
        return finding

    def transition(self, finding: Finding, payload: FindingTransition) -> Finding:
        new_status = payload.status.value
        allowed = self.valid_transitions.get(finding.status, set())
        if new_status not in allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid finding transition: {finding.status} -> {new_status}",
            )

        old_status = finding.status
        finding.status = new_status
        if new_status == FindingStatus.risk_accepted.value:
            finding.risk_accepted = True
            self.db.add(
                RiskAcceptance(
                    finding_id=finding.id,
                    accepted_by=payload.actor,
                    rationale=payload.risk_acceptance_rationale
                    or payload.notes
                    or "Risk accepted through finding workflow.",
                )
            )
            self.audit.record(
                entity_type="finding",
                entity_id=finding.id,
                event_type=AuditEventType.risk_accepted,
                actor=payload.actor,
                old_value=old_status,
                new_value=new_status,
                notes=payload.notes,
            )
        self.db.flush()
        self.audit.record(
            entity_type="finding",
            entity_id=finding.id,
            event_type=AuditEventType.finding_status_changed,
            actor=payload.actor,
            old_value=old_status,
            new_value=new_status,
            notes=payload.notes,
        )
        ScoringEngine(self.db).recalculate_system_scores(
            finding.system_id,
            finding.assessment_id,
            triggered_by=payload.actor,
            change_reason="finding status changed",
        )
        return finding

    def _require_system(self, system_id: str) -> AISystem:
        system = self.db.get(AISystem, system_id)
        if not system:
            raise HTTPException(status_code=404, detail="System not found")
        return system

    def _require_assessment(self, assessment_id: str) -> Assessment:
        assessment = self.db.get(Assessment, assessment_id)
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
        return assessment

    def _require_owner(self, owner_id: str) -> Owner:
        owner = self.db.get(Owner, owner_id)
        if not owner:
            raise HTTPException(status_code=404, detail="Owner not found")
        return owner

    def _enum_values(self, data: dict) -> dict:
        return {
            key: value.value if hasattr(value, "value") else value
            for key, value in data.items()
        }
