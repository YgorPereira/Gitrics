from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class GithubUser:
    id: UUID
    username: str
    github_id: str
    created_at: datetime
    updated_at: datetime
    access_token: str