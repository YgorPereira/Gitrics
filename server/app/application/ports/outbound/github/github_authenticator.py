from typing import Protocol


class GithubAuthenticatorPort(Protocol):
    _url: str

    def authenticate(self, code: str) ->