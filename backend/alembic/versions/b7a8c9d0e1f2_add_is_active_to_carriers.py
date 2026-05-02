"""add is_active to carriers

Revision ID: b7a8c9d0e1f2
Revises: 4eb2ec0c8aa4
Create Date: 2026-04-30 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7a8c9d0e1f2'
down_revision = '4eb2ec0c8aa4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'carriers',
        sa.Column(
            'is_active',
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )
    op.alter_column(
        'carriers',
        'is_active',
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column('carriers', 'is_active')
