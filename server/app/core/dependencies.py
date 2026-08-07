from typing import AsyncGenerator
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionFactory


# Postgresql Database dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as db:
        try:
            yield db
        except Exception:
            logger.exception("Error on database session - running rollback")
            await db.rollback()
            raise
