import pytest

from src.schemas.guards.task_list_dict_guard import is_task_list_dict


@pytest.mark.parametrize("value", [1, 1.0, True, None, False, [1, 2, 3], (1, 2, 3), "John"])
def test_is_task_list_dict_returns_false_when_not_dict(value: object) -> None:
    assert is_task_list_dict(value) is False


def test_is_task_list_dict_returns_true_for_valid(task_list_dict: dict[str, object]) -> None:
    assert is_task_list_dict(task_list_dict) is True


def test_is_task_list_dict_returns_true_for_empty_tasks_list() -> None:
    my_tasklist = {"tasks": []}

    assert is_task_list_dict(my_tasklist) is True


def test_is_task_list_dict_returns_false_when_missing_tasks_key(task_list_dict: dict[str, object]) -> None:
    my_tasklist_invalid = {"jobs": [task_list_dict]}

    assert is_task_list_dict(my_tasklist_invalid) is False


def test_is_task_list_dict_returns_false_when_extra_key_present(task_list_dict: dict[str, list]) -> None:
    task_list_dict["extra"] = ["sth"]

    assert is_task_list_dict(task_list_dict) is False


def test_is_task_list_dict_returns_false_when_tasks_is_not_list() -> None:
    my_tasklist = {"tasks": set()}

    assert is_task_list_dict(my_tasklist) is False


def test_is_task_list_dict_returns_false_when_tasks_contains_non_dict(task_list_dict: dict[str, list]) -> None:
    task_list_dict["tasks"].append(1)

    assert is_task_list_dict(task_list_dict) is False


def test_is_task_list_dict_returns_false_when_tasks_contains_invalid_task(task_dict: dict[str, object]) -> None:
    del task_dict["description"]

    assert is_task_list_dict(task_dict) is False


def test_is_task_list_dict_returns_false_when_tasks_mixed_valid_and_invalid(task_list_dict: dict[str, object]) -> None:
    invalid_task = {**task_list_dict, "idx": "fa50210a-5e38-42e3-85c3-15d43c819515", "extra": 42}
    my_tasklist = {"tasks": [task_list_dict, invalid_task]}

    assert is_task_list_dict(my_tasklist) is False


def test_is_task_list_dict_returns_false_when_value_has_non_str_key() -> None:
    my_task_dict = {42: 10}

    assert is_task_list_dict(my_task_dict) is False
