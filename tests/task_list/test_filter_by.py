from datetime import date

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Task
from src.task_list.task_list import TaskList


def test_filter_by_no_filters(task_1: Task, task_2: Task) -> None:
    task_list = TaskList([task_1, task_2])
    filtr = task_list.filter_by()

    assert len(filtr.tasks) == 2


def test_filter_by_priority_none(task_2: Task, task_3: Task) -> None:
    task_list = TaskList([task_2, task_3])
    result = task_list.filter_by(priority=PriorityEnum.LOW)
    assert len(result.tasks) == 0


def test_filter_by_priority_high(task_list: TaskList) -> None:
    result = task_list.filter_by(priority=PriorityEnum.HIGH)
    assert len(result.tasks) == 1
    assert result.tasks[0].description == "task_4"


def test_filter_by_status_completed(task_list: TaskList) -> None:
    result = task_list.filter_by(status=StatusEnum.COMPLETED)
    assert len(result.tasks) == 2


def test_filter_by_tag_none(task_1: Task, task_2: Task, task_3: Task) -> None:
    task_list = TaskList([task_1, task_2, task_3])
    result = task_list.filter_by(tag="js")
    assert len(result.tasks) == 0


def test_filter_by_tag_match(task_list: TaskList) -> None:
    result = task_list.filter_by(tag="work")
    assert len(result.tasks) == 1
    assert result.tasks[0].description == "task_4"


def test_filter_by_deadline_before_none(task_list: TaskList) -> None:
    result = task_list.filter_by(deadline_before=date(2020, 12, 10))
    assert len(result.tasks) == 0


def test_filter_by_deadline_before_ignores_none_deadlines(task_list: TaskList) -> None:
    result = task_list.filter_by(deadline_before=date(2025, 12, 1))
    assert result.tasks == []


def test_filter_by_deadline_before_match(task_list: TaskList) -> None:
    result = task_list.filter_by(deadline_before=date(2025, 12, 20))
    assert len(result.tasks) == 1
    assert result.tasks[0].description == "task_4"


def test_filter_by_deadline_after_none(task_list: TaskList) -> None:
    result = task_list.filter_by(deadline_after=date(2030, 4, 10))
    assert len(result.tasks) == 0


def test_filter_by_deadline_after_match(task_list: TaskList) -> None:
    result = task_list.filter_by(deadline_after=date(2025, 12, 10))
    assert len(result.tasks) == 1
    assert result.tasks[0].description == "task_4"


def test_filter_by_custom_filter_none(task_list: TaskList) -> None:
    result = task_list.filter_by(custom_filter=lambda task: len(task.tags) > 10)
    assert len(result.tasks) == 0


def test_filter_by_custom_filter(task_list: TaskList, task_1: Task, task_2: Task, task_3: Task) -> None:
    result = task_list.filter_by(custom_filter=lambda task: len(task.tags) == 0 and task.deadline is None)
    assert len(result.tasks) == 3
    assert result.tasks == [task_1, task_2, task_3]
