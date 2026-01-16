from src.task.task import Task
from src.task_list.task_list import TaskList


def test_sort_by_priority_ascending(task_1: Task, task_3: Task, task_4: Task) -> None:
    tasks = TaskList([task_1, task_4, task_3])

    result = tasks.sort_by(key=lambda task: task.priority)

    assert result[0] == task_1
    assert result[1] == task_3
    assert result[2] == task_4


def test_sort_by_priority_descending(task_1: Task, task_3: Task, task_4: Task) -> None:
    tasks = TaskList([task_3, task_4, task_1])

    result = tasks.sort_by(key=lambda task: task.priority, reverse=True)

    assert result[0] == task_4
    assert result[1] == task_3
    assert result[2] == task_1


def test_sort_by_deadline_none_last(task_5: Task, task_3: Task, task_4: Task) -> None:
    tasks = TaskList([task_5, task_3, task_4])

    result = tasks.sort_by(key=lambda task: (task.deadline is None, task.deadline))

    assert result[0] == task_4  # (False, (2025, 12, 15))
    assert result[1] == task_5  # (False, (2026, 1, 10))
    assert result[2] == task_3  # (True, None)


def test_sort_by_stable() -> None:
    t1 = Task("python")
    t2 = Task("java")

    tasks = TaskList([t1, t2])

    result = tasks.sort_by(key=lambda task: task.priority)

    assert result[0] == t1
    assert result[1] == t2


def test_sort_by_does_not_mutate_original(task_5: Task, task_4: Task) -> None:
    tasks = [task_5, task_4]
    my_tasks = TaskList(tasks)

    result = my_tasks.sort_by(key=lambda task: task.priority)

    assert result[0] == task_5
    assert result[1] == task_4
    assert my_tasks.tasks == tasks
