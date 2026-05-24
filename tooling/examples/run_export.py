"""Example: run an export action, then download the produced file in chunks.

Run::

    python examples/run_export.py <exportId> <fileId> <output/path.csv>

Needs a real Anaplan tenant + credentials. The export's ``fileId`` is usually
the same as the export action's ID; confirm via client.list_files / list_exports.
"""

from __future__ import annotations

import sys

from _config import build_client, require_env


def main() -> None:
    if len(sys.argv) != 4:
        sys.exit("Usage: python run_export.py <exportId> <fileId> <outPath>")
    export_id, file_id, out_path = sys.argv[1:4]

    workspace_id = require_env("ANAPLAN_WORKSPACE_ID")
    model_id = require_env("ANAPLAN_MODEL_ID")
    client = build_client()

    client.run_export(workspace_id, model_id, export_id)
    print("Export action complete; downloading file...")

    written = client.download_export(workspace_id, model_id, file_id, out_path)
    print(f"Downloaded export to {written}.")


if __name__ == "__main__":
    main()
