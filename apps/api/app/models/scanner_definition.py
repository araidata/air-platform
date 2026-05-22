from __future__ import annotations

from sqlalchemy import Boolean, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import IdMixin, TimestampMixin


class ScannerDefinition(IdMixin, TimestampMixin, Base):
    __tablename__ = "scanner_definitions"

    scanner_name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    scanner_category: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    adapter_name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    scanner_version: Mapped[str] = mapped_column(String(80), nullable=False)
    execution_mode: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    supported_domains: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    supported_scan_types: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    mock_supported: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    requires_credentials: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
