from rich import box
from rich.table import Table

from src.task_list.task_list import TaskList


def build_task_table(tasks: TaskList) -> Table:
    """Build a Rich table representing the provided task collection."""
    table: Table = Table(
        title="Task List",
        show_header=True,
        header_style="bold magenta",
        box=box.SIMPLE,
    )

    table.add_column("Id", style="dim", no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Priority", justify="center", width=8)
    table.add_column("Description", style="cyan")
    table.add_column("Deadline", justify="center")
    table.add_column("Tags", style="green")

    for i, task in enumerate(tasks, start=1):
        table.add_row(
            str(i),
            task.status.value,
            task.priority.name,
            task.description,
            str(task.deadline),
            ", ".join(task.tags),
        )

    return table
