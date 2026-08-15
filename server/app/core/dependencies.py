from typing import AsyncGenerator
from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionFactory
from app.modules.users.repository import UserRepository
from app.modules.users.service import UserService
from app.modules.auth.service import AuthService
from app.modules.auth.controller import AuthController


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
def get_user_repository(db_session=Depends(get_db)):
    return UserRepository(db_session)


def get_user_service(repository=Depends(get_user_repository)):
    return UserService(repository)


# Auth depencies
def get_auth_service(user_service=Depends(get_user_service)):
    return AuthService(user_service)


def get_auth_controller(auth_service=Depends(get_auth_service)):
    return AuthController(auth_service=auth_service)
