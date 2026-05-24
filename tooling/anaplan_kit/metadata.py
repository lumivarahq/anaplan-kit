"""Read-only metadata listings: workspaces, models and a model's resources.

A typical integration script discovers the IDs it needs by drilling down:
workspaces -> models -> files / imports / exports / actions / processes.

These methods are mixed into :class:`~anaplan_kit.client.AnaplanClient`, so
they rely on its ``_request`` helper. They are written as a mixin (rather than
a standalone class) purely to keep the public surface a single client object.
"""

from __future__ import annotations

from typing import Any, Protocol


class _SupportsRequest(Protocol):
    """Structural type for the client methods this mixin depends on."""

    def _request(self, method: str, path: str, **kwargs: Any) -> Any: ...


class MetadataMixin:
    """Workspace/model/resource listing methods for the client."""

    def list_workspaces(self: _SupportsRequest) -> list[dict[str, Any]]:
        """List workspaces the authenticated user can access."""
        body = self._request("GET", "/workspaces")
        return body.get("workspaces", [])

    def list_models(
        self: _SupportsRequest, workspace_id: str
    ) -> list[dict[str, Any]]:
        """List models within a workspace.

        Args:
            workspace_id: The workspace ID to list models for.
        """
        body = self._request("GET", f"/workspaces/{workspace_id}/models")
        return body.get("models", [])

    def _model_resources(
        self: _SupportsRequest,
        workspace_id: str,
        model_id: str,
        resource: str,
        key: str,
    ) -> list[dict[str, Any]]:
        """List a model's resources of a given type (files, imports, ...)."""
        path = f"/workspaces/{workspace_id}/models/{model_id}/{resource}"
        body = self._request("GET", path)
        return body.get(key, [])

    def list_files(
        self, workspace_id: str, model_id: str
    ) -> list[dict[str, Any]]:
        """List file resources in a model (upload/download targets)."""
        return self._model_resources(workspace_id, model_id, "files", "files")

    def list_imports(
        self, workspace_id: str, model_id: str
    ) -> list[dict[str, Any]]:
        """List import actions in a model."""
        return self._model_resources(
            workspace_id, model_id, "imports", "imports"
        )

    def list_exports(
        self, workspace_id: str, model_id: str
    ) -> list[dict[str, Any]]:
        """List export actions in a model."""
        return self._model_resources(
            workspace_id, model_id, "exports", "exports"
        )

    def list_actions(
        self, workspace_id: str, model_id: str
    ) -> list[dict[str, Any]]:
        """List generic actions (e.g. delete-from-list) in a model."""
        return self._model_resources(
            workspace_id, model_id, "actions", "actions"
        )

    def list_processes(
        self, workspace_id: str, model_id: str
    ) -> list[dict[str, Any]]:
        """List processes (ordered groups of actions) in a model."""
        return self._model_resources(
            workspace_id, model_id, "processes", "processes"
        )
