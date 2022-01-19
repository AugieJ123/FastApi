"""add content column to posts table

Revision ID: 5bf7318f6401
Revises: a38254900338
Create Date: 2022-01-19 06:08:51.881040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bf7318f6401'
down_revision = 'a38254900338'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
