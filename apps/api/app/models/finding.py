from __future__ import annotations

from datetime import date
from typing import Any, List, Optional

from sqlalchemy import Boolean, Date, Float, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import FindingRetestStatus, FindingStatus
from app.models.mixins import IdMixin, TimestampMixin


class Finding(IdMixin, TimestampMixin, Base):
    __tablename__ = "findings"

    system_id: Mapped[str] = mapped_column(
        ForeignKey("ai_systems.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assessment_id: Mapped[str] = mapped_column(
        ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    scanner_name: Mapped[str] = mapped_column(String(160), nullable=False)
    scanner_version: Mapped[str] = mapped_column(String(80), nullable=False)
    domain: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    confidence: Mapped[str] = mapped_column(String(40), nullable=False)
    title: Mapped[str] = mapped_column(String(260), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_summary: Mapped[str] = mapped_column(Text, nullable=False)
    remediation: Mapped[str] = mapped_column(Text, nullable=False)
    owner_id: Mapped[Optional[str]] = mapped_column(ForeignKey("owners.id"), index=True)
    status: Mapped[str] = mapped_column(
        String(40), nullable=False, default=FindingStatus.new.value, index=True
    )
    due_date: Mapped[Optional[date]] = mapped_column(Date)
    retest_status: Mapped[str] = mapped_column(
        String(40), nullable=False, default=FindingRetestStatus.not_started.value
    )
    score_impact: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    risk_accepted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    approval_blocking: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    system: Mapped["AISystem"] = relationship(back_populates="findings")
    assessment: Mapped["Assessment"] = relationship(back_populates="findings")
    owner: Mapped[Optional["Owner"]] = relationship(back_populates="findings")
    evidence: Mapped[List["Evidence"]] = relationship(back_populates="finding")
    retests: Mapped[List["Retest"]] = relationship(back_populates="finding")
    framework_mappings: Mapped[List["FrameworkMapping"]] = relationship(back_populates="finding")
    risk_acceptances: Mapped[List["RiskAcceptance"]] = relationship(back_populates="finding")
