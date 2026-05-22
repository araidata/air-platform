"""phase 2 workflow tables

Revision ID: 202605210001
Revises:
Create Date: 2026-05-21
"""

from alembic import op
import sqlalchemy as sa

revision = "202605210001"
down_revision = None
branch_labels = None
depends_on = None


def timestamps() -> list:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    ]


def upgrade() -> None:
    op.create_table(
        "owners",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("display_name", sa.String(length=160), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("department", sa.String(length=160), nullable=False),
        sa.Column("role", sa.String(length=160), nullable=False),
        *timestamps(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_owners_email", "owners", ["email"])

    op.create_table(
        "ai_systems",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("system_name", sa.String(length=200), nullable=False),
        sa.Column("department_owner", sa.String(length=160), nullable=False),
        sa.Column("business_purpose", sa.Text(), nullable=False),
        sa.Column("public_facing", sa.Boolean(), nullable=False),
        sa.Column("rights_impacting", sa.Boolean(), nullable=False),
        sa.Column("safety_impacting", sa.Boolean(), nullable=False),
        sa.Column("uses_pii", sa.Boolean(), nullable=False),
        sa.Column("uses_phi", sa.Boolean(), nullable=False),
        sa.Column("uses_cjis", sa.Boolean(), nullable=False),
        sa.Column("model_provider", sa.String(length=160), nullable=True),
        sa.Column("model_version", sa.String(length=160), nullable=True),
        sa.Column("deployment_environment", sa.String(length=80), nullable=False),
        sa.Column("risk_tier", sa.String(length=40), nullable=False),
        sa.Column("approval_status", sa.String(length=80), nullable=False),
        *timestamps(),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_systems_system_name", "ai_systems", ["system_name"])

    op.create_table(
        "assessments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("system_id", sa.String(length=36), nullable=False),
        sa.Column("assessment_type", sa.String(length=120), nullable=False),
        sa.Column("initiated_by", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("overall_score", sa.Float(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        *timestamps(),
        sa.ForeignKeyConstraint(["system_id"], ["ai_systems.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_assessments_system_id", "assessments", ["system_id"])

    op.create_table(
        "findings",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("system_id", sa.String(length=36), nullable=False),
        sa.Column("assessment_id", sa.String(length=36), nullable=False),
        sa.Column("scanner_name", sa.String(length=160), nullable=False),
        sa.Column("scanner_version", sa.String(length=80), nullable=False),
        sa.Column("domain", sa.String(length=80), nullable=False),
        sa.Column("severity", sa.String(length=40), nullable=False),
        sa.Column("confidence", sa.String(length=40), nullable=False),
        sa.Column("title", sa.String(length=260), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("evidence_summary", sa.Text(), nullable=False),
        sa.Column("remediation", sa.Text(), nullable=False),
        sa.Column("owner_id", sa.String(length=36), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("retest_status", sa.String(length=40), nullable=False),
        sa.Column("score_impact", sa.JSON(), nullable=False),
        sa.Column("risk_accepted", sa.Boolean(), nullable=False),
        sa.Column("approval_blocking", sa.Boolean(), nullable=False),
        *timestamps(),
        sa.ForeignKeyConstraint(["assessment_id"], ["assessments.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["owner_id"], ["owners.id"]),
        sa.ForeignKeyConstraint(["system_id"], ["ai_systems.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_findings_assessment_id", "findings", ["assessment_id"])
    op.create_index("ix_findings_domain", "findings", ["domain"])
    op.create_index("ix_findings_owner_id", "findings", ["owner_id"])
    op.create_index("ix_findings_severity", "findings", ["severity"])
    op.create_index("ix_findings_status", "findings", ["status"])
    op.create_index("ix_findings_system_id", "findings", ["system_id"])

    op.create_table(
        "evidence",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("finding_id", sa.String(length=36), nullable=True),
        sa.Column("assessment_id", sa.String(length=36), nullable=True),
        sa.Column("system_id", sa.String(length=36), nullable=True),
        sa.Column("evidence_type", sa.String(length=60), nullable=False),
        sa.Column("title", sa.String(length=260), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("file_path", sa.String(length=500), nullable=True),
        sa.Column("raw_text", sa.Text(), nullable=True),
        sa.Column("content_type", sa.String(length=120), nullable=True),
        sa.Column("created_by", sa.String(length=160), nullable=False),
        sa.Column("hash", sa.String(length=128), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["assessment_id"], ["assessments.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["finding_id"], ["findings.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["system_id"], ["ai_systems.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_evidence_assessment_id", "evidence", ["assessment_id"])
    op.create_index("ix_evidence_evidence_type", "evidence", ["evidence_type"])
    op.create_index("ix_evidence_finding_id", "evidence", ["finding_id"])
    op.create_index("ix_evidence_system_id", "evidence", ["system_id"])

    op.create_table(
        "audit_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("entity_type", sa.String(length=80), nullable=False),
        sa.Column("entity_id", sa.String(length=80), nullable=False),
        sa.Column("event_type", sa.String(length=80), nullable=False),
        sa.Column("actor", sa.String(length=160), nullable=False),
        sa.Column("old_value", sa.Text(), nullable=True),
        sa.Column("new_value", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_audit_events_created_at", "audit_events", ["created_at"])
    op.create_index("ix_audit_events_entity_id", "audit_events", ["entity_id"])
    op.create_index("ix_audit_events_entity_type", "audit_events", ["entity_type"])
    op.create_index("ix_audit_events_event_type", "audit_events", ["event_type"])

    op.create_table(
        "retests",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("finding_id", sa.String(length=36), nullable=False),
        sa.Column("initiated_by", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("result_summary", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        *timestamps(),
        sa.ForeignKeyConstraint(["finding_id"], ["findings.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_retests_finding_id", "retests", ["finding_id"])
    op.create_index("ix_retests_status", "retests", ["status"])

    op.create_table(
        "airb_reviews",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("system_id", sa.String(length=36), nullable=False),
        sa.Column("assessment_id", sa.String(length=36), nullable=True),
        sa.Column("review_status", sa.String(length=60), nullable=False),
        sa.Column("decision_notes", sa.Text(), nullable=True),
        sa.Column("reviewed_by", sa.String(length=160), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("exception_granted", sa.Boolean(), nullable=False),
        sa.Column("expiration_date", sa.Date(), nullable=True),
        *timestamps(),
        sa.ForeignKeyConstraint(["assessment_id"], ["assessments.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["system_id"], ["ai_systems.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_airb_reviews_assessment_id", "airb_reviews", ["assessment_id"])
    op.create_index("ix_airb_reviews_review_status", "airb_reviews", ["review_status"])
    op.create_index("ix_airb_reviews_system_id", "airb_reviews", ["system_id"])

    op.create_table(
        "framework_mappings",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("finding_id", sa.String(length=36), nullable=False),
        sa.Column("framework", sa.String(length=160), nullable=False),
        sa.Column("control", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["finding_id"], ["findings.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_framework_mappings_finding_id", "framework_mappings", ["finding_id"])
    op.create_index("ix_framework_mappings_framework", "framework_mappings", ["framework"])

    op.create_table(
        "risk_acceptances",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("finding_id", sa.String(length=36), nullable=False),
        sa.Column("accepted_by", sa.String(length=160), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("expiration_date", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["finding_id"], ["findings.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_risk_acceptances_finding_id", "risk_acceptances", ["finding_id"])


def downgrade() -> None:
    op.drop_index("ix_risk_acceptances_finding_id", table_name="risk_acceptances")
    op.drop_table("risk_acceptances")
    op.drop_index("ix_framework_mappings_framework", table_name="framework_mappings")
    op.drop_index("ix_framework_mappings_finding_id", table_name="framework_mappings")
    op.drop_table("framework_mappings")
    op.drop_index("ix_airb_reviews_system_id", table_name="airb_reviews")
    op.drop_index("ix_airb_reviews_review_status", table_name="airb_reviews")
    op.drop_index("ix_airb_reviews_assessment_id", table_name="airb_reviews")
    op.drop_table("airb_reviews")
    op.drop_index("ix_retests_status", table_name="retests")
    op.drop_index("ix_retests_finding_id", table_name="retests")
    op.drop_table("retests")
    op.drop_index("ix_audit_events_event_type", table_name="audit_events")
    op.drop_index("ix_audit_events_entity_type", table_name="audit_events")
    op.drop_index("ix_audit_events_entity_id", table_name="audit_events")
    op.drop_index("ix_audit_events_created_at", table_name="audit_events")
    op.drop_table("audit_events")
    op.drop_index("ix_evidence_system_id", table_name="evidence")
    op.drop_index("ix_evidence_finding_id", table_name="evidence")
    op.drop_index("ix_evidence_evidence_type", table_name="evidence")
    op.drop_index("ix_evidence_assessment_id", table_name="evidence")
    op.drop_table("evidence")
    op.drop_index("ix_findings_system_id", table_name="findings")
    op.drop_index("ix_findings_status", table_name="findings")
    op.drop_index("ix_findings_severity", table_name="findings")
    op.drop_index("ix_findings_owner_id", table_name="findings")
    op.drop_index("ix_findings_domain", table_name="findings")
    op.drop_index("ix_findings_assessment_id", table_name="findings")
    op.drop_table("findings")
    op.drop_index("ix_assessments_system_id", table_name="assessments")
    op.drop_table("assessments")
    op.drop_index("ix_ai_systems_system_name", table_name="ai_systems")
    op.drop_table("ai_systems")
    op.drop_index("ix_owners_email", table_name="owners")
    op.drop_table("owners")
