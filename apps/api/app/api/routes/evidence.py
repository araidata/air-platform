from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.evidence import Evidence
from app.schemas.evidence import EvidenceCreate, EvidenceRead
from app.services.evidence_service import EvidenceService

router = APIRouter()


@router.get("", response_model=List[EvidenceRead])
def list_evidence(db: Session = Depends(get_db)) -> list:
    return db.scalars(select(Evidence).order_by(Evidence.created_at.desc())).all()


@router.get("/{evidence_id}", response_model=EvidenceRead)
def get_evidence(evidence_id: str, db: Session = Depends(get_db)) -> Evidence:
    evidence = db.get(Evidence, evidence_id)
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return evidence


@router.post("", response_model=EvidenceRead, status_code=201)
def create_evidence(payload: EvidenceCreate, db: Session = Depends(get_db)) -> Evidence:
    evidence = EvidenceService(db).create(payload)
    db.commit()
    db.refresh(evidence)
    return evidence
