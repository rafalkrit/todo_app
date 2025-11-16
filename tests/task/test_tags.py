from src.task.task import Task


def test_tags_with_default() -> None:
    task = Task("Test")
    assert task.tags == []


def test_tags_with_tags_list() -> None:
    task = Task("Write test", tags=["a\t\tB", "a\n\nB", "  foo  ", "Foo   Bar", "single space"])
    assert task.tags == ["a b", "foo", "foo bar", "single space"]
