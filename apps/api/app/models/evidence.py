from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import IdMixin


class Evidence(IdMixin, Base):
    __tablename__ = "evidence"

    finding_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("findings.id", ondelete="SET NULL"), index=True
    )
    assessment_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("assessments.id", ondelete="SET NULL"), index=True
    )
    system_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("ai_systems.id", ondelete="SET NULL"), index=True
    )
    evidence_type: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(260), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    file_path: Mapped[Optional[str]] = mapped_column(String(500))
    raw_text: Mapped[Optional[str]] = mapped_column(Text)
    content_type: Mapped[Optional[str]] = mapped_column(String(120))
    created_by: Mapped[str] = mapped_column(String(160), nullable=False)
    hash: Mapped[Optional[str]] = mapped_column(String(128))
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    finding: Mapped[Optional["Finding"]] = relationship(back_populates="evidence")
    assessment: Mapped[Optional["Assessment"]] = relationship(back_populates="evidence")
    system: Mapped[Optional["AISystem"]] = relationship(back_populates="evidence")
