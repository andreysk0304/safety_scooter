from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.utils.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, pool_size=200)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)