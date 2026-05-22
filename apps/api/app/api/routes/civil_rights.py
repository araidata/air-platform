from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ai_system import AISystem
from app.models.assessment import Assessment
from app.models.assessment_profile import AssessmentProfile
from app.models.evidence import Evidence
from app.models.finding import Finding
from app.models.human_appeal_path_check import HumanAppealPathCheck
from app.models.language_access_scenario import LanguageAccessScenario
from app.schemas.civil_rights import (
    CivilRightsSummary,
    HumanAppealPathCheckCreate,
    HumanAppealPathCheckRead,
    LanguageAccessScenarioCreate,
    LanguageAccessScenarioRead,
)
from app.schemas.scanner import AssessmentProfileRead

router = APIRouter()

CIVIL_RIGHTS_TEMPLATE_NAMES = {
    "Rights-Impacting AI Review",
    "Public Benefits Eligibility AI Review",
    "HR / Employment AI Review",
    "Law Enforcement / CJIS AI Review",
    "Citizen-Facing Chatbot Review",
    "Accessibility and Language Access Review",
    "Human Review and Appeals Review",
}
FAIRNESS_EVIDENCE_TYPES = {
    "bilingual_screenshot",
    "translated_response",
    "escalation_screenshot",
    "policy_comparison",
    "accessibility_evidence",
    "human_review_workflow",
    "appeal_process_documentation",
    "fairness_review_note",
}


@router.get("/templates", response_model=List[AssessmentProfileRead])
def list_civil_rights_templates(db: Session = Depends(get_db)) -> list:
    return db.scalars(
        select(AssessmentProfile)
        .where(AssessmentProfile.profile_name.in_(CIVIL_RIGHTS_TEMPLATE_NAMES))
        .order_by(AssessmentProfile.profile_name)
    ).all()


@router.get("/language-access-scenarios", response_model=List[LanguageAccessScenarioRead])
def list_language_access_scenarios(db: Session = Depends(get_db)) -> list:
    return db.scalars(
        select(LanguageAccessScenario).order_by(LanguageAccessScenario.created_at.desc())
    ).all()


@router.post(
    "/language-access-scenarios",
    response_model=LanguageAccessScenarioRead,
    status_code=201,
)
def create_language_access_scenario(
    payload: LanguageAccessScenarioCreate, db: Session = Depends(get_db)
) -> LanguageAccessScenario:
    _validate_system_assessment(db, payload.system_id, payload.assessment_id)
    scenario = LanguageAccessScenario(**payload.model_dump())
    db.add(scenario)
    db.commit()
    db.refresh(scenario)
    return scenario


@router.get("/appeal-path-checks", response_model=List[HumanAppealPathCheckRead])
def list_appeal_path_checks(db: Session = Depends(get_db)) -> list:
    return db.scalars(
        select(HumanAppealPathCheck).order_by(HumanAppealPathCheck.created_at.desc())
    ).all()


@router.post("/appeal-path-checks", response_model=HumanAppealPathCheckRead, status_code=201)
def create_appeal_path_check(
    payload: HumanAppealPathCheckCreate, db: Session = Depends(get_db)
) -> HumanAppealPathCheck:
    _validate_system_assessment(db, payload.system_id, payload.assessment_id)
    for evidence_id in payload.evidence_ids:
        if not db.get(Evidence, evidence_id):
            raise HTTPException(status_code=404, detail=f"Evidence not found: {evidence_id}")
    check = HumanAppealPathCheck(**payload.model_dump())
    db.add(check)
    db.commit()
    db.refresh(check)
    return check


@router.get("/summary", response_model=CivilRightsSummary)
def get_civil_rights_summary(db: Session = Depends(get_db)) -> dict:
    templates = list_civil_rights_templates(db)
    scenarios = list_language_access_scenarios(db)
    checks = list_appeal_path_checks(db)
    findings = db.scalars(
        select(Finding)
        .where(
            or_(
                Finding.domain == "bias_civil_rights",
                Finding.title.ilike("%appeal%"),
                Finding.title.ilike("%accessibility%"),
                Finding.title.ilike("%language%"),
                Finding.title.ilike("%human review%"),
            )
        )
        .order_by(Finding.created_at.desc())
    ).all()
    evidence = db.scalars(
        select(Evidence)
        .where(
            or_(
                Evidence.evidence_type.in_(FAIRNESS_EVIDENCE_TYPES),
                Evidence.title.ilike("%language%"),
                Evidence.title.ilike("%appeal%"),
                Evidence.title.ilike("%accessibility%"),
                Evidence.title.ilike("%fairness%"),
                Evidence.description.ilike("%language%"),
                Evidence.description.ilike("%appeal%"),
                Evidence.description.ilike("%accessibility%"),
                Evidence.description.ilike("%fairness%"),
            )
        )
        .order_by(Evidence.created_at.desc())
    ).all()
    return {
        "templates": templates,
        "language_access_scenarios": scenarios,
        "appeal_path_checks": checks,
        "fairness_findings": findings,
        "fairness_evidence": evidence,
    }


def _validate_system_assessment(
    db: Session, system_id: Optional[str], assessment_id: Optional[str]
) -> None:
    system = db.get(AISystem, system_id) if system_id else None
    if system_id and not system:
        raise HTTPException(status_code=404, detail="System not found")
    if assessment_id:
        assessment = db.get(Assessment, assessment_id)
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
        if system_id and assessment.system_id != system_id:
            raise HTTPException(status_code=400, detail="Assessment does not belong to system")
