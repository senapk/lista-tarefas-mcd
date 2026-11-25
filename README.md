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

## Structure

- `tasks.py`: task models and business logic.
- `app.py`: `TaskWebApp`, connecting the library to Flask and HTML forms.
- `main.py`: terminal menu.
- `templates/index.html`: web page.
- `static/style.css`: page styles.
- `pyproject.toml` and `uv.lock`: project dependencies and locked versions.

Tasks are stored in memory and are lost when the program stops. Each running
interface has its own task list. The web server is intended for local use.
