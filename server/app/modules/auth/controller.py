from fastapi import Request, Response
from fastapi.responses import RedirectResponse

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
        authorization_url, state = self.auth_service.build_authorization_url_and_state()

        redirect_response = RedirectResponse(url=authorization_url)

        redirect_response.set_cookie(
            key="oauth_state",
            value=state,
            httponly=True,
            max_age=600,
            samesite="lax",
        )

        return redirect_response

    async def github_callback(
        self, code: str, state: str, request: Request
    ) -> RedirectResponse:
        """
        Handle the callback from GitHub's OAuth.

        This method is called when GitHub redirects the user back to the application
        after they have granted or denied access.

        Args:
            code (str): The authorization code received from GitHub.
            state (str): The state parameter received from GitHub.
            o_auth_state (str): The OAuth state parameter.
        """
        state_from_cookie = request.cookies.get("oauth_state")
        jwt = await self.auth_service.callback(code, state, state_from_cookie)

        redirect_response = RedirectResponse(url=settings.CLIENT_REDIRECT_URL)

        redirect_response.set_cookie(
            key="access_jwt",
            value=jwt,
            httponly=True,
            samesite="lax",
            max_age=60 * 60 * 12,
        )

        redirect_response.delete_cookie("oauth_state")

        return redirect_response
