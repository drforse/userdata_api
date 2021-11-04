"""create table user

Revision ID: 7e6adfa8ee51
Revises: fb8f2d679bd1
Create Date: 2021-11-03 23:35:05.147563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e6adfa8ee51'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("first_name", sa.String(255), nullable=False),
        sa.Column("last_name", sa.String(255)),
        sa.Column("email_address", sa.String(256), unique=True),
        sa.Column("photo_path", sa.String(50), unique=True)
    )


def downgrade():
    op.drop_table("user")
