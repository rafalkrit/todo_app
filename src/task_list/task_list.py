from collections import Counter
from collections.abc import Callable, Iterable, Iterator
from datetime import date
from operator import attrgetter
from typing import Any
from uuid import UUID

from src.enums.priority_enum import PriorityEnum
from src.enums.status_enum import StatusEnum
from src.task.task import Task


class TaskList:
    def __init__(self, tasks: Iterable[Task] | None = None) -> None:
        self.tasks: list[Task] = tasks

    @property
    def tasks(self) -> list[Task]:
        return self._tasks

    @tasks.setter
    def tasks(self, value: Iterable[Task] | None = None) -> None:

        if value is None:
            self._tasks: list[Task] = []
        else:
            items: list[Task] = list(value)
            self._unique_ids(items)
            self._tasks: list[Task] = items

    @staticmethod
    def _unique_ids(tasks: Iterable[Task]) -> None:
        ids: list[str] = [str(task.idx) for task in tasks]
        counter = Counter(ids)
        duplicates: list[str] = [idx for idx, count in counter.items() if count > 1]
        if duplicates:
            raise ValueError(f"Duplicate task index detected: {', '.join(duplicates)}.")

    def add(self, task: Task) -> None:
        self._unique_ids([*self._tasks, task])
        self._tasks.append(task)

    def remove(self, idx: UUID) -> None:
        for task in self._tasks:
            if task.idx == idx:
                self._tasks.remove(task)
                return

        raise ValueError(f"Task with {idx} does not exist")

    def get(self, idx: UUID) -> Task:
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

        def matches(task: Task) -> bool:

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
        key_func: Callable[[Task], Any] = key or attrgetter("priority")
        return TaskList(sorted(self.tasks, key=key_func, reverse=reverse))

    def __repr__(self) -> str:
        return f"{type(self).__name__}(tasks={self.tasks!r})"

    def __str__(self) -> str:
        if not self.tasks:
            return "TaskList (empty)"

        tasks_str: str = "\n".join(f"- {task}" for task in self.tasks)
        return f"TaskList ({len(self.tasks)} tasks):\n{tasks_str}"

    def __format__(self, format_spec: str) -> str:
        format_spec: str = (format_spec or "str").lower().strip()

        if format_spec in {"short", "s"}:
            return f"TaskList ({len(self.tasks)} tasks)"

        if format_spec in {"long", "l"}:
            if not self.tasks:
                return "TaskList (empty)"

            tasks_str: str = "\n\n".join(format(task, "long") for task in self.tasks)
            return f"TaskList:\n{tasks_str}"

        return str(self)

    def __len__(self) -> int:
        return len(self.tasks)

    def __iter__(self) -> Iterator[Task]:
        return iter(self.tasks)

    def __contains__(self, idx: UUID) -> bool:
        return any(task.idx == idx for task in self.tasks)

    def __getitem__(self, index: int) -> Task:
        return self.tasks[index]
