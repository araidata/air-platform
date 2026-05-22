from __future__ import annotations

from sqlalchemy import Boolean, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import IdMixin, TimestampMixin


class AssessmentProfile(IdMixin, TimestampMixin, Base):
    __tablename__ = "assessment_profiles"

    profile_name: Mapped[str] = mapped_column(String(180), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    applicable_risk_tiers: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    applicable_system_types: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    required_scan_types: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    optional_scan_types: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    required_evidence_types: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    recommended_scanners: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    governance_expectations: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    score_domains_affected: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
