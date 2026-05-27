from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import ScannerExecutionStatus
from app.models.mixins import IdMixin, TimestampMixin


class ScannerRun(IdMixin, TimestampMixin, Base):
    __tablename__ = "scanner_runs"

    system_id: Mapped[str] = mapped_column(
        ForeignKey("ai_systems.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assessment_id: Mapped[str] = mapped_column(
        ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    scanner_definition_id: Mapped[str] = mapped_column(
        ForeignKey("scanner_definitions.id"), nullable=False, index=True
    )
    scan_type_id: Mapped[str] = mapped_column(ForeignKey("scan_types.id"), nullable=False, index=True)
    assessment_profile_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("assessment_profiles.id"), index=True
    )
    scanner_name: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    scanner_version: Mapped[str] = mapped_column(String(80), nullable=False)
    adapter_name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    execution_status: Mapped[str] = mapped_column(
        String(40), nullable=False, default=ScannerExecutionStatus.pending.value, index=True
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    initiated_by: Mapped[str] = mapped_column(String(160), nullable=False)
    raw_output_path: Mapped[Optional[str]] = mapped_column(String(500))
    log_path: Mapped[Optional[str]] = mapped_column(String(500))
    finding_count: Mapped[int] = mapped_column(default=0, nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    execution_options: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    scanner_definition: Mapped["ScannerDefinition"] = relationship()
    scan_type: Mapped["ScanType"] = relationship()
    assessment_profile: Mapped[Optional["AssessmentProfile"]] = relationship()
    result: Mapped[Optional["ScannerResult"]] = relationship(
        back_populates="scanner_run", cascade="all, delete-orphan"
    )
