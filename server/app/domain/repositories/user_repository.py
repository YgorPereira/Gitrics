from typing import Protocol

from app.domain.entities.user import User


class UserRepository(Protocol):
    def create_user(self, user: User) -> User:
        ...

    def update_user(self, user: User) -> User:
            ...

    def find_user_by_github_id(self, github_id: str) -> User:
            ...