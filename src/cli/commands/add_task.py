from src.cli.commands.print_task_summary import print_task_summary
from src.cli.state import get_task_list, save_task_list
from src.task.task import Task
from src.ui.console import console
from src.ui.prompts import prompt_deadline, prompt_description, prompt_priority, prompt_status, prompt_tags


def add_task() -> None:
    """Run the interactive workflow for creating and saving a new task."""
    description = prompt_description()
    status = prompt_status()
    priority = prompt_priority()
    deadline = prompt_deadline()
    tags = prompt_tags()

    task = Task(
        description=description,
        status=status,
        priority=priority,
        deadline=deadline,
        tags=tags,
    )

    task_list = get_task_list()
    task_list.add(task)
    save_task_list()
    console.print("[green]Task added:[/green]")
    print_task_summary(task, "description")
