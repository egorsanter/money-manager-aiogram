"""change telegram_id to bigint

Revision ID: 01176d77e759
Revises: 8169cd538c56
Create Date: 2026-04-29 16:50:03.547083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01176d77e759'
down_revision: Union[str, Sequence[str], None] = '8169cd538c56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'users',
        'telegram_id',
        type_=sa.BigInteger(),
    )


def downgrade() -> None:
    op.alter_column(
        'users',
        'telegram_id',
        type_=sa.Integer(),
    )