"""phase 4 scanner ecosystem

Revision ID: 202605220002
Revises: 202605220001
Create Date: 2026-05-22
"""

from alembic import op
import sqlalchemy as sa

revision = "202605220002"
down_revision = "202605220001"
branch_labels = None
depends_on = None


def timestamps() -> list:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    ]


def upgrade() -> None:
    op.create_table(
        "scanner_definitions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("scanner_name", sa.String(length=120), nullable=False),
        sa.Column("display_name", sa.String(length=180), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("scanner_category", sa.String(length=80), nullable=False),
        sa.Column("adapter_name", sa.String(length=120), nullable=False),
        sa.Column("scanner_version", sa.String(length=80), nullable=False),
        sa.Column("execution_mode", sa.String(length=40), nullable=False),
        sa.Column("supported_domains", sa.JSON(), nullable=False),
        sa.Column("supported_scan_types", sa.JSON(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("mock_supported", sa.Boolean(), nullable=False),
        sa.Column("requires_credentials", sa.Boolean(), nullable=False),
        *timestamps(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("scanner_name"),
    )
    op.create_index("ix_scanner_definitions_adapter_name", "scanner_definitions", ["adapter_name"])
    op.create_index("ix_scanner_definitions_enabled", "scanner_definitions", ["enabled"])
    op.create_index("ix_scanner_definitions_execution_mode", "scanner_definitions", ["execution_mode"])
    op.create_index("ix_scanner_definitions_scanner_category", "scanner_definitions", ["scanner_category"])
    op.create_index("ix_scanner_definitions_scanner_name", "scanner_definitions", ["scanner_name"])

    op.create_table(
        "scan_types",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("display_name", sa.String(length=180), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("domain", sa.String(length=80), nullable=False),
        sa.Column("default_severity", sa.String(length=40), nullable=False),
        sa.Column("required_for_risk_tiers", sa.JSON(), nullable=False),
        sa.Column("applicable_system_types", sa.JSON(), nullable=False),
        sa.Column("evidence_expectations", sa.JSON(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        *timestamps(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_scan_types_domain", "scan_types", ["domain"])
    op.create_index("ix_scan_types_enabled", "scan_types", ["enabled"])
    op.create_index("ix_scan_types_name", "scan_types", ["name"])

    op.create_table(
        "assessment_profiles",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("profile_name", sa.String(length=180), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("applicable_risk_tiers", sa.JSON(), nullable=False),
        sa.Column("applicable_system_types", sa.JSON(), nullable=False),
        sa.Column("required_scan_types", sa.JSON(), nullable=False),
        sa.Column("optional_scan_types", sa.JSON(), nullable=False),
        sa.Column("required_evidence_types", sa.JSON(), nullable=False),
        sa.Column("recommended_scanners", sa.JSON(), nullable=False),
        sa.Column("governance_expectations", sa.JSON(), nullable=False),
        sa.Column("score_domains_affected", sa.JSON(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        *timestamps(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("profile_name"),
    )
    op.create_index("ix_assessment_profiles_enabled", "assessment_profiles", ["enabled"])
    op.create_index("ix_assessment_profiles_profile_name", "assessment_profiles", ["profile_name"])

    op.create_table(
        "scanner_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("system_id", sa.String(length=36), nullable=False),
        sa.Column("assessment_id", sa.String(length=36), nullable=False),
        sa.Column("scanner_definition_id", sa.String(length=36), nullable=False),
        sa.Column("scan_type_id", sa.String(length=36), nullable=False),
        sa.Column("assessment_profile_id", sa.String(length=36), nullable=True),
        sa.Column("scanner_name", sa.String(length=160), nullable=False),
        sa.Column("scanner_version", sa.String(length=80), nullable=False),
        sa.Column("adapter_name", sa.String(length=120), nullable=False),
        sa.Column("execution_status", sa.String(length=40), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("initiated_by", sa.String(length=160), nullable=False),
        sa.Column("raw_output_path", sa.String(length=500), nullable=True),
        sa.Column("log_path", sa.String(length=500), nullable=True),
        sa.Column("finding_count", sa.Integer(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        *timestamps(),
        sa.ForeignKeyConstraint(["assessment_id"], ["assessments.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["assessment_profile_id"], ["assessment_profiles.id"]),
        sa.ForeignKeyConstraint(["scan_type_id"], ["scan_types.id"]),
        sa.ForeignKeyConstraint(["scanner_definition_id"], ["scanner_definitions.id"]),
        sa.ForeignKeyConstraint(["system_id"], ["ai_systems.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_scanner_runs_adapter_name", "scanner_runs", ["adapter_name"])
    op.create_index("ix_scanner_runs_assessment_id", "scanner_runs", ["assessment_id"])
    op.create_index("ix_scanner_runs_assessment_profile_id", "scanner_runs", ["assessment_profile_id"])
    op.create_index("ix_scanner_runs_execution_status", "scanner_runs", ["execution_status"])
    op.create_index("ix_scanner_runs_scan_type_id", "scanner_runs", ["scan_type_id"])
    op.create_index("ix_scanner_runs_scanner_definition_id", "scanner_runs", ["scanner_definition_id"])
    op.create_index("ix_scanner_runs_scanner_name", "scanner_runs", ["scanner_name"])
    op.create_index("ix_scanner_runs_system_id", "scanner_runs", ["system_id"])

    op.create_table(
        "scanner_results",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("scanner_run_id", sa.String(length=36), nullable=False),
        sa.Column("raw_result_json", sa.JSON(), nullable=False),
        sa.Column("normalized", sa.JSON(), nullable=False),
        sa.Column("normalization_version", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["scanner_run_id"], ["scanner_runs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("scanner_run_id"),
    )
    op.create_index("ix_scanner_results_scanner_run_id", "scanner_results", ["scanner_run_id"])


def downgrade() -> None:
    op.drop_index("ix_scanner_results_scanner_run_id", table_name="scanner_results")
    op.drop_table("scanner_results")
    op.drop_index("ix_scanner_runs_system_id", table_name="scanner_runs")
    op.drop_index("ix_scanner_runs_scanner_name", table_name="scanner_runs")
    op.drop_index("ix_scanner_runs_scanner_definition_id", table_name="scanner_runs")
    op.drop_index("ix_scanner_runs_scan_type_id", table_name="scanner_runs")
    op.drop_index("ix_scanner_runs_execution_status", table_name="scanner_runs")
    op.drop_index("ix_scanner_runs_assessment_profile_id", table_name="scanner_runs")
    op.drop_index("ix_scanner_runs_assessment_id", table_name="scanner_runs")
    op.drop_index("ix_scanner_runs_adapter_name", table_name="scanner_runs")
    op.drop_table("scanner_runs")
    op.drop_index("ix_assessment_profiles_profile_name", table_name="assessment_profiles")
    op.drop_index("ix_assessment_profiles_enabled", table_name="assessment_profiles")
    op.drop_table("assessment_profiles")
    op.drop_index("ix_scan_types_name", table_name="scan_types")
    op.drop_index("ix_scan_types_enabled", table_name="scan_types")
    op.drop_index("ix_scan_types_domain", table_name="scan_types")
    op.drop_table("scan_types")
    op.drop_index("ix_scanner_definitions_scanner_name", table_name="scanner_definitions")
    op.drop_index("ix_scanner_definitions_scanner_category", table_name="scanner_definitions")
    op.drop_index("ix_scanner_definitions_execution_mode", table_name="scanner_definitions")
    op.drop_index("ix_scanner_definitions_enabled", table_name="scanner_definitions")
    op.drop_index("ix_scanner_definitions_adapter_name", table_name="scanner_definitions")
    op.drop_table("scanner_definitions")
