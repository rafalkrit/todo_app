from src.task.task import Task


def test_to_dict_minimum_in_task(task_1: Task) -> None:
    result = task_1.to_dict()

    assert result["description"] == "task_1"
    assert result["status"] == "todo"
    assert result["deadline"] is None
    assert result["completed_at"] is None


def test_to_dict_full(task_4: Task) -> None:
    result = task_4.to_dict()

    assert result["description"] == "task_4"
    assert result["status"] == "in progress"
    assert result["priority"] == 3
    assert result["created_at"] == "2025-11-20T00:00:00+00:00"
    assert result["deadline"] == "2025-12-15"
    assert result["completed_at"] is None
    assert result["tags"] == ["learning", "feature", "work"]
    assert result["idx"] == str(task_4.idx)
