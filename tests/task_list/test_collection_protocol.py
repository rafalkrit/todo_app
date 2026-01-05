from uuid import uuid4

import pytest

from src.task.task import Task
from src.task_list.task_list import TaskList


def test_len_returns_number_of_tasks(task_list: TaskList) -> None:
    assert len(task_list) == 4


def test_iter_returns_tasks_in_order(
    task_list: TaskList, task_1: Task, task_2: Task, task_3: Task, task_4: Task
) -> None:
    it = iter(task_list)

    assert next(it) == task_1
    assert next(it) == task_2
    assert next(it) == task_3
    assert next(it) == task_4

    with pytest.raises(StopIteration):
        next(it)


def test_iter_for_loop(task_list: TaskList, task_1: Task, task_2: Task, task_3: Task, task_4: Task) -> None:
    tasks = [task_1, task_2, task_3, task_4]
    for idx, task in enumerate(task_list):
        assert task == tasks[idx]


def test_contains_returns_true_if_uuid_exists(task_list: TaskList, task_1: Task) -> None:
    assert task_1.idx in task_list


def test_contains_returns_false_if_uuid_not_exists(task_list: TaskList) -> None:
    assert uuid4() not in task_list


def test_getitem_returns_correct_task(
    task_list: TaskList, task_1: Task, task_2: Task, task_3: Task, task_4: Task
) -> None:
    assert task_list[0] == task_1
    assert task_list[-1] == task_4
    assert task_list[-3] == task_2
    assert task_list[2] == task_3


def test_getitem_index_error(task_list: TaskList) -> None:
    with pytest.raises(IndexError):
        task_list[42]
