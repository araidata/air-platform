from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import AssessmentStatus
from app.models.mixins import IdMixin, TimestampMixin


class Assessment(IdMixin, TimestampMixin, Base):
    __tablename__ = "assessments"

    system_id: Mapped[str] = mapped_column(
        ForeignKey("ai_systems.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assessment_type: Mapped[str] = mapped_column(String(120), nullable=False)
    initiated_by: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[str] = mapped_column(
        String(40), nullable=False, default=AssessmentStatus.draft.value
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    summary: Mapped[Optional[str]] = mapped_column(Text)
    overall_score: Mapped[Optional[float]] = mapped_column(Float)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    system: Mapped["AISystem"] = relationship(back_populates="assessments")
    findings: Mapped[List["Finding"]] = relationship(back_populates="assessment")
    evidence: Mapped[List["Evidence"]] = relationship(back_populates="assessment")
    airb_reviews: Mapped[List["AirbReview"]] = relationship(back_populates="assessment")
    domain_scores: Mapped[List["DomainScore"]] = relationship(back_populates="assessment")
    score_history: Mapped[List["ScoreHistory"]] = relationship(back_populates="assessment")
    score_snapshots: Mapped[List["ScoreSnapshot"]] = relationship(back_populates="assessment")
