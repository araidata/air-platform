from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ai_system import AISystem
from app.models.enums import AuditEventType
from app.schemas.ai_system import AISystemCreate, AISystemRead, AISystemUpdate
from app.services.audit_event_service import AuditEventService

router = APIRouter()


@router.get("", response_model=List[AISystemRead])
def list_systems(db: Session = Depends(get_db)) -> list:
    return db.scalars(select(AISystem).order_by(AISystem.system_name)).all()


@router.get("/{system_id}", response_model=AISystemRead)
def get_system(system_id: str, db: Session = Depends(get_db)) -> AISystem:
    system = db.get(AISystem, system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    return system


@router.post("", response_model=AISystemRead, status_code=201)
def create_system(payload: AISystemCreate, db: Session = Depends(get_db)) -> AISystem:
    system = AISystem(**payload.model_dump())
    db.add(system)
    db.flush()
    AuditEventService(db).record(
        entity_type="system",
        entity_id=system.id,
        event_type=AuditEventType.system_created,
        actor="operator",
        new_value=system.system_name,
    )
    db.commit()
    db.refresh(system)
    return system


@router.patch("/{system_id}", response_model=AISystemRead)
def update_system(
    system_id: str, payload: AISystemUpdate, db: Session = Depends(get_db)
) -> AISystem:
    system = db.get(AISystem, system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(system, key, value)
    db.commit()
    db.refresh(system)
    return system
