import pytest

from src.task.task import Task
from src.task_list.task_list import TaskList


def test_task_list_with_empty_list() -> None:
    task_list = TaskList([])

    assert task_list.tasks == []


def test_task_list_with_none() -> None:
    task_list = TaskList(None)

    assert task_list.tasks == []


def test_task_list_with_tuple(task_1: Task, task_2: Task) -> None:
    task_list = TaskList((task_1, task_2))

    assert task_list.tasks == [task_1, task_2]
    assert len(task_list.tasks) == 2


def test_task_list_duplicate_ids(task_1: Task, task_2: Task) -> None:
    message = f"Duplicate task index detected: {task_1.idx}, {task_2.idx}."

    with pytest.raises(ValueError, match=message):
        TaskList([task_1, task_1, task_2, task_2])
