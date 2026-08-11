from typing import AsyncGenerator
from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionFactory
from app.modules.users.repository import UserRepository
from app.modules.users.services import UserService


# Postgresql Database dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as db:
        try:
            yield db
        except Exception:
            logger.exception("Error on database session - running rollback")
            await db.rollback()
            raise


# User dependencies
async def get_user_repository(db_session=Depends(get_db)):
    return UserRepository(db_session)


async def get_user_service(repository=Depends(get_user_repository)):
    return UserService(repository)
