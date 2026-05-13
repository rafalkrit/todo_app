import typer

from src.cli.state import get_task_list, save_task_list
from src.ui.console import console


def remove_task() -> None:
    """Run the interactive workflow for removing a task by list number."""

    tasks = get_task_list()
    if not len(tasks):
        console.print("[yellow]No tasks to remove.[/yellow]")

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
    tasks.remove(task.idx)
    save_task_list()
    console.print(f"[green]Task removed:[/green] {task.description}")
