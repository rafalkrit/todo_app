from src.cli.state import get_task_list
from src.ui.console import console
from src.ui.tasks_table import build_task_table


def list_tasks() -> None:
    """Render the current task list or an empty-state message."""
    task_list = get_task_list()

    if not len(task_list):
        console.print("[yellow]No tasks found.[/yellow]")
        return

    table = build_task_table(task_list)
    console.print(table)
