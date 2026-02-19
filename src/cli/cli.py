from datetime import UTC, date, datetime

from rich.console import Console
from rich.table import Table
import typer

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Task
from src.task_list.task_list import TaskList


app = typer.Typer(name="ToDo App", help="A professionanll ToDo CLI aplication")
console = Console()
tasks = TaskList([
    Task(description="task_1", status=StatusEnum.TODO),
    Task(description="task_2", status=StatusEnum.COMPLETED),
    Task(
        description="task_4",
        status=StatusEnum.IN_PROGRESS,
        priority=PriorityEnum.HIGH,
        created_at=datetime(2025, 11, 20, tzinfo=UTC),
        deadline=date(2025, 12, 15),
        completed_at=datetime(2025, 11, 30, tzinfo=UTC),
        tags=["learning", "feature", "work"],
    ),
])


@app.command()
def list_tasks() -> None:
    if not len(tasks):
        console.print("[yellow]No tasks found.[/yellow]")
        return

    table = Table(title="Task List", show_header=True, header_style="bold magenta")
    table.add_column("Status", justify="center")
    table.add_column("Priority", justify="center", width=8)
    table.add_column("Description", style="cyan")
    table.add_column("Deadline", justify="center")
    table.add_column("Tags", style="green")
    table.add_column("Id", style="dim", no_wrap=True)

    for task in tasks:
        table.add_row(
            task.status.value,
            task.priority.name,
            task.description,
            str(task.deadline),
            ", ".join(task.tags),
            str(task.idx),
        )

    console.print(table)
