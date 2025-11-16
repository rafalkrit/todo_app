from collections.abc import Iterable
from datetime import UTC, date, datetime
import re
from uuid import UUID, uuid4

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum


class Task:
    def __init__(
        self,
        description: str,
        status: StatusEnum = StatusEnum.TODO,
        priority: PriorityEnum = PriorityEnum.MEDIUM,
        created_at: datetime | None = None,
        deadline: date | None = None,
        completed_at: datetime | None = None,
        tags: Iterable[str] | None = None,
        idx: UUID | str | None = None,
    ) -> None:
        self.description: str = description
        self.status: StatusEnum = status
        self.priority: PriorityEnum = priority
        self.created_at: datetime = created_at if created_at is not None else datetime.now(UTC)
        self.deadline: date | None = deadline
        self.completed_at: datetime | None = completed_at
        self.tags: list[str] = tags
        self.idx: UUID = idx

        if self.status is StatusEnum.COMPLETED and self.completed_at is None:
            self.completed_at = datetime.now(UTC)

    @property
    def description(self) -> str:
        """str: A short textual summary of the task.

        Returns the current description of the task. The description
        should clearly communicate the purpose or content of the task.
        """
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Sets the task description.

        Validates the provided description to ensure it meets the
        required length constraints. A valid description must contain
        between 3 and 120 characters after trimming whitespace.
        If the value does not satisfy these constraints, a ValueError
        is raised.

        Args:
            value (str): The new description to assign to the task.

        Raises:
            ValueError: If the description is shorter than 3 characters
                or longer than 120 characters.
        """
        if not (3 <= len(value) <= 120):
            raise ValueError(f"Description: {value} must be between 3 and 120 characters.")
        self._description = value

    @property
    def deadline(self) -> date | None:
        """date | None: The date by which the task is expected to be completed.

        Returns the current deadline assigned to the task. If no deadline
        has been set, returns ``None``.
        """
        return self._deadline

    @deadline.setter
    def deadline(self, value: date | None) -> None:
        """Sets the task's deadline.

        Validates that the provided deadline is not earlier than the task's
        creation date. If the value is ``None``, the deadline is cleared.
        Otherwise, the deadline must represent a future or same-day date
        relative to the task's creation timestamp. A ValueError is raised if
        the validation fails.

        Args:
            value (date | None): The new deadline to assign to the task. Use
                ``None`` to indicate that no deadline is set.

        Raises:
            ValueError: If the provided deadline is earlier than the task's
                creation date.
        """
        if value is None:
            self._deadline = value
        elif value < self.created_at.date():
            raise ValueError(f"Deadline: {value} must be from the future.")
        self._deadline = value

    @property
    def tags(self) -> list[str]:
        return self._tags

    @tags.setter
    def tags(self, value: Iterable[str] | None) -> None:
        if value is None:
            self._tags: list[str] = []
        else:
            self._tags: list[str] = self._unique_values([self._normalize(tag) for tag in value])

    @property
    def status(self) -> StatusEnum:
        return self._status

    @status.setter
    def status(self, value: StatusEnum) -> None:
        old_status = getattr(self, "status", None)

        if old_status is value:
            return

        self._status = value

        if (
            old_status is not StatusEnum.COMPLETED
            and value is StatusEnum.COMPLETED
            and getattr(self, "completed_at", None) is None
        ):
            self.completed_at = datetime.now(UTC)
        elif old_status is StatusEnum.COMPLETED and value is not StatusEnum.COMPLETED:
            self.completed_at = None

    @property
    def idx(self) -> UUID:
        return self._idx

    @idx.setter
    def idx(self, value: UUID | str | None) -> None:
        if value is None:
            self._idx = uuid4()
        elif isinstance(value, str):
            self._idx = UUID(value, version=4)
        else:
            self._idx = value

    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r"\s{2,}", " ", text).strip().lower()

    @staticmethod
    def _unique_values(values: Iterable[str]) -> list[str]:
        seen: set[str] = set()
        out: list[str] = []

        for value in values:
            if value not in seen:
                seen.add(value)
                out.append(value)
        return out
