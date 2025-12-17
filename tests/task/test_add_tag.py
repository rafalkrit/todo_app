from src.task.task import Task


def test_add_tag_new() -> None:
    task = Task(description="siema", tags=[])
    task.add_tag("python")

    assert task.tags == ["python"]


def test_add_tag_no_duplicate() -> None:
    task = Task(description="siema", tags=["python"])
    task.add_tag("python")

    assert task.tags == ["python"]


def test_add_tag_normalize() -> None:
    task = Task(description="siema", tags=[])
    task.add_tag("  python")

    assert task.tags == ["python"]
