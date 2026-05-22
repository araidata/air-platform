from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import IdMixin


class ScoreExplanation(IdMixin, Base):
    __tablename__ = "score_explanations"

    score_id: Mapped[str] = mapped_column(
        ForeignKey("domain_scores.id", ondelete="CASCADE"), nullable=False, index=True
    )
    explanation_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(260), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    impact_value: Mapped[float] = mapped_column(Float, nullable=False)
    related_finding_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("findings.id", ondelete="SET NULL"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    score: Mapped["DomainScore"] = relationship(back_populates="explanations")
    related_finding: Mapped[Optional["Finding"]] = relationship(back_populates="score_explanations")
