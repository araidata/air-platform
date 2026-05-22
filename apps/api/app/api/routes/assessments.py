from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.assessment import Assessment
from app.schemas.assessment import AssessmentCreate, AssessmentRead, AssessmentUpdate
from app.services.assessment_workflow_service import AssessmentWorkflowService

router = APIRouter()


@router.get("", response_model=List[AssessmentRead])
def list_assessments(db: Session = Depends(get_db)) -> list:
    return db.scalars(select(Assessment).order_by(Assessment.created_at.desc())).all()


@router.get("/{assessment_id}", response_model=AssessmentRead)
def get_assessment(assessment_id: str, db: Session = Depends(get_db)) -> Assessment:
    assessment = db.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment


@router.post("", response_model=AssessmentRead, status_code=201)
def create_assessment(
    payload: AssessmentCreate, db: Session = Depends(get_db)
) -> Assessment:
    assessment = AssessmentWorkflowService(db).create(payload)
    db.commit()
    db.refresh(assessment)
    return assessment


@router.patch("/{assessment_id}", response_model=AssessmentRead)
def update_assessment(
    assessment_id: str, payload: AssessmentUpdate, db: Session = Depends(get_db)
) -> Assessment:
    assessment = db.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    assessment = AssessmentWorkflowService(db).update(assessment, payload)
    db.commit()
    db.refresh(assessment)
    return assessment
