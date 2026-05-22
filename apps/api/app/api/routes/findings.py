from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.finding import Finding
from app.schemas.finding import FindingCreate, FindingRead, FindingTransition, FindingUpdate
from app.schemas.retest import RetestCreate, RetestRead
from app.services.finding_workflow_service import FindingWorkflowService
from app.services.retest_service import RetestService

router = APIRouter()


@router.get("", response_model=List[FindingRead])
def list_findings(db: Session = Depends(get_db)) -> list:
    return db.scalars(select(Finding).order_by(Finding.created_at.desc())).all()


@router.get("/{finding_id}", response_model=FindingRead)
def get_finding(finding_id: str, db: Session = Depends(get_db)) -> Finding:
    finding = db.get(Finding, finding_id)
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    return finding


@router.post("", response_model=FindingRead, status_code=201)
def create_finding(payload: FindingCreate, db: Session = Depends(get_db)) -> Finding:
    finding = FindingWorkflowService(db).create(payload)
    db.commit()
    db.refresh(finding)
    return finding


@router.patch("/{finding_id}", response_model=FindingRead)
def update_finding(
    finding_id: str, payload: FindingUpdate, db: Session = Depends(get_db)
) -> Finding:
    finding = db.get(Finding, finding_id)
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    finding = FindingWorkflowService(db).update(finding, payload)
    db.commit()
    db.refresh(finding)
    return finding


@router.post("/{finding_id}/transition", response_model=FindingRead)
def transition_finding(
    finding_id: str, payload: FindingTransition, db: Session = Depends(get_db)
) -> Finding:
    finding = db.get(Finding, finding_id)
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    finding = FindingWorkflowService(db).transition(finding, payload)
    db.commit()
    db.refresh(finding)
    return finding


@router.post("/{finding_id}/retest", response_model=RetestRead, status_code=201)
def create_finding_retest(
    finding_id: str, payload: RetestCreate, db: Session = Depends(get_db)
):
    retest = RetestService(db).create(finding_id, payload)
    db.commit()
    db.refresh(retest)
    return retest
