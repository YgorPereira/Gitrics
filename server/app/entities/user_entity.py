class UserEntity:
    def __init__(
        self,
        id: int,
        username: str,
        avatar_url: str = None,
        github_id: str = None,
        access_token: str = None,
        created_at: str = None,
    ):
        self.id = id
        self.username = username
        self.avatar_url = avatar_url
        self.github_id = github_id
        self.access_token = access_token
        self.created_at = created_at
