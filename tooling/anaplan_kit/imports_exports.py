"""Chunked file transfer and the run-and-poll task lifecycle.

This module holds the **single** implementation of the asynchronous task
lifecycle used by imports, exports, generic actions and processes:

* :meth:`ImportsExportsMixin.run_action_and_wait` starts a task and then
* :meth:`ImportsExportsMixin.poll_task` polls it until it reaches
  ``COMPLETE`` (or fails).

It also implements chunked upload (:meth:`upload_file`) and chunked download
(:meth:`download_export`), matching how Anaplan transfers files.

These methods are mixed into :class:`~anaplan_kit.client.AnaplanClient`.
"""

from __future__ import annotations

import os
import time
from typing import Any, Optional, Protocol

from .errors import AnaplanTaskError

# Default chunk size for uploads (~10 MB). Anaplan recommends chunks in the
# 1-50 MB range; 10 MB is a safe, well-supported default.
DEFAULT_CHUNK_SIZE = 10 * 1024 * 1024

# How often to poll a running task, and how long to wait before giving up.
DEFAULT_POLL_INTERVAL = 2.0
DEFAULT_POLL_TIMEOUT = 600.0


class _SupportsRequest(Protocol):
    """Structural type for the client methods this mixin depends on."""

    def _request(self, method: str, path: str, **kwargs: Any) -> Any: ...


