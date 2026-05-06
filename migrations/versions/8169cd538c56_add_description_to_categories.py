"""add description to categories

Revision ID: 8169cd538c56
Revises: f9eb9bb71abc
Create Date: 2026-04-29 16:21:38.546290

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8169cd538c56'
down_revision: Union[str, Sequence[str], None] = 'f9eb9bb71abc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'categories',
        sa.Column('description', sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column('categories', 'description')