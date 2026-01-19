import pytest

from src.schemas.guards.task_dict_guard import is_task_dict


def test_is_task_dict_returns_true_for_valid_dict_with_deadline_none(task_dict: dict[str, object]) -> None:
    task_dict["deadline"] = None

    assert is_task_dict(task_dict) is True


def test_is_task_dict_returns_true_for_valid_dict_with_deadline_str(task_dict: dict[str, object]) -> None:
    assert is_task_dict(task_dict) is True


def test_is_task_dict_returns_true_for_valid_dict_with_completed_at_none(task_dict: dict[str, object]) -> None:
    assert is_task_dict(task_dict) is True


def test_is_task_dict_returns_true_for_valid_dict_with_completed_at_str(task_dict: dict[str, object]) -> None:
    task_dict["completed_at"] = "2025-12-20T00:00:00+00:00"

    assert is_task_dict(task_dict) is True


@pytest.mark.parametrize("obj", [5, [1, 2, 3], "john"])
def test_is_task_dict_returns_false_when_not_dict(obj: object) -> None:
    assert is_task_dict(obj) is False


def test_is_task_dict_returns_false_when_missing_key(task_dict: dict[str, object]) -> None:
    task_dict.pop("status")

    assert is_task_dict(task_dict) is False


def test_is_task_dict_returns_false_when_extra_key_present(task_dict: dict[str, object]) -> None:
    task_dict["extra"] = 6

    assert is_task_dict(task_dict) is False


def test_is_task_dict_returns_false_when_wrong_type_description(task_dict: dict[str, object]) -> None:
    task_dict["description"] = 5

    assert is_task_dict(task_dict) is False
