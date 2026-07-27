from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from loguru import logger

from app.core import settings

engine = create_async_engine(
    url=settings.database_url,
    echo= settings.DEBUG,
)

SessionFactory = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as db:
        try:
            yield db
        except Exception:
            logger.exception("Error on database session - running rollback")
            await db.rollback()
            raise