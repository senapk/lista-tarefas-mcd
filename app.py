from datetime import date

from flask import Flask, abort, redirect, render_template, request, url_for

from tasks import Task, TaskList


class TaskWebApp:
    """Connect HTML forms to the task library."""

    def __init__(self, task_list: TaskList | None = None) -> None:
        self.task_list = task_list if task_list is not None else TaskList()
        self.app = Flask(__name__)
        self.app.add_url_rule("/", view_func=self.index)
        self.app.add_url_rule("/tasks", view_func=self.add_task, methods=["POST"])
        self.app.add_url_rule(
            "/tasks/<int:task_index>/delete", view_func=self.delete_task, methods=["POST"]
        )
        self.app.add_url_rule(
            "/tasks/<int:task_index>/complete", view_func=self.complete_task, methods=["POST"]
        )

    def index(self):
        return render_template("index.html", tasks=self.task_list.list_tasks(), values={})

    def add_task(self):
        values = request.form
        try:
            text = values.get("text", "").strip()
            if not text:
                raise ValueError("Task text is required.")
            due_date = values.get("due_date", "").strip()
            task = Task(
                text=text,
                due_date=date.fromisoformat(due_date) if due_date else None,
                category=values.get("category", "").strip(),
            )
        except ValueError as error:
            return render_template(
                "index.html", tasks=self.task_list.list_tasks(), values=values, error=str(error)
            ), 400
        self.task_list.add_task(task)
        return redirect(url_for("index"))

    def delete_task(self, task_index: int):
        tasks = self.task_list.list_tasks()
        if task_index >= len(tasks):
            abort(404)
        self.task_list.delete_task(tasks[task_index])
        return redirect(url_for("index"))

    def complete_task(self, task_index: int):
        tasks = self.task_list.list_tasks()
        if task_index >= len(tasks):
            abort(404)
        tasks[task_index].complete()
        return redirect(url_for("index"))


if __name__ == "__main__":
    TaskWebApp().app.run(host="127.0.0.1", port=5000)