class ImportsExportsMixin:
    """File transfer + task lifecycle methods for the client."""

    # -- chunked upload -----------------------------------------------------

    def upload_file(
        self: _SupportsRequest,
        workspace_id: str,
        model_id: str,
        file_id: str,
        file_path: str,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> int:
        """Upload a local file to a model file resource, in chunks.

        The flow is: declare the chunk count, PUT each chunk in order, then
        mark the upload complete. The ``file_id`` is the source file an import
        action expects — uploading replaces its content.

        Args:
            workspace_id: Workspace ID.
            model_id: Model ID.
            file_id: Target file resource ID.
            file_path: Path to the local file to upload.
            chunk_size: Bytes per chunk.

        Returns:
            The number of chunks uploaded.
        """
        file_size = os.path.getsize(file_path)
        chunk_count = max(1, -(-file_size // chunk_size))  # ceil division
        base = (
            f"/workspaces/{workspace_id}/models/{model_id}/files/{file_id}"
        )

        # 1. Declare how many chunks are coming.
        self._request("POST", base, json={"chunkCount": chunk_count})

        # 2. PUT each chunk in order.
        with open(file_path, "rb") as handle:
            for chunk_id in range(chunk_count):
                data = handle.read(chunk_size)
                self._request(
                    "PUT",
                    f"{base}/chunks/{chunk_id}",
                    data=data,
                    headers={"Content-Type": "application/octet-stream"},
                    expect_json=False,
                )

        # 3. Mark the upload complete.
        self._request("POST", f"{base}/complete", json={"chunkCount": chunk_count})
        return chunk_count

    # -- task lifecycle (single source of truth) ----------------------------

    def run_action_and_wait(
        self,
        workspace_id: str,
        model_id: str,
        resource: str,
        resource_id: str,
        *,
        body: Optional[dict[str, Any]] = None,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
        timeout: float = DEFAULT_POLL_TIMEOUT,
    ) -> dict[str, Any]:
        """Start a task for any action type and poll it to completion.

        This is the generic primitive that :meth:`run_import`,
        :meth:`run_export` and :meth:`~anaplan_kit.actions.ActionsMixin.run_process`
        build on.

        Args:
            workspace_id: Workspace ID.
            model_id: Model ID.
            resource: Resource collection name: ``"imports"``, ``"exports"``,
                ``"actions"`` or ``"processes"``.
            resource_id: The ID of the import/export/action/process to run.
            body: Optional task body (defaults to ``{"localeName": "en_US"}``).
            poll_interval: Seconds between status polls.
            timeout: Maximum seconds to wait for completion.

        Returns:
            The completed task status payload (includes ``result``).

        Raises:
            AnaplanTaskError: If the task fails or times out.
        """
        task_id = self.start_task(
            workspace_id, model_id, resource, resource_id, body=body
        )
        return self.poll_task(
            workspace_id,
            model_id,
            resource,
            resource_id,
            task_id,
            poll_interval=poll_interval,
            timeout=timeout,
        )

    def start_task(
        self: _SupportsRequest,
        workspace_id: str,
        model_id: str,
        resource: str,
        resource_id: str,
        *,
        body: Optional[dict[str, Any]] = None,
    ) -> str:
        """Start an async task and return its ``taskId``."""
        path = (
            f"/workspaces/{workspace_id}/models/{model_id}/"
            f"{resource}/{resource_id}/tasks"
        )
        payload = body if body is not None else {"localeName": "en_US"}
        response = self._request("POST", path, json=payload)
        task = response.get("task", response)
        task_id = task.get("taskId")
        if not task_id:
            raise AnaplanTaskError(
                f"Task start response missing taskId: {response!r}"
            )
        return task_id

    def poll_task(
        self: _SupportsRequest,
        workspace_id: str,
        model_id: str,
        resource: str,
        resource_id: str,
        task_id: str,
        *,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
        timeout: float = DEFAULT_POLL_TIMEOUT,
    ) -> dict[str, Any]:
        """Poll a task until it reaches ``COMPLETE`` (or fails / times out).

        Args:
            task_id: The task to poll, from :meth:`start_task`.
            poll_interval: Seconds between polls.
            timeout: Maximum seconds to wait.

        Returns:
            The final task status payload.

        Raises:
            AnaplanTaskError: If the task reports failure or the timeout is hit.
        """
        path = (
            f"/workspaces/{workspace_id}/models/{model_id}/"
            f"{resource}/{resource_id}/tasks/{task_id}"
        )
        deadline = time.monotonic() + timeout
        while True:
            response = self._request("GET", path)
            status = response.get("task", response)
            state = status.get("taskState")

            if state == "COMPLETE":
                result = status.get("result", {})
                # ``successful: false`` means it completed but the work failed
                # (e.g. import rows rejected) — surface it as a task error.
                if result.get("successful") is False:
                    raise AnaplanTaskError(
                        f"Task {task_id} completed unsuccessfully: {result!r}",
                        task_id=task_id,
                        result=result,
                    )
                return status

            if time.monotonic() >= deadline:
                raise AnaplanTaskError(
                    f"Task {task_id} did not complete within {timeout}s "
                    f"(last state: {state}).",
                    task_id=task_id,
                    result=status.get("result"),
                )
            time.sleep(poll_interval)

    # -- typed convenience wrappers -----------------------------------------

    def run_import(
        self,
        workspace_id: str,
        model_id: str,
        import_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Run an import action and wait for it to complete."""
        return self.run_action_and_wait(
            workspace_id, model_id, "imports", import_id, **kwargs
        )

    def run_export(
        self,
        workspace_id: str,
        model_id: str,
        export_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Run an export action and wait for it to complete.

        Use :meth:`download_export` afterwards to fetch the produced file.
        """
        return self.run_action_and_wait(
            workspace_id, model_id, "exports", export_id, **kwargs
        )

    # -- chunked download ---------------------------------------------------

    def download_export(
        self: _SupportsRequest,
        workspace_id: str,
        model_id: str,
        file_id: str,
        dest_path: str,
    ) -> str:
        """Download a generated export file, reassembling its chunks.

        Reads the file's chunk metadata, then GETs each chunk and writes them
        to ``dest_path`` in order. Run the export action first (see
        :meth:`run_export`).

        Args:
            file_id: The export's file resource ID.
            dest_path: Local path to write the reassembled file to.

        Returns:
            ``dest_path``.
        """
        base = (
            f"/workspaces/{workspace_id}/models/{model_id}/files/{file_id}"
        )
        meta = self._request("GET", f"{base}/chunks")
        chunks = meta.get("chunks", [])

        with open(dest_path, "wb") as handle:
            for chunk in chunks:
                chunk_id = chunk["id"]
                data = self._request(
                    "GET", f"{base}/chunks/{chunk_id}", expect_json=False
                )
                handle.write(data)
        return dest_path
