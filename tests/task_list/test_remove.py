from uuid import uuid4

import pytest

from src.task.task import Task
from src.task_list.task_list import TaskList


def test_remove_task(task_1: Task) -> None:
    my_tasks = TaskList([task_1])
    my_tasks.remove(task_1.idx)

    assert len(my_tasks.tasks) == 0


def test_remove_task_idx_not_in_tasks(task_1: Task) -> None:
    idx = uuid4()

    with pytest.raises(ValueError, match=f"Task with {idx} does not exist"):
        TaskList([task_1]).remove(idx)
