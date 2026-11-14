from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from datetime import datetime

from app.domain.entities.github_user import GithubUser

@dataclass
class User:
    id: Optional[UUID] = None
    github_user: GithubUser = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

