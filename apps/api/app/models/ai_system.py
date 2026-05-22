from __future__ import annotations

from typing import List, Optional

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import IdMixin, TimestampMixin


class AISystem(IdMixin, TimestampMixin, Base):
    __tablename__ = "ai_systems"

    system_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    department_owner: Mapped[str] = mapped_column(String(160), nullable=False)
    business_purpose: Mapped[str] = mapped_column(Text, nullable=False)
    public_facing: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    rights_impacting: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    safety_impacting: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    uses_pii: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    uses_phi: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    uses_cjis: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    model_provider: Mapped[Optional[str]] = mapped_column(String(160))
    model_version: Mapped[Optional[str]] = mapped_column(String(160))
    deployment_environment: Mapped[str] = mapped_column(String(80), nullable=False)
    risk_tier: Mapped[str] = mapped_column(String(40), nullable=False, default="moderate")
    approval_status: Mapped[str] = mapped_column(String(80), nullable=False, default="pending")

    assessments: Mapped[List["Assessment"]] = relationship(back_populates="system")
    findings: Mapped[List["Finding"]] = relationship(back_populates="system")
    evidence: Mapped[List["Evidence"]] = relationship(back_populates="system")
    airb_reviews: Mapped[List["AirbReview"]] = relationship(back_populates="system")
