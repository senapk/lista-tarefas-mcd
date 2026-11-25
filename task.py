from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """A task identified by a persistent, unique integer."""

    text: str
    category: str
    due_date: date | None = None
    done: bool = False
    id: int | None = None

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("Task text must not be empty.")
        if not self.category.strip():
            raise ValueError("Category must not be empty.")

