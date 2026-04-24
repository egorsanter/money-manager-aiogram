from datetime import datetime
from decimal import Decimal

from sqlalchemy import func, String, Integer, DateTime, ForeignKey, Numeric#, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.config import DATABASE_URL


engine = create_async_engine(url=DATABASE_URL)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    categories: Mapped[list['Category']] = relationship('Category', back_populates='user')


class Category(Base):
    __tablename__ = 'categories'

    # __table_args__ = (
    #     UniqueConstraint('user_id', 'name', name='uq_user_category_name'),
    # )

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    type: Mapped[str] = mapped_column(String(15))
    name: Mapped[str] = mapped_column(String(30))

    user: Mapped['User'] = relationship('User', back_populates='categories')


class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.category_id'))
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())