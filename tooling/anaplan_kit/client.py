"""The :class:`AnaplanClient` — the entry point for talking to the API.

The client owns an :class:`~anaplan_kit.auth.Authenticator` and a
:class:`requests.Session`, and exposes a single :meth:`AnaplanClient._request`
method that every higher-level call goes through. That method:

* attaches a fresh auth token (``Authorization: AnaplanAuthToken <token>``),
* retries a small number of times on *transient network* errors,
* raises :class:`~anaplan_kit.errors.AnaplanAPIError` on HTTP error statuses,
* parses JSON responses.

Higher-level capabilities (listing metadata, imports/exports, processes) are
provided as mixins so they all share this one request path.
"""

from __future__ import annotations

import time
from typing import Any

import requests

from .actions import ActionsMixin
from .auth import Authenticator
from .errors import AnaplanAPIError
from .imports_exports import ImportsExportsMixin
from .metadata import MetadataMixin

DEFAULT_API_BASE = "https://api.anaplan.com/2/0"


class AnaplanClient(MetadataMixin, ImportsExportsMixin, ActionsMixin):
    """A thin, typed client for the Anaplan REST API v2.

    Args:
        authenticator: An :class:`Authenticator` configured with credentials.
        api_base: Base URL for the API (no trailing slash).
        session: Optional pre-configured :class:`requests.Session`. If omitted,
            the authenticator's session is reused.
        timeout: Per-request timeout in seconds.
        max_retries: Number of retry attempts for transient network errors.
        backoff: Base seconds for exponential backoff between retries.
    """

    def __init__(
        self,
        authenticator: Authenticator,
        api_base: str = DEFAULT_API_BASE,
        session: requests.Session | None = None,
        timeout: float = 60.0,
        max_retries: int = 3,
        backoff: float = 0.5,
    ) -> None:
        self.auth = authenticator
        self.api_base = api_base.rstrip("/")
        self.session = session or authenticator._session
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff = backoff

    @classmethod
    def from_credentials(
        cls,
        email: str,
        password: str,
        api_base: str = DEFAULT_API_BASE,
        auth_url: str | None = None,
        **kwargs: Any,
    ) -> AnaplanClient:
        """Construct a client directly from an email/password pair.

        A convenience wrapper that builds the :class:`Authenticator` for you.
        """
        auth_kwargs = {} if auth_url is None else {"auth_url": auth_url}
        authenticator = Authenticator(email=email, password=password, **auth_kwargs)
        return cls(authenticator, api_base=api_base, **kwargs)

    # -- core request path --------------------------------------------------

    def _url(self, path: str) -> str:
        """Join a path fragment onto the API base."""
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self.api_base}/{path.lstrip('/')}"

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
        data: bytes | None = None,
        headers: dict[str, str] | None = None,
        expect_json: bool = True,
    ) -> Any:
        """Make an authenticated request and return parsed JSON (or raw bytes).

        Args:
            method: HTTP method, e.g. ``"GET"``.
            path: Path fragment relative to ``api_base`` (or a full URL).
            params: Query-string parameters.
            json: A JSON-serialisable body.
            data: A raw bytes body (used for chunk uploads).
            headers: Extra headers to merge on top of the auth header.
            expect_json: If ``True`` parse and return JSON; otherwise return
                the raw :class:`bytes` body (used for chunk downloads).

        Returns:
            Parsed JSON (``dict``/``list``) when ``expect_json`` is true, else
            the response body as ``bytes``.

        Raises:
            AnaplanAPIError: On HTTP error status or unparseable JSON.
        """
        url = self._url(path)
        request_headers: dict[str, str] = {"Accept": "application/json"}
        request_headers.update(self.auth.auth_header())
        if headers:
            request_headers.update(headers)

        response = self._send_with_retry(
            method=method,
            url=url,
            params=params,
            json=json,
            data=data,
            headers=request_headers,
        )

        if not (200 <= response.status_code < 300):
            self._raise_for_status(response)

        if not expect_json:
            return response.content

        if not response.content:
            return {}
        try:
            return response.json()
        except ValueError as exc:
            raise AnaplanAPIError(
                "Expected JSON response but could not parse it.",
                status_code=response.status_code,
            ) from exc

    def _send_with_retry(
        self,
        *,
        method: str,
        url: str,
        params: dict[str, Any] | None,
        json: Any | None,
        data: bytes | None,
        headers: dict[str, str],
    ) -> requests.Response:
        """Send the request, retrying on transient network-level errors.

        Only :class:`requests.ConnectionError` and :class:`requests.Timeout`
        are retried (with exponential backoff). HTTP error *statuses* are not
        retried here — they're surfaced to :meth:`_request`.
        """
        last_exc: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                return self.session.request(
                    method,
                    url,
                    params=params,
                    json=json,
                    data=data,
                    headers=headers,
                    timeout=self.timeout,
                )
            except (requests.ConnectionError, requests.Timeout) as exc:
                last_exc = exc
                if attempt < self.max_retries - 1:
                    time.sleep(self.backoff * (2**attempt))
        raise AnaplanAPIError(f"Network error after {self.max_retries} attempts: {last_exc}")

    @staticmethod
    def _raise_for_status(response: requests.Response) -> None:
        """Translate an HTTP error response into an :class:`AnaplanAPIError`."""
        payload: Any
        try:
            payload = response.json()
        except ValueError:
            payload = response.text[:500]
        raise AnaplanAPIError(
            f"Anaplan API returned HTTP {response.status_code}: {payload!r}",
            status_code=response.status_code,
            payload=payload,
        )
