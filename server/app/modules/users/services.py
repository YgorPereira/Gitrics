from uuid import UUID

from fastapi import Depends

from app.modules.users.repository import UserRepository
from app.entities.user_entity import UserEntity
from app.modules.users.exceptions import UserNotFoundException


class UserServices:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self.repository = repository

    async def create_user(self, user: UserEntity) -> UserEntity:
        return await self.repository.create_user(user=user)

    async def get_user_by_id(self, user_id: UUID) -> UserEntity:
        user = await self.repository.get_user_by_id(user_id=user_id)

        if user is None:
            raise UserNotFoundException()

        return user

    async def get_user_by_github_id(self, github_id: str) -> UserEntity:
        user = await self.repository.get_user_by_github_id(github_id=github_id)

        if user is None:
            raise UserNotFoundException()

        return user

    async def update_user(self, user: UserEntity) -> UserEntity:
        updated_user = await self.repository.update_user(user=user)

        if updated_user is None:
            raise UserNotFoundException()

        return updated_user
