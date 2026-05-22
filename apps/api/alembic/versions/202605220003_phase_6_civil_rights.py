"""phase 6 civil rights assessment support

Revision ID: 202605220003
Revises: 202605220002
Create Date: 2026-05-22
"""

from alembic import op
import sqlalchemy as sa

revision = "202605220003"
down_revision = "202605220002"
branch_labels = None
depends_on = None


def timestamps() -> list:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    ]


def upgrade() -> None:
    op.create_table(
        "language_access_scenarios",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("system_id", sa.String(length=36), nullable=True),
        sa.Column("assessment_id", sa.String(length=36), nullable=True),
        sa.Column("name", sa.String(length=180), nullable=False),
        sa.Column("primary_language", sa.String(length=80), nullable=False),
        sa.Column("comparison_language", sa.String(length=80), nullable=False),
        sa.Column("scenario_type", sa.String(length=120), nullable=False),
        sa.Column("prompt_text", sa.Text(), nullable=False),
        sa.Column("expected_behavior", sa.Text(), nullable=False),
        sa.Column("evidence_requirements", sa.JSON(), nullable=False),
        *timestamps(),
        sa.ForeignKeyConstraint(["assessment_id"], ["assessments.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["system_id"], ["ai_systems.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_language_access_scenarios_assessment_id", "language_access_scenarios", ["assessment_id"])
    op.create_index("ix_language_access_scenarios_name", "language_access_scenarios", ["name"])
    op.create_index("ix_language_access_scenarios_scenario_type", "language_access_scenarios", ["scenario_type"])
    op.create_index("ix_language_access_scenarios_system_id", "language_access_scenarios", ["system_id"])

    op.create_table(
        "human_appeal_path_checks",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("system_id", sa.String(length=36), nullable=False),
        sa.Column("assessment_id", sa.String(length=36), nullable=True),
        sa.Column("check_type", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=60), nullable=False),
        sa.Column("required_control", sa.Text(), nullable=False),
        sa.Column("validation_notes", sa.Text(), nullable=True),
        sa.Column("evidence_requirements", sa.JSON(), nullable=False),
        sa.Column("evidence_ids", sa.JSON(), nullable=False),
        *timestamps(),
        sa.ForeignKeyConstraint(["assessment_id"], ["assessments.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["system_id"], ["ai_systems.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_human_appeal_path_checks_assessment_id", "human_appeal_path_checks", ["assessment_id"])
    op.create_index("ix_human_appeal_path_checks_check_type", "human_appeal_path_checks", ["check_type"])
    op.create_index("ix_human_appeal_path_checks_system_id", "human_appeal_path_checks", ["system_id"])

    op.add_column(
        "airb_reviews",
        sa.Column("civil_rights_review_status", sa.String(length=60), nullable=False, server_default="not_started"),
    )
    op.add_column(
        "airb_reviews",
        sa.Column("accessibility_review_status", sa.String(length=60), nullable=False, server_default="not_started"),
    )
    op.add_column(
        "airb_reviews",
        sa.Column("language_access_review_status", sa.String(length=60), nullable=False, server_default="not_started"),
    )
    op.add_column(
        "airb_reviews",
        sa.Column("fairness_review_status", sa.String(length=60), nullable=False, server_default="not_started"),
    )
    op.add_column(
        "airb_reviews",
        sa.Column("human_review_validated", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "airb_reviews",
        sa.Column("appeal_path_validated", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_column("airb_reviews", "appeal_path_validated")
    op.drop_column("airb_reviews", "human_review_validated")
    op.drop_column("airb_reviews", "fairness_review_status")
    op.drop_column("airb_reviews", "language_access_review_status")
    op.drop_column("airb_reviews", "accessibility_review_status")
    op.drop_column("airb_reviews", "civil_rights_review_status")
    op.drop_index("ix_human_appeal_path_checks_system_id", table_name="human_appeal_path_checks")
    op.drop_index("ix_human_appeal_path_checks_check_type", table_name="human_appeal_path_checks")
    op.drop_index("ix_human_appeal_path_checks_assessment_id", table_name="human_appeal_path_checks")
    op.drop_table("human_appeal_path_checks")
    op.drop_index("ix_language_access_scenarios_system_id", table_name="language_access_scenarios")
    op.drop_index("ix_language_access_scenarios_scenario_type", table_name="language_access_scenarios")
    op.drop_index("ix_language_access_scenarios_name", table_name="language_access_scenarios")
    op.drop_index("ix_language_access_scenarios_assessment_id", table_name="language_access_scenarios")
    op.drop_table("language_access_scenarios")
