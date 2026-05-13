from typing import TypeGuard, cast

from src.schemas.tasks_schema import TaskDict


def is_task_dict(obj: object) -> TypeGuard[TaskDict]:
    """Return whether an object matches the serialized TaskDict shape."""
    if not isinstance(obj, dict):
        return False

    data: dict[str, object] = cast("dict[str, object]", obj)

    required_keys: dict[str, type[object] | tuple[type[object], ...]] = {
        "description": str,
        "status": str,
        "priority": int,
        "created_at": str,
        "deadline": (str, type(None)),
        "completed_at": (str, type(None)),
        "tags": list,
        "idx": str,
    }

    if set(required_keys) != set(obj):
        return False

    for key, expected_type in required_keys.items():
        if not isinstance(data[key], expected_type):
            return False

    tags: object = data["tags"]

    if not isinstance(tags, list):  # pragma: no cover
        return False

    return all(isinstance(tag, str) for tag in tags)
