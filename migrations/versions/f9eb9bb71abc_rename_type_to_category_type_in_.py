"""rename type to category_type in categories

Revision ID: f9eb9bb71abc
Revises: 8a05cb9bd4ab
Create Date: 2026-04-29 16:08:59.073009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f9eb9bb71abc'
down_revision: Union[str, Sequence[str], None] = '8a05cb9bd4ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'categories',
        'type',
        new_column_name='category_type',
    )

    op.add_column(
        'categories',
        sa.Column('description', sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column('categories', 'description')

    op.alter_column(
        'categories',
        'category_type',
        new_column_name='type',
    )
