import pytest
from rich.table import Table

from src.cli.commands.list_tasks import list_tasks
from src.task.task import Task
from src.task_list.task_list import TaskList


def test_list_tasks_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    msgs = []

    def spy_print(msg: str) -> None:
        msgs.append(msg)

    monkeypatch.setattr("src.cli.commands.list_tasks.get_task_list", TaskList)
    monkeypatch.setattr("src.cli.commands.list_tasks.console.print", spy_print)

    list_tasks()

    assert len(msgs) == 1
    assert msgs[0] == "[yellow]No tasks found.[/yellow]"


def test_list_tasks_prints_table(monkeypatch: pytest.MonkeyPatch, task_1: Task, task_2: Task) -> None:
    task_list = TaskList([task_1, task_2])
    msgs = []

    def spy_print(msg: str) -> None:
        msgs.append(msg)

    monkeypatch.setattr("src.cli.commands.list_tasks.get_task_list", lambda: task_list)
    monkeypatch.setattr("src.cli.commands.list_tasks.console.print", spy_print)

    list_tasks()

    assert len(msgs) == 1
    assert isinstance(msgs[0], Table)
    assert msgs[0].title == "Task List"
    assert msgs[0].row_count == 2
