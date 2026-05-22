from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ai_system import AISystem
from app.models.airb_review import AirbReview
from app.models.assessment import Assessment
from app.models.enums import AuditEventType
from app.schemas.airb_review import AirbReviewCreate, AirbReviewRead, AirbReviewUpdate
from app.services.audit_event_service import AuditEventService

router = APIRouter()


@router.get("", response_model=List[AirbReviewRead])
def list_airb_reviews(db: Session = Depends(get_db)) -> list:
    return db.scalars(select(AirbReview).order_by(AirbReview.created_at.desc())).all()


@router.post("", response_model=AirbReviewRead, status_code=201)
def create_airb_review(
    payload: AirbReviewCreate, db: Session = Depends(get_db)
) -> AirbReview:
    if not db.get(AISystem, payload.system_id):
        raise HTTPException(status_code=404, detail="System not found")
    if payload.assessment_id and not db.get(Assessment, payload.assessment_id):
        raise HTTPException(status_code=404, detail="Assessment not found")
    data = payload.model_dump(exclude={"actor"})
    data["review_status"] = payload.review_status.value
    review = AirbReview(**data)
    db.add(review)
    db.flush()
    AuditEventService(db).record(
        entity_type="airb_review",
        entity_id=review.id,
        event_type=AuditEventType.airb_review_created,
        actor=payload.actor,
        new_value=review.review_status,
    )
    db.commit()
    db.refresh(review)
    return review


@router.patch("/{review_id}", response_model=AirbReviewRead)
def update_airb_review(
    review_id: str, payload: AirbReviewUpdate, db: Session = Depends(get_db)
) -> AirbReview:
    review = db.get(AirbReview, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="AIRB review not found")
    updates = payload.model_dump(exclude_unset=True, exclude={"actor"})
    if "review_status" in updates and updates["review_status"] is not None:
        updates["review_status"] = updates["review_status"].value
    old_status = review.review_status
    for key, value in updates.items():
        setattr(review, key, value)
    if "review_status" in updates and review.review_status != old_status:
        AuditEventService(db).record(
            entity_type="airb_review",
            entity_id=review.id,
            event_type=AuditEventType.airb_decision_recorded,
            actor=payload.actor,
            old_value=old_status,
            new_value=review.review_status,
            notes=review.decision_notes,
        )
    db.commit()
    db.refresh(review)
    return review
