from datetime import timedelta, datetime, timezone
from secrets import token_urlsafe
from urllib.parse import urlencode

from fastapi import HTTPException, Request, Response
import httpx
import jwt

from app.core import settings


class AuthService:
    def build_authorization_url_and_state(self) -> tuple[str, str]:
        """
        Build the GitHub OAuth authorization URL and generate a state parameter.

        Generates a unique state parameter to protect against CSRF attacks
        and constructs the authorization URL with the configured client ID,
        redirect URI, and requested OAuth scopes.

        Returns:
            tuple[str, str]: A tuple containing the authorization URL and
            the generated state parameter.
        """
        state = token_urlsafe(32)

        scopes = ["read:user", "read:project"]

        params = {
            "client_id": settings.GH_CLIENT_ID,
            "redirect_uri": settings.GH_REDIRECT_URI,
            "scope": " ".join(scopes),
            "state": state,
        }

        base_url = "https://github.com/login/oauth/authorize"

        authorization_url = f"{base_url}?{urlencode(params)}"

        return authorization_url, state

    async def callback(
        self, code: str, state: str, state_from_cookie: str | None
    ) -> str:
        """
        Handle the callback from GitHub's OAuth.

        This method is called when GitHub redirects the user back to the application
        after they have granted or denied access. It validates the state parameter
        and exchanges the authorization code for an access token.

        Args:
            code (str): The authorization code received from GitHub.
            state (str): The state parameter received from GitHub.
            state_from_cookie (str): The state parameter from the cookie.
        """
        if not self.validate_state(state, state_from_cookie):
            raise HTTPException(status_code=400, detail="Invalid state parameter.")

        github_access_token = await self.exchange_code_for_token(code)

        user = await self.get_user_info(github_access_token)

        user_id = user.get("id")

        if not user_id:
            raise HTTPException(
                status_code=400,
                detail="Failed to retrieve user information from GitHub.",
            )

        access_token_jwt = self.create_access_jwt_token(user_id)

        return access_token_jwt

    async def exchange_code_for_token(self, code: str) -> str:
        """
        Exchange the authorization code for an access token.

        This method sends a POST request to GitHub's token endpoint with the
        provided authorization code, client ID, and client secret to obtain
        an access token.

        Args:
            code (str): The authorization code received from GitHub.

        Returns:
            str: The access token received from GitHub.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://github.com/login/oauth/access_token",
                headers={
                    "Accept": "application/json",
                },
                data={
                    "client_id": settings.GH_CLIENT_ID,
                    "client_secret": settings.GH_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": settings.GH_REDIRECT_URI,
                },
            )

        response.raise_for_status()

        data = response.json()

        access_token = data.get("access_token")

        if not access_token:
            raise HTTPException(
                status_code=400, detail="Failed to obtain access token from GitHub."
            )

        return access_token

    def validate_state(self, state: str, state_from_cookie: str | None) -> bool:
        """
        Validate the state parameter received from GitHub's OAuth callback.

        This method should compare the received state with the one generated
        during the initial authorization request to protect against CSRF attacks.

        Args:
            state (str): The state parameter received from GitHub.

        Returns:
            bool: True if the state is valid, False otherwise.
        """
        return state_from_cookie is not None and state_from_cookie == state

    def create_access_jwt_token(self, user_id: int) -> str:
        """
        Create an access token for the authenticated user.

        This method generates a secure access token that can be used for
        subsequent API requests to authenticate the user.

        Args:
            user_id (int): The unique identifier of the authenticated user.
        """
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(hours=12),
        }

        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

    async def get_user_info(self, access_token: str) -> dict:
        """
        Retrieve user information from GitHub using the access token.

        This method sends a GET request to GitHub's user API endpoint with
        the provided access token to obtain the authenticated user's information.

        Args:
            access_token (str): The access token received from GitHub.

        Returns:
            dict: A dictionary containing the user's information.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )

        response.raise_for_status()

        return response.json()
