"""add published and created at to the post table

Revision ID: 1ca9c47542c5
Revises: 42ad3d4bd65f
Create Date: 2022-01-19 06:36:23.263734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ca9c47542c5'
down_revision = '42ad3d4bd65f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default=sa.text('True')),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
