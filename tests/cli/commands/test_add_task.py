import pytest

from src.cli.commands.add_task import add_task
from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Task
from src.task_list.task_list import TaskList


def test_add_task(monkeypatch: pytest.MonkeyPatch) -> None:

    task_list = TaskList()
    saved = {"called": False}
    summary: dict[str, object] = {"task": None, "highlight_field": ""}

    monkeypatch.setattr("src.cli.commands.add_task.prompt_description", lambda: "Task description")
    monkeypatch.setattr("src.cli.commands.add_task.prompt_status", lambda: StatusEnum.COMPLETED)
    monkeypatch.setattr("src.cli.commands.add_task.prompt_priority", lambda: PriorityEnum.HIGH)
    monkeypatch.setattr("src.cli.commands.add_task.prompt_deadline", lambda: None)
    monkeypatch.setattr("src.cli.commands.add_task.prompt_tags", lambda: ["python", "nauka"])

    monkeypatch.setattr("src.cli.commands.add_task.get_task_list", lambda: task_list)

    def spy_save_task_list() -> None:
        saved["called"] = True

    monkeypatch.setattr("src.cli.commands.add_task.save_task_list", spy_save_task_list)

    def spy_print_task_summary(task: Task, highlight_field: str) -> None:
        summary["task"] = task
        summary["highlight_field"] = highlight_field

    monkeypatch.setattr("src.cli.commands.add_task.print_task_summary", spy_print_task_summary)

    add_task()

    assert len(task_list) == 1
    task = task_list[0]

    assert task.description == "Task description"
    assert task.status == StatusEnum.COMPLETED
    assert task.priority == PriorityEnum.HIGH
    assert task.deadline is None
    assert task.tags == ["python", "nauka"]
    assert saved["called"] is True
    assert summary["task"] == task
    assert summary["highlight_field"] == "description"
