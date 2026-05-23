from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import IdMixin, TimestampMixin


class AssessmentToolRun(IdMixin, TimestampMixin, Base):
    __tablename__ = "assessment_tool_runs"

    engine: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="pending", index=True)
    target_name: Mapped[str] = mapped_column(String(200), nullable=False)
    target_url: Mapped[str] = mapped_column(String(500), nullable=False)
    method: Mapped[str] = mapped_column(String(12), nullable=False, default="POST")
    selected_tests: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    request_template: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    response_path: Mapped[str] = mapped_column(String(200), nullable=False, default="response")
    request_headers: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    steps: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    findings: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    report: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    artifacts: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
