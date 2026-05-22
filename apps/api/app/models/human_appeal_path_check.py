from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import IdMixin, TimestampMixin


class HumanAppealPathCheck(IdMixin, TimestampMixin, Base):
    __tablename__ = "human_appeal_path_checks"

    system_id: Mapped[str] = mapped_column(
        ForeignKey("ai_systems.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assessment_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("assessments.id", ondelete="SET NULL"), index=True
    )
    check_type: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(60), nullable=False, default="needs_evidence")
    required_control: Mapped[str] = mapped_column(Text, nullable=False)
    validation_notes: Mapped[Optional[str]] = mapped_column(Text)
    evidence_requirements: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    evidence_ids: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

    system: Mapped["AISystem"] = relationship()
    assessment: Mapped[Optional["Assessment"]] = relationship()
