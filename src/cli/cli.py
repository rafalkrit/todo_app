from datetime import UTC, date, datetime
from enum import StrEnum
from typing import Annotated

import questionary
from rich import box
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

    table = Table(title="Task List", show_header=True, header_style="bold magenta", box=box.SIMPLE)
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


@app.command()
def add_task(
    deadline: Annotated[
        str | None,
        typer.Option("--deadline", help="Deadline in YYYY-MM-DD format."),
    ] = None,
    tags: Annotated[list[str] | None, typer.Option("--tag", "-t")] = None,
) -> None:
    description = typer.prompt("Task description").strip()

    if not (3 <= len(description) <= 120):
        console.print("[yellow]Description: must be between 3 and 120 characters.[/yellow]")

    status_options = [s.value for s in StatusEnum]
    chosen_status = questionary.select(
        "Choose status:",
        choices=status_options,
    ).ask()
    status = StatusEnum(chosen_status)

    priority_options = [priority.name.title() for priority in PriorityEnum]
    chosen_priority = questionary.select("Choose priority", choices=priority_options).ask()
    priority = PriorityEnum[chosen_priority.upper()]

    parsed_deadline: date | None = None
    if deadline is not None:
        try:
            parsed_deadline = date.fromisoformat(deadline)
        except ValueError as error:
            console.print("[red]Invalid deadline format. Use YYYY-MM-DD.[/red]")
            raise typer.Exit(code=1) from error

    try:
        task = Task(
            description=description,
            status=status,
            priority=priority,
            deadline=parsed_deadline,
            tags=tags,
        )
        tasks.add(task)
    except ValueError as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(code=1) from error

    console.print(f"[green]Task added:[/green] {task.description} (id: {task.idx})")


class MenuAction(StrEnum):
    ADD = "1"
    LIST = "2"
    EXIT = "3"


def prompt_action() -> MenuAction:
    console.print("[bold]Menu[/bold]")
    console.print("[cyan]1[/cyan] Add Task")
    console.print("[cyan]2[/cyan] Show Tasks")
    console.print("[cyan]3[/cyan] Exit")

    def _coerce(raw: str) -> MenuAction:
        raw = raw.strip()
        try:
            return MenuAction(raw)
        except ValueError as error:
            raise typer.BadParameter("Choose 1, 2, 3") from error

    return typer.prompt("Choose", default=MenuAction.LIST.value, value_proc=_coerce)


@app.command()
def interactive():
    handlers = {MenuAction.ADD: add_task, MenuAction.LIST: list_tasks}

    while True:
        action = prompt_action()
        if action is MenuAction.EXIT:
            console.print("[dim]Bye 👋[/dim]")
            raise typer.Exit(code=0)
        handlers[action]()
