from datetime import timezone, datetime
from typing import cast
from unittest.mock import AsyncMock, MagicMock
from urllib.parse import parse_qs, urlparse


from fastapi import HTTPException
import httpx
import jwt
import pytest

from app.modules.auth.service import AuthService
from app.core import settings


@pytest.fixture
def auth_service(user_service):
    return AuthService(user_service)


class TestAuthService:
    @pytest.mark.unit()
    def test_build_authorization_url_and_state_should_return_right_url_and_state(
        self, auth_service: AuthService, monkeypatch
    ):
        # nomes corrigidos: o Settings real usa GH_CLIENT_ID / GH_REDIRECT_URI
        monkeypatch.setattr(settings, "GH_CLIENT_ID", "client_id_test")
        monkeypatch.setattr(
            settings, "GH_REDIRECT_URI", "http://localhost:8000/auth/github/callback"
        )

        url, state = auth_service.build_authorization_url_and_state()

        parsed = urlparse(url)

        assert parsed.scheme == "https"
        assert parsed.netloc == "github.com"
        assert parsed.path == "/login/oauth/authorize"

        query = parse_qs(parsed.query)

        assert query["client_id"] == ["client_id_test"]
        assert query["redirect_uri"] == ["http://localhost:8000/auth/github/callback"]
        assert query["scope"] == ["read:user read:project"]

        assert query["state"] == [state]
        assert len(state) > 0

    @pytest.mark.unit()
    def test_validate_state_should_return_true_for_valid_state(
        self, auth_service: AuthService
    ):
        assert auth_service._validate_state("matching_state", "matching_state") is True

    @pytest.mark.unit()
    def test_validate_state_should_return_false_for_invalid_state(
        self, auth_service: AuthService
    ):
        assert (
            auth_service._validate_state("state_from_github", "different_state")
            is False
        )

    @pytest.mark.unit()
    def test_validate_state_should_return_false_when_cookie_is_missing(
        self, auth_service: AuthService
    ):
        assert auth_service._validate_state("any_state", "") is False

    @pytest.mark.unit()
    async def test_exchange_code_for_token_should_return_access_token(
        self, auth_service: AuthService, monkeypatch
    ):
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "fake_access_token"}
        mock_response.raise_for_status = MagicMock()

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        monkeypatch.setattr(httpx, "AsyncClient", lambda *args, **kwargs: mock_client)

        code = "fake_code"
        access_token = await auth_service._exchange_code_for_token(code)

        assert access_token == "fake_access_token"

    @pytest.mark.unit()
    async def test_exchange_code_for_token_should_raise_http_exception_on_failure(
        self, auth_service: AuthService, monkeypatch
    ):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Error", request=MagicMock(), response=MagicMock()
        )

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        monkeypatch.setattr(httpx, "AsyncClient", lambda *args, **kwargs: mock_client)

        code = "fake_code"

        with pytest.raises(httpx.HTTPStatusError):
            await auth_service._exchange_code_for_token(code)

    @pytest.mark.unit()
    async def test_get_user_info_should_return_user_data(
        self, auth_service: AuthService, monkeypatch
    ):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": 12345,
            "login": "ygor",
            "name": "Ygor",
            "avatar_url": "https://avatars.githubusercontent.com/u/12345",
        }
        mock_response.raise_for_status = MagicMock()

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        monkeypatch.setattr(httpx, "AsyncClient", lambda *args, **kwargs: mock_client)

        access_token = "fake_access_token"
        user_info = await auth_service._get_user_info(access_token)

        assert user_info["login"] == "ygor"
        assert user_info["id"] == 12345

        mock_client.get.assert_called_once_with(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )

    @pytest.mark.unit()
    async def test_get_user_info_should_raise_http_status_error_on_failure(
        self, auth_service: AuthService, monkeypatch
    ):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Unauthorized", request=MagicMock(), response=MagicMock()
        )

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        monkeypatch.setattr(httpx, "AsyncClient", lambda *args, **kwargs: mock_client)

        access_token = "invalid_token"

        with pytest.raises(httpx.HTTPStatusError):
            await auth_service._get_user_info(access_token)

    @pytest.mark.unit()
    def test_create_access_token_should_return_valid_jwt(
        self, auth_service: AuthService
    ):
        user_id = 12345

        token = auth_service._create_access_jwt(user_id)

        assert isinstance(token, str)

        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        assert decoded["sub"] == str(user_id)

    @pytest.mark.unit()
    def test_create_access_token_should_set_expiration_in_the_future(
        self, auth_service: AuthService
    ):
        user_id = 12345

        token = auth_service._create_access_jwt(user_id)
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])

        exp_timestamp = decoded["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)

        assert exp_datetime > datetime.now(timezone.utc)

    @pytest.mark.unit()
    def test_create_access_token_should_raise_error_for_invalid_signature(
        self, auth_service: AuthService
    ):
        user_id = 12345
        token = auth_service._create_access_jwt(user_id)

        with pytest.raises(jwt.InvalidSignatureError):
            jwt.decode(token, "wrong_secret_key", algorithms=["HS256"])

    @pytest.mark.unit()
    async def test_callback_should_return_jwt_when_state_is_valid_and_flow_succeeds(
        self, auth_service: AuthService, monkeypatch
    ):
        monkeypatch.setattr(
            auth_service, "_validate_state", MagicMock(return_value=True)
        )
        monkeypatch.setattr(
            auth_service,
            "_exchange_code_for_token",
            AsyncMock(return_value="fake_github_token"),
        )
        monkeypatch.setattr(
            auth_service,
            "_get_user_info",
            AsyncMock(
                return_value={
                    "id": 12345,
                    "login": "ygor",
                    "avatar_url": "https://avatars.githubusercontent.com/u/12345",
                }
            ),
        )
        monkeypatch.setattr(
            auth_service,
            "_create_access_jwt",
            MagicMock(return_value="fake_jwt_token"),
        )

        result = await auth_service.callback(
            code="fake_code", state="fake_state", state_from_cookie="fake_state"
        )

        assert result == "fake_jwt_token"
        cast(MagicMock, auth_service._validate_state).assert_called_once_with(
            "fake_state", "fake_state"
        )
        cast(AsyncMock, auth_service._exchange_code_for_token).assert_called_once_with(
            "fake_code"
        )
        cast(AsyncMock, auth_service._get_user_info).assert_called_once_with(
            "fake_github_token"
        )
        cast(MagicMock, auth_service._create_access_jwt).assert_called_once_with(12345)

    @pytest.mark.unit()
    async def test_callback_should_raise_http_exception_when_state_is_invalid(
        self, auth_service: AuthService, monkeypatch
    ):
        monkeypatch.setattr(
            auth_service, "_validate_state", MagicMock(return_value=False)
        )
        exchange_mock = AsyncMock()
        monkeypatch.setattr(auth_service, "_exchange_code_for_token", exchange_mock)

        with pytest.raises(HTTPException) as exc_info:
            await auth_service.callback(
                code="fake_code",
                state="invalid_state",
                state_from_cookie="different_state",
            )

        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Invalid state parameter."

        exchange_mock.assert_not_called()

    @pytest.mark.unit()
    async def test_callback_should_raise_http_exception_when_user_id_is_missing(
        self, auth_service: AuthService, monkeypatch
    ):
        monkeypatch.setattr(
            auth_service, "_validate_state", MagicMock(return_value=True)
        )
        monkeypatch.setattr(
            auth_service,
            "_exchange_code_for_token",
            AsyncMock(return_value="fake_github_token"),
        )
        monkeypatch.setattr(
            auth_service, "_get_user_info", AsyncMock(return_value={"login": "ygor"})
        )
        create_token_mock = MagicMock()
        monkeypatch.setattr(auth_service, "_create_access_jwt", create_token_mock)

        with pytest.raises(HTTPException) as exc_info:
            await auth_service.callback(
                code="fake_code", state="fake_state", state_from_cookie="fake_state"
            )

        assert exc_info.value.status_code == 400
        assert (
            exc_info.value.detail == "Failed to retrieve user information from GitHub."
        )

        create_token_mock.assert_not_called()
