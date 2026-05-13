from typing import TypedDict


class TaskDict(TypedDict):
    """Serialized dictionary representation of a task.

    This shape is used as the JSON persistence contract between the domain
    object and the storage layer.
    """

    description: str
    status: str
    priority: int
    created_at: str
    deadline: str | None
    completed_at: str | None
    tags: list[str]
    idx: str
