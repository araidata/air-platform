"""Add direct assessment tool runs.

Revision ID: 202605220005
Revises: 202605220004
Create Date: 2026-05-22 00:05:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "202605220005"
down_revision: Union[str, None] = "202605220004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "assessment_tool_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("engine", sa.String(length=40), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("target_name", sa.String(length=200), nullable=False),
        sa.Column("target_url", sa.String(length=500), nullable=False),
        sa.Column("method", sa.String(length=12), nullable=False),
        sa.Column("selected_tests", sa.JSON(), nullable=False),
        sa.Column("request_template", sa.JSON(), nullable=False),
        sa.Column("response_path", sa.String(length=200), nullable=False),
        sa.Column("request_headers", sa.JSON(), nullable=False),
        sa.Column("steps", sa.JSON(), nullable=False),
        sa.Column("findings", sa.JSON(), nullable=False),
        sa.Column("report", sa.JSON(), nullable=False),
        sa.Column("artifacts", sa.JSON(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_assessment_tool_runs")),
    )
    op.create_index(op.f("ix_assessment_tool_runs_engine"), "assessment_tool_runs", ["engine"], unique=False)
    op.create_index(op.f("ix_assessment_tool_runs_status"), "assessment_tool_runs", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_assessment_tool_runs_status"), table_name="assessment_tool_runs")
    op.drop_index(op.f("ix_assessment_tool_runs_engine"), table_name="assessment_tool_runs")
    op.drop_table("assessment_tool_runs")
