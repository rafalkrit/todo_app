from typing import TypeGuard, cast

from src.schemas.guards.task_dict_guard import is_task_dict
from src.schemas.task_list_schema import TaskListDict


def is_task_list_dict(obj: object) -> TypeGuard[TaskListDict]:
    """Return whether an object matches the serialized TaskListDict shape."""
    if not isinstance(obj, dict):
        return False

    if set(obj.keys()) != {"tasks"}:
        return False

    data: dict[str, object] = cast("dict[str, object]", obj)

    tasks: object = data["tasks"]

    if not isinstance(tasks, list):
        return False

    return all(is_task_dict(task) for task in tasks)
