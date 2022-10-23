"""Create post table

Revision ID: 198f1f949f36
Revises: 
Create Date: 2022-10-22 17:29:01.029864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '198f1f949f36'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable = False, primary_key=True),
                    sa.Column('title', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
