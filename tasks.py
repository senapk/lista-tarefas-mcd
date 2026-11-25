from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """A task with a description, category, due date, and completion status."""

    text: str
    category: str
    due_date: date | None = None
    done: bool = False

    def __post_init__(self) -> None:
        if not self.category.strip():
            raise ValueError("Category must not be empty.")

    def complete(self) -> None:
        """Mark this task as done."""
        self.done = True


class TaskList:
    """Store registered tasks in memory."""

    def __init__(self) -> None:
        self._tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the list."""
        self._tasks.append(task)

    def list_tasks(self) -> list[Task]:
        """Return a copy of the tasks in registration order."""
        return self._tasks.copy()

    def delete_task(self, task: Task) -> None:
        """Delete a task, raising ValueError if it is not in the list."""
        self._tasks.remove(task)
