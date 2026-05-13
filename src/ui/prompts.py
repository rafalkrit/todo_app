from collections.abc import Iterable
from datetime import UTC, date, datetime, timedelta

from questionary import Style, select
import typer

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.ui.console import console


style = Style([
    ("highlighted", "fg:#ffffff bg:#44475a bold"),
    ("pointer", "fg:#50fa7b bold"),
    ("selected", "fg:#50fa7b"),
    ("question", "bold"),
])


def prompt_menu(choices: Iterable[str], *, title: str = "Menu") -> str:
    """Prompt the user to choose one item from a menu."""
    return select(title, choices=list(choices), style=style).ask()


def prompt_description() -> str:
    """Prompt until the user provides a valid task description."""
    while True:
        description = typer.prompt("Task description").strip()

        if 3 <= len(description) <= 120:
            return description

        console.print("[yellow]Description must be between 3 and 120 characters.[/yellow]")


def prompt_status() -> StatusEnum:
    """Prompt the user to select a task status."""
    status_options = [s.value.capitalize() for s in StatusEnum]
    chosen_status = select("Choose status:", choices=status_options, style=style).ask()

    return StatusEnum(chosen_status.lower())


def prompt_priority() -> PriorityEnum:
    """Prompt the user to select a task priority."""
    priority_options = [priority.name.title() for priority in PriorityEnum]
    chosen_priority = select("Choose priority", choices=priority_options, style=style).ask()

    return PriorityEnum[chosen_priority.upper()]


def prompt_deadline() -> date | None:
    """Prompt the user to choose or enter an optional deadline."""
    options = ["No deadline", "Today", "Tomorrow", "In 7 days", "In 14 days", "Pick exact day (YYYY-MM-DD)"]
    chosen_option = select("Choose option", choices=options, style=style).ask()

    today = datetime.now(tz=UTC).date()

    if chosen_option == "No deadline":
        return None
    if chosen_option == "Today":
        return today
    if chosen_option == "Tomorrow":
        return today + timedelta(days=1)
    if chosen_option == "In 7 days":
        return today + timedelta(days=7)
    if chosen_option == "In 14 days":
        return today + timedelta(days=14)

    while True:
        raw = typer.prompt("Deadline (YYYY-MM-DD)").strip()

        try:
            user_deadline = date.fromisoformat(raw)
            if user_deadline >= today:
                return user_deadline
            typer.echo("Date shoud be in the future")
        except ValueError:
            typer.echo("Invalid deadline format. Use YYYY-MM-DD")


def prompt_tags() -> list[str]:
    """Prompt the user for comma-separated tags."""
    tags_raw = typer.prompt("Enter tags", default="").strip()
    return [tag.strip() for tag in tags_raw.split(",") if tag.strip()]
