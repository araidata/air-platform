from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.owner import Owner
from app.schemas.owner import OwnerCreate, OwnerRead

router = APIRouter()


@router.get("", response_model=List[OwnerRead])
def list_owners(db: Session = Depends(get_db)) -> list:
    return db.scalars(select(Owner).order_by(Owner.display_name)).all()


@router.post("", response_model=OwnerRead, status_code=201)
def create_owner(payload: OwnerCreate, db: Session = Depends(get_db)) -> Owner:
    owner = Owner(**payload.model_dump())
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return owner
