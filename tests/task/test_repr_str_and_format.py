from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Task


def test_repr(task_4: Task) -> None:
    expected = (
        "Task(description='task_4', "
        f"status={StatusEnum.IN_PROGRESS!r}, "
        f"priority={PriorityEnum.HIGH!r}, "
        "created_at=datetime.datetime(2025, 11, 20, 0, 0, tzinfo=datetime.timezone.utc), "
        "deadline=datetime.date(2025, 12, 15), "
        "completed_at=None, "
        "tags=['learning', 'feature', 'work'])"
    )

    assert repr(task_4) == expected


def test_str(task_4: Task) -> None:
    excepted = "[✗] task_4 | Priority: HIGH | Deadline: 15/12/2025 | Tags: learning, feature, work | Completed: -"
    assert str(task_4) == excepted


def test_str_status_completed(task_4: Task) -> None:
    task_4.status = StatusEnum.COMPLETED
    excepted = (
        "[✓] task_4 | Priority: HIGH | Deadline: 15/12/2025 | Tags: learning, feature, work | Completed: 04/12/2025"
    )
    assert str(task_4) == excepted


def test_str_without_deadline(task_4: Task) -> None:
    task_4.deadline = None
    excepted = "[✗] task_4 | Priority: HIGH | Deadline: - | Tags: learning, feature, work | Completed: -"
    assert str(task_4) == excepted


def test_str_without_tags(task_4: Task) -> None:
    task_4.tags = []
    excepted = "[✗] task_4 | Priority: HIGH | Deadline: 15/12/2025 | Tags: - | Completed: -"
    assert str(task_4) == excepted


def test_format_short(task_4: Task) -> None:
    expected = "[✗] task_4, HIGH, deadline: 15/12/2025"
    assert f"{task_4:short}" == expected
    assert f"{task_4:s}" == expected


def test_format_short_no_deadline(task_4: Task) -> None:
    task_4.deadline = None
    expected = "[✗] task_4, HIGH, deadline: -"
    assert f"{task_4:short}" == expected
    assert f"{task_4:s}" == expected


def test_format_short_status_completed(task_4: Task) -> None:
    task_4.status = StatusEnum.COMPLETED
    expected = "[✓] task_4, HIGH, deadline: 15/12/2025"
    assert f"{task_4:short}" == expected
    assert f"{task_4:s}" == expected


def test_format_long(task_4: Task) -> None:
    task_4.deadline = None
    expected = (
        "Task:\n"
        "  Status: in progress (✗)\n"
        "  Description: task_4\n"
        "  Priority: HIGH\n"
        "  Created At: 20/11/2025\n"
        "  Deadline: -\n"
        "  Completed: -\n"
        "  Tags: learning, feature, work"
    )
    assert f"{task_4:long}" == expected
    assert f"{task_4:l}" == expected


def test_format_long_status_completeed(task_4: Task) -> None:
    task_4.status = StatusEnum.COMPLETED
    expected = (
        "Task:\n"
        "  Status: completed (✓)\n"
        "  Description: task_4\n"
        "  Priority: HIGH\n"
        "  Created At: 20/11/2025\n"
        "  Deadline: 15/12/2025\n"
        "  Completed: 04/12/2025\n"
        "  Tags: learning, feature, work"
    )
    assert f"{task_4:long}" == expected
    assert f"{task_4:l}" == expected


def test_format_fallback_to_str(task_4: Task) -> None:
    assert f"{task_4:unknown}" == str(task_4)
    assert f"{task_4:}" == str(task_4)
