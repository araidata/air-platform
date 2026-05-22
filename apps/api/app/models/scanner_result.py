from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import IdMixin


class ScannerResult(IdMixin, Base):
    __tablename__ = "scanner_results"

    scanner_run_id: Mapped[str] = mapped_column(
        ForeignKey("scanner_runs.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    raw_result_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    normalized: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    normalization_version: Mapped[str] = mapped_column(String(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    scanner_run: Mapped["ScannerRun"] = relationship(back_populates="result")
