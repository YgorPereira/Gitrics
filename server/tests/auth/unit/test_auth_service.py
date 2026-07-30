import random
from urllib.parse import parse_qs, urlparse

import pytest

from app.modules.auth.service import AuthService
from app.core import settings


@pytest.fixture
def auth_service():
    return AuthService()


@pytest.mark.unit()
def test_build_authorization_url_should_return_right_ur(
    auth_service: AuthService, monkeypatch
):
    monkeypatch.setattr(
        settings,
        "GITHUB_CLIENT_ID",
        "client_id_test",
    )

    monkeypatch.setattr(
        settings,
        "GITHUB_REDIRECT_URI",
        "http://localhost:8000/auth/github/callback",
    )

    url = auth_service.build_authorization_url()

    parsed = urlparse(url)

    assert parsed.scheme == "https"
    assert parsed.netloc == "github.com"
    assert parsed.path == "/login/oauth/authorize"

    query = parse_qs(parsed.query)

    print(url)

    assert query["client_id"] == ["client_id_test"]
    assert query["redirect_uri"] == ["http://localhost:8000/auth/github/callback"]
    assert query["scope"] == ["read:user read:project"]

    assert "state" in query
    assert len(query["state"][0]) > 0
