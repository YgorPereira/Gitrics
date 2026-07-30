from secrets import token_urlsafe
from urllib.parse import urlencode

from app.core import settings


class AuthService:
    def build_authorization_url(self) -> str:
        """
        Build the GitHub OAuth authorization URL.

        Generates a unique state parameter to protect against CSRF attacks
        and constructs the authorization URL with the configured client ID,
        redirect URI, and requested OAuth scopes.

        Returns:
            str: The complete GitHub OAuth authorization URL.
        """
        state = token_urlsafe(32)

        scopes = ["read:user", "read:project"]

        params = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "redirect_uri": settings.GITHUB_REDIRECT_URI,
            "scope": " ".join(scopes),
            "state": state,
        }

        base_url = "https://github.com/login/oauth/authorize"

        return f"{base_url}?{urlencode(params)}"
