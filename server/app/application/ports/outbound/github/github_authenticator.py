from typing import Optional, Protocol

from server.app.application.ports.dtos import SessionStates


class GithubAuthenticatorPort(Protocol):
    def build_authorization_url(self, state: str) -> str: ...

    async def authenticate(self, code: str) -> str: ...
