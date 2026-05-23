"""Add assessment target configuration to systems.

Revision ID: 202605220004
Revises: 202605220003
Create Date: 2026-05-22 00:04:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "202605220004"
down_revision: Union[str, None] = "202605220003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "ai_systems",
        sa.Column(
            "target_type",
            sa.String(length=80),
            nullable=False,
            server_default="manual_review_only",
        ),
    )
    op.add_column(
        "ai_systems",
        sa.Column(
            "target_location",
            sa.String(length=500),
            nullable=False,
            server_default="manual review packet",
        ),
    )
    op.add_column(
        "ai_systems",
        sa.Column("authentication_type", sa.String(length=80), nullable=False, server_default="none"),
    )
    op.add_column("ai_systems", sa.Column("authentication_reference", sa.String(length=300), nullable=True))
    op.add_column(
        "ai_systems",
        sa.Column(
            "assessment_method",
            sa.String(length=80),
            nullable=False,
            server_default="manual_governance_review",
        ),
    )
    op.add_column(
        "ai_systems",
        sa.Column("scanner_compatible", sa.JSON(), nullable=False, server_default="[]"),
    )
    op.add_column(
        "ai_systems",
        sa.Column("manual_review_only", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "ai_systems",
        sa.Column("uploaded_artifact_supported", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_column("ai_systems", "uploaded_artifact_supported")
    op.drop_column("ai_systems", "manual_review_only")
    op.drop_column("ai_systems", "scanner_compatible")
    op.drop_column("ai_systems", "assessment_method")
    op.drop_column("ai_systems", "authentication_reference")
    op.drop_column("ai_systems", "authentication_type")
    op.drop_column("ai_systems", "target_location")
    op.drop_column("ai_systems", "target_type")
