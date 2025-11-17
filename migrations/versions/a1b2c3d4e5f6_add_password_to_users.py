"""add password column to users

Revision ID: a1b2c3d4e5f6
Revises: 7be28979d578
Create Date: 2025-11-17 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"
down_revision = "7be28979d578"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("password", sa.String(length=255), nullable=False, server_default="tmp"),
    )
    # Після додавання поля можна прибрати server_default
    op.alter_column("users", "password", server_default=None)


def downgrade():
    op.drop_column("users", "password")
