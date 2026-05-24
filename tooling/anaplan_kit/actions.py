"""Running processes (ordered groups of actions).

A *process* runs exactly like any other action — start a task, poll until
``COMPLETE`` — so this mixin simply delegates to the shared task lifecycle in
:mod:`anaplan_kit.imports_exports` rather than duplicating the polling logic.
"""

from __future__ import annotations

from typing import Any, Protocol


class _SupportsRunActionAndWait(Protocol):
    """Structural type for the lifecycle method this mixin reuses."""

    def run_action_and_wait(
        self, workspace_id: str, model_id: str, resource: str,
        resource_id: str, **kwargs: Any,
    ) -> dict[str, Any]: ...


class ActionsMixin:
    """Process-running convenience methods for the client."""

    def run_process(
        self: _SupportsRunActionAndWait,
        workspace_id: str,
        model_id: str,
        process_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Run a process and wait for it to complete.

        Reuses :meth:`~anaplan_kit.imports_exports.ImportsExportsMixin.run_action_and_wait`
        (and therefore its single ``poll_task`` implementation) so there is no
        duplicated polling logic.

        Args:
            workspace_id: Workspace ID.
            model_id: Model ID.
            process_id: The process to run.

        Returns:
            The completed task status payload, whose ``result`` rolls up each
            contained action's outcome.
        """
        return self.run_action_and_wait(
            workspace_id, model_id, "processes", process_id, **kwargs
        )

    def run_generic_action(
        self: _SupportsRunActionAndWait,
        workspace_id: str,
        model_id: str,
        action_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Run a generic action (e.g. delete-from-list) and wait for it.

        Args:
            workspace_id: Workspace ID.
            model_id: Model ID.
            action_id: The action to run.
        """
        return self.run_action_and_wait(
            workspace_id, model_id, "actions", action_id, **kwargs
        )
