from enum import StrEnum


class StatusEnum(StrEnum):
    """Supported workflow states for a task."""

    TODO = "todo"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
