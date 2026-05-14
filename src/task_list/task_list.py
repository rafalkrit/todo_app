from collections import Counter
from collections.abc import Callable, Iterable, Iterator
from datetime import date
import json
from operator import attrgetter
from typing import Any
from uuid import UUID

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.schemas.guards.task_list_dict_guard import is_task_list_dict
from src.schemas.task_list_schema import TaskListDict
from src.task.task import Task


class TaskList:
    """Manage an ordered collection of unique tasks.

    The collection enforces unique task identifiers and provides domain-level
    operations for adding, removing, retrieving, filtering, sorting, iterating,
    and serializing tasks.
    """

    def __init__(self, tasks: Iterable[Task] | None = None) -> None:
        """Create a task collection.

        Args:
            tasks: Optional iterable of tasks used to initialize the collection.

        Raises:
            ValueError: If duplicate task identifiers are provided.
        """
        self.tasks = tasks

    @property
    def tasks(self) -> list[Task]:
        """Return the mutable list of tasks held by the collection."""
        return self._tasks

    @tasks.setter
    def tasks(self, value: Iterable[Task] | None = None) -> None:
        """Set collection items while enforcing unique task identifiers.

        Args:
            value: Optional iterable of tasks. None creates an empty collection.

        Raises:
            ValueError: If duplicate task identifiers are detected.
        """

        if value is None:
            self._tasks: list[Task] = []
        else:
            items: list[Task] = list(value)
            self._unique_ids(items)
            self._tasks: list[Task] = items

    @staticmethod
    def _unique_ids(tasks: Iterable[Task]) -> None:
        """Validate that all provided tasks have unique identifiers.

        Args:
            tasks: Tasks to validate.

        Raises:
            ValueError: If any task identifier appears more than once.
        """
        ids: list[str] = [str(task.idx) for task in tasks]
        counter = Counter(ids)
        duplicates: list[str] = [idx for idx, count in counter.items() if count > 1]
        if duplicates:
            raise ValueError(f"Duplicate task index detected: {', '.join(duplicates)}.")

    def add(self, task: Task) -> None:
        """Add a task to the collection.

        Args:
            task: Task to append.

        Raises:
            ValueError: If the task identifier already exists in the collection.
        """
        self._unique_ids([*self._tasks, task])
        self._tasks.append(task)

    def remove(self, idx: UUID) -> None:
        """Remove a task by identifier.

        Args:
            idx: Identifier of the task to remove.

        Raises:
            ValueError: If no task with the given identifier exists.
        """
        for task in self._tasks:
            if task.idx == idx:
                self._tasks.remove(task)
                return

        raise ValueError(f"Task with {idx} does not exist")

    def get(self, idx: UUID) -> Task:
        """Return a task by identifier.

        Args:
            idx: Identifier of the task to retrieve.

        Returns:
            Task: Matching task.

        Raises:
            ValueError: If no task with the given identifier exists.
        """
        for task in self._tasks:
            if task.idx == idx:
                return task

        raise ValueError(f"Task with {idx} does not exist")

    def filter_by(
        self,
        status: StatusEnum | None = None,
        priority: PriorityEnum | None = None,
        tag: str | None = None,
        deadline_before: date | None = None,
        deadline_after: date | None = None,
        custom_filter: Callable[[Task], bool] | None = None,
    ) -> "TaskList":
        """Return tasks matching the provided filter criteria.

        Args:
            status: Optional status filter.
            priority: Optional priority filter.
            tag: Optional tag filter.
            deadline_before: Optional upper deadline bound.
            deadline_after: Optional lower deadline bound.
            custom_filter: Optional predicate applied to each task.

        Returns:
            TaskList: New collection containing only matching tasks.
        """

        def matches(task: Task) -> bool:
            """Return whether a task satisfies all active filters."""

            priority_ok = priority is None or task.priority is priority
            status_ok = status is None or task.status is status
            tag_ok = tag is None or tag in task.tags

            deadline_before_ok = deadline_before is None or (
                task.deadline is not None and task.deadline < deadline_before
            )
            deadline_after_ok = deadline_after is None or (task.deadline is not None and task.deadline > deadline_after)
            custom_filter_ok = custom_filter is None or custom_filter(task)

            return all((priority_ok, status_ok, tag_ok, deadline_before_ok, deadline_after_ok, custom_filter_ok))

        return TaskList([task for task in self._tasks if matches(task)])

    def sort_by(self, *, key: Callable[[Task], Any] | None = None, reverse: bool = False) -> "TaskList":
        """Return a sorted copy of the collection.

        Args:
            key: Optional key function. Defaults to sorting by priority.
            reverse: Whether to return descending order.

        Returns:
            TaskList: New collection with sorted tasks.
        """
        key_func: Callable[[Task], Any] = key or attrgetter("priority")
        return TaskList(sorted(self.tasks, key=key_func, reverse=reverse))

    def __repr__(self) -> str:
        """Return an unambiguous representation useful for debugging."""
        return f"{type(self).__name__}(tasks={self.tasks!r})"

    def __str__(self) -> str:
        """Return a compact human-readable collection summary."""
        if not self.tasks:
            return "TaskList (empty)"

        return f"TaskList ({len(self.tasks)} tasks)"

    def __format__(self, format_spec: str) -> str:
        """Format the collection as short, long, or default text.

        Args:
            format_spec: Format selector. Supports "short"/"s" and "long"/"l".

        Returns:
            str: Formatted collection representation.
        """
        format_spec: str = (format_spec or "str").lower().strip()

        if format_spec in {"short", "s"}:
            return f"TaskList ({len(self.tasks)} tasks)"

        if format_spec in {"long", "l"}:
            if not self.tasks:
                return "TaskList (empty)"

            tasks_str: str = "\n".join(f"- {format(task, 'long')}" for task in self.tasks)
            return f"TaskList:\n{tasks_str}"

        return str(self)

    def to_dict(self) -> TaskListDict:
        """Serialize the collection to a storage-ready dictionary.

        Returns:
            TaskListDict: Dictionary containing serialized tasks.
        """
        return {"tasks": [task.to_dict() for task in self]}

    @classmethod
    def from_dict(cls, data: TaskListDict) -> "TaskList":
        """Create a collection from its dictionary representation.

        Args:
            data: Serialized task-list data matching the TaskListDict contract.

        Returns:
            TaskList: Rehydrated task collection.
        """
        return cls([Task.from_dict(task) for task in data["tasks"]])

    def to_json(self, *, indent: int | None = None) -> str:
        """Serialize the collection to a JSON string.

        Args:
            indent: Optional indentation level passed to json.dumps.

        Returns:
            str: JSON representation of the collection.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    @classmethod
    def from_json(cls, raw: str) -> "TaskList":
        """Create a collection from a JSON string.

        The payload is validated with the runtime TaskListDict guard before the
        domain collection is constructed.

        Args:
            raw: JSON string containing a serialized task collection.

        Returns:
            TaskList: Rehydrated task collection.

        Raises:
            TypeError: If the JSON payload does not match TaskListDict.
            json.JSONDecodeError: If the input is not valid JSON.
        """
        payload: Any = json.loads(raw)

        if not is_task_list_dict(payload):
            raise TypeError("Invalid TaskList json structure.")

        return cls.from_dict(payload)

    def __len__(self) -> int:
        """Return the number of tasks in the collection."""
        return len(self.tasks)

    def __iter__(self) -> Iterator[Task]:
        """Iterate over tasks in insertion order."""
        return iter(self.tasks)

    def __contains__(self, idx: UUID) -> bool:
        """Return whether a task identifier exists in the collection."""
        return any(task.idx == idx for task in self.tasks)

    def __getitem__(self, index: int) -> Task:
        """Return the task at a zero-based list index."""
        return self.tasks[index]
