from src.task.task import Task
from src.task_list.task_list import TaskList


def test_repr(task_1: Task, task_2: Task) -> None:
    tasks = TaskList([task_1, task_2])

    result = repr(tasks)

    assert result == f"TaskList(tasks={[task_1, task_2]!r})"


def test_repr_empty() -> None:
    tasks = TaskList()

    assert repr(tasks) == "TaskList(tasks=[])"
