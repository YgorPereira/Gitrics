from uuid import UUID

from app.modules.users.repository import UserRepository
from server.app.entities.user_entity import UserEntity


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user: UserEntity) -> UserEntity:
        return await self.repository.create_user(user=user)

    async def get_user_by_id(self, user_id: UUID) -> UserEntity:
        return await self.repository.get_user_by_id(user_id=user_id)

    async def get_user_by_github_id(self, github_id: str) -> UserEntity:
        return await self.repository.get_user_by_github_id(github_id=github_id)

    async def update_user(self, user: UserEntity) -> UserEntity:
        return await self.repository.update_user(user=user)

    async def delete_user(self, user_id: UUID) -> bool:
        return await self.repository.delete_user(user_id=user_id)
