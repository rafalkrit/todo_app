from collections.abc import Iterable
from datetime import UTC, date, datetime
import json
import re
from typing import Any, Literal
from uuid import UUID, uuid4

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.schemas.guards.task_dict_guard import is_task_dict
from src.schemas.tasks_schema import TaskDict


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

        if self.status is not StatusEnum.COMPLETED:
            self.completed_at = None

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
        """list[str]: A list of normalized, unique tags assigned to the task.

        Returns the list of tags currently associated with the task.
        All tags are stored in lowercase, trimmed of excess whitespace,
        and duplicates are removed.
        """
        return self._tags

    @tags.setter
    def tags(self, value: Iterable[str] | None) -> None:
        """Sets the list of tags for the task.

        Normalizes each tag (lowercases, trims whitespace, removes
        repeated spaces) and ensures all tags are unique. If ``None`` is
        provided, an empty list is assigned.

        Args:
            value (Iterable[str] | None): A collection of tag strings or
                ``None`` to clear all tags.
        """
        if value is None:
            self._tags: list[str] = []
        else:
            self._tags: list[str] = self._unique_values([self._normalize(tag) for tag in value])

    @property
    def status(self) -> StatusEnum:
        """StatusEnum: The current workflow state of the task.
        Returns the task's status, such as TODO, IN_PROGRESS,
        or COMPLETED.
        """
        return self._status

    @status.setter
    def status(self, value: StatusEnum) -> None:
        """Sets the task's status.
        If the status transitions to ``COMPLETED`` and no completion time
        has been set, the current UTC timestamp is assigned automatically.
        If the status transitions away from ``COMPLETED``, the completion
        timestamp is cleared.

        Args:
            value (StatusEnum): The new status to assign.
        """
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
        """UUID: A unique identifier for the task.

        Returns the UUID associated with this task instance.
        """
        return self._idx

    @idx.setter
    def idx(self, value: UUID | str | None) -> None:
        """Sets the unique identifier of the task.

        If ``None`` is provided, a new random UUIDv4 is generated.
        If a string is provided, it is interpreted as a UUIDv4 value.

        Args:
            value (UUID | str | None): The UUID to assign, a string
                representation of a UUID, or ``None`` to auto-generate one.

        Raises:
            ValueError: If the provided string is not a valid UUIDv4.
        """
        if value is None:
            self._idx = uuid4()
        elif isinstance(value, str):
            self._idx = UUID(value, version=4)
        else:
            self._idx = value

    @staticmethod
    def _normalize(text: str) -> str:
        """Normalizes a text value.

        Replaces multiple consecutive whitespace characters with a
        single space, trims leading/trailing whitespace, and converts
        the text to lowercase.

        Args:
            text (str): The text to normalize.

        Returns:
            str: A cleaned, standardized representation of the string.
        """
        return re.sub(r"\s{2,}", " ", text).strip().lower()

    @staticmethod
    def _unique_values(values: Iterable[str]) -> list[str]:
        """Returns unique values from an iterable while preserving order.

        Iterates through the provided values and builds a list containing
        only the first occurrence of each distinct value.

        Args:
            values (Iterable[str]): The collection of strings to deduplicate.

        Returns:
            list[str]: A list containing unique items in their original order.
        """
        seen: set[str] = set()
        out: list[str] = []

        for value in values:
            if value not in seen:
                seen.add(value)
                out.append(value)
        return out

    def add_tag(self, value: str) -> None:
        """Adds a tag to the task.

        Normalizes the provided tag value and appends it to the task's tag list
        if it is not already present.

        Args:
            value (str): The tag to add.

        Returns:
            None
        """
        tag = self._normalize(value)
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, value: str) -> None:
        """Removes a tag from the task.

        Normalizes the provided tag value and removes it from the task's tag list
        if it exists.

        Args:
            value (str): The tag to remove.

        Returns:
            None
        """
        tag = self._normalize(value)
        if tag in self.tags:
            self.tags.remove(tag)

    def clone(self) -> "Task":
        """Creates a copy of the task with updated timestamps.

        Produces a new Task instance based on the current one. The cloned task
        receives a new creation timestamp. Deadline and completion date are
        preserved only if they are not in the past relative to the new creation
        time.

        Returns:
            Task: A new task instance cloned from the original.
        """
        created_at: datetime = datetime.now(UTC)
        status: StatusEnum = StatusEnum.TODO if self.status is StatusEnum.COMPLETED else self.status
        deadline: date | None = None if self.deadline and self.deadline < created_at.date() else self.deadline
        return Task(
            description=self.description,
            status=status,
            priority=self.priority,
            created_at=created_at,
            deadline=deadline,
            completed_at=None,
            tags=list(self.tags),
        )

    def to_dict(self) -> TaskDict:
        return {
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "created_at": self.created_at.isoformat(),
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "tags": self.tags,
            "idx": str(self.idx),
        }

    @classmethod
    def from_dict(cls, data: TaskDict) -> "Task":
        return cls(
            description=data["description"],
            status=StatusEnum(data["status"]),
            priority=PriorityEnum(data["priority"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            deadline=date.fromisoformat(data["deadline"]) if data["deadline"] else None,
            completed_at=datetime.fromisoformat(data["completed_at"]) if data["completed_at"] else None,
            tags=data["tags"],
            idx=data["idx"],
        )

    def to_json(self, *, indent: int | None = None) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    @classmethod
    def from_json(cls, raw: str) -> "Task":
        payload: Any = json.loads(raw)

        if not is_task_dict(payload):
            raise TypeError("Invalid Task json structure.")

        return cls.from_dict(payload)

    def __repr__(self) -> str:
        """Returns an unambiguous string representation of the task.

        The returned string contains all core task attributes and is
        intended for debugging and logging purposes.

        Returns:
            str: A detailed string representing the task object.
        """
        return (
            f"{type(self).__name__}(description={self.description!r}, status={self.status!r}, "
            f"priority={self.priority!r}, created_at={self.created_at!r}, deadline={self.deadline!r}, "
            f"completed_at={self.completed_at!r}, tags={self.tags!r})"
        )

    def __str__(self) -> str:
        """Returns a human-readable representation of the task.

        Produces a compact summary including status, description, priority,
        deadline, completion date, and tags.

        Returns:
            str: A concise, user-friendly description of the task.
        """
        status: Literal["✓", "✗"] = "✓" if self.status == StatusEnum.COMPLETED else "✗"
        deadline: str = self.deadline.strftime("%d/%m/%Y") if self.deadline else "-"
        completed: str = self.completed_at.strftime("%d/%m/%Y") if self.completed_at else "-"
        tags: str = ", ".join(self.tags) if self.tags else "-"

        return (
            f"[{status}] {self.description} | "
            f"Priority: {self.priority.name} | "
            f"Deadline: {deadline} | "
            f"Tags: {tags} | "
            f"Completed: {completed}"
        )

    def __format__(self, format_spec: str) -> str:
        """Formats the task according to the given specification.

        Supported formats:
            - ``'short'`` or ``'s'``: A compact summary.
            - ``'long'`` or ``'l'``: A verbose, multi-line description.
            - Default: Same as ``str(self)``.

        Args:
            format_spec (str): The format instruction.

        Returns:
            str: The formatted string representation of the task.
        """
        format_spec: str = (format_spec or "str").lower().strip()
        status: Literal["✓", "✗"] = "✓" if self.status == StatusEnum.COMPLETED else "✗"
        tags: str = ", ".join(self.tags) if self.tags else "-"
        deadline: str = self.deadline.strftime("%d/%m/%Y") if self.deadline else "-"
        completed: str = self.completed_at.strftime("%d/%m/%Y") if self.completed_at else "-"
        created: str = self.created_at.strftime("%d/%m/%Y")

        if format_spec in {"short", "s"}:
            return f"[{status}] {self.description}, {self.priority.name}, deadline: {deadline}"

        if format_spec in {"long", "l"}:
            return (
                f"Task:\n"
                f"  Status: {self.status} ({status})\n"
                f"  Description: {self.description}\n"
                f"  Priority: {self.priority.name}\n"
                f"  Created At: {created}\n"
                f"  Deadline: {deadline}\n"
                f"  Completed: {completed}\n"
                f"  Tags: {tags}"
            )
        return str(self)
