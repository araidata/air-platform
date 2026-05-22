from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from app.models.score import DomainScore
from app.models.score_explanation import ScoreExplanation
from app.models.score_history import ScoreHistory
from app.schemas.score import (
    DomainScoreRead,
    DomainScoreWithExplanations,
    ScoreExplanationRead,
    ScoreHistoryRead,
    ScoreRecalculateRequest,
    ScoreRecalculateResponse,
)
from app.scoring.scoring_engine import ScoringEngine

router = APIRouter()


@router.get("/scores", response_model=List[DomainScoreRead])
def list_scores(db: Session = Depends(get_db)) -> list:
    return db.scalars(
        select(DomainScore).order_by(DomainScore.calculated_at.desc(), DomainScore.score_domain)
    ).all()


@router.get("/scores/{score_id}", response_model=DomainScoreWithExplanations)
def get_score(score_id: str, db: Session = Depends(get_db)) -> DomainScore:
    score = db.scalar(
        select(DomainScore)
        .where(DomainScore.id == score_id)
        .options(selectinload(DomainScore.explanations))
    )
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")
    return score


@router.get("/scores/{score_id}/explanations", response_model=List[ScoreExplanationRead])
def get_score_explanations(score_id: str, db: Session = Depends(get_db)) -> list:
    if not db.get(DomainScore, score_id):
        raise HTTPException(status_code=404, detail="Score not found")
    return db.scalars(
        select(ScoreExplanation)
        .where(ScoreExplanation.score_id == score_id)
        .order_by(ScoreExplanation.impact_value, ScoreExplanation.created_at)
    ).all()


@router.get("/systems/{system_id}/scores", response_model=List[DomainScoreWithExplanations])
def get_system_scores(system_id: str, db: Session = Depends(get_db)) -> list:
    scores = db.scalars(
        select(DomainScore)
        .where(DomainScore.system_id == system_id)
        .options(selectinload(DomainScore.explanations))
        .order_by(DomainScore.calculated_at.desc())
    ).all()
    if not scores:
        scores, _ = ScoringEngine(db).recalculate_system_scores(
            system_id,
            triggered_by="system",
            change_reason="lazy score initialization",
        )
        db.commit()
        scores = db.scalars(
            select(DomainScore)
            .where(DomainScore.system_id == system_id)
            .options(selectinload(DomainScore.explanations))
            .order_by(DomainScore.calculated_at.desc())
        ).all()
    latest_by_domain = {}
    for score in scores:
        latest_by_domain.setdefault(score.score_domain, score)
    return sorted(latest_by_domain.values(), key=lambda score: score.score_domain)


@router.get("/systems/{system_id}/score-history", response_model=List[ScoreHistoryRead])
def get_system_score_history(system_id: str, db: Session = Depends(get_db)) -> list:
    return db.scalars(
        select(ScoreHistory)
        .where(ScoreHistory.system_id == system_id)
        .order_by(ScoreHistory.created_at.desc())
    ).all()


@router.post("/systems/{system_id}/recalculate-scores", response_model=ScoreRecalculateResponse)
def recalculate_system_scores(
    system_id: str,
    payload: ScoreRecalculateRequest = ScoreRecalculateRequest(),
    db: Session = Depends(get_db),
) -> dict:
    scores, snapshot = ScoringEngine(db).recalculate_system_scores(
        system_id,
        triggered_by=payload.triggered_by,
        change_reason=payload.change_reason,
    )
    db.commit()
    return {"system_id": system_id, "assessment_id": snapshot.assessment_id, "scores": scores, "snapshot": snapshot}


@router.post("/assessments/{assessment_id}/recalculate-scores", response_model=ScoreRecalculateResponse)
def recalculate_assessment_scores(
    assessment_id: str,
    payload: ScoreRecalculateRequest = ScoreRecalculateRequest(),
    db: Session = Depends(get_db),
) -> dict:
    scores, snapshot = ScoringEngine(db).recalculate_assessment_scores(
        assessment_id,
        triggered_by=payload.triggered_by,
        change_reason=payload.change_reason,
    )
    db.commit()
    return {
        "system_id": snapshot.system_id,
        "assessment_id": assessment_id,
        "scores": scores,
        "snapshot": snapshot,
    }
