from datetime import UTC, date, datetime
import re
from typing import TYPE_CHECKING, cast
from uuid import UUID

import pytest

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Task


if TYPE_CHECKING:
    from src.schemas.tasks_schema import TaskDict


def test_from_dict_correct() -> None:
    data: TaskDict = {
        "description": "Python learn",
        "status": "in progress",
        "priority": 2,
        "created_at": "2025-11-20T00:00:00+00:00",
        "deadline": "2026-10-15",
        "completed_at": None,
        "tags": ["learning", "feature", "work"],
        "idx": "63614577-08fa-4049-8e23-267d6867517c",
    }

    t: Task = Task.from_dict(data)

    assert isinstance(t, Task)
    assert t.description == "Python learn"
    assert t.status == StatusEnum.IN_PROGRESS
    assert t.priority == PriorityEnum.MEDIUM
    assert t.created_at == datetime(2025, 11, 20, tzinfo=UTC)
    assert t.deadline == date(2026, 10, 15)
    assert t.completed_at is None
    assert t.tags == ["learning", "feature", "work"]
    assert t.idx == UUID("63614577-08fa-4049-8e23-267d6867517c", version=4)


def test_from_dict_incorrect_keys() -> None:
    data: dict[str, str] = {"description": "learn python"}
    with pytest.raises(KeyError):
        Task.from_dict(cast("TaskDict", data))


def test_from_dict_incorrect_value() -> None:
    data: dict[str, object] = {"description": "learn python", "status": [1, 3]}

    msg = re.escape("[1, 3] is not a valid StatusEnum")
    with pytest.raises(ValueError, match=msg):
        Task.from_dict(cast("TaskDict", data))
