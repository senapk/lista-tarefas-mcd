from abc import ABC, abstractmethod
from dataclasses import asdict
from datetime import date
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from task import Task


class TaskStorage(ABC):
    """Persistence contract used by the task manager."""

    @abstractmethod
    def load(self) -> tuple[dict[int, Task], int]:
        """Load saved tasks and the next available ID."""
    @abstractmethod
    def save(self, tasks: dict[int, Task], next_id: int) -> None:
        """Save tasks and the next available ID."""


class JsonTaskStorage(TaskStorage):
    """Serialize task snapshots and atomically store them in JSON."""

    def __init__(self, storage_path: str | Path | None = None) -> None:
        self.storage_path = (
            Path(storage_path) if storage_path is not None
            else Path(__file__).resolve().parent / "data" / "tasks.json"
        )

    def load(self) -> tuple[dict[int, Task], int]:
        if not self.storage_path.exists():
            return {}, 1
        # Invalid files raise an error rather than silently losing saved tasks.
        data = json.loads(self.storage_path.read_text(encoding="utf-8"))
        tasks = {}
        for key, record in data["tasks"].items():
            task_id = int(key)
            if task_id < 1 or record["id"] != task_id or task_id in tasks:
                raise ValueError("Invalid task ID in storage.")
            record = dict(record)
            record["due_date"] = date.fromisoformat(record["due_date"]) if record["due_date"] else None
            if type(record["done"]) is not bool:
                raise ValueError("Invalid completion status in storage.")
            tasks[task_id] = Task(**record)
        next_id = data["next_id"]
        if type(next_id) is not int or next_id <= max(tasks, default=0):
            raise ValueError("Invalid next task ID in storage.")
        return tasks, next_id

    def save(self, tasks: dict[int, Task], next_id: int) -> None:
        records = {}
        for task_id, task in tasks.items():
            record = asdict(task)
            record["due_date"] = task.due_date.isoformat() if task.due_date else None
            records[str(task_id)] = record
        payload = {"next_id": next_id, "tasks": records}
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = None
        try:
            with NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=self.storage_path.parent,
                prefix=".tasks-", suffix=".tmp", delete=False,
            ) as temporary:
                temporary_path = Path(temporary.name)
                json.dump(payload, temporary, ensure_ascii=False, indent=2)
                temporary.write("\n")
                temporary.flush()
                os.fsync(temporary.fileno())
            os.replace(temporary_path, self.storage_path)
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
