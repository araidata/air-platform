from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import IdMixin, TimestampMixin


class LanguageAccessScenario(IdMixin, TimestampMixin, Base):
    __tablename__ = "language_access_scenarios"

    system_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("ai_systems.id", ondelete="CASCADE"), index=True
    )
    assessment_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("assessments.id", ondelete="SET NULL"), index=True
    )
    name: Mapped[str] = mapped_column(String(180), nullable=False, index=True)
    primary_language: Mapped[str] = mapped_column(String(80), nullable=False)
    comparison_language: Mapped[str] = mapped_column(String(80), nullable=False)
    scenario_type: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    prompt_text: Mapped[str] = mapped_column(Text, nullable=False)
    expected_behavior: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_requirements: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

    system: Mapped[Optional["AISystem"]] = relationship()
    assessment: Mapped[Optional["Assessment"]] = relationship()
