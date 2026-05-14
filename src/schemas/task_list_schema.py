from typing import TypedDict

from src.schemas.tasks_schema import TaskDict


class TaskListDict(TypedDict):
    """Serialized dictionary representation of a task collection."""

    tasks: list[TaskDict]
