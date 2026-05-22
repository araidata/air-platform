from datetime import datetime
from typing import Dict, List, Optional

from app.schemas.base import ApiModel, StrictApiModel


class ScoreExplanationRead(ApiModel):
    id: str
    score_id: str
    explanation_type: str
    title: str
    description: str
    weight: float
    impact_value: float
    related_finding_id: Optional[str]
    created_at: datetime


class DomainScoreRead(ApiModel):
    id: str
    system_id: str
    assessment_id: Optional[str]
    score_domain: str
    score_value: float
    weighted_score: float
    calculated_at: datetime
    calculation_version: str
    created_at: datetime
    updated_at: datetime


class DomainScoreWithExplanations(DomainScoreRead):
    explanations: List[ScoreExplanationRead] = []


class ScoreHistoryRead(ApiModel):
    id: str
    system_id: str
    assessment_id: Optional[str]
    score_domain: str
    previous_score: Optional[float]
    new_score: float
    change_reason: str
    triggered_by: str
    created_at: datetime


class ScoreSnapshotRead(ApiModel):
    id: str
    system_id: str
    assessment_id: Optional[str]
    overall_score: float
    domain_scores: Dict[str, float]
    weights: Dict[str, float]
    explanation_summary: Optional[str]
    calculation_version: str
    calculated_at: datetime
    created_at: datetime


class ScoreRecalculateRequest(StrictApiModel):
    triggered_by: str = "operator"
    change_reason: str = "manual score recalculation"


class ScoreRecalculateResponse(ApiModel):
    system_id: str
    assessment_id: Optional[str]
    scores: List[DomainScoreRead]
    snapshot: ScoreSnapshotRead
