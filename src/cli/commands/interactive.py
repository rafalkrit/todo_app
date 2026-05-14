from typing import Never

import typer

from src.cli.commands.add_task import add_task
from src.cli.commands.flow_update import update_task
from src.cli.commands.list_tasks import list_tasks
from src.cli.commands.remove_task import remove_task
from src.ui.console import console
from src.ui.prompts import prompt_menu


def exit_app() -> Never:
    """Print the exit message and terminate the Typer application."""
    console.print("[dim]Bye 👋[/dim]")
    raise typer.Exit(code=0)


def interactive() -> None:
    """Run the main interactive application menu until the user exits."""
    handlers = {
        "Show tasks": list_tasks,
        "Add task": add_task,
        "Update task": update_task,
        "Remove task": remove_task,
        "Exit": exit_app,
    }

    while True:
        action = prompt_menu(handlers.keys())
        handlers[action]()


# $ export STORAGE_PATH_ENV="/c/Users/rafal/pythonprojects/todo_app/temp/rafal_todo_list.json"
