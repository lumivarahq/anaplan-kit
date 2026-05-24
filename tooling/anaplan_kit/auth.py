"""Authentication against the Anaplan Auth service.

Anaplan's REST API v2 is protected by a short-lived auth token (the
``AnaplanAuthToken`` scheme — *not* ``Bearer``). You obtain the token by
POSTing your credentials (HTTP Basic auth) to the auth service, then send it
on every subsequent API call as::

    Authorization: AnaplanAuthToken <token>

The token expires (typically ~30 minutes), so it must be refreshed before
expiry for long-running jobs. :class:`Authenticator` handles acquiring,
caching and transparently refreshing the token.

.. warning::
   Running this against a live tenant requires a real Anaplan account and
   credentials. Credentials must come from the environment, never hard-coded.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional

import requests

from .errors import AnaplanAuthError

DEFAULT_AUTH_URL = "https://auth.anaplan.com/token/authenticate"

# Refresh the token this many seconds before its stated expiry, to avoid
# racing the server clock on long operations.
_EXPIRY_SKEW_SECONDS = 60


@dataclass
class AuthToken:
    """An auth token returned by the Anaplan auth service.

    Sent as ``Authorization: AnaplanAuthToken <token>`` (the Anaplan scheme,
    not ``Bearer``).

    Attributes:
        value: The opaque token string.
        expires_at: Unix epoch seconds at which the token expires.
    """

    value: str
    expires_at: float

    def is_expired(self, skew: float = _EXPIRY_SKEW_SECONDS) -> bool:
        """Return ``True`` if the token has expired (or is about to).

        Args:
            skew: Treat the token as expired this many seconds early.
        """
        return time.time() >= (self.expires_at - skew)

    @property
    def header_value(self) -> str:
        """The value for the ``Authorization`` header."""
        return f"AnaplanAuthToken {self.value}"


class Authenticator:
    """Acquires and refreshes an Anaplan :class:`AuthToken`.

    Args:
        email: Anaplan account email (username for basic auth).
        password: Anaplan account password.
        auth_url: The auth service endpoint. Defaults to the public service.
        session: Optional pre-configured :class:`requests.Session`.
        timeout: Per-request timeout in seconds.
    """

    def __init__(
        self,
        email: str,
        password: str,
        auth_url: str = DEFAULT_AUTH_URL,
        session: Optional[requests.Session] = None,
        timeout: float = 30.0,
    ) -> None:
        if not email or not password:
            raise AnaplanAuthError(
                "Anaplan email and password are required (set them via "
                "environment variables, never hard-code them)."
            )
        self.email = email
        self._password = password
        self.auth_url = auth_url
        self._session = session or requests.Session()
        self.timeout = timeout
        self._token: Optional[AuthToken] = None

    def get_token(self, force_refresh: bool = False) -> AuthToken:
        """Return a valid token, acquiring or refreshing it as needed.

        Args:
            force_refresh: Acquire a brand-new token even if a cached one is
                still valid.
        """
        if force_refresh or self._token is None or self._token.is_expired():
            self._token = self._authenticate()
        return self._token

    def auth_header(self) -> dict[str, str]:
        """Return the ``Authorization`` header dict for an API request."""
        return {"Authorization": self.get_token().header_value}

    def _authenticate(self) -> AuthToken:
        """Perform basic-auth login and parse the token response."""
        try:
            response = self._session.post(
                self.auth_url,
                auth=(self.email, self._password),
                timeout=self.timeout,
            )
        except requests.RequestException as exc:  # network-level failure
            raise AnaplanAuthError(f"Auth request failed: {exc}") from exc

        if response.status_code != 200:
            raise AnaplanAuthError(
                f"Authentication failed with HTTP {response.status_code}: "
                f"{response.text[:500]}"
            )

        try:
            body = response.json()
        except ValueError as exc:
            raise AnaplanAuthError("Auth response was not valid JSON.") from exc

        return self._parse_token(body)

    @staticmethod
    def _parse_token(body: dict) -> AuthToken:
        """Extract token value and expiry from an auth response body.

        Anaplan returns a structure like::

            {"tokenInfo": {"tokenValue": "...", "expiresAt": 1700000000000}}

        ``expiresAt`` is in epoch *milliseconds*.
        """
        token_info = body.get("tokenInfo") or {}
        value = token_info.get("tokenValue")
        expires_at_ms = token_info.get("expiresAt")
        if not value:
            raise AnaplanAuthError(
                f"Auth response missing token value: {body!r}"
            )

        if isinstance(expires_at_ms, (int, float)):
            expires_at = float(expires_at_ms) / 1000.0
        else:
            # Fall back to a conservative 30-minute lifetime.
            expires_at = time.time() + 30 * 60

        return AuthToken(value=value, expires_at=expires_at)
