from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.database.database_manager import engine as ENGINE

from sqlalchemy import *



class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    phone_number: Mapped[str] = mapped_column(String(16))
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime())


async def create_db():
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)