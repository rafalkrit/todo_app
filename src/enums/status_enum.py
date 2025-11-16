from enum import StrEnum


class StatusEnum(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
