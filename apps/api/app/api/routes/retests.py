from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.retest import Retest
from app.schemas.retest import RetestRead, RetestUpdate
from app.services.retest_service import RetestService

router = APIRouter()


@router.get("/retests/{retest_id}", response_model=RetestRead)
def get_retest(retest_id: str, db: Session = Depends(get_db)) -> Retest:
    retest = db.get(Retest, retest_id)
    if not retest:
        raise HTTPException(status_code=404, detail="Retest not found")
    return retest


@router.patch("/retests/{retest_id}", response_model=RetestRead)
def update_retest(
    retest_id: str, payload: RetestUpdate, db: Session = Depends(get_db)
) -> Retest:
    retest = db.get(Retest, retest_id)
    if not retest:
        raise HTTPException(status_code=404, detail="Retest not found")
    retest = RetestService(db).update(retest, payload)
    db.commit()
    db.refresh(retest)
    return retest
