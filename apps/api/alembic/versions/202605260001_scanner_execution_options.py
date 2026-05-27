"""scanner execution options

Revision ID: 202605260001
Revises: 202605220005
Create Date: 2026-05-26
"""

from alembic import op
import sqlalchemy as sa

revision = "202605260001"
down_revision = "202605220005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "scanner_runs",
        sa.Column("execution_options", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
    )
    op.alter_column("scanner_runs", "execution_options", server_default=None)


def downgrade() -> None:
    op.drop_column("scanner_runs", "execution_options")
