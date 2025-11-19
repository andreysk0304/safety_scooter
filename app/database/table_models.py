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


class AccessTokens(Base):
    __tablename__ = "access_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    access_token: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)


class Applications(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    key: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default='pending')
    gps_longitude: Mapped[str] = mapped_column(String(32))
    gps_width: Mapped[str] = mapped_column(String(32))
    record_time: Mapped[datetime] = mapped_column(DateTime())
    is_delete: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(DateTime())
    last_change: Mapped[datetime] = mapped_column(DateTime())


class Verdicts(Base):
    __tablename__ = "verdicts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(String(255))  # Тип нарушения
    scooter_type: Mapped[str] = mapped_column(String(64), nullable=True)  # Тип самоката (Yandex/Whoosh/Urent)
    object_id: Mapped[int] = mapped_column(nullable=True)  # ID объекта из YOLO tracking
    timestamp: Mapped[float] = mapped_column(nullable=True)  # Время в видео (секунды)
    coordinates: Mapped[str] = mapped_column(String(255), nullable=True)  # Координаты на кадре
    created_at: Mapped[datetime] = mapped_column(DateTime())

async def create_db():
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)