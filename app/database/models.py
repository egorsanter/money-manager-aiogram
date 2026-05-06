from datetime import datetime
from decimal import Decimal
from typing import Literal

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


CategoryType = Literal['income', 'expense']


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        index=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    categories: Mapped[list['Category']] = relationship(
        'Category',
        back_populates='user',
        cascade='all, delete-orphan',
    )

    accounts: Mapped[list['Account']] = relationship(
        'Account',
        back_populates='user',
        cascade='all, delete-orphan',
    )


class Account(Base):
    __tablename__ = 'accounts'

    __table_args__ = (
        UniqueConstraint(
            'user_id',
            'name',
            name='uq_accounts_user_name',
        ),
    )

    account_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            'users.user_id',
            ondelete='CASCADE',
            name='fk_accounts_user_id',
        ),
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    balance: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=Decimal('0.00'),
        nullable=False,
    )
    currency: Mapped[str] = mapped_column(
        String(3),
        default='RUB',
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped['User'] = relationship(
        'User',
        back_populates='accounts',
    )


class Category(Base):
    __tablename__ = 'categories'

    __table_args__ = (
        UniqueConstraint(
            'user_id',
            'name',
            'category_type',
            name='uq_categories_user_name_type',
        ),
        CheckConstraint(
            "category_type IN ('income', 'expense')",
            name='ck_categories_category_type',
        ),
    )

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            'users.user_id',
            ondelete='CASCADE',
            name='fk_categories_user_id',
        ),
        index=True,
        nullable=False,
    )
    category_type: Mapped[CategoryType] = mapped_column(
        String(15),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    user: Mapped['User'] = relationship(
        'User',
        back_populates='categories',
    )


class Transaction(Base): 
    __tablename__ = 'transactions'

    transaction_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            'users.user_id',
            ondelete='CASCADE',
            name='fk_transactions_user_id',
        ),
        index=True,
        nullable=False,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey(
            'accounts.account_id',
            name='fk_transactions_account_id',
        ),
        index=True,
        nullable=False,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            'categories.category_id',
            name='fk_transactions_category_id',
        ),
        index=True,
        nullable=False,
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )