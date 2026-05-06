"""add accounts table

Revision ID: 9e2610fb047a
Revises: 4491bcb2698e
Create Date: 2026-04-29 17:48:47.166844

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9e2610fb047a'
down_revision: Union[str, Sequence[str], None] = '4491bcb2698e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'accounts',
        sa.Column('account_id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('balance', sa.Numeric(10, 2), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.user_id'],
            name='fk_accounts_user_id',
            ondelete='CASCADE',
        ),
        sa.UniqueConstraint(
            'user_id',
            'name',
            name='uq_accounts_user_name',
        ),
    )
    op.create_index('ix_accounts_user_id', 'accounts', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_accounts_user_id', table_name='accounts')
    op.drop_table('accounts')