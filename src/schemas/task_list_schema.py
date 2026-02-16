from typing import TypedDict

from src.schemas.tasks_schema import TaskDict


class TaskListDict(TypedDict):
    tasks: list[TaskDict]
