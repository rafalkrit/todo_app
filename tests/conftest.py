from datetime import UTC, date, datetime, timezone

from _pytest.monkeypatch import MonkeyPatch
import pytest

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
import src.task.task as task_module
from src.task.task import Task
from src.task_list.task_list import TaskList


class _FixedDatetime(datetime):
    """A datetime subclass that always returns a fixed timestamp.

    This class overrides :func:`datetime.now` to return a constant
    datetime value, which is useful for deterministic tests that rely
    on time-dependent logic.

    Attributes:
        _fixed_now (datetime): The fixed datetime value returned
            by :func:`now`.

    Example:
        >>> _FixedDatetime.now()
        datetime.datetime(2025, 12, 4, 0, 0, tzinfo=UTC)

    """

    _fixed_now = datetime(2025, 12, 4, tzinfo=UTC)

    @classmethod
    def now(cls, tz: timezone | None = None) -> datetime:
        """Return the fixed datetime instance.

        Args:
            tz (timezone | None): Optional timezone. If provided,
                the returned datetime will be converted to this timezone.

        Returns:
            datetime: The fixed datetime value, optionally converted
            to the given timezone.

        """
        return cls._fixed_now if tz is None else cls._fixed_now.astimezone(tz)


@pytest.fixture(autouse=True)
def _freeze_datetime(monkeypatch: MonkeyPatch) -> None:
    """Pytest fixture that freezes the datetime inside the test module.

    This fixture automatically replaces the `datetime` class in
    `task_module` with :class:`_FixedDatetime`, ensuring that
    any calls to :func:`datetime.now` inside the module return a
    deterministic value.

    Args:
        monkeypatch (MonkeyPatch): Pytest helper to dynamically
            replace object attributes during tests.

    """
    monkeypatch.setattr(task_module, "datetime", _FixedDatetime)


@pytest.fixture
def task_1() -> Task:
    return Task(
        description="task_1",
        status=StatusEnum.TODO,
    )


@pytest.fixture
def task_2() -> Task:
    return Task(
        description="task_2",
        status=StatusEnum.COMPLETED,
    )


@pytest.fixture
def task_3() -> Task:
    return Task(description="task_3", status=StatusEnum.COMPLETED, completed_at=datetime(2025, 11, 30, tzinfo=UTC))


@pytest.fixture
def task_4() -> Task:
    return Task(
        description="task_4",
        status=StatusEnum.IN_PROGRESS,
        priority=PriorityEnum.HIGH,
        created_at=datetime(2025, 11, 20, tzinfo=UTC),
        deadline=date(2025, 12, 15),
        completed_at=datetime(2025, 11, 30, tzinfo=UTC),
        tags=["learning", "feature", "work"],
    )


@pytest.fixture
def task_5() -> Task:
    return Task(description="task_2", status=StatusEnum.COMPLETED, deadline=date(2026, 1, 10))


@pytest.fixture
def task_list(task_1: Task, task_2: Task, task_3: Task, task_4: Task) -> TaskList:
    return TaskList([task_1, task_2, task_3, task_4])
