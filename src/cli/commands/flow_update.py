import typer

from src.cli.state import get_task_list, save_task_list
from src.task.task import Task
from src.ui.console import console
from src.ui.prompts import prompt_deadline, prompt_description, prompt_menu, prompt_priority, prompt_status, prompt_tags


class BackToMenuError(Exception):
    """Exception used to signal returning to the main Menu."""


def update_description(task: Task) -> None:
    """Prompt for and update a task description."""
    task.description = prompt_description()
    console.print("[green]Description updated.[/green]")


def update_status(task: Task) -> None:
    """Prompt for and update a task status."""
    task.status = prompt_status()
    console.print("[green]Status updated.[/green]")


def update_priority(task: Task) -> None:
    """Prompt for and update a task priority."""
    task.priority = prompt_priority()
    console.print("[green]Priority updated.[/green]")


def update_deadline(task: Task) -> None:
    """Prompt for and update a task deadline."""
    task.deadline = prompt_deadline()
    console.print("[green] Deadline updated.[/green]")


def update_tags(task: Task) -> None:
    """Prompt for and replace task tags."""
    task.tags = prompt_tags()
    console.print("[green]Tags updated.[/green]")


def move_back(_: Task) -> None:
    """Signal that the update submenu should return to the main menu."""
    raise BackToMenuError()


def update_task() -> None:
    """Run the interactive workflow for updating an existing task."""
    tasks = get_task_list()

    if not len(tasks):
        console.print("[yellow] No tasks to update.[/yellow]")
        return

    task_number = typer.prompt("Task number").strip()

    try:
        task_index = int(task_number) - 1
    except ValueError:
        console.print("[red]Invalid task number.[/red]")
        return

    if not (0 <= task_index < len(tasks)):
        console.print("[red]Provided task number is out of range.[/red]")
        return

    task = list(tasks)[task_index]

    handlers = {
        "Description": update_description,
        "Status": update_status,
        "Priority": update_priority,
        "Deadline": update_deadline,
        "Tags": update_tags,
        "Back": move_back,
    }

    while True:
        action = prompt_menu(handlers.keys())

        try:
            handlers[action](task)
        except BackToMenuError:
            break

    save_task_list()
    console.print("[green]Task updated successfully.[/green]")
    typer.pause()
