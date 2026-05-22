from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import IdMixin


class ScoreHistory(IdMixin, Base):
    __tablename__ = "score_history"

    system_id: Mapped[str] = mapped_column(
        ForeignKey("ai_systems.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assessment_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("assessments.id", ondelete="SET NULL"), index=True
    )
    score_domain: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    previous_score: Mapped[Optional[float]] = mapped_column(Float)
    new_score: Mapped[float] = mapped_column(Float, nullable=False)
    change_reason: Mapped[str] = mapped_column(Text, nullable=False)
    triggered_by: Mapped[str] = mapped_column(String(160), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )

    system: Mapped["AISystem"] = relationship(back_populates="score_history")
    assessment: Mapped[Optional["Assessment"]] = relationship(back_populates="score_history")
