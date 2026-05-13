import pytest

from src.cli.commands.remove_task import remove_task
from src.task.task import Task
from src.task_list.task_list import TaskList


def test_remove_task_empty_task_list(monkeypatch: pytest.MonkeyPatch) -> None:
    msgs = []

    def spy_print(msg: str) -> None:
        msgs.append(msg)

    monkeypatch.setattr("src.cli.commands.remove_task.get_task_list", TaskList)
    monkeypatch.setattr("src.cli.commands.remove_task.console.print", spy_print)

    remove_task()
    assert len(msgs) == 1
    assert msgs[0] == "[yellow]No tasks to remove.[/yellow]"


def test_remove_task_success(monkeypatch: pytest.MonkeyPatch) -> None:
    msgs: list[str] = []

    def spy_print(msg: str) -> None:
        msgs.append(msg)

    task_list = TaskList([Task(description="Task1"), Task(description="Task2")])
    saved = {"called": False}

    def spy_save_task_list() -> None:
        saved["called"] = True

    monkeypatch.setattr("src.cli.commands.remove_task.get_task_list", lambda: task_list)
    monkeypatch.setattr("src.cli.commands.remove_task.typer.prompt", lambda *_: "1")
    monkeypatch.setattr("src.cli.commands.remove_task.save_task_list", spy_save_task_list)
    monkeypatch.setattr("src.cli.commands.remove_task.console.print", spy_print)

    remove_task()

    assert len(task_list) == 1
    assert saved["called"] is True
    assert msgs[0] == "[green]Task removed:[/green] Task1"


def test_remove_task_invalid_number(monkeypatch: pytest.MonkeyPatch) -> None:
    msgs: list[str] = []

    def spy_print(msg: str) -> None:
        msgs.append(msg)

    def stub_prompt(text: str) -> str:
        return "abc"

    task_list = TaskList([Task(description="Task1")])

    monkeypatch.setattr("src.cli.commands.remove_task.get_task_list", lambda: task_list)
    monkeypatch.setattr("src.cli.commands.remove_task.typer.prompt", stub_prompt)
    monkeypatch.setattr("src.cli.commands.remove_task.console.print", spy_print)

    remove_task()

    assert len(msgs) == 1
    assert msgs[0] == "[red]Invalid task number.[/red]"


def test_update_task_out_of_range(monkeypatch: pytest.MonkeyPatch, task_1: Task) -> None:
    task_list = TaskList([task_1])
    msgs = []

    def spy_print(msg: str) -> None:
        msgs.append(msg)

    monkeypatch.setattr("src.cli.commands.remove_task.get_task_list", lambda: task_list)
    monkeypatch.setattr("src.cli.commands.remove_task.console.print", spy_print)
    monkeypatch.setattr("typer.prompt", lambda _: "99")

    remove_task()

    assert len(msgs) == 1
    assert msgs[0] == "[red]Provided task number is out of range.[/red]"
