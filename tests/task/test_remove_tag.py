from src.task.task import Task


def test_remove_tag(task_4: Task) -> None:
    task_4.remove_tag("work")

    assert task_4.tags == ["learning", "feature"]


def test_remove_tag_normalize(task_4: Task) -> None:
    task_4.remove_tag("  Workk")

    assert task_4.tags == ["learning", "feature", "work"]
