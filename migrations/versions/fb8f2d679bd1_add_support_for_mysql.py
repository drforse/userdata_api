"""add support for mysql

Revision ID: fb8f2d679bd1
Revises: 
Create Date: 2021-11-03 16:08:46.817493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb8f2d679bd1'
down_revision = '6313e1cb41c9'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user") as batch_op:
        batch_op.alter_column("first_name", type_=sa.String(255), nullable=False)
        batch_op.alter_column("last_name", type_=sa.String(255))
        batch_op.alter_column("email_address", type_=sa.String(256), unique=True)
        batch_op.alter_column("photo_path", type_=sa.String(50), unique=True)
    with op.batch_alter_table("user_pass") as batch_op:
        batch_op.alter_column("number", type_=sa.String(9), nullable=False)
        batch_op.alter_column("country", type_=sa.String(100), nullable=False)


def downgrade():
    with op.batch_alter_table("user") as batch_op:
        batch_op.alter_column("first_name", type_=sa.String())
        batch_op.alter_column("last_name", type_=sa.String())
        batch_op.alter_column("email_address", type_=sa.String())
        batch_op.alter_column("photo_path", type_=sa.String())
    with op.batch_alter_table("user_pass") as batch_op:
        batch_op.alter_column("number", type_=sa.String())
        batch_op.alter_column("country", type_=sa.String())
