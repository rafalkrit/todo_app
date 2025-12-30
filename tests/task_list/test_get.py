from uuid import uuid4

import pytest

from src.task.task import Task
from src.task_list.task_list import TaskList


def test_get_task_with_id(task_1: Task, task_3: Task) -> None:
    my_list = TaskList([task_1, task_3])
    task = my_list.get(task_1.idx)

    assert task is task_1


def test_get_idx_not_in_tasks(task_1: Task, task_2: Task) -> None:
    idx = uuid4()

    with pytest.raises(ValueError, match=f"Task with {idx} does not exist"):
        TaskList([task_2, task_1]).get(idx)
