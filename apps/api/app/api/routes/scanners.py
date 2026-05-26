from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.assessment_profile import AssessmentProfile
from app.models.scan_type import ScanType
from app.models.scanner_definition import ScannerDefinition
from app.models.scanner_result import ScannerResult
from app.models.scanner_run import ScannerRun
from app.schemas.scanner import (
    AssessmentProfileCreate,
    AssessmentProfileRead,
    AssessmentProfileUpdate,
    ScanTypeCreate,
    ScanTypeRead,
    ScanTypeUpdate,
    ScannerAdapterRead,
    ScannerDefinitionCreate,
    ScannerDefinitionRead,
    ScannerDefinitionUpdate,
    ScannerResultRead,
    ScannerRunCreate,
    ScannerRunExecuteRequest,
    ScannerRunRead,
    SystemScanRecommendations,
)
from app.scanners.adapters.garak_adapter import GarakCliAdapter
from app.scanners.services.scanner_execution_service import ScannerExecutionService

router = APIRouter()


@router.get("/scanner-definitions", response_model=List[ScannerDefinitionRead])
def list_scanner_definitions(db: Session = Depends(get_db)) -> list:
    return db.scalars(select(ScannerDefinition).order_by(ScannerDefinition.display_name)).all()


@router.get("/scanner-definitions/{scanner_definition_id}", response_model=ScannerDefinitionRead)
def get_scanner_definition(scanner_definition_id: str, db: Session = Depends(get_db)):
    scanner = db.get(ScannerDefinition, scanner_definition_id)
    if not scanner:
        raise HTTPException(status_code=404, detail="Scanner definition not found")
    return scanner


@router.post("/scanner-definitions", response_model=ScannerDefinitionRead, status_code=201)
def create_scanner_definition(
    payload: ScannerDefinitionCreate, db: Session = Depends(get_db)
):
    scanner = ScannerDefinition(**payload.model_dump())
    db.add(scanner)
    db.commit()
    db.refresh(scanner)
    return scanner


@router.patch("/scanner-definitions/{scanner_definition_id}", response_model=ScannerDefinitionRead)
def update_scanner_definition(
    scanner_definition_id: str,
    payload: ScannerDefinitionUpdate,
    db: Session = Depends(get_db),
):
    scanner = db.get(ScannerDefinition, scanner_definition_id)
    if not scanner:
        raise HTTPException(status_code=404, detail="Scanner definition not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(scanner, key, value)
    db.commit()
    db.refresh(scanner)
    return scanner


@router.get("/scan-types", response_model=List[ScanTypeRead])
def list_scan_types(db: Session = Depends(get_db)) -> list:
    return db.scalars(select(ScanType).order_by(ScanType.domain, ScanType.display_name)).all()


@router.get("/scan-types/{scan_type_id}", response_model=ScanTypeRead)
def get_scan_type(scan_type_id: str, db: Session = Depends(get_db)):
    scan_type = db.get(ScanType, scan_type_id)
    if not scan_type:
        raise HTTPException(status_code=404, detail="Scan type not found")
    return scan_type


@router.post("/scan-types", response_model=ScanTypeRead, status_code=201)
def create_scan_type(payload: ScanTypeCreate, db: Session = Depends(get_db)):
    scan_type = ScanType(**payload.model_dump())
    db.add(scan_type)
    db.commit()
    db.refresh(scan_type)
    return scan_type


@router.patch("/scan-types/{scan_type_id}", response_model=ScanTypeRead)
def update_scan_type(scan_type_id: str, payload: ScanTypeUpdate, db: Session = Depends(get_db)):
    scan_type = db.get(ScanType, scan_type_id)
    if not scan_type:
        raise HTTPException(status_code=404, detail="Scan type not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(scan_type, key, value)
    db.commit()
    db.refresh(scan_type)
    return scan_type


@router.get("/assessment-profiles", response_model=List[AssessmentProfileRead])
def list_assessment_profiles(db: Session = Depends(get_db)) -> list:
    return db.scalars(select(AssessmentProfile).order_by(AssessmentProfile.profile_name)).all()


@router.get("/assessment-profiles/{assessment_profile_id}", response_model=AssessmentProfileRead)
def get_assessment_profile(assessment_profile_id: str, db: Session = Depends(get_db)):
    profile = db.get(AssessmentProfile, assessment_profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Assessment profile not found")
    return profile


@router.post("/assessment-profiles", response_model=AssessmentProfileRead, status_code=201)
def create_assessment_profile(
    payload: AssessmentProfileCreate, db: Session = Depends(get_db)
):
    profile = AssessmentProfile(**payload.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.patch("/assessment-profiles/{assessment_profile_id}", response_model=AssessmentProfileRead)
def update_assessment_profile(
    assessment_profile_id: str,
    payload: AssessmentProfileUpdate,
    db: Session = Depends(get_db),
):
    profile = db.get(AssessmentProfile, assessment_profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Assessment profile not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/scanner-runs", response_model=List[ScannerRunRead])
def list_scanner_runs(db: Session = Depends(get_db)) -> list:
    return db.scalars(select(ScannerRun).order_by(ScannerRun.created_at.desc())).all()


@router.get("/scanner-runs/{scanner_run_id}", response_model=ScannerRunRead)
def get_scanner_run(scanner_run_id: str, db: Session = Depends(get_db)):
    run = db.get(ScannerRun, scanner_run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Scanner run not found")
    return run


@router.post("/scanner-runs", response_model=ScannerRunRead, status_code=201)
def create_scanner_run(payload: ScannerRunCreate, db: Session = Depends(get_db)):
    run = ScannerExecutionService(db).create_run(payload)
    db.commit()
    db.refresh(run)
    return run


@router.post("/scanner-runs/{scanner_run_id}/execute", response_model=ScannerRunRead)
def execute_scanner_run(
    scanner_run_id: str,
    payload: ScannerRunExecuteRequest = ScannerRunExecuteRequest(),
    db: Session = Depends(get_db),
):
    run = ScannerExecutionService(db).execute_run(scanner_run_id, initiated_by=payload.initiated_by)
    db.commit()
    db.refresh(run)
    return run


@router.get("/scanner-results/{scanner_result_id}", response_model=ScannerResultRead)
def get_scanner_result(scanner_result_id: str, db: Session = Depends(get_db)):
    result = db.get(ScannerResult, scanner_result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Scanner result not found")
    return result


@router.get("/systems/{system_id}/recommended-scans", response_model=SystemScanRecommendations)
def get_recommended_scans(
    system_id: str,
    assessment_profile_id: Optional[str] = None,
    db: Session = Depends(get_db),
) -> dict:
    return ScannerExecutionService(db).recommended_scans(
        system_id,
        assessment_profile_id=assessment_profile_id,
    )


@router.get("/systems/{system_id}/scanner-runs", response_model=List[ScannerRunRead])
def get_system_scanner_runs(system_id: str, db: Session = Depends(get_db)) -> list:
    return db.scalars(
        select(ScannerRun).where(ScannerRun.system_id == system_id).order_by(ScannerRun.created_at.desc())
    ).all()


@router.get("/scanner-adapters", response_model=List[ScannerAdapterRead])
def list_scanner_adapters() -> list[dict]:
    garak_adapter = GarakCliAdapter()
    return [
        {
            "adapter_name": "garak_cli_adapter",
            "scanner_name": garak_adapter.get_name(),
            "scanner_version": garak_adapter.get_version(),
            "supported_execution_modes": ["cli"],
            "supported_scan_types": [
                "prompt_injection",
                "jailbreak_resistance",
                "system_prompt_leakage",
            ],
            "mock_supported": False,
        },
    ]
