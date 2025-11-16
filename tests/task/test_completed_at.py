from datetime import UTC, datetime

from src.enums.status_enum import StatusEnum
from src.task.task import Task


def test_completed_at_change_after_sets_status_to_completed(task_1: Task) -> None:
    assert task_1.completed_at is None
    task_1.status = StatusEnum.COMPLETED
    assert task_1.completed_at == datetime(2025, 12, 4, tzinfo=UTC)


def test_completed_at_change_after_sets_status_to_not_completed(task_2: Task) -> None:
    assert task_2.status is StatusEnum.COMPLETED
    assert isinstance(task_2.completed_at, datetime)
    task_2.status = StatusEnum.IN_PROGRESS
    assert task_2.completed_at is None


def test_completed_at_keeps_default_value(task_3: Task) -> None:
    assert task_3.status is StatusEnum.COMPLETED
    assert task_3.completed_at == datetime(2025, 11, 30, tzinfo=UTC)


def test_completed_at_none_uses_current_datetime(task_2: Task) -> None:
    assert task_2.status is StatusEnum.COMPLETED
    assert isinstance(task_2.completed_at, datetime)
    assert task_2.completed_at == datetime(2025, 12, 4, tzinfo=UTC)
