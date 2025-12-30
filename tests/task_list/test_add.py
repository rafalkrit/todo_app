import pytest

from src.task.task import Task
from src.task_list.task_list import TaskList


def test_add_task(task_1: Task) -> None:
    tasks = TaskList()
    tasks.add(task_1)
    assert len(tasks._tasks) == 1
    assert tasks._tasks[0] == task_1


def test_add_with_error(task_1: Task, task_2: Task) -> None:
    message = f"Duplicate task index detected: {task_1.idx}, {task_2.idx}."

    with pytest.raises(ValueError, match=message):
        TaskList([task_1, task_1, task_2, task_2])
