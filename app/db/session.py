import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.models import Base

async_engine = create_async_engine(url=os.getenv("DATABASE_URL"), pool_size=5, max_overflow=5)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
