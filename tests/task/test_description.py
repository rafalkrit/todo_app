import pytest

from src.task.task import Task


def test_description_valid() -> None:
    task_description = "First task."
    task = Task(task_description)
    assert task.description == task_description


def test_too_short_description() -> None:
    with pytest.raises(ValueError, match=r"Description: ad must be between 3 and 120 characters."):
        Task("ad")


def test_too_long_description() -> None:
    with pytest.raises(ValueError, match=r"must be between 3 and 120 characters."):
        Task(description=("test" * 40))
