from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import IdMixin, TimestampMixin


class DomainScore(IdMixin, TimestampMixin, Base):
    __tablename__ = "domain_scores"

    system_id: Mapped[str] = mapped_column(
        ForeignKey("ai_systems.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assessment_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("assessments.id", ondelete="SET NULL"), index=True
    )
    score_domain: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    score_value: Mapped[float] = mapped_column(Float, nullable=False)
    weighted_score: Mapped[float] = mapped_column(Float, nullable=False)
    calculated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )
    calculation_version: Mapped[str] = mapped_column(String(40), nullable=False)

    system: Mapped["AISystem"] = relationship(back_populates="domain_scores")
    assessment: Mapped[Optional["Assessment"]] = relationship(back_populates="domain_scores")
    explanations: Mapped[List["ScoreExplanation"]] = relationship(
        back_populates="score", cascade="all, delete-orphan"
    )


class ScoreSnapshot(IdMixin, Base):
    __tablename__ = "score_snapshots"

    system_id: Mapped[str] = mapped_column(
        ForeignKey("ai_systems.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assessment_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("assessments.id", ondelete="SET NULL"), index=True
    )
    overall_score: Mapped[float] = mapped_column(Float, nullable=False)
    domain_scores: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    weights: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    explanation_summary: Mapped[Optional[str]] = mapped_column(Text)
    calculation_version: Mapped[str] = mapped_column(String(40), nullable=False)
    calculated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    system: Mapped["AISystem"] = relationship(back_populates="score_snapshots")
    assessment: Mapped[Optional["Assessment"]] = relationship(back_populates="score_snapshots")
