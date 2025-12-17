from datetime import date

from src.enums.status_enum import StatusEnum
from src.task.task import Task


def test_clone_completed_task(task_2: Task) -> None:
    clone = task_2.clone()

    assert clone.status is StatusEnum.TODO
    assert clone.completed_at is None


def test_clone_sets_new_created_at(task_4: Task) -> None:
    clone = task_4.clone()

    assert clone.created_at > task_4.created_at


def test_clone_description(task_4: Task) -> None:
    clone = task_4.clone()

    assert clone.description == task_4.description


def test_clone_preserves_future_deadline(task_4: Task) -> None:
    clone = task_4.clone()

    assert clone.deadline == date(2025, 12, 15)


def test_clone_copies_tags_not_reference(task_4: Task) -> None:
    clone = task_4.clone()

    assert clone.tags == task_4.tags
    assert clone.tags is not task_4.tags


def test_clone_tags_are_independent(task_4: Task) -> None:
    clone = task_4.clone()

    clone.add_tag("new-tag")

    assert "new-tag" not in task_4.tags
