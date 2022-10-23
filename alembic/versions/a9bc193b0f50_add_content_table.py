"""add content table

Revision ID: a9bc193b0f50
Revises: 198f1f949f36
Create Date: 2022-10-22 17:38:32.949602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9bc193b0f50'
down_revision = '198f1f949f36'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
