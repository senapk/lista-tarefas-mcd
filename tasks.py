from dataclasses import replace
from threading import RLock

from task import Task
from task_storage import TaskStorage


class TaskList:
    """Manage tasks and unique IDs, delegating persistence to storage.

    A lock serializes requests within one server process.
    """

    def __init__(self, storage: TaskStorage) -> None:
        self._storage = storage
        self._lock = RLock()
        self._tasks, self._next_id = storage.load()

    def add_task(self, task: Task) -> Task:
        """Assign a new ID, save the task, and return a copy."""
        with self._lock:
            stored = replace(task, id=self._next_id)
            tasks = {**self._tasks, stored.id: stored}
            self._storage.save(tasks, self._next_id + 1)
            self._tasks = tasks
            self._next_id += 1
            return replace(stored)

    def list_tasks(self) -> list[Task]:
        """Return task copies in registration order."""
        with self._lock:
            return [replace(task) for task in self._tasks.values()]

    def delete_task(self, task_id: int) -> None:
        """Delete by ID; raise KeyError if the task no longer exists."""
        with self._lock:
            tasks = self._tasks.copy()
            del tasks[task_id]
            self._storage.save(tasks, self._next_id)
            self._tasks = tasks

    def complete_task(self, task_id: int) -> None:
        """Complete by ID and persist the new status."""
        with self._lock:
            task = self._tasks[task_id]
            tasks = {**self._tasks, task_id: replace(task, done=True)}
            self._storage.save(tasks, self._next_id)
            self._tasks = tasks
