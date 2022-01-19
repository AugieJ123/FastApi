"""create posts table

Revision ID: a38254900338
Revises: 
Create Date: 2022-01-19 05:36:40.491817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a38254900338'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), primary_key=True, nullable=False), 
                        sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    pass
