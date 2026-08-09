from uuid import UUID
from fastapi import Depends
from sqlalchemy import select

from app.entities import UserEntity
from app.modules.users.mapper import UserMapper

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.modules.users.models import UserModel


class UserRepository:
    def __init__(self, db_session=Depends(get_db)):
        self.db_session = db_session

    async def create_user(self, user: UserEntity) -> UserEntity:
        user_model = UserMapper.to_model(user)
        self.db_session.add(user_model)
        await self.db_session.commit()
        await self.db_session.refresh(user_model)
        return UserMapper.to_entity(user_model)

    async def get_user_by_id(self, user_id: UUID) -> UserEntity | None:
        result = await self.db_session.get(UserModel, user_id)

        if result is None:
            return None

        return UserMapper.to_entity(result)

    async def get_user_by_github_id(self, github_id: str) -> UserEntity | None:
        result = await self.db_session.execute(
            select(UserModel).where(UserModel.github_id == github_id)
        )
        user_model = result.scalar_one_or_none()

        if user_model is None:
            return None

        return UserMapper.to_entity(user_model)

    async def update_user(self, user: UserEntity) -> UserEntity | None:
        user_model = await self.db_session.get(UserModel, user.id)

        if user_model is None:
            return None

        updated_data = UserMapper.to_model(user)
        for column in UserModel.__table__.columns.keys():
            if column in ("id", "created_at"):
                continue
            setattr(user_model, column, getattr(updated_data, column))

        await self.db_session.commit()
        await self.db_session.refresh(user_model)

        return UserMapper.to_entity(user_model)

    async def delete_user(self, user_id: UUID) -> bool:
        user_model = await self.db_session.get(UserModel, user_id)

        if user_model is None:
            return False

        await self.db_session.delete(user_model)
        await self.db_session.commit()

        return True
