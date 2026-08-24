from uuid import UUID
from typing import Optional
from datetime import datetime


class UserEntity:
    def __init__(
        self,
        username: str,
        id: Optional[UUID] = None,
        avatar_url: Optional[str] = None,
        github_id: Optional[str] = None,
        access_token: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.username = username
        self.avatar_url = avatar_url
        self.github_id = github_id
        self.access_token = access_token
        self.created_at = created_at
