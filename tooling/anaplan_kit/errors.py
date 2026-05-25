"""Exception types raised by :mod:`anaplan_kit`.

All exceptions inherit from :class:`AnaplanError`, so callers can catch that
single base class to handle any failure originating from this package.
"""

from __future__ import annotations

from typing import Any


class AnaplanError(Exception):
    """Base class for every error raised by ``anaplan_kit``."""


class AnaplanAuthError(AnaplanError):
    """Raised when authentication or token refresh fails."""


class AnaplanAPIError(AnaplanError):
    """Raised when the Anaplan REST API returns a non-success HTTP status.

    Attributes:
        status_code: The HTTP status code returned by the API (if known).
        payload: The parsed JSON body of the error response (if any).
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        payload: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


class AnaplanTaskError(AnaplanError):
    """Raised when an asynchronous task (import/export/action/process) fails.

    Attributes:
        task_id: The ID of the task that failed.
        result: The ``result`` block returned by the task status endpoint.
    """

    def __init__(
        self,
        message: str,
        task_id: str | None = None,
        result: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.task_id = task_id
        self.result = result
