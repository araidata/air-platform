from __future__ import annotations

from sqlalchemy import Boolean, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import IdMixin, TimestampMixin


class ScanType(IdMixin, TimestampMixin, Base):
    __tablename__ = "scan_types"

    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    domain: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    default_severity: Mapped[str] = mapped_column(String(40), nullable=False)
    required_for_risk_tiers: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    applicable_system_types: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    evidence_expectations: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
