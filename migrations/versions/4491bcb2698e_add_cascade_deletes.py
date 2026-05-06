"""name foreign keys and add user cascades

Revision ID: 4491bcb2698e
Revises: 01176d77e759
Create Date: 2026-04-29 17:09:15.181002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4491bcb2698e'
down_revision: Union[str, Sequence[str], None] = '01176d77e759'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op


def upgrade() -> None:
    op.drop_constraint(
        'categories_user_id_fkey',
        'categories',
        type_='foreignkey',
    )
    op.create_foreign_key(
        'fk_categories_user_id',
        'categories',
        'users',
        ['user_id'],
        ['user_id'],
        ondelete='CASCADE',
    )

    op.drop_constraint(
        'transactions_user_id_fkey',
        'transactions',
        type_='foreignkey',
    )
    op.create_foreign_key(
        'fk_transactions_user_id',
        'transactions',
        'users',
        ['user_id'],
        ['user_id'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    op.drop_constraint(
        'fk_transactions_category_id',
        'transactions',
        type_='foreignkey'
    )
    op.create_foreign_key(
        'transactions_category_id_fkey',
        'transactions',
        'categories',
        ['category_id'],
        ['category_id'],
    )

    op.drop_constraint(
        'fk_transactions_account_id',
        'transactions',
        type_='foreignkey'
    )
    op.create_foreign_key(
        'transactions_account_id_fkey',
        'transactions',
        'accounts',
        ['account_id'],
        ['account_id'],
    )

    op.drop_constraint(
        'fk_transactions_user_id',
        'transactions',
        type_='foreignkey'
    )
    op.create_foreign_key(
        'transactions_user_id_fkey',
        'transactions',
        'users',
        ['user_id'],
        ['user_id'],
    )

    op.drop_constraint(
        'fk_categories_user_id',
        'categories',
        type_='foreignkey'
    )
    op.create_foreign_key(
        'categories_user_id_fkey',
        'categories',
        'users',
        ['user_id'],
        ['user_id'],
    )