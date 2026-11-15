from urllib.parse import urlencode

import httpx

from server.app.domain.exceptions import AuthenticateException


class GithubOAuthAuthenticator:
    _AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
    _TOKEN_URL = "https://github.com/login/oauth/access_token"

    def __init__(
        self,
        http: httpx.AsyncClient,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scopes: list[str],
    ):
        self._http = http
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._scopes = scopes

    def build_authorization_url(self, state: str) -> str:
        # scopes = ["read:user", "read:project"]

        params = {
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "scope": " ".join(self._scopes),
            "state": state,
        }

        authorization_url = f"{self._AUTHORIZE_URL}?{urlencode(params)}"

        return authorization_url

    async def authenticate(self, code: str) -> str:
        """
        Handle the callback from GitHub's OAuth.

        This method is called when GitHub redirects the user back to the application
        after they have granted or denied access. It validates the state parameter
        and exchanges the authorization code for an access token.

        Args:
            code (str): The authorization code received from GitHub.
            states (SessionStates): object with state and state from cookie
        """
        # if not self._validate_state(state, state_to_validate):
        #     raise AuthenticateException("Invalid state.")

        return await self._exchange_code_for_token(code)

    # def _validate_state(self, state: str, state_from_cookie: str | None) -> bool:
    #     """
    #     Validate the state parameter received from GitHub's OAuth callback.

    #     This method should compare the received state with the one generated
    #     during the initial authorization request to protect against CSRF attacks.

    #     Args:
    #         state (str): The state parameter received from GitHub.

    #     Returns:
    #         bool: True if the state is valid, False otherwise.
    #     """
    #     return state_from_cookie is not None and state_from_cookie == state

    async def _exchange_code_for_token(self, code: str) -> str:
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
        try:
            response = await self._http.post(
                self._TOKEN_URL,
                headers={
                    "Accept": "application/json",
                },
                data={
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                    "code": code,
                    "redirect_uri": self._redirect_uri,
                },
            )

            response.raise_for_status()

            data = response.json()
        except (httpx.HTTPError, ValueError) as e:
            raise AuthenticateException("Error to exchange code for token.") from e

        access_token = data.get("access_token")

        if not access_token:
            raise AuthenticateException("Github error to return access token.")

        return access_token
