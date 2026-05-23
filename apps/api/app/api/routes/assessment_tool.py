from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.assessment_tool_run import AssessmentToolRun
from app.schemas.assessment_tool import AssessmentToolRunCreate, AssessmentToolRunRead
from app.services.assessment_tool_service import AssessmentToolService

router = APIRouter()


@router.get("/runs", response_model=list[AssessmentToolRunRead])
def list_assessment_tool_runs(db: Session = Depends(get_db)) -> list[AssessmentToolRun]:
    return AssessmentToolService(db).list_runs()


@router.post("/runs", response_model=AssessmentToolRunRead, status_code=201)
def create_assessment_tool_run(
    payload: AssessmentToolRunCreate,
    db: Session = Depends(get_db),
) -> AssessmentToolRun:
    run = AssessmentToolService(db).create_and_execute(payload)
    db.commit()
    db.refresh(run)
    return run


@router.get("/runs/{run_id}", response_model=AssessmentToolRunRead)
def get_assessment_tool_run(run_id: str, db: Session = Depends(get_db)) -> AssessmentToolRun:
    run = db.get(AssessmentToolRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Assessment tool run not found")
    return run


@router.get("/runs/{run_id}/report")
def get_assessment_tool_report(run_id: str, db: Session = Depends(get_db)) -> dict:
    run = db.get(AssessmentToolRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Assessment tool run not found")
    return run.report
