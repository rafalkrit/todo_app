from src.task.task import Task
from src.task_list.task_list import TaskList


def test_to_dict_empty() -> None:
    task_list = TaskList([])
    result = task_list.to_dict()
    assert result == {"tasks": []}


def test_to_dict_multiple_tasks(task_1: Task, task_2: Task, task_3: Task, task_4: Task) -> None:
    tasks = TaskList([task_1, task_2, task_3, task_4])
    expected = {"tasks": [task_1.to_dict(), task_2.to_dict(), task_3.to_dict(), task_4.to_dict()]}
    assert tasks.to_dict() == expected
