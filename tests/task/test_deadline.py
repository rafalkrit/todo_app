from datetime import UTC, date, datetime, timedelta

import pytest

from src.task.task import Task


def test_deadline_none() -> None:
    task = Task(description="test", deadline=None)
    assert task.deadline is None


def test_deadline_invalid() -> None:
    with pytest.raises(ValueError, match=r"Deadline: .* must be from the future."):
        Task(description="Test", deadline=date(2025, 11, 1))


def test_deadline_valid() -> None:
    deadline = datetime.now(UTC).date() + timedelta(days=5)
    task = Task(description="task", deadline=deadline)

    assert task.deadline == deadline
