from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.opencontrol_service import OpenControlService

router = APIRouter()


@router.get("/opencontrol/assessments/{assessment_id}")
def export_assessment_opencontrol(assessment_id: str, db: Session = Depends(get_db)) -> dict:
    return OpenControlService(db).export_assessment(assessment_id)
