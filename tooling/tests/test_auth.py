"""Tests for token acquisition, caching, refresh and header formatting."""

from __future__ import annotations

import time

import pytest
import responses

from anaplan_kit import Authenticator
from anaplan_kit.auth import AuthToken
from anaplan_kit.errors import AnaplanAuthError

from .conftest import AUTH_URL


def _token_body(value: str = "TOK", expires_in_ms: int = 30 * 60 * 1000) -> dict:
    return {
        "tokenInfo": {
            "tokenValue": value,
            "expiresAt": int((time.time() * 1000) + expires_in_ms),
        }
    }


@responses.activate
def test_get_token_acquires_and_caches() -> None:
    responses.add(responses.POST, AUTH_URL, json=_token_body("TOK1"), status=200)

    auth = Authenticator("a@b.com", "pw", auth_url=AUTH_URL)
    token = auth.get_token()

    assert token.value == "TOK1"
    # Second call should reuse the cached token (no second HTTP call).
    assert auth.get_token().value == "TOK1"
    assert len(responses.calls) == 1


@responses.activate
def test_force_refresh_reauthenticates() -> None:
    responses.add(responses.POST, AUTH_URL, json=_token_body("TOK1"), status=200)
    responses.add(responses.POST, AUTH_URL, json=_token_body("TOK2"), status=200)

    auth = Authenticator("a@b.com", "pw", auth_url=AUTH_URL)
    assert auth.get_token().value == "TOK1"
    assert auth.get_token(force_refresh=True).value == "TOK2"
    assert len(responses.calls) == 2


def test_header_value_format() -> None:
    token = AuthToken(value="ABC", expires_at=time.time() + 100)
    assert token.header_value == "AnaplanAuthToken ABC"


@responses.activate
def test_auth_header_uses_anaplan_scheme() -> None:
    responses.add(responses.POST, AUTH_URL, json=_token_body("XYZ"), status=200)
    auth = Authenticator("a@b.com", "pw", auth_url=AUTH_URL)
    assert auth.auth_header() == {"Authorization": "AnaplanAuthToken XYZ"}


def test_expired_token_detection() -> None:
    assert AuthToken("t", time.time() - 1).is_expired() is True
    assert AuthToken("t", time.time() + 3600).is_expired() is False


def test_missing_credentials_raise() -> None:
    with pytest.raises(AnaplanAuthError):
        Authenticator("", "pw")


@responses.activate
def test_auth_failure_raises() -> None:
    responses.add(responses.POST, AUTH_URL, json={"status": "fail"}, status=401)
    auth = Authenticator("a@b.com", "pw", auth_url=AUTH_URL)
    with pytest.raises(AnaplanAuthError):
        auth.get_token()
