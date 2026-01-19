import json

import pytest

from src.task_list.task_list import TaskList


def test_to_json_returns_string(task_list: TaskList) -> None:
    raw = task_list.to_json()

    parsed = json.loads(raw)

    assert set(parsed.keys()) == {"tasks"}
    assert isinstance(parsed["tasks"], list)


def test_to_json_with_indent(task_list: TaskList) -> None:
    raw = task_list.to_json(indent=2)

    parsed = json.loads(raw)

    assert isinstance(raw, str)
    assert "\n" in raw
    assert "  " in raw
    assert len(parsed["tasks"]) == 4


def test_from_json_returns_task_list(task_list: TaskList) -> None:
    data = task_list.to_dict()
    raw = json.dumps(data)

    task_restored = TaskList.from_json(raw)

    assert isinstance(task_restored, TaskList)


def test_from_json_with_wrong_json() -> None:
    invalid_json: str = "{ invalid-json }"

    with pytest.raises(json.JSONDecodeError):
        TaskList.from_json(invalid_json)


def test_tasklist_from_json_invalid_structure() -> None:
    raw = json.dumps({"tasks": "test"})

    with pytest.raises(TypeError, match=r"Invalid TaskList json structure."):
        TaskList.from_json(raw)
