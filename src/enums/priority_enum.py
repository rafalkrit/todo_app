from enum import IntEnum, auto


class PriorityEnum(IntEnum):
    """Supported task priority levels ordered from lowest to highest."""

    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
