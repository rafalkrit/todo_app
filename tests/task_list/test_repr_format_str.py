from src.task.task import Task
from src.task_list.task_list import TaskList


def test_repr(task_1: Task, task_2: Task) -> None:
    tasks = TaskList([task_1, task_2])

    result = repr(tasks)

    assert result == f"TaskList(tasks={[task_1, task_2]!r})"


def test_repr_empty() -> None:
    tasks = TaskList()

    assert repr(tasks) == "TaskList(tasks=[])"


def test_str_empty() -> None:
    tasks = TaskList()

    assert str(tasks) == "TaskList (empty)"


def test_str_not_empty(task_1: Task, task_2: Task) -> None:
    tasks = TaskList([task_1, task_2])

    assert str(tasks) == "TaskList (2 tasks)"


def test_tasklist_format_short(task_list: TaskList) -> None:
    result = format(task_list, "s")

    assert result == "TaskList (4 tasks)"


def test_tasklist_format_long_empty() -> None:
    task_list = TaskList()

    result = format(task_list, "long")

    assert result == "TaskList (empty)"


def test_tasklist_format_long_two_tasks(task_1: Task, task_2: Task) -> None:
    task_list = TaskList([task_1, task_2])

    result = format(task_list, "long")

    assert result.startswith("TaskList:")
    assert "task_1" in result
    assert "task_2" in result


def test_tasklist_format_empty_string_calls_str(task_list: TaskList) -> None:
    assert format(task_list, "") == str(task_list)
