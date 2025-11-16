from src.enums.status_enum import StatusEnum
from src.task.task import Task


def test_status_no_changes(task_2: Task) -> None:
    old = task_2.completed_at
    task_2.status = StatusEnum.COMPLETED
    assert task_2.completed_at == old


def test_status_changes_to_completed(task_1: Task) -> None:
    assert task_1.completed_at is None
    task_1.status = StatusEnum.COMPLETED
    assert task_1.completed_at is not None
    assert task_1.status == StatusEnum.COMPLETED


def test_status_changes_status(task_2: Task) -> None:
    assert task_2.completed_at is not None
    task_2.status = StatusEnum.TODO
    assert task_2.completed_at is None
    assert task_2.status == StatusEnum.TODO
