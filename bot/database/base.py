from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from bot.settings.config import PG_URL

engine = create_async_engine(PG_URL, echo=False)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession,
                             expire_on_commit=False)


async def __init__models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
