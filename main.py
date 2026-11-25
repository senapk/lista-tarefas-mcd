from datetime import date

from tasks import Task, TaskList


def main() -> None:
    task_list = TaskList()

    while True:
        print("\n1. Add task\n2. List tasks\n3. Delete task\n0. Exit")
        option = input("Choose an option: ").strip()

        if option == "0":
            break

        if option == "1":
            text = input("Text: ").strip()
            category = input("Category: ").strip()
            try:
                date_text = input("Due date (YYYY-MM-DD, optional): ").strip()
                due_date = date.fromisoformat(date_text) if date_text else None
                task = Task(text=text, due_date=due_date, category=category)
            except ValueError as error:
                print(f"Could not add task: {error}")
                continue
            task_list.add_task(task)
            print("Task added.")

        elif option in {"2", "3"}:
            tasks = task_list.list_tasks()
            if not tasks:
                print("No tasks registered.")
                continue

            for number, task in enumerate(tasks, start=1):
                status = "Done" if task.done else "Pending"
                print(f"\n{number}. {task.text}")
                print(f"   Category: {task.category}")
                print(f"   Due date: {task.due_date or 'Not defined'} | Status: {status}")

            if option == "3":
                try:
                    number = int(input("Task number to delete (0 to cancel): "))
                except ValueError:
                    print("Enter a valid task number.")
                    continue
                if number == 0:
                    continue
                if not 1 <= number <= len(tasks):
                    print("Invalid task number.")
                    continue
                task_list.delete_task(tasks[number - 1])
                print("Task deleted.")
        else:
            print("Invalid option.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")
