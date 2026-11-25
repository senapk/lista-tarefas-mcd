# Task List

A Python task library with a Flask web interface and a terminal interface.

## Setup

Install [uv](https://docs.astral.sh/uv/), then run from the project directory:

```bash
uv sync --locked
```

Dependencies are installed in the local `.venv` directory.

## Web interface

```bash
uv run app.py
```

Open http://127.0.0.1:5000 to add, list, complete, and delete tasks.
Each task has a single text field, a required category, and an optional due date.
The web interface uses HTML forms without JavaScript.

## Terminal interface

```bash
uv run main.py
```

The terminal menu supports adding, listing, and deleting tasks.

## GitHub Codespaces

Create a Codespace from the repository's **Code > Codespaces** menu.
The dev container includes Python 3.12 and uv, installs the locked dependencies
in `.venv`, and starts `app.py` automatically on port 5000. The forwarded port
opens in the browser. If it does not open, use **Open in Browser** in the
**Ports** tab for port 5000.

When the editor attaches, the GitHub CLI sets port 5000 to **public** using
`gh codespace ports visibility`. Anyone with the forwarded URL can access
the task list, including adding, completing, and deleting tasks.
If a GitHub permission or organization policy prevents the change, the
attachment hook reports an error; check the **Visibility** column in **Ports**.

The server also starts when the Codespace is restarted. For an existing
Codespace, run **Codespaces: Rebuild Container** after adding this configuration.
Server output is saved in `.devcontainer/.runtime/server.log`.
To start the server manually if needed:

```bash
bash .devcontainer/start-server.sh
```

The start script prevents duplicate instances. To apply Python code changes,
stop and restart the Codespace. No automatic reload is enabled.

## Structure

- `task.py`: the `Task` model.
- `tasks.py`: `TaskList`, managing tasks by ID and coordinating operations.
- `task_storage.py`: the `TaskStorage` contract and `JsonTaskStorage`, responsible
  for JSON serialization, loading, validation, and atomic file writes.
- `app.py`: `TaskWebApp`, connecting the library to Flask and HTML forms.
- `main.py`: terminal menu.
- `templates/index.html`: web page.
- `static/style.css`: page styles.
- `pyproject.toml` and `uv.lock`: project dependencies and locked versions.

Tasks are stored by incremental ID in a Python dictionary. Add, complete, and
delete operations automatically save to `data/tasks.json`. The next ID is also
saved, so deleted IDs are not reused after a restart. Both interfaces restore
the saved tasks on startup. The runtime data directory is excluded from Git.

The interfaces assemble the manager with its storage dependency:

```python
from tasks import TaskList
from task_storage import JsonTaskStorage

task_list = TaskList(JsonTaskStorage())
```

`TaskList` works through the `TaskStorage` contract and does not handle JSON or
file paths. A future storage implementation can supply the same `load` and
`save` methods without changing task management.

Writes use a temporary file and atomic replacement. An invalid JSON file stops
startup instead of silently overwriting saved data. Back up the JSON file before
repairing it if necessary.

Run one server process per JSON file; requests within that process are serialized
for safe updates. Do not run the terminal interface and server against the same
file at the same time. Storage survives a server/Codespace restart, but deleting
the Codespace also deletes its local data unless you back it up separately.

Run the regression tests with:

```bash
uv run python -m unittest discover -s tests -v
```
