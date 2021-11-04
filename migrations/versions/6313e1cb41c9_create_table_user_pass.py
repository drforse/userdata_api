"""create table user_pass

Revision ID: 6313e1cb41c9
Revises: 7e6adfa8ee51
Create Date: 2021-11-03 23:35:30.576611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6313e1cb41c9'
down_revision = '7e6adfa8ee51'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_pass",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"), nullable=False),
        sa.Column("number", sa.String(9), nullable=False),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("issue_date", sa.Date, nullable=False),
        sa.Column("expiration_date", sa.Date, nullable=False)
    )


def downgrade():
    op.drop_table("user_pass")
