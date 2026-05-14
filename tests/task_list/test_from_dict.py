from dataclasses import dataclass
from typing import TYPE_CHECKING, cast
from uuid import UUID, uuid4

import pytest

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
import src.task_list.task_list as task_list_module
from src.task_list.task_list import TaskList


if TYPE_CHECKING:
    from collections.abc import Iterable

    from src.schemas.task_list_schema import TaskListDict
    from src.task.task import Task


@dataclass(frozen=True)
class _TaskStub:
    payload: dict[str, str]
    idx: UUID

    def to_dict(self) -> dict[str, str]:
        return self.payload

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "_TaskStub":
        return cls(payload=data, idx=uuid4())


def test_to_dict_builds_tasks_list(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr(task_list_module, "Task", _TaskStub, raising=True)
    tasks = [_TaskStub({"description": "a"}, idx=uuid4()), _TaskStub({"description": "b"}, idx=uuid4())]
    task_list = TaskList(cast("Iterable[Task]", tasks))

    assert task_list.to_dict() == {"tasks": [{"description": "a"}, {"description": "b"}]}


def test_from_dict_creates_task_list_and_calls_task_from_dict(monkeypatch: pytest.MonkeyPatch) -> None:

    calls: list[dict] = []

    class _TaskSpy(_TaskStub):
        @classmethod
        def from_dict(cls, data: dict[str, str]) -> "_TaskSpy":
            calls.append(data)
            return cls(payload=data, idx=uuid4())

    monkeypatch.setattr(task_list_module, "Task", _TaskSpy, raising=True)
    data: dict[str, list[dict[str, str]]] = {"tasks": [{"description": "a"}, {"description": "b"}]}

    tasks = TaskList.from_dict(cast("TaskListDict", data))

    assert isinstance(tasks, TaskList)
    assert len(calls) == 2
    assert calls == [{"description": "a"}, {"description": "b"}]


def test_task_list_from_dict_creates_full_task_collection_correctly(task_dict: dict[str, object]) -> None:
    data: TaskListDict = {
        "tasks": [
            {
                "description": "Python learn",
                "status": "in progress",
                "priority": 2,
                "created_at": "2025-11-20T00:00:00+00:00",
                "deadline": "2026-10-15",
                "completed_at": None,
                "tags": ["learning", "work"],
                "idx": "63614577-08fa-4049-8e23-267d6867517c",
            },
            {
                "description": "Write tests",
                "status": "completed",
                "priority": 1,
                "created_at": "2025-12-01T10:00:00+00:00",
                "deadline": "2025-12-31",
                "completed_at": "2025-12-20T12:00:00+00:00",
                "tags": ["testing", "backend"],
                "idx": "d2719a58-6c9e-4c5c-9ef0-8a2c8f5b8b1e",
            },
        ]
    }

    task_list = TaskList.from_dict(data)

    assert isinstance(task_list, TaskList)
    assert len(task_list.tasks) == 2

    first, second = task_list.tasks
    assert first.description == "Python learn"
    assert first.status is StatusEnum.IN_PROGRESS
    assert first.priority is PriorityEnum.MEDIUM

    assert second.description == "Write tests"
    assert second.status is StatusEnum.COMPLETED
    assert second.priority is PriorityEnum.LOW


def test_task_list_from_dict_empty_tasks() -> None:
    data: TaskListDict = {"tasks": []}

    task_list = TaskList.from_dict(data)

    assert isinstance(task_list, TaskList)
    assert task_list.tasks == []


def test_task_list_from_dict_tasks_is_not_list() -> None:
    data = {"tasks": "not a list"}

    with pytest.raises(TypeError):
        TaskList.from_dict(cast("TaskListDict", data))
