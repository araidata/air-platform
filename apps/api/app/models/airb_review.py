from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import AirbReviewStatus
from app.models.mixins import IdMixin, TimestampMixin


class AirbReview(IdMixin, TimestampMixin, Base):
    __tablename__ = "airb_reviews"

    system_id: Mapped[str] = mapped_column(
        ForeignKey("ai_systems.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assessment_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("assessments.id", ondelete="SET NULL"), index=True
    )
    review_status: Mapped[str] = mapped_column(
        String(60), nullable=False, default=AirbReviewStatus.pending.value, index=True
    )
    decision_notes: Mapped[Optional[str]] = mapped_column(Text)
    reviewed_by: Mapped[Optional[str]] = mapped_column(String(160))
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    exception_granted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    expiration_date: Mapped[Optional[date]] = mapped_column(Date)

    system: Mapped["AISystem"] = relationship(back_populates="airb_reviews")
    assessment: Mapped[Optional["Assessment"]] = relationship(back_populates="airb_reviews")
