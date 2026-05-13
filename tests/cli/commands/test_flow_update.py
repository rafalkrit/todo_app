from datetime import date

import pytest

from src.cli.commands import flow_update
from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Task
from src.task_list.task_list import TaskList


def test_update_description(monkeypatch: pytest.MonkeyPatch, task_1: Task) -> None:

    msgs: list[str] = []

    def spy_print(msg: str) -> None:
        msgs.append(msg)

    monkeypatch.setattr(flow_update, "prompt_description", lambda: "New task_1")
    monkeypatch.setattr(flow_update.console, "print", spy_print)

    flow_update.update_description(task_1)
    assert task_1.description == "New task_1"
    assert msgs[0] == "[green]Description updated.[/green]"


def test_update_status(monkeypatch: pytest.MonkeyPatch, task_1: Task) -> None:

    msgs: list[str] = []

    def spy_print(msg: str) -> None:
        msgs.append(msg)

    monkeypatch.setattr(flow_update, "prompt_status", lambda: StatusEnum.COMPLETED)
    monkeypatch.setattr(flow_update.console, "print", spy_print)

    flow_update.update_status(task_1)

    assert task_1.status == StatusEnum.COMPLETED
    assert msgs[0] == "[green]Status updated.[/green]"


def test_update_priority(monkeypatch: pytest.MonkeyPatch, task_4: Task) -> None:

    msgs: list[str] = []

    def spy_print(msg: str) -> None:
        msgs.append(msg)

    monkeypatch.setattr(flow_update, "prompt_priority", lambda: PriorityEnum.LOW)
    monkeypatch.setattr(flow_update.console, "print", spy_print)

    flow_update.update_priority(task_4)

    assert task_4.priority == PriorityEnum.LOW
    assert msgs[0] == "[green]Priority updated.[/green]"


def test_update_deadline(task_4: Task, monkeypatch: pytest.MonkeyPatch) -> None:

    msgs: list[str] = []

    def spy_print(msg: str) -> None:
        msgs.append(msg)

    monkeypatch.setattr(flow_update, "prompt_deadline", lambda: date(2025, 12, 31))
    monkeypatch.setattr(flow_update.console, "print", spy_print)

    flow_update.update_deadline(task_4)

    assert task_4.deadline == date(2025, 12, 31)
    assert msgs[0] == "[green] Deadline updated.[/green]"


def test_update_tags(monkeypatch: pytest.MonkeyPatch, task_4: Task) -> None:

    msgs: list[str] = []

    def spy_print(msg: str) -> None:
        msgs.append(msg)

    monkeypatch.setattr(flow_update, "prompt_tags", lambda: ["python", "test"])
    monkeypatch.setattr(flow_update.console, "print", spy_print)

    flow_update.update_tags(task_4)

    assert task_4.tags == ["python", "test"]
    assert msgs[0] == "[green]Tags updated.[/green]"


def test_move_back(task_1: Task) -> None:
    with pytest.raises(flow_update.BackToMenuError):
        flow_update.move_back(task_1)


def test_update_task_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    msgs: list[str] = []

    def spy_print(msg: str) -> None:
        msgs.append(msg)

    monkeypatch.setattr(flow_update, "get_task_list", TaskList)
    monkeypatch.setattr(flow_update.console, "print", spy_print)

    flow_update.update_task()
    assert len(msgs) == 1
    assert msgs[0] == "[yellow] No tasks to update.[/yellow]"


def test_update_task_invalid_number(monkeypatch: pytest.MonkeyPatch) -> None:
    msgs: list[str] = []

    def spy_print(msg: str) -> None:
        msgs.append(msg)

    monkeypatch.setattr(flow_update, "get_task_list", lambda: TaskList([Task(description="Task1")]))
    monkeypatch.setattr(flow_update.console, "print", spy_print)
    monkeypatch.setattr(flow_update.typer, "prompt", lambda _: "abc")

    flow_update.update_task()

    assert len(msgs) == 1
    assert msgs[0] == "[red]Invalid task number.[/red]"


def test_update_task_out_of_range(monkeypatch: pytest.MonkeyPatch) -> None:
    msgs: list[str] = []

    def spy_print(msg: str) -> None:
        msgs.append(msg)

    monkeypatch.setattr(flow_update, "get_task_list", lambda: TaskList([Task(description="Task1")]))
    monkeypatch.setattr(flow_update.console, "print", spy_print)
    monkeypatch.setattr(flow_update.typer, "prompt", lambda _: "99")

    flow_update.update_task()

    assert len(msgs) == 1
    assert msgs[0] == "[red]Provided task number is out of range.[/red]"


def test_update_task_update_description(monkeypatch: pytest.MonkeyPatch, task_1: Task) -> None:

    msgs: list[str] = []
    saved = {"called": False}
    actions = iter(["Description", "Back"])

    def spy_print(msg: str) -> None:
        msgs.append(msg)

    def spy_save() -> None:
        saved["called"] = True

    monkeypatch.setattr(flow_update, "get_task_list", lambda: TaskList([task_1]))
    monkeypatch.setattr(flow_update.console, "print", spy_print)
    monkeypatch.setattr(flow_update, "save_task_list", spy_save)
    monkeypatch.setattr(flow_update.typer, "prompt", lambda _: "1")
    monkeypatch.setattr(flow_update, "update_description", lambda _: None)
    monkeypatch.setattr(flow_update, "prompt_menu", lambda _: next(actions))
    monkeypatch.setattr(flow_update.typer, "pause", lambda: None)

    flow_update.update_task()

    assert saved["called"] is True
    assert msgs[0] == "[green]Task updated successfully.[/green]"
