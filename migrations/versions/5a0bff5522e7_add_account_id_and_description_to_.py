"""add account_id and description to transactions

Revision ID: 5a0bff5522e7
Revises: 9e2610fb047a
Create Date: 2026-04-30 17:09:34.840645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5a0bff5522e7'
down_revision: Union[str, Sequence[str], None] = '9e2610fb047a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "transactions",
        sa.Column("account_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "transactions",
        sa.Column("description", sa.Text(), nullable=True)
    )

    op.create_index(
        op.f("ix_transactions_account_id"),
        "transactions",
        ["account_id"],
        unique=False
    )

    op.create_foreign_key(
        "fk_transactions_account_id",
        "transactions",
        "accounts",
        ["account_id"],
        ["account_id"]
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_transactions_account_id",
        "transactions",
        type_="foreignkey"
    )

    op.drop_index(
        op.f("ix_transactions_account_id"),
        table_name="transactions"
    )

    op.drop_column("transactions", "account_id")
    op.drop_column("transactions", "description")