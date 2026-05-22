"""phase 3 scoring tables

Revision ID: 202605220001
Revises: 202605210001
Create Date: 2026-05-22
"""

from alembic import op
import sqlalchemy as sa

revision = "202605220001"
down_revision = "202605210001"
branch_labels = None
depends_on = None


def timestamps() -> list:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    ]


def upgrade() -> None:
    op.create_table(
        "domain_scores",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("system_id", sa.String(length=36), nullable=False),
        sa.Column("assessment_id", sa.String(length=36), nullable=True),
        sa.Column("score_domain", sa.String(length=80), nullable=False),
        sa.Column("score_value", sa.Float(), nullable=False),
        sa.Column("weighted_score", sa.Float(), nullable=False),
        sa.Column("calculated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("calculation_version", sa.String(length=40), nullable=False),
        *timestamps(),
        sa.ForeignKeyConstraint(["assessment_id"], ["assessments.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["system_id"], ["ai_systems.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_domain_scores_assessment_id", "domain_scores", ["assessment_id"])
    op.create_index("ix_domain_scores_calculated_at", "domain_scores", ["calculated_at"])
    op.create_index("ix_domain_scores_score_domain", "domain_scores", ["score_domain"])
    op.create_index("ix_domain_scores_system_id", "domain_scores", ["system_id"])

    op.create_table(
        "score_history",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("system_id", sa.String(length=36), nullable=False),
        sa.Column("assessment_id", sa.String(length=36), nullable=True),
        sa.Column("score_domain", sa.String(length=80), nullable=False),
        sa.Column("previous_score", sa.Float(), nullable=True),
        sa.Column("new_score", sa.Float(), nullable=False),
        sa.Column("change_reason", sa.Text(), nullable=False),
        sa.Column("triggered_by", sa.String(length=160), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["assessment_id"], ["assessments.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["system_id"], ["ai_systems.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_score_history_assessment_id", "score_history", ["assessment_id"])
    op.create_index("ix_score_history_created_at", "score_history", ["created_at"])
    op.create_index("ix_score_history_score_domain", "score_history", ["score_domain"])
    op.create_index("ix_score_history_system_id", "score_history", ["system_id"])

    op.create_table(
        "score_snapshots",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("system_id", sa.String(length=36), nullable=False),
        sa.Column("assessment_id", sa.String(length=36), nullable=True),
        sa.Column("overall_score", sa.Float(), nullable=False),
        sa.Column("domain_scores", sa.JSON(), nullable=False),
        sa.Column("weights", sa.JSON(), nullable=False),
        sa.Column("explanation_summary", sa.Text(), nullable=True),
        sa.Column("calculation_version", sa.String(length=40), nullable=False),
        sa.Column("calculated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["assessment_id"], ["assessments.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["system_id"], ["ai_systems.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_score_snapshots_assessment_id", "score_snapshots", ["assessment_id"])
    op.create_index("ix_score_snapshots_calculated_at", "score_snapshots", ["calculated_at"])
    op.create_index("ix_score_snapshots_system_id", "score_snapshots", ["system_id"])

    op.create_table(
        "score_explanations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("score_id", sa.String(length=36), nullable=False),
        sa.Column("explanation_type", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=260), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("impact_value", sa.Float(), nullable=False),
        sa.Column("related_finding_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["related_finding_id"], ["findings.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["score_id"], ["domain_scores.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_score_explanations_explanation_type",
        "score_explanations",
        ["explanation_type"],
    )
    op.create_index(
        "ix_score_explanations_related_finding_id",
        "score_explanations",
        ["related_finding_id"],
    )
    op.create_index("ix_score_explanations_score_id", "score_explanations", ["score_id"])


def downgrade() -> None:
    op.drop_index("ix_score_explanations_score_id", table_name="score_explanations")
    op.drop_index("ix_score_explanations_related_finding_id", table_name="score_explanations")
    op.drop_index("ix_score_explanations_explanation_type", table_name="score_explanations")
    op.drop_table("score_explanations")
    op.drop_index("ix_score_snapshots_system_id", table_name="score_snapshots")
    op.drop_index("ix_score_snapshots_calculated_at", table_name="score_snapshots")
    op.drop_index("ix_score_snapshots_assessment_id", table_name="score_snapshots")
    op.drop_table("score_snapshots")
    op.drop_index("ix_score_history_system_id", table_name="score_history")
    op.drop_index("ix_score_history_score_domain", table_name="score_history")
    op.drop_index("ix_score_history_created_at", table_name="score_history")
    op.drop_index("ix_score_history_assessment_id", table_name="score_history")
    op.drop_table("score_history")
    op.drop_index("ix_domain_scores_system_id", table_name="domain_scores")
    op.drop_index("ix_domain_scores_score_domain", table_name="domain_scores")
    op.drop_index("ix_domain_scores_calculated_at", table_name="domain_scores")
    op.drop_index("ix_domain_scores_assessment_id", table_name="domain_scores")
    op.drop_table("domain_scores")
