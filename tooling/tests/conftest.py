"""Shared pytest fixtures.

All tests run fully offline: HTTP is mocked with the ``responses`` library, so
no Anaplan tenant or network access is needed.
"""

from __future__ import annotations

import time

import pytest

from anaplan_kit import AnaplanClient, Authenticator
from anaplan_kit.auth import AuthToken

# Fake base URLs used throughout the tests. They are never actually reached;
# ``responses`` intercepts the calls.
AUTH_URL = "https://auth.test.local/token/authenticate"
API_BASE = "https://api.test.local/2/0"

WORKSPACE_ID = "ws123"
MODEL_ID = "m456"


@pytest.fixture
def authenticator() -> Authenticator:
    """An authenticator pre-loaded with a non-expiring fake token.

    Because the token is already cached and valid, the client will not hit the
    auth endpoint unless a test forces a refresh.
    """
    auth = Authenticator(
        email="tester@example.com",
        password="secret",  # noqa: S106 - dummy value for offline tests
        auth_url=AUTH_URL,
    )
    auth._token = AuthToken(value="FAKE-TOKEN", expires_at=time.time() + 3600)
    return auth


@pytest.fixture
def client(authenticator: Authenticator) -> AnaplanClient:
    """A client pointed at the fake API base, with no inter-retry sleeping."""
    return AnaplanClient(
        authenticator,
        api_base=API_BASE,
        # Keep tests fast: tiny backoff and no real poll delays.
        backoff=0.0,
    )
