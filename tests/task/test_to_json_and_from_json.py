from datetime import UTC, date, datetime
import json
from uuid import UUID

import pytest

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Task


def test_to_json_contains_all_fields(task_4: Task) -> None:
    raw = task_4.to_json()

    parsed = json.loads(raw)

    assert set(parsed.keys()) == {
        "description",
        "status",
        "priority",
        "created_at",
        "deadline",
        "completed_at",
        "tags",
        "idx",
    }


def test_to_json_correct_values(task_4: Task) -> None:
    raw = task_4.to_json()

    parsed = json.loads(raw)

    assert parsed["description"] == "task_4"
    assert parsed["status"] == "in progress"
    assert parsed["priority"] == 3
    assert parsed["created_at"] == "2025-11-20T00:00:00+00:00"
    assert parsed["deadline"] == "2025-12-15"
    assert parsed["completed_at"] is None
    assert parsed["tags"] == ["learning", "feature", "work"]
    assert parsed["idx"] == str(task_4.idx)


def test_to_json_with_indent(task_4: Task) -> None:
    raw = task_4.to_json(indent=2)

    parsed = json.loads(raw)

    assert isinstance(raw, str)
    assert "\n" in raw
    assert "  " in raw
    assert parsed["description"] == "task_4"


def test_from_json_returns_task() -> None:
    raw: str = (
        '{"description": "task_4", "status": "in progress", "priority": 3,'
        '"created_at": "2025-11-20T00:00:00+00:00", "deadline": "2025-12-15",'
        '"completed_at": null, "tags": ["learning", "feature", "work"],'
        '"idx": "c91b0ef1-b65f-4885-bb39-9ebb32410720"}'
    )

    task_restored = Task.from_json(raw)

    assert isinstance(task_restored, Task)
    assert task_restored.description == "task_4"
    assert task_restored.status == StatusEnum.IN_PROGRESS
    assert task_restored.priority == PriorityEnum.HIGH
    assert task_restored.created_at == datetime(2025, 11, 20, tzinfo=UTC)
    assert task_restored.deadline == date(2025, 12, 15)
    assert task_restored.completed_at is None
    assert task_restored.tags == ["learning", "feature", "work"]
    assert task_restored.idx == UUID("c91b0ef1-b65f-4885-bb39-9ebb32410720", version=4)


def task_from_json_with_wrong_json() -> None:
    invalid_json: str = "{ invalid-json }"

    with pytest.raises(json.JSONDecodeError):
        Task.from_json(invalid_json)


def test_from_json_with_missing_fields() -> None:
    incomplete_json = json.dumps({"description": "test"})

    with pytest.raises(TypeError, match=r"Invalid Task json structure."):
        Task.from_json(incomplete_json)
