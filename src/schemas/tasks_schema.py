from typing import TypedDict


class TaskDict(TypedDict):
    description: str
    status: str
    priority: int
    created_at: str
    deadline: str | None
    completed_at: str | None
    tags: list[str]
    idx: str
