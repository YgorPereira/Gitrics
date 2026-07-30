from fastapi.responses import RedirectResponse
from loguru import logger

from app.modules.auth.service import AuthService
from app.core import settings


class AuthController:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    async def github_login(self) -> RedirectResponse:
        """
        Redirect the user to GitHub's OAuth authorization page.

        Builds the GitHub authorization URL and returns an HTTP redirect
        response so the user can grant access to the application.

        Returns:
            RedirectResponse: Redirect response to GitHub's OAuth
            authorization endpoint.
        """

        authorization_url = self.auth_service.build_authorization_url()
        return RedirectResponse(url=authorization_url)

    async def github_callback(self, code: str, state: str):
        logger.debug(f"Code: {code}")
        logger.debug(f"State: {state}")
        pass
