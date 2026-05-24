"""Example: upload a CSV in chunks, run a named import, print the result.

Run::

    python examples/run_import.py <fileId> <importId> <path/to/data.csv>

Needs a real Anaplan tenant + credentials, plus the file/import IDs from the
target model (discover them with list_models.py and client.list_files / ...).
"""

from __future__ import annotations

import sys

from _config import build_client, require_env


def main() -> None:
    if len(sys.argv) != 4:
        sys.exit("Usage: python run_import.py <fileId> <importId> <csvPath>")
    file_id, import_id, csv_path = sys.argv[1:4]

    workspace_id = require_env("ANAPLAN_WORKSPACE_ID")
    model_id = require_env("ANAPLAN_MODEL_ID")
    client = build_client()

    chunks = client.upload_file(workspace_id, model_id, file_id, csv_path)
    print(f"Uploaded {csv_path} in {chunks} chunk(s).")

    status = client.run_import(workspace_id, model_id, import_id)
    result = status.get("result", {})
    print(f"Import complete. successful={result.get('successful')}")
    print(f"  rows: {result.get('details', result)}")


if __name__ == "__main__":
    main()
