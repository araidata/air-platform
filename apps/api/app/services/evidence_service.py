from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.ai_system import AISystem
from app.models.assessment import Assessment
from app.models.enums import AuditEventType
from app.models.evidence import Evidence
from app.models.finding import Finding
from app.schemas.evidence import EvidenceCreate
from app.scoring.scoring_engine import ScoringEngine
from app.services.audit_event_service import AuditEventService


class EvidenceService:
    def __init__(self, db: Session):
        self.db = db
        self.audit = AuditEventService(db)

    def create(self, payload: EvidenceCreate) -> Evidence:
        data = payload.model_dump()
        data["evidence_type"] = payload.evidence_type.value

        finding = None
        assessment = None
        if payload.finding_id:
            finding = self.db.get(Finding, payload.finding_id)
            if not finding:
                raise HTTPException(status_code=404, detail="Finding not found")
            data["assessment_id"] = data["assessment_id"] or finding.assessment_id
            data["system_id"] = data["system_id"] or finding.system_id
        if data.get("assessment_id"):
            assessment = self.db.get(Assessment, data["assessment_id"])
            if not assessment:
                raise HTTPException(status_code=404, detail="Assessment not found")
            data["system_id"] = data["system_id"] or assessment.system_id
        if data.get("system_id") and not self.db.get(AISystem, data["system_id"]):
            raise HTTPException(status_code=404, detail="System not found")
        if not data.get("finding_id") and not data.get("assessment_id"):
            raise HTTPException(
                status_code=400,
                detail="Evidence must link to a finding or assessment",
            )

        evidence = Evidence(**data)
        self.db.add(evidence)
        self.db.flush()
        self.audit.record(
            entity_type="evidence",
            entity_id=evidence.id,
            event_type=AuditEventType.evidence_created,
            actor=evidence.created_by,
            new_value=evidence.evidence_type,
            notes=evidence.title,
        )
        ScoringEngine(self.db).recalculate_system_scores(
            evidence.system_id,
            evidence.assessment_id,
            triggered_by=evidence.created_by,
            change_reason="evidence added",
        )
        return evidence
