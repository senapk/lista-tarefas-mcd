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

- `tasks.py`: task models and business logic.
- `app.py`: `TaskWebApp`, connecting the library to Flask and HTML forms.
- `main.py`: terminal menu.
- `templates/index.html`: web page.
- `static/style.css`: page styles.
- `pyproject.toml` and `uv.lock`: project dependencies and locked versions.

Tasks are stored in memory and are lost when the program stops. Each running
interface has its own task list. The web server is intended for local use.
